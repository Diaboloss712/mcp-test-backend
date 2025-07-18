import os
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.embedding import Embedding
from app.models.problem import Problem
from app.crud.embedding import save_embedding

# CLOVA API 설정
CLOVA_API_KEY = os.getenv('CLOVA_API_KEY')
CLOVA_API_HOST = "https://clovastudio.stream.ntruss.com"
CLOVA_API_PATH = "/testapp/v1/api-tools/embedding/v2"

# Clova로부터 임베딩 벡터 받아오기
async def get_embedding_from_clova(text: str) -> list[float]:
    if CLOVA_API_KEY is None:
        raise ValueError("CLOVA_API_KEY is not set in environment variables")

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {CLOVA_API_KEY}",
        "X-NCP-CLOVASTUDIO-REQUEST-ID": 'cb74c8fb916a4ebbba73c47fe99e8c83' 
    }

    data = { "text": text }
    url = CLOVA_API_HOST + CLOVA_API_PATH

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

    result = response.json()

    if result["status"]["code"] != "20000":
        raise ValueError(f"Embedding API Error: {result['status']['message']}")

    return result["result"]["embedding"]

# 문제 중 벡터가 없는 항목들만 찾아서 Pinecone + DB 기록
async def generate_missing_embeddings(db: AsyncSession):
    # 벡터가 없는 문제 조회 (DB에는 문제 ID만 저장해 추적)
    stmt = select(Problem).where(
        ~Problem.id.in_(select(Embedding.problem_id))
    )
    result = await db.execute(stmt)
    problems = result.scalars().all()

    if not problems:
        return {"message": "임베딩이 없는 문제가 없습니다."}

    for problem in problems:
        # 1. 벡터 생성
        embedding_vector = await get_embedding_from_clova(problem.content)

        # 2. Pinecone에 저장 (벡터 ID = 문제 ID)
        await save_embedding(
            problem_id=problem.id,
            embedding=embedding_vector,
            metadata={"category_id": problem.category_id}
        )

        # 3. DB에는 추적용으로 문제 ID만 저장 (벡터 없음)
        db.add(Embedding(problem_id=problem.id))

    await db.commit()
    return {"message": f"{len(problems)}개 문제에 대한 임베딩을 생성했습니다."}
