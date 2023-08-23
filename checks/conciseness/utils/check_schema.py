from typing import Dict
from pydantic import BaseModel


class LLMToolkitStdCheckInputSchema(BaseModel):
    id: str
    question: str
    new_answer: str
    old_answer: str


class LLMToolkitStdCheckOutputSchema(BaseModel):
    id: str
    result: Dict[str, str | int | float | bool]

class ErrorSchema(BaseModel):
    message: str
    reason: str