from pydantic import BaseModel


class TokenSchema(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str


class AccessTokenInputDataSchema(BaseModel):
    email: str | None = None


class RefreshTokenSchema(BaseModel):
    refresh_token: str
