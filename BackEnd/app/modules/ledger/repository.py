from sqlalchemy.orm import Session

from .models import StockLedger


class LedgerRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        entry: StockLedger
    ):

        self.db.add(entry)
        self.db.flush()
        self.db.refresh(entry)

        return entry

    def get_all(self):

        return (
            self.db.query(StockLedger)
            .order_by(
                StockLedger.created_at.desc()
            )
            .all()
        )

    def get_by_product(
        self,
        product_id: int
    ):

        return (
            self.db.query(StockLedger)
            .filter(
                StockLedger.product_id == product_id
            )
            .order_by(
                StockLedger.created_at.desc()
            )
            .all()
        )

    def get_by_warehouse(
        self,
        warehouse_id: int
    ):

        return (
            self.db.query(StockLedger)
            .filter(
                StockLedger.warehouse_id == warehouse_id
            )
            .order_by(
                StockLedger.created_at.desc()
            )
            .all()
        )