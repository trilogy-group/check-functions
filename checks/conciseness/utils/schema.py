from typing import Dict, Optional
from pydantic import BaseModel


class InputSchema(BaseModel):
    id: str
    question: str
    new_answer: str
    old_answer: str


class OutputSchema(BaseModel):
    id: str
    result: Dict[str, str | int | float | bool]

class ErrorSchema(BaseModel):
    message: str
    reason: str