from app.models.problem import Problem
from app.schemas.problem import ProblemCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.problem import Problem
from sqlalchemy import select, func
from sqlalchemy.sql import text
import ast


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
SIMILARITY_THRESHOLD = 0.9

async def is_similar_problem_exist(db: AsyncSession, category_id: int, new_embedding: list[float]) -> bool:
    # PostgreSQL의 vector 연산을 위해 문자열로 벡터 표현
    vector_str = f"'[{','.join(map(str, new_embedding))}]'::vector"

    stmt = text(f"""
        SELECT p.id, p.content, e.vector
        FROM problems p
        JOIN embeddings e ON p.id = e.problem_id
        WHERE p.category_id = :category_id
        ORDER BY e.vector <-> {vector_str}
        LIMIT 1
    """).bindparams(category_id=category_id)

    result = await db.execute(stmt)
    row = result.first()

    if row is None:
        return False  # 비교 대상 없음
    
    stored_vector = ast.literal_eval(row.vector)  # 문자열 → 리스트
    stored_vector = list(map(float, stored_vector))  # 리스트 요소를 float으로 변환

    similarity = 1 - vector_distance(stored_vector, new_embedding)
    return similarity >= SIMILARITY_THRESHOLD


def vector_distance(vec1, vec2) -> float:
    from math import sqrt
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sqrt(sum(a * a for a in vec1))
    norm2 = sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 1.0  # 무조건 멀다
    return 1 - dot / (norm1 * norm2)