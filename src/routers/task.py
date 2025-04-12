from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.repositories.task_repository import TaskRepository
from src.schemas.task import BaseTaskSchema, TaskCreateOutSchema
from src.schemas.user import UserInDBSchema
from src.services.auth import get_current_active_user

router = APIRouter(
    prefix="/task",
    tags=["task"],
)


@router.post("/create/", response_model=TaskCreateOutSchema, name="task:create", status_code=status.HTTP_201_CREATED)
async def create_task_router(
    task: BaseTaskSchema,
    current_user: UserInDBSchema = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Create a new task.
    """
    try:
        return await TaskRepository(db).create_task(**task.model_dump(), user_id=current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create task: {str(e)}",
        )