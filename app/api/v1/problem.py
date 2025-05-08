from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.problem import ProblemPrompt, ProblemOut
from app.db.session import get_db
from app.services.problem_service import generate_problem_from_prompt
from app.crud.problem import get_mock_exam_by_category_path


router = APIRouter(prefix="/api/v1/problems", tags=["Problems"])

@router.post("/generate", response_model=ProblemOut)
async def generate_problem(prompt: ProblemPrompt, db: AsyncSession = Depends(get_db)):
    return await generate_problem_from_prompt(prompt.prompt, db)

@router.get("/mock_exam_by_title", response_model=list[ProblemOut])
async def mock_exam_by_title(
    path: str,  # 예: "Science/Biology/Cell Structure"
    count: int,
    db: AsyncSession = Depends(get_db)
):
    path_list = path.split("/")
    return await get_mock_exam_by_category_path(db, path_list, count)
