from app.models.embedding import Embedding
from app.core.pinecone_client import pinecone_index
from sqlalchemy.ext.asyncio import AsyncSession

async def save_embedding(db: AsyncSession, problem_id: int, embedding: list[float], metadata: dict = None):
    print(f"✅ save_embedding 호출됨")
    print(f"🧠 problem_id: {problem_id}")
    print(f"🧠 embedding 타입: {type(embedding)} / 길이: {len(embedding)}")
    print(f"🧠 metadata: {metadata}")

    assert isinstance(embedding, list), f"embedding이 list가 아님: {type(embedding)}"
    assert all(isinstance(x, float) for x in embedding[:5]), "embedding 안에 float이 아님"
    
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
