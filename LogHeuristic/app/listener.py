import os, json, asyncio, asyncpg, aiohttp
from collections import deque
from datetime import datetime, timezone
from heuristics import update_baselines, compute_score

PG_DSN       = os.getenv("LOGS_PG_DSN", "postgresql://postgres:password@postgres-logs:5432/logsdb")
ALERT_URL    = os.getenv("ALERT_URL", "http://log-api:8090/logs")
SERVICE_NAME = "log-heuristic"

# Evitar alertar dos veces el mismo log
RECENT_MAX = 5000
recent_alerted = deque(maxlen=RECENT_MAX)
recent_alerted_set = set()

def remember_alerted(log_id: int | None):
    if log_id is None:
        return
    recent_alerted.append(log_id)
    recent_alerted_set.add(log_id)
    # mantener set consistente con la deque
    while len(recent_alerted_set) > len(recent_alerted):
        recent_alerted_set.clear()
        recent_alerted_set.update(recent_alerted)

def already_alerted(log_id: int | None) -> bool:
    return (log_id is not None) and (log_id in recent_alerted_set)

def _parse_ts(ts_str: str | None) -> datetime | None:
    if not ts_str:
        return None
    try:
        ts_str = ts_str.replace('Z', '+00:00')
        return datetime.fromisoformat(ts_str)
    except Exception:
        return None

async def send_alert(session: aiohttp.ClientSession, payload, score, reasons,
                     detect_latency_ms: float | None, processing_ms: float | None):
    now_utc = datetime.now(timezone.utc).isoformat()
    alert_body = {
        "service": SERVICE_NAME,
        "level": "ERROR",
        "message": f"[HEURISTIC] log anómalo score={score:.2f} reasons={','.join(reasons)}",
        "context": payload | {
            "__heuristic_alert": True,
            "detected_at": now_utc,
            "detect_latency_ms": detect_latency_ms,
            "processing_ms": processing_ms,
        },
    }
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        print("→ POST alerta a log-api:", ALERT_URL)  # DEBUG
        async with session.post(ALERT_URL, json=alert_body, timeout=timeout) as resp:
            body = await resp.text()
            print(f"← resp alerta status={resp.status} body={body[:200]}")  # DEBUG
            if resp.status >= 400:
                print(f"⚠️ POST alerta falló status={resp.status}")
    except Exception as e:
        print("❌ fallo enviando alerta:", e)


async def run_listener():
    # Una sola sesión HTTP para todo el proceso (pool)
    connector = aiohttp.TCPConnector(limit=50, ssl=False, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        q: asyncio.Queue[str] = asyncio.Queue()

        async def _on_notify(_conn, _pid, _channel, payload):
            await q.put(payload)

        while True:
            conn = None
            try:
                conn = await asyncpg.connect(PG_DSN)
                await conn.execute("LISTEN app_logs_events;")
                await conn.add_listener("app_logs_events", _on_notify)
                print("📡 Escuchando app_logs_events…")

                while True:
                    payload = await q.get()
                    t_start = datetime.now(timezone.utc)

                    try:
                        data = json.loads(payload)

                        # Evitar bucle con nuestras propias alertas
                        if (data.get("service") or "").lower() == SERVICE_NAME:
                            continue
                        if isinstance(data.get("context"), dict) and data["context"].get("__heuristic_alert"):
                            continue

                        log_id  = data.get("id")
                        service = data.get("service", "unknown")
                        level   = data.get("level", "INFO")
                        message = data.get("message", "")
                        context = data.get("context") or {}

                        # Latencia de detección (insert -> ahora)
                        ts_insert = _parse_ts(data.get("ts"))
                        detect_latency_ms = None
                        if ts_insert:
                            detect_latency_ms = (t_start - ts_insert).total_seconds() * 1000.0

                        # Heurística
                        update_baselines(service, message)
                        score, reasons = compute_score(service, level, message, context)

                        # Guardar insight con la latencia
                        insight_ctx = data | {"detect_latency_ms": detect_latency_ms}
                        await conn.execute("""
                            INSERT INTO log_insights(service, rule, score, sample_log_id, sample_msg, context)
                            VALUES($1,$2,$3,$4,$5,$6::jsonb)
                        """, service, ",".join(reasons) or "heuristic", score, log_id, message, json.dumps(insight_ctx))

                        # Enviar alerta (una sola por log_id)
                        if (score >= 4.0) and not already_alerted(log_id):
                            t_before_alert = datetime.now(timezone.utc)
                            await send_alert(
                                session,
                                {**data, "score": score, "reasons": reasons},
                                score, reasons,
                                detect_latency_ms=detect_latency_ms,
                                processing_ms=(t_before_alert - t_start).total_seconds() * 1000.0,
                            )
                            remember_alerted(log_id)

                    except Exception as e:
                        print("❌ error procesando notify:", e)

            except Exception as e:
                print("❌ conexión a logsdb falló:", e)
                await asyncio.sleep(2)

            finally:
                # Quitar listener y cerrar conexión PG de forma limpia
                if conn:
                    try:
                        await conn.remove_listener("app_logs_events", _on_notify)
                    except Exception:
                        pass
                    try:
                        await conn.close()
                    except Exception:
                        pass

if __name__ == "__main__":
    asyncio.run(run_listener())
