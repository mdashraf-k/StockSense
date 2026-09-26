from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.config.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# =====================================
# PASSWORD
# =====================================

def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password cannot be longer than 72 bytes")

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    if len(plain_password.encode("utf-8")) > 72:
        return False

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# =====================================
# JWT
# =====================================

def create_access_token(
    user_id: int,
    username: str,
    role: str,
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(days=30)
    )

    payload = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )