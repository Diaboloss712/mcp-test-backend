from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models.category import Category


def normalize_category_name(name: str) -> str:
    return name.replace(" ", "").lower()

async def get_or_create_category(db: AsyncSession, path: str) -> Category:
    levels = path.strip().split("/")
    parent = None
    current = None

    for name in levels:
        normalized = normalize_category_name(name)

        # 이미 존재하는 카테고리인지 확인
        stmt = select(Category).where(
            func.lower(func.replace(Category.name, " ", "")) == normalized,
            Category.parent_id == (parent.id if parent else None)
        )

        result = await db.execute(stmt)
        current = result.scalar_one_or_none()

        if not current:
            try:
                current = Category(name=name, parent_id=parent.id if parent else None)
                db.add(current)
                await db.commit()
                await db.refresh(current)

            except IntegrityError:
                # id 중복 에러 발생 시 rollback 후 다시 조회
                await db.rollback()
                result = await db.execute(stmt)
                current = result.scalar_one_or_none()

                if not current:
                    raise RuntimeError(f"카테고리 생성 실패: {name} (부모 id: {parent.id if parent else 'None'})")

        parent = current

    return current
