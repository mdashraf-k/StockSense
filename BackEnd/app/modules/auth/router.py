from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from sqlalchemy.orm import Session

# from config.config import settings
from app.core.db import DB

from .repository import AuthRepository
from .schemas import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    LoginResponse,
    LoginUserResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    SignupRequest,
    SignupResponse,
)
from .service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# DEPENDENCY

def get_auth_service(
    db: DB,
) -> AuthService:

    repository = AuthRepository(db)

    return AuthService(repository)


# =====================================
# SIGN UP
# =====================================

@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    data: SignupRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    user = service.signup(data)

    return SignupResponse(
        message="Account created successfully",
        user_id=user.id,
    )


# =====================================
# LOGIN
# =====================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    data: LoginRequest,
    response: Response,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    user, token = service.login(data)

    response.set_cookie(
        key="access_token",
        value=token,

        # JavaScript cannot access this cookie
        httponly=True,

        # Local development
        # Change to True in production HTTPS
        secure=False,

        # Good default for same-site frontend/backend
        samesite="lax",

        # 30 days
        max_age=60 * 60 * 24 * 30,

        # Also set expiration
        expires=60 * 60 * 24 * 30,
    )

    return LoginResponse(
        message="Login successful",
        user=LoginUserResponse(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            role=user.role,
        ),
    )


# =====================================
# LOGOUT
# =====================================

@router.post(
    "/logout",
)
def logout(
    response: Response,
):

    response.delete_cookie(
        key="access_token",
    )

    return {
        "message": "Logout successful"
    }


# =====================================
# FORGOT PASSWORD
# =====================================

@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
)
def forgot_password(
    data: ForgotPasswordRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    service.forgot_password(data)

    # Same response whether email exists
    return ForgotPasswordResponse(
        message=(
            "If the email exists, "
            "an OTP has been sent."
        )
    )


# =====================================
# RESET PASSWORD
# =====================================

@router.post(
    "/reset-password",
    response_model=ResetPasswordResponse,
)
def reset_password(
    data: ResetPasswordRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    service.reset_password(data)

    return ResetPasswordResponse(
        message="Password reset successfully"
    )