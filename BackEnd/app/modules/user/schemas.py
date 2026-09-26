from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    email: EmailStr | None = None