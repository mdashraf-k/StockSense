from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.config.databases import Base
from app.core.enums import DocumentStatus


class Adjustment(Base):

    __tablename__ = "adjustments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    status = Column(
        SQLEnum(DocumentStatus),
        nullable=False,
        default=DocumentStatus.DRAFT
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    items = relationship(
        "AdjustmentItem",
        back_populates="adjustment",
        cascade="all, delete-orphan"
    )


class AdjustmentItem(Base):

    __tablename__ = "adjustment_items"

    id = Column(
        Integer,
        primary_key=True
    )

    adjustment_id = Column(
        Integer,
        ForeignKey(
            "adjustments.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    counted_quantity = Column(
        Integer,
        nullable=False
    )

    previous_quantity = Column(
        Integer,
        nullable=False
    )

    difference = Column(
        Integer,
        nullable=False
    )

    adjustment = relationship(
        "Adjustment",
        back_populates="items"
    )