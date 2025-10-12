import os, json, asyncio, asyncpg, aiohttp
from collections import deque
from heuristics import update_baselines, compute_score

PG_DSN       = os.getenv("LOGS_PG_DSN", "postgresql://postgres:password@postgres-logs:5432/logsdb")
ALERT_URL    = os.getenv("ALERT_URL", "http://log-api:8090/logs")
SERVICE_NAME = "log-heuristic"

# Mantener último N ids alertados para no repetir alertas del mismo evento
RECENT_MAX = 5000
recent_alerted = deque(maxlen=RECENT_MAX)
recent_alerted_set = set()

def remember_alerted(log_id: int | None):
    if log_id is None:
        return
    recent_alerted.append(log_id)
    recent_alerted_set.add(log_id)
    # mantener set en sincronía con deque
    while len(recent_alerted_set) > len(recent_alerted):
        # debería no pasar, pero por seguridad
        recent_alerted_set = set(recent_alerted)

def already_alerted(log_id: int | None) -> bool:
    return (log_id is not None) and (log_id in recent_alerted_set)

async def send_alert(payload, score, reasons):
    alert_body = {
        "service": SERVICE_NAME,
        "level": "ERROR",
        "message": f"[HEURISTIC] log anómalo score={score:.2f} reasons={','.join(reasons)}",
        "context": payload | {"__heuristic_alert": True}
    }
    async with aiohttp.ClientSession() as s:
        await s.post(ALERT_URL, json=alert_body)

async def run_listener():
    q: asyncio.Queue[str] = asyncio.Queue()

    async def _on_notify(conn, pid, channel, payload):
        await q.put(payload)

    while True:
        conn = None
        try:
            conn: asyncpg.Connection = await asyncpg.connect(PG_DSN)
            await conn.execute("LISTEN app_logs_events;")
            await conn.add_listener("app_logs_events", _on_notify)
            print("📡 Escuchando app_logs_events…")

            while True:
                payload = await q.get()
                try:
                    data = json.loads(payload)
                    if (data.get("service") or "").lower() == SERVICE_NAME:
                        continue
                    if isinstance(data.get("context"), dict) and data["context"].get("__heuristic_alert"):
                        continue

                    log_id  = data.get("id")
                    service = data.get("service", "unknown")
                    level   = data.get("level", "INFO")
                    message = data.get("message", "")
                    context = data.get("context") or {}
                    update_baselines(service, message)
                    score, reasons = compute_score(service, level, message, context)
                    await conn.execute("""
                        INSERT INTO log_insights(service, rule, score, sample_log_id, sample_msg, context)
                        VALUES($1,$2,$3,$4,$5,$6::jsonb)
                    """, service, ",".join(reasons) or "heuristic", score, log_id, message, json.dumps(data))
                    if (score >= 4.0) and not already_alerted(log_id):
                        await send_alert({**data, "score": score, "reasons": reasons}, score, reasons)
                        remember_alerted(log_id)

                except Exception as e:
                    print("❌ error procesando notify:", e)

        except Exception as e:
            print("❌ conexión a logsdb falló:", e)
            await asyncio.sleep(2)
        finally:
            if conn:
                try:
                    await conn.close()
                except Exception:
                    pass

if __name__ == "__main__":
    asyncio.run(run_listener())
