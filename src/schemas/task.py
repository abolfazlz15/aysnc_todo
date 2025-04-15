from datetime import datetime

from pydantic import BaseModel, Field


class BaseTaskSchema(BaseModel):
    title: str
    status: bool = Field(default=False)

class TaskListSchema(BaseTaskSchema):
    id: int
    class Config:
        from_attributes = True
class TaskCreateOutSchema(BaseTaskSchema):
    id: int
    content: str
    created_at: datetime
    user_id: int