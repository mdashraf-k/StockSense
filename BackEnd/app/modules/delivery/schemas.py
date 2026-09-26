from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import DocumentStatus


class DeliveryItemCreate(BaseModel):

    product_id: int

    quantity: int = Field(
        gt=0
    )


class DeliveryCreate(BaseModel):

    customer: str | None = None

    warehouse_id: int

    items: list[DeliveryItemCreate]


class DeliveryItemResponse(BaseModel):

    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class DeliveryResponse(BaseModel):

    id: int
    customer: str | None
    warehouse_id: int
    status: DocumentStatus
    created_by: int
    created_at: datetime
    items: list[DeliveryItemResponse]

    class Config:
        from_attributes = True