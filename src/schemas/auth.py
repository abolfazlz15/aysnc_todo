from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenInputDataSchema(BaseModel):
    email: str | None = None
