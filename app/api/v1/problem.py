from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.problem import ProblemPrompt, ProblemOut, ProblemCreate
from app.db.session import get_db
from app.services.problem_service import generate_problem_from_prompt
from app.services.embedding_service import get_embedding_from_clova
from app.crud.embedding import save_embedding
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


@router.post("/check_similarity/", response_model=ProblemOut)
async def create_problem_with_check(
    problem_in: ProblemCreate,
    db: AsyncSession = Depends(get_db),
):
    # 1. 임베딩 벡터 생성
    embedding = get_embedding_from_clova(problem_in.content)

    # 2. 유사도 검사 (이제는 embedding 테이블에서 검색)
    is_duplicate = await is_similar_problem_exist(db, problem_in.category_id, embedding)
    if is_duplicate:
        raise HTTPException(status_code=400, detail="유사한 문제가 존재합니다.")

    # 3. 문제 저장
    problem = await create_problem(db, problem_in)

    # 4. 임베딩 저장 (분리된 테이블에 저장)
    await save_embedding(db, problem.id, embedding)

    return problem