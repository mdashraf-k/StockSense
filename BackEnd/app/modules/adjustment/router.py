from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import current_user
from app.core.db import DB


from .repository import AdjustmentRepository
from .schemas import (
    AdjustmentCreate,
    AdjustmentResponse
)
from .service import AdjustmentService


router = APIRouter(
    prefix="/adjustments",
    tags=["Adjustments"]
)


def get_adjustment_service(
    db: DB
):

    return AdjustmentService(
        AdjustmentRepository(db),
        db
    )


@router.post(
    "",
    response_model=AdjustmentResponse,
    status_code=201
)
def create_adjustment(
    data: AdjustmentCreate,
    user: current_user,
    service: AdjustmentService = Depends(
        get_adjustment_service
    )
):

    return service.create(
        data,
        user.id
    )


@router.get(
    "",
    response_model=list[AdjustmentResponse]
)
def get_adjustments(
    user: current_user,
    service: AdjustmentService = Depends(
        get_adjustment_service
    )
):

    return service.get_all()


@router.get(
    "/{adjustment_id}",
    response_model=AdjustmentResponse
)
def get_adjustment(
    adjustment_id: int,
    user: current_user,
    service: AdjustmentService = Depends(
        get_adjustment_service
    )
):

    return service.get_by_id(
        adjustment_id
    )


@router.post(
    "/{adjustment_id}/validate",
    response_model=AdjustmentResponse
)
def validate_adjustment(
    adjustment_id: int,
    user: current_user,
    service: AdjustmentService = Depends(
        get_adjustment_service
    )
):

    return service.validate(
        adjustment_id,
        user.id
    )