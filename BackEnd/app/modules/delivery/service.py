from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import DocumentStatus, MovementType

from .models import Delivery, DeliveryItem
from .repository import DeliveryRepository
from .schemas import DeliveryCreate


class DeliveryService:

    def __init__(
        self,
        repository: DeliveryRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    def create(
        self,
        data: DeliveryCreate,
        user_id: int
    ):

        if not data.items:

            raise HTTPException(
                status_code=400,
                detail="Delivery must contain items"
            )

        delivery = Delivery(
            customer=data.customer,
            warehouse_id=data.warehouse_id,
            created_by=user_id,
            status=DocumentStatus.DRAFT
        )

        for item in data.items:

            delivery.items.append(
                DeliveryItem(
                    product_id=item.product_id,
                    quantity=item.quantity
                )
            )

        self.db.add(delivery)
        self.db.commit()
        self.db.refresh(delivery)

        return delivery

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, delivery_id: int):

        delivery = self.repository.get_by_id(
            delivery_id
        )

        if not delivery:

            raise HTTPException(
                status_code=404,
                detail="Delivery not found"
            )

        return delivery

    def validate(
        self,
        delivery_id: int,
        user_id: int
    ):

        delivery = self.get_by_id(
            delivery_id
        )

        if delivery.status == DocumentStatus.DONE:

            raise HTTPException(
                status_code=400,
                detail="Delivery already validated"
            )

        if delivery.status == DocumentStatus.CANCELED:

            raise HTTPException(
                status_code=400,
                detail="Canceled delivery cannot be validated"
            )

        try:

            from modules.inventory.repository import (
                InventoryRepository
            )
            from modules.inventory.service import (
                InventoryService
            )
            from modules.ledger.repository import (
                LedgerRepository
            )
            from modules.ledger.service import (
                LedgerService
            )

            inventory_service = InventoryService(
                InventoryRepository(self.db),
                self.db
            )

            ledger_service = LedgerService(
                LedgerRepository(self.db),
                self.db
            )

            for item in delivery.items:

                inventory_service.change_stock(
                    product_id=item.product_id,
                    warehouse_id=delivery.warehouse_id,
                    quantity_change=-item.quantity
                )

                ledger_service.create_entry(
                    product_id=item.product_id,
                    warehouse_id=delivery.warehouse_id,
                    quantity=-item.quantity,
                    movement_type=MovementType.DELIVERY,
                    created_by=user_id,
                    reference_id=delivery.id,
                    reference_type="delivery"
                )

            delivery.status = DocumentStatus.DONE

            self.db.commit()
            self.db.refresh(delivery)

            return delivery

        except Exception:
            self.db.rollback()
            raise