from app.models.embedding import Embedding
from app.core.pinecone_client import pinecone_index

async def save_embedding(problem_id: int, embedding: list[float], metadata: dict = None) -> None:
    pinecone_index.upsert([
        {
            "id": str(problem_id),
            "values": embedding,
            "metadata": metadata or {}
        }
    ])


# async def save_embedding(db: AsyncSession, problem_id: int, vector: list[float]):
#     embedding = Embedding(problem_id=problem_id, vector=vector)
#     db.add(embedding)
#     await db.commit()
#     await db.refresh(embedding)
#     return embedding
