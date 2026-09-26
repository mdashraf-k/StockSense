from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import DocumentStatus, MovementType

from .models import Transfer, TransferItem
from .repository import TransferRepository
from .schemas import TransferCreate


class TransferService:

    def __init__(
        self,
        repository: TransferRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    def create(
        self,
        data: TransferCreate,
        user_id: int
    ):

        if (
            data.source_warehouse_id
            == data.destination_warehouse_id
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Source and destination "
                    "warehouses must be different"
                )
            )

        if not data.items:

            raise HTTPException(
                status_code=400,
                detail="Transfer must contain items"
            )

        transfer = Transfer(
            source_warehouse_id=(
                data.source_warehouse_id
            ),
            destination_warehouse_id=(
                data.destination_warehouse_id
            ),
            created_by=user_id,
            status=DocumentStatus.DRAFT
        )

        for item in data.items:

            transfer.items.append(
                TransferItem(
                    product_id=item.product_id,
                    quantity=item.quantity
                )
            )

        self.db.add(transfer)
        self.db.commit()
        self.db.refresh(transfer)

        return transfer

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, transfer_id: int):

        transfer = self.repository.get_by_id(
            transfer_id
        )

        if not transfer:

            raise HTTPException(
                status_code=404,
                detail="Transfer not found"
            )

        return transfer

    def validate(
        self,
        transfer_id: int,
        user_id: int
    ):

        transfer = self.get_by_id(
            transfer_id
        )

        if transfer.status == DocumentStatus.DONE:

            raise HTTPException(
                status_code=400,
                detail="Transfer already validated"
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

            for item in transfer.items:

                # Remove from source
                inventory_service.change_stock(
                    product_id=item.product_id,
                    warehouse_id=(
                        transfer.source_warehouse_id
                    ),
                    quantity_change=-item.quantity
                )

                # Add to destination
                inventory_service.change_stock(
                    product_id=item.product_id,
                    warehouse_id=(
                        transfer.destination_warehouse_id
                    ),
                    quantity_change=item.quantity
                )

                # Source ledger
                ledger_service.create_entry(
                    product_id=item.product_id,
                    warehouse_id=(
                        transfer.source_warehouse_id
                    ),
                    quantity=-item.quantity,
                    movement_type=(
                        MovementType.TRANSFER_OUT
                    ),
                    created_by=user_id,
                    reference_id=transfer.id,
                    reference_type="transfer"
                )

                # Destination ledger
                ledger_service.create_entry(
                    product_id=item.product_id,
                    warehouse_id=(
                        transfer.destination_warehouse_id
                    ),
                    quantity=item.quantity,
                    movement_type=(
                        MovementType.TRANSFER_IN
                    ),
                    created_by=user_id,
                    reference_id=transfer.id,
                    reference_type="transfer"
                )

            transfer.status = DocumentStatus.DONE

            self.db.commit()
            self.db.refresh(transfer)

            return transfer

        except Exception:
            self.db.rollback()
            raise