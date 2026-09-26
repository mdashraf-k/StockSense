from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Inventory
from .repository import InventoryRepository


class InventoryService:

    def __init__(
        self,
        repository: InventoryRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    def get_all(self):

        return self.repository.get_all()

    def get_stock(
        self,
        product_id: int,
        warehouse_id: int
    ):

        inventory = self.repository.get(
            product_id,
            warehouse_id
        )

        if not inventory:

            return {
                "product_id": product_id,
                "warehouse_id": warehouse_id,
                "quantity": 0
            }

        return inventory

    def get_product_stock(
        self,
        product_id: int
    ):

        return self.repository.get_by_product(
            product_id
        )

    def get_warehouse_stock(
        self,
        warehouse_id: int
    ):

        return self.repository.get_by_warehouse(
            warehouse_id
        )

    def change_stock(
        self,
        product_id: int,
        warehouse_id: int,
        quantity_change: int
    ):

        inventory = self.repository.get(
            product_id,
            warehouse_id
        )

        if not inventory:

            if quantity_change < 0:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient stock"
                )

            inventory = Inventory(
                product_id=product_id,
                warehouse_id=warehouse_id,
                quantity=quantity_change
            )

            return self.repository.create(
                inventory
            )

        new_quantity = (
            inventory.quantity
            + quantity_change
        )

        if new_quantity < 0:

            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        inventory.quantity = new_quantity

        self.db.flush()

        return inventory