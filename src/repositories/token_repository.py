from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.models.jwt import BlackListRefreshToken


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_token_by_jti(self, token_jti: str) -> bool:
        return True if await self.session.scalar(
            sa.select(
                BlackListRefreshToken,
            ).where(
                BlackListRefreshToken.jti == token_jti,
            )
        ) else False

    async def create_revoke_token(self, token_jti: str, user_id: int):
        blacklist_refresh_token = BlackListRefreshToken(
            user_id=user_id,
            jti=token_jti, # TODO find a solution for generate unique UUID 
            revoked=True,
        )
        self.session.add(blacklist_refresh_token)
        await self.session.commit()