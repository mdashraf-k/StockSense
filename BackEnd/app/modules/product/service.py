from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Product
from .repository import ProductRepository
from .schemas import ProductCreate, ProductUpdate


class ProductService:

    def __init__(
        self,
        repository: ProductRepository,
        db: Session
    ):
        self.repository = repository
        self.db = db

    def create(
        self,
        data: ProductCreate
    ):

        if self.repository.get_by_sku(data.sku):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="SKU already exists"
            )

        product = Product(
            **data.model_dump()
        )

        product = self.repository.create(product)

        self.db.commit()

        return product

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, product_id: int):

        product = self.repository.get_by_id(
            product_id
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product

    def update(
        self,
        product_id: int,
        data: ProductUpdate
    ):

        product = self.get_by_id(product_id)

        for key, value in data.model_dump(
            exclude_unset=True
        ).items():

            setattr(product, key, value)

        product = self.repository.update(product)

        self.db.commit()

        return product

    def delete(self, product_id: int):

        product = self.get_by_id(product_id)

        self.repository.delete(product)

        self.db.commit()