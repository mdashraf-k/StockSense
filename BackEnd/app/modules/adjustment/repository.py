from sqlalchemy.orm import Session

from .models import Adjustment


class AdjustmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        adjustment: Adjustment
    ):

        self.db.add(adjustment)
        self.db.flush()
        self.db.refresh(adjustment)

        return adjustment

    def get_by_id(
        self,
        adjustment_id: int
    ):

        return (
            self.db.query(Adjustment)
            .filter(
                Adjustment.id == adjustment_id
            )
            .first()
        )

    def get_all(self):

        return (
            self.db.query(Adjustment)
            .order_by(
                Adjustment.created_at.desc()
            )
            .all()
        )