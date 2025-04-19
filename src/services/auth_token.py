import uuid
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.config import Settings
from src.repositories.token_repository import TokenRepository

settings = Settings()

class AuthTokenService:
    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """Generate a refresh token."""
        to_encode = data.copy() 
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=30))
        to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    async def revoke_refresh_token(session: AsyncSession, jti: str, user_id: int) -> None:
        await TokenRepository(session).create_revoke_token(
            token_jti=jti,
            user_id=user_id,
        )

    @staticmethod
    async def is_token_revoked(session: AsyncSession, jti: str) -> bool:
        """Check if a refresh token is revoked."""
        return await TokenRepository(session).get_token_by_jti(token_jti=jti)


    async def verify_refresh_token(self, token: str, session: AsyncSession) -> dict:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            if await self.is_token_revoked(session, payload["jti"]):
                raise ValueError("Invalid token")
            return payload
        except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
            raise ValueError("Invalid token")

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)