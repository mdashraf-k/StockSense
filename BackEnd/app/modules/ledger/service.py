from sqlalchemy.orm import Session

from app.core.enums import MovementType

from .models import StockLedger
from .repository import LedgerRepository


class LedgerService:

    def __init__(
        self,
        repository: LedgerRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    def create_entry(
        self,
        product_id: int,
        warehouse_id: int,
        quantity: int,
        movement_type: MovementType,
        created_by: int | None = None,
        reference_id: int | None = None,
        reference_type: str | None = None
    ):

        entry = StockLedger(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            movement_type=movement_type,
            created_by=created_by,
            reference_id=reference_id,
            reference_type=reference_type
        )

        return self.repository.create(entry)

    def get_all(self):
        return self.repository.get_all()

    def get_product_history(
        self,
        product_id: int
    ):

        return self.repository.get_by_product(
            product_id
        )

    def get_warehouse_history(
        self,
        warehouse_id: int
    ):

        return self.repository.get_by_warehouse(
            warehouse_id
        )