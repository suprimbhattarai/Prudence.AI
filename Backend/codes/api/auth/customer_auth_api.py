from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from codes.database import get_db
from codes.dependencies.authentication import get_current_user

from codes.models.users.user import User

from codes.schemas.auth.customer_register import (
    UserRegisterRequest,
    UserRegisterResponse,
)
from codes.schemas.auth.customer_login import UserLoginRequest
from codes.schemas.auth.token import (
    TokenResponse,
    CurrentUserResponse,
)

from codes.services.auth.customer_auth_service import (
    CustomerAuthService,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserRegisterRequest,
    db: Annotated[Session, Depends(get_db)],
):
    return CustomerAuthService(db).register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    data: UserLoginRequest,
    db: Annotated[Session, Depends(get_db)],
):
    tokens = CustomerAuthService(db).login(data)

    return TokenResponse(**tokens)


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_my_account(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return current_user
