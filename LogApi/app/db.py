import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Variables de entorno con defaults razonables para correr en Compose
LOG_DB_HOST = os.getenv("LOG_DB_HOST", "postgres-logs")
LOG_DB_PORT = os.getenv("LOG_DB_PORT", "5432")
LOG_DB_USER = os.getenv("LOG_DB_USER", "postgres")
LOG_DB_PASSWORD = os.getenv("LOG_DB_PASSWORD", "password")
LOG_DB_NAME = os.getenv("LOG_DB_NAME", "logsdb")

DATABASE_URL = f"postgresql://{LOG_DB_USER}:{LOG_DB_PASSWORD}@{LOG_DB_HOST}:{LOG_DB_PORT}/{LOG_DB_NAME}"

# Motor y sesión (sin async para mantenerlo simple)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def ensure_table():
    """
    Crea la tabla app_logs si no existe (por si el init.sql no corrió
    o quieres portabilidad).
    """
    ddl = """
    CREATE TABLE IF NOT EXISTS app_logs (
        id BIGSERIAL PRIMARY KEY,
        service TEXT NOT NULL,
        level TEXT NOT NULL,
        message TEXT NOT NULL,
        context JSONB,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_app_logs_created_at ON app_logs (created_at);
    CREATE INDEX IF NOT EXISTS idx_app_logs_level ON app_logs (level);
    CREATE INDEX IF NOT EXISTS idx_app_logs_service ON app_logs (service);
    """
    with engine.connect() as conn:
        conn.execute(text(ddl))
        conn.commit()
