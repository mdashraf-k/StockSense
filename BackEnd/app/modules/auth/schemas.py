from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.core.enums import UserRole


# CURRENT USER
class CurrentUser(BaseModel):
    id: int
    username: str
    role: UserRole


# SIGN UP

from pydantic import BaseModel, field_validator


class SignupRequest(BaseModel):
    name: str
    username: str
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:

        if len(password) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )

        if len(password.encode("utf-8")) > 72:
            raise ValueError(
                "Password cannot be longer than 72 bytes"
            )

        return password


class SignupResponse(BaseModel):
    message: str
    user_id: int


# LOGIN

class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class LoginUserResponse(BaseModel):

    id: int
    name: str
    username: str
    email: EmailStr
    role: UserRole


class LoginResponse(BaseModel):

    message: str
    user: LoginUserResponse


# FORGOT PASSWORD

class ForgotPasswordRequest(BaseModel):

    email: EmailStr


class ForgotPasswordResponse(BaseModel):

    message: str


# RESET PASSWORD

class ResetPasswordRequest(BaseModel):

    email: EmailStr

    otp: str = Field(
        min_length=6,
        max_length=6,
    )

    new_password: str = Field(
        min_length=8,
        max_length=100,
    )


class ResetPasswordResponse(BaseModel):

    message: str