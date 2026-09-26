from sqlalchemy.orm import Session

from app.modules.user.models import User
from .models import PasswordResetOTP


class AuthRepository:

    def __init__(self, db: Session):
        self.db = db

    # =====================================
    # USER
    # =====================================

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_user_by_username(
        self,
        username: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

    def create_user(
        self,
        user: User,
    ) -> User:

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    # =====================================
    # OTP
    # =====================================

    def create_otp(
        self,
        otp: PasswordResetOTP,
    ) -> PasswordResetOTP:

        self.db.add(otp)
        self.db.commit()
        self.db.refresh(otp)

        return otp

    def get_latest_otp(
        self,
        user_id: int,
    ) -> PasswordResetOTP | None:

        return (
            self.db.query(PasswordResetOTP)
            .filter(
                PasswordResetOTP.user_id == user_id,
                PasswordResetOTP.is_used == False,
            )
            .order_by(
                PasswordResetOTP.created_at.desc()
            )
            .first()
        )

    def update(self) -> None:

        self.db.commit()

    def delete_unused_otps(
        self,
        user_id: int,
    ) -> None:

        (
            self.db.query(PasswordResetOTP)
            .filter(
                PasswordResetOTP.user_id == user_id,
                PasswordResetOTP.is_used == False,
            )
            .update(
                {
                    PasswordResetOTP.is_used: True
                }
            )
        )

        self.db.commit()