# app/core/pinecone_client.py
import os
import pinecone
from dotenv import load_dotenv

load_dotenv()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)

index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME"))
