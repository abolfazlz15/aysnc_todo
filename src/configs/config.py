from datetime import timedelta
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # general settings
    debug: bool = True

    # Database Config
    database_hostname: str
    database_username: str
    database_password: str
    database_name: str
    database_url: Optional[str] = None
    
    # JWT Config
    secret_key: str
    algorithm: str = "HS256"
    access_token_lifetime: int = 3600  # seconds
    refresh_token_lifetime: timedelta = timedelta(days=20)  # 20 days
    # reset_pass_access_token_lifetime: int = 10 * 60  # minutes

    @field_validator("refresh_token_lifetime", mode="before")
    def parse_refresh_token_lifetime(cls, value):
        if isinstance(value, str):
            # Convert string to integer days, then to timedelta
            try:
                days = int(value)
                return timedelta(days=days)
            except ValueError:
                raise ValueError(f"Invalid refresh_token_lifetime: {value}")
        return value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database_url = (
            f"postgresql+asyncpg://{self.database_username}:{self.database_password}"
            f"@{self.database_hostname}/{self.database_name}"
        )

    class Config:
        env_file = ".env"
