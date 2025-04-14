from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
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
    try:
        return await TaskRepository(db).create_task(**task.model_dump(), user_id=current_user.id)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="something went wrong",
        )
    
@router.get("/get/{task_id}/", response_model=TaskCreateOutSchema, name="task:get")
async def get_task_router(
    task_id: int,
    current_user: UserInDBSchema = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    if task := await TaskRepository(db).get_task_by_id(task_id=task_id, user_id=current_user.id):
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="task not found",
    )