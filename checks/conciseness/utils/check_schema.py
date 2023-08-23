from typing import Dict, Union
from pydantic import BaseModel


class LLMToolkitStdCheckInputSchema(BaseModel):
    id: str
    question: str
    new_answer: str
    old_answer: str


class LLMToolkitStdCheckOutputSchema(BaseModel):
    id: str
    result: Dict[str, Union[str, int, float, bool]]

class ErrorSchema(BaseModel):
    message: str
    reason: str