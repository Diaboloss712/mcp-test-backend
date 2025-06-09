from app.llm.client import call_llm_generate_problem
from app.schemas.problem import ProblemOut, ProblemCreate
from app.crud.problem import create_problem, save_embedding, get_similar_problem
from app.services.embedding_service import get_embedding_from_clova
from app.crud.category import get_or_create_category
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_db


SIMILARITY_THRESHOLD = 0.7
MAX_RETRIES = 5

async def generate_problem_from_prompt(prompt: str, db: AsyncSession) -> ProblemOut:
    previous_attempts: list[dict] = []

    for _ in range(MAX_RETRIES):
        # 1. 이전 시도 내용을 기반으로 프롬프트 구성
        if previous_attempts:
            avoided_block = "\n".join(
                f"- {p['content']}" for p in previous_attempts
            )
            augmented_prompt = f"""
                                Try to avoid making problem similar to the following list

                                Similar problem lists:
                                {avoided_block}
                                """
        else:
            augmented_prompt = prompt

        # 2. 문제 생성
        llm_response = await call_llm_generate_problem(augmented_prompt)

        # 3. 카테고리 생성/탐색
        category = await get_or_create_category(db, llm_response["category"])

        # 4. 문제 객체 준비
        problem_data = ProblemCreate(
            title=llm_response["title"],
            content=llm_response["content"],
            type=llm_response["type"],
            answer=llm_response["answer"],
            category_id=category.id,
        )

        # 5. 임베딩 + 유사도 검사
        embedding = await get_embedding_from_clova(problem_data.content)
        similar = await get_similar_problem(db, category.id, embedding, threshold=SIMILARITY_THRESHOLD)

        if similar:
            print(f"[SKIP] 유사 문제 존재: {similar['id']} - 유사도 {similar['similarity']}")
            previous_attempts.append({
                "content": problem_data.content,
                "similarity": similar["similarity"]
            })
            continue

        # 6. 저장 성공
        problem = await create_problem(db, problem_data)
        await save_embedding(db, problem.id, embedding)
        return ProblemOut.from_orm(problem)

    raise Exception("유사 문제를 회피한 생성에 실패했습니다.")
