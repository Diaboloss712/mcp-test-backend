# app/core/pinecone_client.py
import os
from pinecone import Pinecone, ServerlessSpec

# API 키로 Pinecone 인스턴스 초기화
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# 인덱스 이름
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "mcp-index")

# 존재하지 않으면 인덱스 생성
if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1024, 
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="ap-northeast-2"  
        )
    )

# 인덱스 객체 가져오기
pinecone_index = pc.Index(PINECONE_INDEX_NAME)
