from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import DocumentStatus


class TransferItemCreate(BaseModel):

    product_id: int

    quantity: int = Field(
        gt=0
    )


class TransferCreate(BaseModel):

    source_warehouse_id: int

    destination_warehouse_id: int

    items: list[TransferItemCreate]


class TransferItemResponse(BaseModel):

    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class TransferResponse(BaseModel):

    id: int
    source_warehouse_id: int
    destination_warehouse_id: int
    status: DocumentStatus
    created_by: int
    created_at: datetime
    items: list[TransferItemResponse]

    class Config:
        from_attributes = True