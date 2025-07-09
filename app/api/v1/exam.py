import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.problem import Problem
from app.models.exam import Exam, ExamProblem
from app.crud import exam as exam_crud
from app.schemas.exam import ExamCreateRequest, ExamCreateResponse, ProblemInExam, UserAnswer, ExamSubmitResponse, GradedProblem
from app.utils.exam_hash import hash_problem_ids
from app.services.problem_service import generate_problem_from_prompt

router = APIRouter()

@router.post("/exams/create", response_model=ExamCreateResponse)
async def create_exam(req: ExamCreateRequest, db: AsyncSession = Depends(get_db)):
    # 1. 기준 문제 확인
    result = await db.execute(select(Problem).where(Problem.id == req.base_problem_id))
    base_problem = result.scalar_one_or_none()
    if not base_problem:
        raise HTTPException(status_code=404, detail="기준 문제를 찾을 수 없습니다.")

    category_id = base_problem.category_id

    # 2. 해당 카테고리에서 기준 문제 외 문제 추출
    result = await db.execute(
        select(Problem).where(
            Problem.category_id == category_id,
            Problem.id != req.base_problem_id
        )
    )
    other_problems = result.scalars().all()

    # 3. 랜덤으로 문제 선택
    selected_problems = [base_problem]
    selected_problems += random.sample(
        other_problems,
        min(len(other_problems), req.num_problems - 1)
    )

    # 4. 부족한 개수만큼 LLM을 통해 문제 생성
    if len(selected_problems) < req.num_problems:
        needed = req.num_problems - len(selected_problems)
        base_prompt = f"""
        Please generate a {base_problem.type} type problem related to the following topic:

        Title: {base_problem.title}
        Content: {base_problem.content}

        The new problem should be in the same topic, but not duplicate.
        """

        for _ in range(needed):
            try:
                generated = await generate_problem_from_prompt(
                    prompt=base_prompt,
                    db=db,
                    llm="chatgpt"
                )
                selected_problems.append(generated)
            except Exception as e:
                print(f"[ERROR] 문제 생성 실패: {e}")

    # 5. Exam 생성
    new_exam = Exam()
    db.add(new_exam)
    await db.flush()  # ID 확보

    # 6. ExamProblem 매핑
    for idx, problem in enumerate(selected_problems):
        db.add(ExamProblem(
            exam_id=new_exam.id,
            problem_id=problem.id,
            order=idx
        ))

    await db.commit()

    # 7. 응답 구성 (title + content만)
    response_problems = [
        ProblemInExam(title=p.title, content=p.content)
        for p in selected_problems
    ]

    return ExamCreateResponse(
        exam_id=new_exam.id,
        problems=response_problems
    )


@router.post("/exams/{exam_id}/submit", response_model=ExamSubmitResponse)
def submit_exam(exam_id: int, answers: List[UserAnswer], db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    # 문제 ID → 정답 매핑
    problem_ids = [a.problem_id for a in answers]
    problem_dict = {
        p.id: p for p in db.query(Problem).filter(Problem.id.in_(problem_ids)).all()
    }

    results = []
    correct_count = 0

    for answer in answers:
        problem = problem_dict.get(answer.problem_id)
        if not problem:
            continue  # 혹시 DB에 없는 문제면 건너뜀

        is_correct = problem.answer.strip().lower() == answer.user_answer.strip().lower()
        if is_correct:
            correct_count += 1

        results.append(GradedProblem(
            problem_id=problem.id,
            is_correct=is_correct,
            correct_answer=problem.answer
        ))

    score = round(100 * correct_count / len(answers), 2) if answers else 0.0

    return ExamSubmitResponse(
        exam_id=exam_id,
        score=score,
        results=results
    )