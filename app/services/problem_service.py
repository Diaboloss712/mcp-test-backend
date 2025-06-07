from app.llm.client import call_llm_generate_problem
from app.schemas.problem import ProblemOut, ProblemCreate
from app.crud.problem import create_problem, save_embedding, get_similar_problem
from app.services.embedding_service import get_embedding_from_clova
from app.crud.category import get_or_create_category
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_db

async def generate_problem_from_prompt(prompt: str, db: AsyncSession = get_db()) -> ProblemOut:
    llm_response = await call_llm_generate_problem(prompt)
    category = await get_or_create_category(db, llm_response["category"])

    problem_data = ProblemCreate(
        title=llm_response["title"],
        content=llm_response["content"],
        type=llm_response["type"],
        answer=llm_response["answer"],
        category_id=category.id
    )

    problem = await create_problem(db, problem_data)
    return ProblemOut.from_orm(problem)

SIMILARITY_THRESHOLD = 0.9
MAX_RETRIES = 5

async def generate_problem_from_prompt(prompt: str, db: AsyncSession) -> ProblemOut:
    for _ in range(MAX_RETRIES):
        # 1. LLM 문제 생성
        llm_response = await call_llm_generate_problem(prompt)

        # 2. 카테고리 확인/생성
        category = await get_or_create_category(db, llm_response["category"])

        # 3. 임시 문제 객체 구성
        problem_data = ProblemCreate(
            title=llm_response["title"],
            content=llm_response["content"],
            type=llm_response["type"],
            answer=llm_response["answer"],
            category_id=category.id,
        )

        # 4. 임베딩 추출
        embedding = get_embedding_from_clova(problem_data.content)

        # 5. 유사 문제 검색
        similar = await get_similar_problem(db, category.id, embedding, threshold=SIMILARITY_THRESHOLD)
        if similar:
            print(f"[SKIP] 유사 문제 존재: {similar['id']} - 유사도 {similar['similarity']}")
            continue  # 다시 생성 시도

        # 6. DB 저장 및 벡터 저장
        problem = await create_problem(db, problem_data)
        await save_embedding(db, problem.id, embedding)
        return ProblemOut.from_orm(problem)

    raise Exception("유사 문제를 회피한 생성에 실패했습니다.")