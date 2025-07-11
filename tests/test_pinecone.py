import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv  
load_dotenv()

import asyncio
from app.core.pinecone_client import pinecone_index

# 임의 벡터 및 메타데이터
test_id = "test_001"
test_vector = [0.1] * 1024
test_metadata = {"test": "ping"}

async def test_pinecone():
    # 업서트
    pinecone_index.upsert([{
        "id": test_id,
        "values": test_vector,
        "metadata": test_metadata
    }])
    print("✅ 업서트 성공")

    # 쿼리
    result = pinecone_index.query(
        vector=test_vector,
        top_k=1,
        include_metadata=True
    )
    if result.matches:
        print("✅ 쿼리 성공:", result.matches[0].metadata)
    else:
        print("❌ 쿼리 결과 없음")

if __name__ == "__main__":
    asyncio.run(test_pinecone())