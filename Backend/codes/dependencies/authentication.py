from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from codes.core.security.jwt import decode_access_token
from codes.database import get_db

from codes.models.users.user import User

from codes.repositories.auth.user_repository import UserRepository
from codes.repositories.organizations.organization_repository import (
    OrganizationRepository,
)

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)

        raw_user_id = payload.get("sub")

        if not isinstance(raw_user_id, str):
            raise unauthorized

        user_id = int(raw_user_id)

        if user_id <= 0:
            raise unauthorized

    except (InvalidTokenError, ValueError, TypeError):
        raise unauthorized

    user = UserRepository(db).get_by_id(user_id)

    if user is None:
        raise unauthorized

    if not user.is_active or not user.is_verified:
        raise unauthorized

    if (
        payload.get("organization_id") != user.organization_id
        or payload.get("role") != user.role.value
    ):
        raise unauthorized

    organization = OrganizationRepository(db).get_active_by_id(user.organization_id)

    if organization is None:
        raise unauthorized

    return user


def get_current_admin(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> User:
    from codes.core.enums.user_role import UserRole

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator permission required",
        )

    return current_user
