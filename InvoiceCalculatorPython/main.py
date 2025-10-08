from fastapi import FastAPI
from app.routers import invoice_router
from app.db.Database_Connection_ORM import DatabaseConnectionORM, Base

app = FastAPI(
    title="Invoice Calculator Python",
    description="Invoice Calculator Python",
    version="1.0.0"
)

db_connection = DatabaseConnectionORM()
engine = db_connection.get_engine()
Base.metadata.create_all(bind=engine)

app.include_router(invoice_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
