import sqlalchemy as sa
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.utils.enums.task import TaskFieldEnum


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

    async def get_task_list(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        sort_by: TaskFieldEnum = TaskFieldEnum.CREATED_AT.value,
        sort_order: str = "desc",
        status: bool | None = None,
    ) -> list[tuple[Task, ...]]:
        query = sa.select(Task.id, Task.title, Task.status).where(Task.user_id == user_id)
        
        if status is not None:
            query = query.where(Task.status == status)
            
        if sort_order.lower() == "asc":
            query = query.order_by(asc(getattr(Task, sort_by)))
        else:
            query = query.order_by(desc(getattr(Task, sort_by)))
            
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        return result.all()

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        task_obj = await self.get_task_by_id(task_id=task_id, user_id=user_id)
        if task_obj is None:
            return False
        await self.session.delete(task_obj)
        await self.session.commit()
        return True
    
    async def update_task(self, task_id: int, user_id: int, **kwargs) -> Task | None:
        """
        Task a user's fields.
        
        Args:
            task_id: ID of the task to update.
            kwargs: Fields to update (e.g., title, content, status).
        
        Returns:
            The updated task object or None if the task doesn't exist.
        """
        stmt = sa.update(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
            ).values(
                updated_at=sa.func.now(),
                **kwargs,
            ).returning(Task)
        result = await self.session.execute(stmt)
        updated_task = result.scalar_one_or_none()
        if updated_task:
            await self.session.commit()
        return updated_task
