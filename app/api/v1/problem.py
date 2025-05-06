from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.problem import ProblemPrompt, ProblemOut
from app.db.session import get_db
from app.services.problem_service import generate_problem_from_prompt

router = APIRouter(prefix="/api/v1/problems", tags=["Problems"])

@router.post("/generate", response_model=ProblemOut)
async def generate_problem(prompt: ProblemPrompt, db: AsyncSession = Depends(get_db)):
    return await generate_problem_from_prompt(prompt.prompt, db)