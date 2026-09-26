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


class Delivery(Base):

    __tablename__ = "deliveries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer = Column(
        String(150),
        nullable=True
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
        "DeliveryItem",
        back_populates="delivery",
        cascade="all, delete-orphan"
    )


class DeliveryItem(Base):

    __tablename__ = "delivery_items"

    id = Column(
        Integer,
        primary_key=True
    )

    delivery_id = Column(
        Integer,
        ForeignKey(
            "deliveries.id",
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

    delivery = relationship(
        "Delivery",
        back_populates="items"
    )