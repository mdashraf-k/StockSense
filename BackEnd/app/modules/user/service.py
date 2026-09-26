from fastapi import HTTPException

from .repository import UserRepository
from .schemas import UserUpdate


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: int):

        user = self.repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    def get_all_users(self):

        return self.repository.get_all()

    def update_user(
        self,
        user_id: int,
        data: UserUpdate
    ):

        user = self.get_user(user_id)

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:

            existing = self.repository.get_by_email(
                update_data["email"]
            )

            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists"
                )

        if "username" in update_data:

            existing = self.repository.get_by_username(
                update_data["username"]
            )

            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=409,
                    detail="Username already exists"
                )

        for key, value in update_data.items():
            setattr(user, key, value)

        return self.repository.update(user)

    def delete_user(self, user_id: int):

        user = self.get_user(user_id)

        self.repository.delete(user)