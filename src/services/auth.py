from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.config import Settings
from src.configs.database import get_db
from src.repositories.user_repository import UserRepository
from src.schemas.auth import AccessTokenInputDataSchema
from src.schemas.user import UserInDBSchema, UserSchema
from src.utils.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

settings = Settings() 

async def authenticate_user(session: AsyncSession, email: str, password: str) -> UserInDBSchema | bool:
    user_dict = await UserRepository(session).get_user_by_email(email=email)
    if not user_dict:
        return False
    user = UserInDBSchema(
        id=user_dict.id,
        fullname=user_dict.fullname,
        email=user_dict.email,
        is_active=user_dict.is_active,
        created_at=user_dict.created_at,
        updated_at=user_dict.updated_at,
        password=user_dict.password,
    )
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_db)], 
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserInDBSchema:   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = AccessTokenInputDataSchema(email=email)

    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        raise credentials_exception
    user_dict = await UserRepository(session).get_user_by_email(email=token_data.email)
    user = UserInDBSchema(
        id=user_dict.id,
        fullname=user_dict.fullname,
        email=user_dict.email,
        is_active=user_dict.is_active,
        created_at=user_dict.created_at,
        updated_at=user_dict.updated_at,
        password=user_dict.password,
    )
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
) -> UserInDBSchema:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
