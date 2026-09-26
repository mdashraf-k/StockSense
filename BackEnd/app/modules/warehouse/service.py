from fastapi import HTTPException

from .models import Warehouse
from .repository import WarehouseRepository
from .schemas import (
    WarehouseCreate,
    WarehouseUpdate
)


class WarehouseService:

    def __init__(
        self,
        repository: WarehouseRepository,
        db
    ):
        self.repository = repository
        self.db = db

    def create(
        self,
        data: WarehouseCreate
    ):

        warehouse = Warehouse(
            **data.model_dump()
        )

        warehouse = self.repository.create(
            warehouse
        )

        self.db.commit()

        return warehouse

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, warehouse_id: int):

        warehouse = self.repository.get_by_id(
            warehouse_id
        )

        if not warehouse:
            raise HTTPException(
                status_code=404,
                detail="Warehouse not found"
            )

        return warehouse

    def update(
        self,
        warehouse_id: int,
        data: WarehouseUpdate
    ):

        warehouse = self.get_by_id(
            warehouse_id
        )

        for key, value in data.model_dump(
            exclude_unset=True
        ).items():

            setattr(warehouse, key, value)

        warehouse = self.repository.update(
            warehouse
        )

        self.db.commit()

        return warehouse