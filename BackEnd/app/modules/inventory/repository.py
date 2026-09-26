from sqlalchemy.orm import Session

from .models import Inventory


class InventoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get(
        self,
        product_id: int,
        warehouse_id: int
    ):

        return (
            self.db.query(Inventory)
            .filter(
                Inventory.product_id == product_id,
                Inventory.warehouse_id == warehouse_id
            )
            .first()
        )

    def get_by_product(
        self,
        product_id: int
    ):

        return (
            self.db.query(Inventory)
            .filter(
                Inventory.product_id == product_id
            )
            .all()
        )

    def get_by_warehouse(
        self,
        warehouse_id: int
    ):

        return (
            self.db.query(Inventory)
            .filter(
                Inventory.warehouse_id == warehouse_id
            )
            .all()
        )

    def get_all(self):

        return self.db.query(Inventory).all()

    def create(
        self,
        inventory: Inventory
    ):

        self.db.add(inventory)
        self.db.flush()
        self.db.refresh(inventory)

        return inventory