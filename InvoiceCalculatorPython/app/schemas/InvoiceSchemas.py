from pydantic import BaseModel
from typing import List


class InvoiceItemRequest(BaseModel):
    productId: int
    quantity: int


class InvoiceRequest(BaseModel):
    items: List[InvoiceItemRequest]


class InvoiceItemResponse(BaseModel):
    productId: int
    productName: str
    quantity: int
    unitPrice: float
    subtotal: float


class InvoiceResponse(BaseModel):
    items: List[InvoiceItemResponse]
    total: float
