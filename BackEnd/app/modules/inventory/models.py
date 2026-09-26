from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.config.databases import Base


class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey(
            "products.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    warehouse_id = Column(
        Integer,
        ForeignKey(
            "warehouses.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "warehouse_id",
            name="uq_product_warehouse"
        ),
    )

    product = relationship(
        "Product"
    )

    warehouse = relationship(
        "Warehouse"
    )