from sqlalchemy.orm import Session

from .models import Receipt, ReceiptItem


class ReceiptRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        receipt: Receipt
    ):

        self.db.add(receipt)
        self.db.flush()
        self.db.refresh(receipt)

        return receipt

    def get_by_id(
        self,
        receipt_id: int
    ):

        return (
            self.db.query(Receipt)
            .filter(
                Receipt.id == receipt_id
            )
            .first()
        )

    def get_all(self):

        return (
            self.db.query(Receipt)
            .order_by(
                Receipt.created_at.desc()
            )
            .all()
        )

    def update(
        self,
        receipt: Receipt
    ):

        self.db.flush()
        self.db.refresh(receipt)

        return receipt