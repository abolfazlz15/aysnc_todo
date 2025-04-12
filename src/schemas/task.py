from pydantic import BaseModel, Field
from datetime import datetime


class BaseTaskSchema(BaseModel):
    title: str
    content: str
    status: bool = Field(default=False)


class TaskCreateOutSchema(BaseTaskSchema):
    id: int
    created_at: datetime
    user_id: int