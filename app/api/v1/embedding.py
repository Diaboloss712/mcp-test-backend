from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.embedding_service import generate_missing_embeddings

router = APIRouter()

@router.post("/generate-missing/")
async def generate_missing_embeddings_route(db: AsyncSession = Depends(get_db)):
    return await generate_missing_embeddings(db)
