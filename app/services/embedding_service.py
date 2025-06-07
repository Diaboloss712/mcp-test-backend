import requests
import os
import json
import http.client
import httpx
import numpy as np
from dotenv import load_dotenv
from app.models.embedding import Embedding
from app.models.problem import Problem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

load_dotenv()

CLOVA_API_KEY = os.getenv('CLOVA_API_KEY')
CLOVA_API_HOST = "https://clovastudio.stream.ntruss.com"
CLOVA_API_PATH = "/testapp/v1/api-tools/embedding/v2"

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


async def generate_missing_embeddings(db: AsyncSession):
    # Embedding이 없는 문제들 조회
    stmt = select(Problem).where(
        ~Problem.id.in_(select(Embedding.problem_id))
    )
    result = await db.execute(stmt)
    problems = result.scalars().all()

    # 없을 경우 메시지 반환
    if not problems:
        return {"message": "임베딩이 없는 문제가 없습니다."}

    # 벡터 생성 및 저장
    for problem in problems:
        embedding_vector = get_embedding_from_clova(problem.content)
        embedding = Embedding(problem_id=problem.id, vector=embedding_vector)
        db.add(embedding)

    await db.commit()
    return {"message": f"{len(problems)}개 문제에 대한 임베딩을 생성했습니다."}