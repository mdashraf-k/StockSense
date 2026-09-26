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


class Transfer(Base):

    __tablename__ = "transfers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    source_warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    destination_warehouse_id = Column(
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
        "TransferItem",
        back_populates="transfer",
        cascade="all, delete-orphan"
    )


class TransferItem(Base):

    __tablename__ = "transfer_items"

    id = Column(
        Integer,
        primary_key=True
    )

    transfer_id = Column(
        Integer,
        ForeignKey(
            "transfers.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    transfer = relationship(
        "Transfer",
        back_populates="items"
    )