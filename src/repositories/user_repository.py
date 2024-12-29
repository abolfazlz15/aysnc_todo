from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from ..models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> sa.RowMapping | None:
        """Fetch a user by their ID."""
        result = await self.session.execute(sa.select(User).where(User.email == email))
        return result.fetchone()._mapping

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Fetch a user by their ID."""
        result = await self.session.execute(sa.select(User).where(User.id == user_id))
        return result.fetchone()

    async def get_user_by_email(self, email: str) -> User | None:
        """Fetch a user by their email."""
        result = await self.session.execute(sa.select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, fullname: str, email: str, password: str) -> User:
        """Create a new user."""
        new_user = User(fullname=fullname, email=email, password=password)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user) 
        return new_user

    async def update_user(self, user_id: int, **kwargs) -> User | None:
        """
        Update a user's fields.
        
        Args:
            user_id: ID of the user to update.
            kwargs: Fields to update (e.g., fullname, email).
        
        Returns:
            The updated user object or None if the user doesn't exist.
        """
        stmt = sa.update(User).where(User.id == user_id).values(**kwargs).returning(User)
        result = await self.session.execute(stmt)
        updated_user = result.scalar_one_or_none()
        if updated_user:
            await self.session.commit()
        return updated_user

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user by their ID."""
        user = await self.get_user_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False
