from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category

async def get_or_create_category(db: AsyncSession, path: str) -> Category:
    levels = path.split("/")
    parent = None

    for name in levels:
        stmt = select(Category).where(
            Category.name == name,
            Category.parent_id == (parent.id if parent else None)
        )
        result = await db.execute(stmt)
        current = result.scalar_one_or_none()

        if not current:
            current = Category(name=name, parent_id=parent.id if parent else None)
            db.add(current)
            await db.commit()
            await db.refresh(current)

        parent = current

    return current
