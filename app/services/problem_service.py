from app.llm.client import call_llm_generate_problem
from app.schemas.problem import ProblemOut, ProblemCreate
from app.crud.problem import create_problem
from app.crud.category import get_or_create_category
from sqlalchemy.ext.asyncio import AsyncSession

async def generate_problem_from_prompt(prompt: str, db: AsyncSession) -> ProblemOut:
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
