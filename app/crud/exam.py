from sqlalchemy.orm import Session
from app.models.exam import Exam, ExamProblem
from app.models.problem import Problem
from app.utils.exam_hash import hash_problem_ids

def get_exam_by_hash(db: Session, key_hash: str) -> Exam | None:
    return db.query(Exam).filter(Exam.key_hash == key_hash).first()

def create_exam(db: Session, problem_ids: list[int], created_by: int | None = None) -> Exam:
    problem_hash = hash_problem_ids(problem_ids)
    new_exam = Exam(key_hash=problem_hash, created_by=created_by)
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    for order, pid in enumerate(sorted(problem_ids)):
        exam_problem = ExamProblem(exam_id=new_exam.id, problem_id=pid, problem_order=order)
        db.add(exam_problem)

    db.commit()
    return new_exam
