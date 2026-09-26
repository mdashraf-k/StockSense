from sqlalchemy import Column, Integer, String, Text

from app.config.databases import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    location = Column(
        String(255),
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )