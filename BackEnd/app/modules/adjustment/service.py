from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import DocumentStatus, MovementType

from .models import Adjustment, AdjustmentItem
from .repository import AdjustmentRepository
from .schemas import AdjustmentCreate


class AdjustmentService:

    def __init__(
        self,
        repository: AdjustmentRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    def create(
        self,
        data: AdjustmentCreate,
        user_id: int
    ):

        if not data.items:

            raise HTTPException(
                status_code=400,
                detail="Adjustment must contain items"
            )

        from modules.inventory.repository import (
            InventoryRepository
        )

        inventory_repository = InventoryRepository(
            self.db
        )

        adjustment = Adjustment(
            warehouse_id=data.warehouse_id,
            created_by=user_id,
            status=DocumentStatus.DRAFT
        )

        for item in data.items:

            inventory = inventory_repository.get(
                item.product_id,
                data.warehouse_id
            )

            previous_quantity = (
                inventory.quantity
                if inventory
                else 0
            )

            difference = (
                item.counted_quantity
                - previous_quantity
            )

            adjustment.items.append(
                AdjustmentItem(
                    product_id=item.product_id,
                    counted_quantity=item.counted_quantity,
                    previous_quantity=previous_quantity,
                    difference=difference
                )
            )

        self.db.add(adjustment)
        self.db.commit()
        self.db.refresh(adjustment)

        return adjustment

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(
        self,
        adjustment_id: int
    ):

        adjustment = self.repository.get_by_id(
            adjustment_id
        )

        if not adjustment:

            raise HTTPException(
                status_code=404,
                detail="Adjustment not found"
            )

        return adjustment

    def validate(
        self,
        adjustment_id: int,
        user_id: int
    ):

        adjustment = self.get_by_id(
            adjustment_id
        )

        if adjustment.status == DocumentStatus.DONE:

            raise HTTPException(
                status_code=400,
                detail="Adjustment already validated"
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

            for item in adjustment.items:

                inventory_service.change_stock(
                    product_id=item.product_id,
                    warehouse_id=(
                        adjustment.warehouse_id
                    ),
                    quantity_change=item.difference
                )

                ledger_service.create_entry(
                    product_id=item.product_id,
                    warehouse_id=(
                        adjustment.warehouse_id
                    ),
                    quantity=item.difference,
                    movement_type=(
                        MovementType.ADJUSTMENT
                    ),
                    created_by=user_id,
                    reference_id=adjustment.id,
                    reference_type="adjustment"
                )

            adjustment.status = DocumentStatus.DONE

            self.db.commit()
            self.db.refresh(adjustment)

            return adjustment

        except Exception:
            self.db.rollback()
            raise