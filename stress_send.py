#!/usr/bin/env python3
import asyncio, aiohttp, random, time, json

API = "http://localhost:8090/logs"
HEADERS = {"Content-Type":"application/json"}

# definiciones de mensajes por categoría
NORMAL = [
    ("service-a","INFO","Scheduled job completed"),
    ("service-b","INFO","Cache refreshed"),
    ("service-c","INFO","Request processed"),
    ("service-d","INFO","OK healthcheck"),
]

SUSPECT = [
    ("invoice-controller","ERROR","Unauthorized admin access attempt at 03:12 UTC from 10.0.5.23", {"user":"qa6","ip":"10.0.5.23"}),
    ("rbac","ERROR","Privilege escalation attempt detected", {"user":"guest-223","role_from":"viewer","role_to":"admin"}),
    ("config-service","ERROR","Unauthorized config push to production", {"actor":"ci-bot","branch":"hotfix/unknown"}),
    ("payment-gateway","ERROR","Fatal exception: DB connection refused", {"user":"payment-svc"}),
    ("auth-service","ERROR","Login failed for user admin from 10.0.0.11", {"ip":"10.0.0.11","user":"admin"}),
    ("service-x","WARN","Suspicious payload size change detected", {"size": "900MB"}),
]

async def send(session, payload):
    async with session.post(API, json=payload, headers=HEADERS) as resp:
        # opcional: return status/text
        return resp.status

async def worker(n_requests, suspect_prob=0.05, concurrency=50):
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session:
        async def do_one(i):
            async with sem:
                if random.random() < suspect_prob:
                    svc, lvl, msg, ctx = random.choice(SUSPECT)
                else:
                    svc, lvl, msg = random.choice(NORMAL)
                    ctx = {"user": f"qa{random.randint(1,40)}"}
                payload = {"service": svc, "level": lvl, "message": msg, "context": ctx}
                return await send(session, payload)

        tasks = [asyncio.create_task(do_one(i)) for i in range(n_requests)]
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=1000, help="total requests")
    p.add_argument("--suspect", type=float, default=0.05, help="probabilidad de enviar sospechoso")
    p.add_argument("--c", type=int, default=100, help="concurrency")
    args = p.parse_args()
    t0 = time.time()
    res = asyncio.run(worker(args.n, suspect_prob=args.suspect, concurrency=args.c))
    print("Done", len(res), "time", time.time()-t0)
