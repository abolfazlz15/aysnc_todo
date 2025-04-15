from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.config import Settings
from src.configs.database import get_db
from src.schemas.auth import ChangePasswordIn, RefreshTokenSchema, TokenSchema
from src.schemas.user import UserInDBSchema
from src.services.auth import (authenticate_user, change_password,
                               get_current_active_user, logout_user)
from src.services.auth_token import AuthTokenService
from src.utils.exceptions import TokenAlreadyRevoked, TokenInvalid

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

settings = Settings()

@router.post("/login/", response_model=TokenSchema, name="auth:login")
async def login_router(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> TokenSchema:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AuthTokenService.create_access_token(
        data={"sub": str(user.id)}, expires_delta=timedelta(minutes=settings.access_token_lifetime)
    )
    refresh_token = AuthTokenService.create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.refresh_token_lifetime),
    )
    return TokenSchema(
        refresh_token=refresh_token,
        access_token=access_token,
        token_type="bearer",
    )

@router.post("/token/refresh/", response_model=TokenSchema, name="auth:refresh_token")
async def get_refresh_token_router(
    refresh_token: RefreshTokenSchema,
    db: AsyncSession = Depends(get_db),
) -> TokenSchema:
    try:
        payload = await AuthTokenService().verify_refresh_token(
            token=refresh_token.refresh_token,
            session=db,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token is invalid or expired",
        )
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    new_access_token = AuthTokenService.create_access_token({"sub": payload["sub"]})
    return TokenSchema(
        refresh_token=refresh_token.refresh_token,
        access_token=new_access_token,
        token_type="bearer",
    )

@router.post("/logout/", response_model=None, name="auth:logout", status_code=status.HTTP_200_OK)
async def logout_user_router(
    refresh_token: RefreshTokenSchema,
    current_user: UserInDBSchema = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await logout_user(refresh_token.refresh_token, db, current_user.id)
    except (TokenAlreadyRevoked, TokenInvalid) as exp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exp))

@router.post("/change-password/")
async def change_password_router(
    user_new_password: ChangePasswordIn,
    current_user: UserInDBSchema = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        new_password = await change_password(current_user, user_new_password, db)
        if not new_password:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'something wrong')
        return {'message': 'Your password has been successfully changed'}
    except ValueError as exp:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exp))


@router.get("/test", response_model=dict, name="auth:test_token")
def test_token(current_user: UserInDBSchema = Depends(get_current_active_user)) -> dict:
    return {"message": f"test token {current_user.email}"}


