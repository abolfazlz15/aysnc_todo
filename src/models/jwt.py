from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from src.configs.database import Base
from src.models.user import User


class BlackListRefreshToken(Base):
    __tablename__ = "blacklist_refresh_tokens"

    id: Mapped[int] = mapped_column(
        primary_key=True,
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

    jti: Mapped[str] = mapped_column()

    __table_args__ = (
        Index("idx_user_jti", "user_id", "jti"),  
    )
