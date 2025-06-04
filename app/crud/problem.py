from app.models.problem import Problem
from app.schemas.problem import ProblemCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.problem import Problem
from sqlalchemy import select, func


# 새로운 문제를 DB에 저장 
async def create_problem(db: AsyncSession, problem_data: ProblemCreate) -> Problem:
    problem = Problem(**problem_data.dict())
    db.add(problem)
    await db.commit()
    await db.refresh(problem)
    return problem

# 재귀적으로 하위 카테고리 탐색 
async def collect_descendant_ids(db, parent_id):
    ids = [parent_id]
    stmt = select(Category).where(Category.parent_id == parent_id)
    result = await db.execute(stmt)
    children = result.scalars().all()
    for child in children:
        ids.extend(await collect_descendant_ids(db, child.id))
    return ids

# 카테고리에 포함된 문제를 특정 개수만큼 추출 (Subject/Topic/Subtopic )
async def get_mock_exam_by_category_path(db, path: list[str], count: int):
    parent_id = None
    for name in path:
        stmt = select(Category).where(Category.name == name, Category.parent_id == parent_id)
        result = await db.execute(stmt)
        category = result.scalar_one_or_none()
        if not category:
            raise ValueError(f"카테고리 '{name}'을 찾을 수 없습니다.")
        parent_id = category.id

    # 하위 카테고리 존재 여부 확인 
    stmt = select(Category).where(Category.parent_id == parent_id)
    result = await db.execute(stmt)
    children = result.scalars().all()

    if children:
        category_ids = await collect_descendant_ids(db, parent_id)
    else:
        category_ids = [parent_id]

    stmt = (
        select(Problem)
        .where(Problem.category_id.in_(category_ids))
        .order_by(func.random())
        .limit(count)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

# 문제 유사도 제한
SIMILARITY_LIMIT = 0.9

async def is_similar_problem_exist(db, category_id: int, embedding: list[float]) -> bool:
    stmt = (
        select(Problem)
        .where(Problem.category_id == category_id)
        .where(func.cosine_distance(Problem.embedding, embedding) < (1 - SIMILARITY_LIMIT))
        .order_by(func.cosine_distance(Problem.embedding, embedding))
    )
    result = await db.execute(stmt)
    return result.scalars().first() is not None