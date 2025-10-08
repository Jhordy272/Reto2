from sqlalchemy.orm import Session
from app.models.Product import Product
from typing import Optional


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.query(Product).filter(Product.id == product_id).first()
