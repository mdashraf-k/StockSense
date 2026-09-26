from sqlalchemy import Column, Integer, String, Text

from app.config.databases import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    sku = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    category = Column(
        String(100),
        nullable=True
    )

    unit_of_measure = Column(
        String(30),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )