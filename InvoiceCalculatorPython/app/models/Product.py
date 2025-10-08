from sqlalchemy import Column, Integer, String, Float
from app.db.Database_Connection_ORM import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
