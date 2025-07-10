from app.models.problem import Problem
from app.models.embedding import Embedding
from app.schemas.problem import ProblemCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.problem import Problem
from app.core.pinecone_client import pinecone_index
from sqlalchemy import select, func, insert
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


async def save_embedding(problem_id: int, embedding: list[float], metadata: dict = None) -> None:
    pinecone_index.upsert(
        vectors=[{
            "id": str(problem_id),  # Pinecone은 ID를 문자열로 받습니다.
            "values": embedding,
            "metadata": metadata or {}
        }]
    )


async def get_similar_problem(
    new_embedding: list[float],
    threshold: float = 0.8,
    top_k: int = 3
) -> dict | None:
    result = pinecone_index.query(vector=new_embedding, top_k=top_k, include_metadata=True)
    if not result.matches:
        return None

    top = result.matches[0]
    if top.score >= threshold:
        return {
            "id": top.id,
            "similarity": round(top.score, 4),
            "metadata": top.metadata
        }
    return None
