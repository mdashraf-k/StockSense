from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import DB

from .repository import WarehouseRepository
from .schemas import (
    WarehouseCreate,
    WarehouseResponse,
    WarehouseUpdate
)
from .service import WarehouseService


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)


def get_warehouse_service(
    db: DB
):

    return WarehouseService(
        WarehouseRepository(db),
        db
    )


@router.post(
    "/",
    response_model=WarehouseResponse,
    status_code=201
)
def create_warehouse(
    data: WarehouseCreate,
    service: WarehouseService = Depends(
        get_warehouse_service
    )
):

    return service.create(data)


@router.get(
    "/",
    response_model=list[WarehouseResponse]
)
def get_warehouses(
    service: WarehouseService = Depends(
        get_warehouse_service
    )
):

    return service.get_all()


@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def get_warehouse(
    warehouse_id: int,
    service: WarehouseService = Depends(
        get_warehouse_service
    )
):

    return service.get_by_id(
        warehouse_id
    )


@router.patch(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def update_warehouse(
    warehouse_id: int,
    data: WarehouseUpdate,
    service: WarehouseService = Depends(
        get_warehouse_service
    )
):

    return service.update(
        warehouse_id,
        data
    )