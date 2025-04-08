from datetime import datetime

from pydantic import BaseModel


class UserProfileDetailSchema(BaseModel):
    id: int
    fullname: str
    email: str


class UserFullDataSchema(UserProfileDetailSchema):
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserInDBSchema(UserFullDataSchema):
    password: str