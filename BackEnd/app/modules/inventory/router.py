from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import DB


from .repository import InventoryRepository
from .schemas import InventoryResponse
from .service import InventoryService


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


def get_inventory_service(
    db: DB
):

    return InventoryService(
        InventoryRepository(db),
        db
    )


@router.get(
    "/",
    response_model=list[InventoryResponse]
)
def get_inventory(
    service: InventoryService = Depends(
        get_inventory_service
    )
):

    return service.get_all()


@router.get(
    "/product/{product_id}"
)
def get_product_stock(
    product_id: int,
    service: InventoryService = Depends(
        get_inventory_service
    )
):

    return service.get_product_stock(
        product_id
    )


@router.get(
    "/warehouse/{warehouse_id}"
)
def get_warehouse_stock(
    warehouse_id: int,
    service: InventoryService = Depends(
        get_inventory_service
    )
):

    return service.get_warehouse_stock(
        warehouse_id
    )


@router.get(
    "/product/{product_id}/warehouse/{warehouse_id}"
)
def get_stock(
    product_id: int,
    warehouse_id: int,
    service: InventoryService = Depends(
        get_inventory_service
    )
):

    return service.get_stock(
        product_id,
        warehouse_id
    )