from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum


# 문제 타입 enum (FastAPI docs와 연동됨)
class ProblemType(str, Enum):
    select = "select"
    write = "write"

# 요청 스키마
class ProblemPrompt(BaseModel):
    prompt: str
    llm: Literal["ollama", "chatgpt", "hyperclova"] = Field(default="hyperclova", description="사용할 LLM 종류")

# 응답 스키마
class ProblemOut(BaseModel):
    id: int
    title: str
    content: str
    type: ProblemType
    answer: str
    category_id: int

    model_config = {
        "from_attributes": True
    }

class ProblemCreate(BaseModel):
    title: str
    content: str
    type: ProblemType
    answer: str
    category_id: int