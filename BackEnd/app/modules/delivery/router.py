from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import current_user
from app.core.db import DB


from .repository import DeliveryRepository
from .schemas import DeliveryCreate, DeliveryResponse
from .service import DeliveryService


router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"]
)


def get_delivery_service(
    db: DB
):

    return DeliveryService(
        DeliveryRepository(db),
        db
    )


@router.post(
    "/",
    response_model=DeliveryResponse,
    status_code=201
)
def create_delivery(
    data: DeliveryCreate,
    user: current_user,
    service: DeliveryService = Depends(
        get_delivery_service
    )
):

    return service.create(
        data,
        user.id
    )


@router.get(
    "/",
    response_model=list[DeliveryResponse]
)
def get_deliveries(
    user: current_user,
    service: DeliveryService = Depends(
        get_delivery_service
    )
):

    return service.get_all()


@router.get(
    "/{delivery_id}",
    response_model=DeliveryResponse
)
def get_delivery(
    delivery_id: int,
    user: current_user,
    service: DeliveryService = Depends(
        get_delivery_service
    )
):

    return service.get_by_id(
        delivery_id
    )


@router.post(
    "/{delivery_id}/validate",
    response_model=DeliveryResponse
)
def validate_delivery(
    delivery_id: int,
    user: current_user,
    service: DeliveryService = Depends(
        get_delivery_service
    )
):

    return service.validate(
        delivery_id,
        user.id
    )