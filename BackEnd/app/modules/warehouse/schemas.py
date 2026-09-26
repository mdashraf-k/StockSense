from pydantic import BaseModel, Field


class WarehouseCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    location: str | None = None

    description: str | None = None


class WarehouseUpdate(BaseModel):

    name: str | None = None

    location: str | None = None

    description: str | None = None


class WarehouseResponse(BaseModel):

    id: int
    name: str
    location: str | None
    description: str | None

    class Config:
        from_attributes = True