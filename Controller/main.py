from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import httpx
import asyncio

from services_config import enabled_services, TIMEOUT_SECS, PRECISION
from voting import majority_vote

class InvoiceItemRequest(BaseModel):
    productId: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1)

class InvoiceRequest(BaseModel):
    items: List[InvoiceItemRequest] = Field(min_length=1)

class ServiceVote(BaseModel):
    service: str
    ok: bool
    total: float | None = None
    error: str | None = None
    raw: Dict[str, Any] | None = None

class VoteResponse(BaseModel):
    finalTotal: float
    precision: int
    votes: List[ServiceVote]
    tally: Dict[str, int]

app = FastAPI(title="Invoice Controller", version="1.0.0")

@app.get("/health")
async def health():
    return {"ok": True, "services": enabled_services()}

def extract_total(payload: Dict[str, Any]) -> float:
    if isinstance(payload, dict):
        for k in ("total","Total","grandTotal","GrandTotal","amount","Amount"):
            v = payload.get(k)
            if isinstance(v, (int, float)):
                return float(v)
    raise ValueError("total_not_found")

async def call_service(client: httpx.AsyncClient, name: str, base: str, body: Dict[str, Any]):
    try:
        r = await client.post(f"{base}/invoice/calculate", json=body, timeout=TIMEOUT_SECS)
        if r.status_code >= 400:
            return ServiceVote(service=name, ok=False, error=f"{r.status_code} {r.text[:200]}")
        data = r.json()
        total = extract_total(data)
        return ServiceVote(service=name, ok=True, total=total, raw=data)
    except Exception as e:
        return ServiceVote(service=name, ok=False, error=str(e))

@app.post("/invoice/calculate", response_model=VoteResponse)
async def calculate_invoice(req: InvoiceRequest, request: Request):
    svcs = enabled_services()
    if not svcs:
        raise HTTPException(status_code=503, detail="no_services_enabled")
    body = req.model_dump()
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[call_service(client, n, u, body) for n, u in svcs.items()])
    ok_totals = [v.total for v in results if v.ok and v.total is not None]
    if not ok_totals:
        raise HTTPException(status_code=502, detail="no_successful_results")
    final, tally = majority_vote(ok_totals, precision=PRECISION)
    return VoteResponse(
        finalTotal=final,
        precision=PRECISION,
        votes=results,
        tally={f"{k:.{PRECISION}f}": c for k, c in tally.items()},
    )
