# app/api/v1/category.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryOut

router = APIRouter()

@router.get("/", response_model=List[CategoryOut])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()


# 모의고사 출제용 최하위 카테고리 목록 
@router.get("/leaves", response_model=List[CategoryOut])
async def get_leaf_categories(db: AsyncSession = Depends(get_db)):
    # 모든 카테고리 가져오기
    result = await db.execute(select(Category))
    all_categories = result.scalars().all()

    # 부모로 참조된 id들 모으기
    parent_ids = set(c.parent_id for c in all_categories if c.parent_id is not None)

    # 하위 카테고리가 없는 것만 필터링
    leaf_categories = [c for c in all_categories if c.id not in parent_ids]

    return leaf_categories
