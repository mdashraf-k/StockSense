from datetime import datetime

from pydantic import BaseModel

from app.core.enums import MovementType


class LedgerResponse(BaseModel):

    id: int
    product_id: int
    warehouse_id: int
    quantity: int
    movement_type: MovementType
    reference_id: int | None
    reference_type: str | None
    created_by: int | None
    created_at: datetime

    class Config:
        from_attributes = True