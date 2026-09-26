from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import DocumentStatus


class ReceiptItemCreate(BaseModel):

    product_id: int

    quantity: int = Field(
        gt=0
    )


class ReceiptCreate(BaseModel):

    supplier: str | None = None

    warehouse_id: int

    items: list[ReceiptItemCreate]


class ReceiptItemResponse(BaseModel):

    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class ReceiptResponse(BaseModel):

    id: int
    supplier: str | None
    warehouse_id: int
    status: DocumentStatus
    created_by: int
    created_at: datetime
    items: list[ReceiptItemResponse]

    class Config:
        from_attributes = True