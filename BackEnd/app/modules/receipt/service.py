from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import DocumentStatus, MovementType

from .models import Receipt, ReceiptItem
from .repository import ReceiptRepository
from .schemas import ReceiptCreate


class ReceiptService:

    def __init__(
        self,
        repository: ReceiptRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    def create(
        self,
        data: ReceiptCreate,
        user_id: int
    ):

        if not data.items:

            raise HTTPException(
                status_code=400,
                detail="Receipt must contain items"
            )

        receipt = Receipt(
            supplier=data.supplier,
            warehouse_id=data.warehouse_id,
            created_by=user_id,
            status=DocumentStatus.DRAFT
        )

        for item in data.items:

            receipt.items.append(
                ReceiptItem(
                    product_id=item.product_id,
                    quantity=item.quantity
                )
            )

        self.db.add(receipt)
        self.db.flush()
        self.db.commit()
        self.db.refresh(receipt)

        return receipt

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, receipt_id: int):

        receipt = self.repository.get_by_id(
            receipt_id
        )

        if not receipt:

            raise HTTPException(
                status_code=404,
                detail="Receipt not found"
            )

        return receipt

    def validate(
        self,
        receipt_id: int,
        user_id: int
    ):

        receipt = self.get_by_id(receipt_id)

        if receipt.status == DocumentStatus.DONE:

            raise HTTPException(
                status_code=400,
                detail="Receipt already validated"
            )

        if receipt.status == DocumentStatus.CANCELED:

            raise HTTPException(
                status_code=400,
                detail="Canceled receipt cannot be validated"
            )

        try:

            for item in receipt.items:

                # Get/create inventory
                from modules.inventory.repository import (
                    InventoryRepository
                )
                from modules.inventory.service import (
                    InventoryService
                )

                inventory_service = InventoryService(
                    InventoryRepository(self.db),
                    self.db
                )

                inventory_service.change_stock(
                    product_id=item.product_id,
                    warehouse_id=receipt.warehouse_id,
                    quantity_change=item.quantity
                )

                # Ledger
                from modules.ledger.repository import (
                    LedgerRepository
                )
                from modules.ledger.service import (
                    LedgerService
                )

                ledger_service = LedgerService(
                    LedgerRepository(self.db),
                    self.db
                )

                ledger_service.create_entry(
                    product_id=item.product_id,
                    warehouse_id=receipt.warehouse_id,
                    quantity=item.quantity,
                    movement_type=MovementType.RECEIPT,
                    created_by=user_id,
                    reference_id=receipt.id,
                    reference_type="receipt"
                )

            receipt.status = DocumentStatus.DONE

            self.db.commit()
            self.db.refresh(receipt)

            return receipt

        except Exception:
            self.db.rollback()
            raise