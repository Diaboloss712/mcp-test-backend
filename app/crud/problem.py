from app.models.problem import Problem
from app.schemas.problem import ProblemCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def create_problem(db: AsyncSession, problem_data: ProblemCreate) -> Problem:
    problem = Problem(**problem_data.dict())
    db.add(problem)
    await db.commit()
    await db.refresh(problem)
    return problem
