from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ExamCreateRequest(BaseModel):
    base_problem_id: int
    num_problems: int = 5

class ExamCreateResponse(BaseModel):
    exam_id: int
    problem_ids: List[int]

class ExamDetail(BaseModel):
    id: int
    name: Optional[str]
    key_hash: str
    created_at: datetime
    problem_ids: List[int]

    class Config:
        orm_mode = True
