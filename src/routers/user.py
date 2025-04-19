from fastapi import APIRouter, Depends, status

from src.schemas.user import UserFullDataSchema, UserProfileDetailSchema
from src.services.auth import get_current_active_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get(
    "profile/",
    response_model=UserProfileDetailSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user_profile_detail_router(
    current_user: UserFullDataSchema = Depends(get_current_active_user),
):
    return UserProfileDetailSchema(
        id=current_user.id,
        fullname=current_user.fullname,
        email=current_user.email,
    )