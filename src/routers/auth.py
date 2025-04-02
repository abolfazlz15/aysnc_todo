from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.config import Settings
from src.configs.database import get_db
from src.schemas.auth import RefreshTokenSchema, TokenSchema
from src.schemas.user import UserInDBSchema
from src.services.auth import authenticate_user, get_current_active_user
from src.services.auth_token import AuthTokenService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

settings = Settings()

@router.post("/login", response_model=TokenSchema, name="user:login")
async def login_for_access_token(
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
    access_token_expires = timedelta(minutes=settings.access_token_lifetime)
    refresh_token_expires = timedelta(minutes=settings.refresh_token_lifetime)
    access_token = AuthTokenService.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = AuthTokenService.create_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires,
    )
    return TokenSchema(
        refresh_token=refresh_token,
        access_token=access_token,
        token_type="bearer",
    )

@router.post("/token/refresh/", response_model=TokenSchema, name="user:login")
async def get_refresh_token(
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
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_access_token = AuthTokenService.create_access_token({"sub": payload["sub"]})
    return TokenSchema(
        refresh_token=refresh_token.refresh_token,
        access_token=new_access_token,
        token_type="bearer",
    )


@router.get('test', response_model=dict, name="user:test_token")
def test_token(current_user: UserInDBSchema = Depends(get_current_active_user)) -> dict:
    return {'message': f'test token {current_user.email}'}

