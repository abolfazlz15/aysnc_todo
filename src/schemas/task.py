from datetime import datetime

from pydantic import BaseModel, Field


class BaseTaskSchema(BaseModel):
    title: str
    status: bool = Field(default=False)

class TaskListSchema(BaseTaskSchema):
    id: int

class TaskUpdateInSchema(BaseModel):
    title: str | None = None
    status: bool | None = None
    content: str | None = None


class TaskCreateOutSchema(BaseTaskSchema):
    id: int
    content: str
    created_at: datetime
    user_id: int