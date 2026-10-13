from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from codes.core.config.config import settings
from codes.core.enums.user_role import UserRole


def create_access_token(
    user_id: int,
    organization_id: int,
    role: UserRole,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "organization_id": organization_id,
        "role": role.value,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_access_token_expire_minutes),
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(
    user_id: int,
    organization_id: int,
    role: UserRole,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "organization_id": organization_id,
        "role": role.value,
        "iat": now,
        "exp": now + timedelta(days=settings.jwt_refresh_token_expire_days),
        "type": "refresh",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        options={
            "require": ["sub", "iat", "exp"],
        },
    )

    if payload.get("type") != "access":
        raise InvalidTokenError("Invalid token type")

    return payload
