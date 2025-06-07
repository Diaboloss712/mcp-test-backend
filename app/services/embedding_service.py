import requests
import os
import json
import http.client
import numpy as np
from dotenv import load_dotenv
from app.models.embedding import Embedding
from app.models.problem import Problem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

def get_embedding_from_clova(text: str) -> list[float]:
    load_dotenv()

    host = 'clovastudio.stream.ntruss.com'
    api_key = os.getenv('CLOVA_API_KEY')
    request_id = 'cb74c8fb916a4ebbba73c47fe99e8c83'  # 필요시 uuid.uuid4().hex

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {api_key}",
        'X-NCP-CLOVASTUDIO-REQUEST-ID': request_id
    }

    body = { "text": text }

    conn = http.client.HTTPSConnection(host)
    conn.request('POST', '/testapp/v1/api-tools/embedding/v2', json.dumps(body), headers)
    response = conn.getresponse()
    result = json.loads(response.read().decode('utf-8'))
    conn.close()

    if result['status']['code'] != '20000':
        raise ValueError(f"Embedding API Error: {result['status']['message']}")

    return result['result']['embedding']


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