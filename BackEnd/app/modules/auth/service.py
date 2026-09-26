from datetime import datetime, timedelta, timezone
import secrets

from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.modules.user.models import User

from .models import PasswordResetOTP
from .repository import AuthRepository
from .schemas import (
    ForgotPasswordRequest,
    LoginRequest,
    ResetPasswordRequest,
    SignupRequest,
)


class AuthService:

    def __init__(
        self,
        repository: AuthRepository,
    ):
        self.repository = repository

    # =====================================
    # SIGN UP
    # =====================================

    def signup(
        self,
        data: SignupRequest,
    ) -> User:

        # Check email
        existing_email = (
            self.repository
            .get_user_by_email(data.email)
        )

        if existing_email:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # Check username
        existing_username = (
            self.repository
            .get_user_by_username(data.username)
        )

        if existing_username:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )

        # Create user
        user = User(
            name=data.name,
            username=data.username,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
            role="warehouse_staff",
        )

        return self.repository.create_user(user)

    # =====================================
    # LOGIN
    # =====================================

    def login(
        self,
        data: LoginRequest,
    ):

        user = (
            self.repository
            .get_user_by_email(data.email)
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        password_valid = verify_password(
            data.password,
            user.password_hash,
        )

        if not password_valid:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Create JWT
        token = create_access_token(
            user_id=user.id,
            username=user.username,
            role=user.role,
        )

        return user, token

    # =====================================
    # FORGOT PASSWORD
    # =====================================

    def forgot_password(
        self,
        data: ForgotPasswordRequest,
    ) -> None:

        user = (
            self.repository
            .get_user_by_email(data.email)
        )

        # Don't reveal whether email exists
        if not user:
            return

        # Invalidate previous OTPs
        self.repository.delete_unused_otps(
            user.id
        )

        # Generate 6-digit OTP
        otp = f"{secrets.randbelow(1_000_000):06d}"

        # Hash OTP
        otp_hash = hash_password(otp)

        # OTP valid for 10 minutes
        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(minutes=10)
        )

        reset_otp = PasswordResetOTP(
            user_id=user.id,
            otp_hash=otp_hash,
            expires_at=expires_at,
        )

        self.repository.create_otp(
            reset_otp
        )

        # ---------------------------------
        # TEMPORARY FOR HACKATHON DEVELOPMENT
        # ---------------------------------
        print(
            f"[PASSWORD RESET OTP] "
            f"{user.email} -> {otp}"
        )

        # Later:
        # send OTP through email service

    # RESET PASSWORD

    def reset_password(
        self,
        data: ResetPasswordRequest,
    ) -> None:

        user = (
            self.repository
            .get_user_by_email(data.email)
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP or email",
            )

        otp_record = (
            self.repository
            .get_latest_otp(user.id)
        )

        if not otp_record:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )

        # Check expiration
        now = datetime.now(timezone.utc)

        if otp_record.expires_at < now:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired",
            )

        # Verify OTP
        valid_otp = verify_password(
            data.otp,
            otp_record.otp_hash,
        )

        if not valid_otp:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP",
            )

        # Update password
        user.password_hash = hash_password(
            data.new_password
        )

        # Mark OTP as used
        otp_record.is_used = True

        self.repository.update()
