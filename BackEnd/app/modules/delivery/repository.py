from sqlalchemy.orm import Session

from .models import Delivery


class DeliveryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        delivery: Delivery
    ):

        self.db.add(delivery)
        self.db.flush()
        self.db.refresh(delivery)

        return delivery

    def get_by_id(
        self,
        delivery_id: int
    ):

        return (
            self.db.query(Delivery)
            .filter(
                Delivery.id == delivery_id
            )
            .first()
        )

    def get_all(self):

        return (
            self.db.query(Delivery)
            .order_by(
                Delivery.created_at.desc()
            )
            .all()
        )