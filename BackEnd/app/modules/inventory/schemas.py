from pydantic import BaseModel


class InventoryResponse(BaseModel):

    id: int
    product_id: int
    warehouse_id: int
    quantity: int

    class Config:
        from_attributes = True


class StockUpdate(BaseModel):

    product_id: int
    warehouse_id: int
    quantity: int