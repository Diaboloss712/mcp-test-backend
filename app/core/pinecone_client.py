# app/core/pinecone_client.py

import os
from pinecone import Pinecone, ServerlessSpec

# Pinecone 인스턴스 생성
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# 인덱스 이름은 .env에 저장해두었거나 하드코딩 가능
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "mcp-index")

# 인덱스 객체 가져오기
pinecone_index = pc.Index(PINECONE_INDEX_NAME)