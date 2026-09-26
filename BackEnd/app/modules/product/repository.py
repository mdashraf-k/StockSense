from sqlalchemy.orm import Session

from .models import Product


class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product):
        self.db.add(product)
        self.db.flush()
        self.db.refresh(product)
        return product

    def get_by_id(self, product_id: int):
        return (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_sku(self, sku: str):
        return (
            self.db.query(Product)
            .filter(Product.sku == sku)
            .first()
        )

    def get_all(self):
        return (
            self.db.query(Product)
            .order_by(Product.id.desc())
            .all()
        )

    def update(self, product: Product):
        self.db.flush()
        self.db.refresh(product)
        return product

    def delete(self, product: Product):
        self.db.delete(product)
        self.db.flush()