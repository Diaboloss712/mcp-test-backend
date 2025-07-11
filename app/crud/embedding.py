from app.models.embedding import Embedding
from app.core.pinecone_client import pinecone_index
from sqlalchemy.ext.asyncio import AsyncSession

async def save_embedding(db: AsyncSession, problem_id: int, embedding: list[float], metadata: dict = None):
    pinecone_index.upsert([
        {
            "id": str(problem_id),
            "values": embedding,
            "metadata": metadata or {}
        }
    ])

    db.add(Embedding(
        problem_id=problem_id,
        pinecone_id=str(problem_id),
        synced=True
    ))
    await db.commit()
