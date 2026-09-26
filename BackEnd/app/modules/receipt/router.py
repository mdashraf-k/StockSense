from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import current_user
from app.core.db import DB


from .repository import ReceiptRepository
from .schemas import ReceiptCreate, ReceiptResponse
from .service import ReceiptService


router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"]
)


def get_receipt_service(
    db: DB

):

    return ReceiptService(
        ReceiptRepository(db),
        db
    )


@router.post(
    "/",
    response_model=ReceiptResponse,
    status_code=201
)
def create_receipt(
    data: ReceiptCreate,
    user: current_user,
    service: ReceiptService = Depends(
        get_receipt_service
    )
):

    return service.create(
        data,
        user.id
    )


@router.get(
    "/",
    response_model=list[ReceiptResponse]
)
def get_receipts(
    user: current_user,
    service: ReceiptService = Depends(
        get_receipt_service
    )
):

    return service.get_all()


@router.get(
    "/{receipt_id}",
    response_model=ReceiptResponse
)
def get_receipt(
    receipt_id: int,
    user: current_user,
    service: ReceiptService = Depends(
        get_receipt_service
    )
):

    return service.get_by_id(
        receipt_id
    )


@router.post(
    "/{receipt_id}/validate",
    response_model=ReceiptResponse
)
def validate_receipt(
    receipt_id: int,
    user: current_user,
    service: ReceiptService = Depends(
        get_receipt_service
    )
):

    return service.validate(
        receipt_id,
        user.id
    )