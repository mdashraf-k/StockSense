from sqlalchemy.orm import Session

from .models import Transfer


class TransferRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        transfer: Transfer
    ):

        self.db.add(transfer)
        self.db.flush()
        self.db.refresh(transfer)

        return transfer

    def get_by_id(
        self,
        transfer_id: int
    ):

        return (
            self.db.query(Transfer)
            .filter(
                Transfer.id == transfer_id
            )
            .first()
        )

    def get_all(self):

        return (
            self.db.query(Transfer)
            .order_by(
                Transfer.created_at.desc()
            )
            .all()
        )