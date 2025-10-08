from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.InvoiceSchemas import InvoiceRequest, InvoiceResponse
from app.services.InvoiceService import InvoiceService
from app.repositories.ProductRepository import ProductRepository
from app.db.Database_Connection_ORM import DatabaseConnectionORM

router = APIRouter(prefix="/invoice", tags=["invoice"])


def get_db():
    db_connection = DatabaseConnectionORM()
    db = db_connection.get_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/calculate", response_model=InvoiceResponse)
def calculate_invoice(request: InvoiceRequest, db: Session = Depends(get_db)):
    try:
        product_repository = ProductRepository(db)
        invoice_service = InvoiceService(product_repository)
        response = invoice_service.calculate_invoice(request)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
