from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.problem import ProblemPrompt, ProblemOut, ProblemCreate
from app.db.session import get_db
from app.services.problem_service import generate_problem_from_prompt
from app.services.embedding_service import get_embedding_from_clova
from app.crud.problem import create_problem, get_mock_exam_by_category_path, is_similar_problem_exist


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


@router.post("/problems/", response_model=ProblemOut)
async def create_problem_with_check(
    problem_in: ProblemCreate,
    db: AsyncSession = Depends(get_db),
):
    # 1. 임베딩 벡터 생성
    embedding = get_embedding_from_clova(problem_in.content)

    # 2. 유사도 검사
    is_duplicate = await is_similar_problem_exist(db, problem_in.category_id, embedding)
    if is_duplicate:
        raise HTTPException(status_code=400, detail="해당 카테고리에 유사한 문제가 이미 존재합니다.")

    # 3. 문제 생성 (벡터 포함)
    data = problem_in.dict()
    data["embedding"] = embedding  # 벡터 추가
    return await create_problem(db, ProblemCreate(**data))