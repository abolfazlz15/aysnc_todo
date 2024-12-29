from pydantic_settings import BaseSettings
from typing import Optional

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
    # access_token_lifetime: int = 3600  # seconds
    # reset_pass_access_token_lifetime: int = 10 * 60  # minutes
    # refresh_token_lifetime: int = 86400 * 365  # seconds

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database_url = (
            f"postgresql+asyncpg://{self.database_username}:{self.database_password}"
            f"@{self.database_hostname}/{self.database_name}"
        )
        print(self.database_url)

    class Config:
        env_file = ".env"
