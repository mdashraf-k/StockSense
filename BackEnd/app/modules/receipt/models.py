from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.config.databases import Base
from app.core.enums import DocumentStatus


class Receipt(Base):

    __tablename__ = "receipts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    supplier = Column(
        String(150),
        nullable=True
    )

    warehouse_id = Column(
        Integer,
        ForeignKey(
            "warehouses.id"
        ),
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
        "ReceiptItem",
        back_populates="receipt",
        cascade="all, delete-orphan"
    )


class ReceiptItem(Base):

    __tablename__ = "receipt_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    receipt_id = Column(
        Integer,
        ForeignKey(
            "receipts.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey(
            "products.id"
        ),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    receipt = relationship(
        "Receipt",
        back_populates="items"
    )