from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.session import get_db
from app.models.problem import Problem
from app.crud import exam as exam_crud
from app.schemas.exam import ExamCreateRequest, ExamCreateResponse
from app.utils.exam_hash import hash_problem_ids

router = APIRouter()

@router.post("/exams/create", response_model=ExamCreateResponse)
def create_exam(
    req: ExamCreateRequest,
    db: Session = Depends(get_db)
):
    # 1. 기준 문제 존재 여부 확인
    base_problem = db.query(Problem).filter(Problem.id == req.base_problem_id).first()
    if not base_problem:
        raise HTTPException(status_code=404, detail="기준 문제가 존재하지 않습니다.")

    # 2. 동일 카테고리 문제 랜덤 추출
    category_id = base_problem.category_id
    other_problems = (
        db.query(Problem)
        .filter(Problem.category_id == category_id, Problem.id != req.base_problem_id)
        .order_by(func.random())
        .limit(req.num_problems - 1)
        .all()
    )

    selected_ids = [req.base_problem_id] + [p.id for p in other_problems]

    # 3. 부족한 경우: 자동 생성 필요 (지금은 생략)
    if len(selected_ids) < req.num_problems:
        raise HTTPException(status_code=400, detail="문제 수 부족: LLM 연동 필요")

    # 4. 중복 검사 (해시)
    key_hash = hash_problem_ids(selected_ids)
    existing_exam = exam_crud.get_exam_by_hash(db, key_hash)
    if existing_exam:
        return ExamCreateResponse(
            exam_id=existing_exam.id,
            problem_ids=sorted(selected_ids)
        )

    # 5. 새 모의고사 생성
    new_exam = exam_crud.create_exam(db, selected_ids)
    return ExamCreateResponse(
        exam_id=new_exam.id,
        problem_ids=sorted(selected_ids)
    )
