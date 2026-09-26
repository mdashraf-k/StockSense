from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import DB

from .repository import UserRepository
from .schemas import UserResponse, UserUpdate
from .service import UserService
from app.core.auth import current_user as CurrentUser


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_user_service(
    db: DB
):

    repository = UserRepository(db)

    return UserService(repository)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: CurrentUser,
    service: UserService = Depends(get_user_service),
):
    return service.get_user(current_user.id)

@router.patch(
    "/me",
    response_model=UserResponse
)
def update_my_profile(
    data: UserUpdate,
    current_user,
    service: UserService = Depends(get_user_service)
):

    return service.update_user(
        current_user.id,
        data
    )