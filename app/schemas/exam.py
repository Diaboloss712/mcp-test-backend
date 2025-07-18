from pydantic import BaseModel
from typing import List

class ExamCreateRequest(BaseModel):
    base_problem_id: int
    num_problems: int = 5

class ProblemInExam(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True

class ExamCreateResponse(BaseModel):
    exam_id: int
    problems: List[ProblemInExam]

class UserAnswer(BaseModel):
    problem_id: int
    user_answer: str

class GradedProblem(BaseModel):
    problem_id: int
    is_correct: bool
    correct_answer: str

class ExamSubmitResponse(BaseModel):
    exam_id: int
    score: float  # 정답률 %
    results: List[GradedProblem]