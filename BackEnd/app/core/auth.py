from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config.config import settings
from app.modules.auth.schemas import CurrentUser
from app.core.enums import UserRole

def get_current_user(
    request: Request
) -> CurrentUser:

    # Get JWT from cookie
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        # Get data from JWT
        username: str | None = payload.get("sub")
        user_id: int | None = payload.get("id")
        role: str | None = payload.get("role")

        # Validate required data
        if (
            username is None
            or user_id is None
            or role is None
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user"
            )

        # Return current user
        return CurrentUser(
            id=user_id,
            username=username,
            role=UserRole(role)
        )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )


# Reusable dependency
current_user = Annotated[
    CurrentUser,
    Depends(get_current_user)
]

# ROLE CHECK

def require_role(
    required_role: UserRole,
):

    def role_checker(
        user: CurrentUser = Depends(
            get_current_user
        ),
    ) -> CurrentUser:

        if user.role != required_role:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You don't have permission "
                    "to perform this action"
                ),
            )

        return user

    return role_checker


inventory_manager = Annotated[
    CurrentUser,
    Depends(
        require_role(
            UserRole.INVENTORY_MANAGER
        )
    ),
]


warehouse_staff = Annotated[
    CurrentUser,
    Depends(
        require_role(
            UserRole.WAREHOUSE_STAFF
        )
    ),
]