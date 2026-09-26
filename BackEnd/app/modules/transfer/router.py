from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import current_user
from app.core.db import DB


from .repository import TransferRepository
from .schemas import TransferCreate, TransferResponse
from .service import TransferService


router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"]
)


def get_transfer_service(
    db:DB
):

    return TransferService(
        TransferRepository(db),
        db
    )


@router.post(
    "/",
    response_model=TransferResponse,
    status_code=201
)
def create_transfer(
    data: TransferCreate,
    user: current_user,
    service: TransferService = Depends(
        get_transfer_service
    )
):

    return service.create(
        data,
        user.id
    )


@router.get(
    "/",
    response_model=list[TransferResponse]
)
def get_transfers(
    user: current_user,
    service: TransferService = Depends(
        get_transfer_service
    )
):

    return service.get_all()


@router.get(
    "/{transfer_id}",
    response_model=TransferResponse
)
def get_transfer(
    transfer_id: int,
    user: current_user,
    service: TransferService = Depends(
        get_transfer_service
    )
):

    return service.get_by_id(
        transfer_id
    )


@router.post(
    "/{transfer_id}/validate",
    response_model=TransferResponse
)
def validate_transfer(
    transfer_id: int,
    user: current_user,
    service: TransferService = Depends(
        get_transfer_service
    )
):

    return service.validate(
        transfer_id,
        user.id
    )