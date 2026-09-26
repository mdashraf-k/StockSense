from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import DocumentStatus


class AdjustmentItemCreate(BaseModel):

    product_id: int

    counted_quantity: int = Field(
        ge=0
    )


class AdjustmentCreate(BaseModel):

    warehouse_id: int

    items: list[AdjustmentItemCreate]


class AdjustmentItemResponse(BaseModel):

    id: int
    product_id: int
    counted_quantity: int
    previous_quantity: int
    difference: int

    class Config:
        from_attributes = True


class AdjustmentResponse(BaseModel):

    id: int
    warehouse_id: int
    status: DocumentStatus
    created_by: int
    created_at: datetime
    items: list[AdjustmentItemResponse]

    class Config:
        from_attributes = True