from app.models.embedding import Embedding
from sqlalchemy.ext.asyncio import AsyncSession

async def save_embedding(db: AsyncSession, problem_id: int, vector: list[float]):
    embedding = Embedding(problem_id=problem_id, vector=vector)
    db.add(embedding)
    await db.commit()
    await db.refresh(embedding)
    return embedding
