import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_task_by_id(self, task_id: int, user_id: int) -> Task | None:
        task_obj = await self.session.scalar(sa.select(Task).where(Task.id == task_id, Task.user_id == user_id))
        if task_obj is None:
            return None
        return task_obj

    async def create_task(self, title: str, content: str, user_id: int, status: bool = True) -> Task:
        new_task = Task(title=title, content=content, user_id=user_id, status=status)
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        return new_task