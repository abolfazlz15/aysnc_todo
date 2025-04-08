from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.config import Settings
from src.configs.database import get_db
from src.repositories.user_repository import UserRepository
from src.schemas.auth import AccessTokenInputDataSchema, ChangePasswordIn
from src.schemas.user import UserInDBSchema, UserSchema
from src.services.auth_token import AuthTokenService
from src.utils.exceptions import TokenAlreadyRevoked, TokenInvalid
from src.utils.security import get_password_hash, verify_password

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


async def logout_user(refresh_token: str, session: AsyncSession, user_id: int) -> None:
    token_service = AuthTokenService()
    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=["HS256"])
        if await token_service.is_token_revoked(session, payload["jti"]):
            raise TokenAlreadyRevoked("token already revoked")
        await token_service.revoke_refresh_token(session, payload["jti"], user_id=user_id)
    except KeyError:
        ... # TODO after config logging system add log here
    except jwt.exceptions.InvalidSignatureError:
        raise TokenInvalid("invalid token")
    

async def change_password(
        user: UserInDBSchema,
        password_data: ChangePasswordIn,
        session: AsyncSession,
    ) -> bool:
    if not verify_password(password_data.current_password, user.password):
        raise ValueError("Old password is incorrect")

    hashed_new_password = get_password_hash(password_data.new_password)
    updated_user = await UserRepository(session).update_user(user.id, password=hashed_new_password)
    return bool(updated_user)