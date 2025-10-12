from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List

from .db import SessionLocal, ensure_table
from .models import AppLog
from .schemas import LogCreate, LogOut

app = FastAPI(
    title="Log API",
    description="Servicio para recibir y consultar logs. Swagger en /docs",
    version="1.0.0",
)

# Dependencia de sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    # Garantiza que la tabla exista
    ensure_table()
    # Escribe un log de arranque
    with SessionLocal() as db:
        db.add(AppLog(service="log-api", level="INFO", message="Log API started", context=None))
        db.commit()

@app.post("/logs", response_model=LogOut, status_code=status.HTTP_201_CREATED, summary="Crear un log")
def create_log(payload: LogCreate, db: Session = Depends(get_db)):
    row = AppLog(
        service=payload.service,
        level=payload.level,
        message=payload.message,
        context=payload.context,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return LogOut(id=row.id, **payload.model_dump())

@app.get("/logs", response_model=List[LogOut], summary="Listar últimos logs")
def list_logs(limit: int = 50, db: Session = Depends(get_db)):
    stmt = select(AppLog).order_by(desc(AppLog.created_at)).limit(limit)
    rows = db.execute(stmt).scalars().all()
    return [
        LogOut(
            id=r.id,
            service=r.service,
            level=r.level,
            message=r.message,
            context=r.context,
        )
        for r in rows
    ]

@app.get("/health", summary="Healthcheck simple")
def health():
    return JSONResponse({"status": "ok"})
