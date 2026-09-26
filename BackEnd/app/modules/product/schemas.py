from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    sku: str = Field(
        min_length=2,
        max_length=50
    )

    category: str | None = None

    unit_of_measure: str = Field(
        min_length=1,
        max_length=30
    )

    description: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    category: str | None = None

    unit_of_measure: str | None = None

    description: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    category: str | None
    unit_of_measure: str
    description: str | None

    class Config:
        from_attributes = True