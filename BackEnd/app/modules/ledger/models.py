from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy import Enum as SQLEnum
from app.config.databases import Base
from app.core.enums import MovementType


class StockLedger(Base):

    __tablename__ = "stock_ledger"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey(
            "products.id"
        ),
        nullable=False,
        index=True
    )

    warehouse_id = Column(
        Integer,
        ForeignKey(
            "warehouses.id"
        ),
        nullable=False,
        index=True
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    movement_type = Column(
        SQLEnum(MovementType),
        nullable=False
    )

    reference_id = Column(
        Integer,
        nullable=True
    )

    reference_type = Column(
        String(50),
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )