from app.repositories.ProductRepository import ProductRepository
from app.schemas.InvoiceSchemas import InvoiceRequest, InvoiceResponse, InvoiceItemResponse
from fastapi import HTTPException


class InvoiceService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def calculate_invoice(self, request: InvoiceRequest) -> InvoiceResponse:
        item_responses = []
        total = 0.0

        for item in request.items:
            product = self.product_repository.find_by_id(item.productId)

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product not found with id: {item.productId}"
                )

            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product: {product.name}"
                )

            subtotal = product.price * item.quantity
            total += subtotal

            item_response = InvoiceItemResponse(
                productId=product.id,
                productName=product.name,
                quantity=item.quantity,
                unitPrice=product.price,
                subtotal=subtotal
            )

            item_responses.append(item_response)

        return InvoiceResponse(items=item_responses, total=total)
