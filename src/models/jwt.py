import hashlib
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column
from src.configs.database import Base
from src.models.user import User

# def hash_jti(jti: str) -> str:
#     """Hash the jti for storage in the database."""
#     return hashlib.sha256(jti.encode('utf-8')).hexdigest()

class BlackListRefreshToken(Base):
    __tablename__ = "blacklist_refresh_tokens"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"),
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
    )
    revoked: Mapped[bool] = mapped_column(
        default=False,
    )

    hashed_jti: Mapped[str] = mapped_column()

    __table_args__ = (
        Index("idx_user_hashed_jti", "user_id", "hashed_jti"),  
    )

    def revoke(self):
        """Mark this token as revoked."""
        self.revoked = True
