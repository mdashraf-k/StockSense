from sqlalchemy.orm import Session

from .models import Warehouse


class WarehouseRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, warehouse: Warehouse):

        self.db.add(warehouse)
        self.db.flush()
        self.db.refresh(warehouse)

        return warehouse

    def get_by_id(self, warehouse_id: int):

        return (
            self.db.query(Warehouse)
            .filter(
                Warehouse.id == warehouse_id
            )
            .first()
        )

    def get_all(self):

        return (
            self.db.query(Warehouse)
            .order_by(Warehouse.id.desc())
            .all()
        )

    def update(self, warehouse: Warehouse):

        self.db.flush()
        self.db.refresh(warehouse)

        return warehouse