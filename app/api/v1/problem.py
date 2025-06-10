from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.problem import ProblemPrompt, ProblemOut, ProblemCreate
from app.db.session import get_db
from app.services.problem_service import generate_problem_from_prompt
from app.services.embedding_service import get_embedding_from_clova
from app.crud.embedding import save_embedding
from app.crud.category import get_or_create_category
from app.crud.problem import (
    create_problem,
    get_mock_exam_by_category_path,
    save_embedding,
    get_similar_problem,
)


router = APIRouter(tags=["Problems"])

@router.post("/generate_problem", response_model=ProblemOut)
async def generate_problem(prompt: ProblemPrompt, db: AsyncSession = Depends(get_db)):
    return await generate_problem_from_prompt(prompt.prompt, db, prompt.llm)

@router.get("/mock_exam_by_title", response_model=list[ProblemOut])
async def mock_exam_by_title(
    path: str,  # 예: "Science/Biology/Cell Structure"
    count: int,
    db: AsyncSession = Depends(get_db)
):
    path_list = path.split("/")
    return await get_mock_exam_by_category_path(db, path_list, count)


@router.post("/upload_problem", response_model=ProblemOut)
async def upload_problem_from_json(
    data: dict,
    db: AsyncSession = Depends(get_db),
):
    try:
        category_path = data.pop("category_path", None)
        if not category_path:
            raise HTTPException(status_code=400, detail="category_path가 누락되었습니다.")
        
        # 1. 카테고리 먼저 생성/탐색
        category = await get_or_create_category(db, category_path)
        data["category_id"] = category.id

        # 2. 문제 검증
        problem_data = ProblemCreate(**data)

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"입력 데이터 오류: {str(e)}")

    # 3. 임베딩 추출
    embedding = await get_embedding_from_clova(problem_data.content)

    # 4. 유사도 검사
    threshold = 0.92
    similar = await get_similar_problem(db, category.id, embedding, threshold)
    if similar:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "유사한 문제가 이미 존재합니다.",
                "similar_problem": similar
            }
        )

    # 5. 문제 및 임베딩 저장
    created = await create_problem(db, problem_data)
    await save_embedding(db, created.id, embedding)

    return created
