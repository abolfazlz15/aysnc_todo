from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    fullname: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserInDB(User):
    hashed_password: str