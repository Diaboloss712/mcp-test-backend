from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserRead, UserUpdate
)
from app.services.user_service import (
    update_profile_service,
    get_profile_service
)

router = APIRouter()

@router.patch("/profile/update", response_model=UserRead)
async def update_profile(update: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await update_profile_service(update, current_user, db)

@router.get("/profile", response_model=UserRead)
async def read_profile(current_user: User = Depends(get_current_user)):
    return await get_profile_service(current_user)
