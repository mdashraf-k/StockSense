from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import DB


from .repository import LedgerRepository
from .schemas import LedgerResponse
from .service import LedgerService


router = APIRouter(
    prefix="/ledger",
    tags=["Stock Ledger"]
)


def get_ledger_service(
    db: DB
):

    return LedgerService(
        LedgerRepository(db),
        db
    )


@router.get(
    "/",
    response_model=list[LedgerResponse]
)
def get_ledger(
    service: LedgerService = Depends(
        get_ledger_service
    )
):

    return service.get_all()


@router.get(
    "/product/{product_id}",
    response_model=list[LedgerResponse]
)
def get_product_history(
    product_id: int,
    service: LedgerService = Depends(
        get_ledger_service
    )
):

    return service.get_product_history(
        product_id
    )


@router.get(
    "/warehouse/{warehouse_id}",
    response_model=list[LedgerResponse]
)
def get_warehouse_history(
    warehouse_id: int,
    service: LedgerService = Depends(
        get_ledger_service
    )
):

    return service.get_warehouse_history(
        warehouse_id
    )