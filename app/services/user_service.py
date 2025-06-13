from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserUpdate
from app.crud.user import update_user_fields


async def update_profile_service(update_data: UserUpdate, user: User, db: AsyncSession):
    fields = update_data.model_dump(exclude_unset=True)
    return await update_user_fields(user, fields, db)


async def get_profile_service(user: User):
    return user
