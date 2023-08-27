from pydantic import ValidationError, BaseModel
import json
import openai
from openai.error import Timeout, APIError, APIConnectionError, InvalidRequestError, AuthenticationError, PermissionError, RateLimitError

from prompt import compare_answers_prompt
from utils.secret_manager import get_secret
from utils.logger import get_logger
from typing import Dict, Union

logger = get_logger(__name__)
openai_errors = ( Timeout, APIError, APIConnectionError, InvalidRequestError, AuthenticationError, PermissionError, RateLimitError )

# TODO: we should move these into a different repo, probably llm-toolkit-api, and import them here
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

class OutputSchema(BaseModel):
    statusCode: int
    body: Union[LLMToolkitStdCheckOutputSchema, ErrorSchema]


def lambda_handler(event: dict, context: dict) -> OutputSchema:
    '''
    This function accesses the conciseness of the new answer compared to the old answer. It conforms to the LLM Toolkit Standard Check API defined here: SAHIL ADD THE URL HERE
    '''

    logger.info(f"Going to run conciseness check on {event=}")
    try:
        input_data = LLMToolkitStdCheckInputSchema(**event)
    except ValidationError  as ve:
        response = ErrorSchema(
            message="Bad Request Body",
            reason=str(ve),
        )
        return OutputSchema(statusCode=400, body=response)
    
    try:
        secrets = get_secret()
    except Exception as e:
        logger.error(f"Failed to retrieve secrets: {e}")
        response = ErrorSchema(
            message="Internal Server Error",
            reason=str(e),
        )
        return OutputSchema(statusCode=500, body=response)
    
    return do(secrets["OPENAI_API_KEY"], input_data)

def do(openai_api_key: str, input_data: LLMToolkitStdCheckInputSchema)->OutputSchema:
    user_prompt, system_prompt = compare_answers_prompt(
            question=input_data.question,
            old_answer = input_data.old_answer,
            new_answer=input_data.new_answer
        )
    try:
        openai_model: str = 'gpt-3.5-turbo'
        check_result = make_llm_call(openai_api_key, openai_model, user_prompt=user_prompt, system_prompt=system_prompt)
    except openai_errors as e:
        logger.error(f"Failed to make call to openai: {e}")
        response = ErrorSchema(
            message="Internal Server Error",
            reason=str(e),
        )
        return OutputSchema(statusCode=500, body=response)

    try:
        check_dictionary = json.loads(check_result)
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Failed while trying to parse response {check_result}: {e}")
        return OutputSchema(statusCode=500, body=ErrorSchema(
            message="Check result not valid json",
            reason=str(e),
        ))
    
    try:
        return OutputSchema(statusCode=200, body=LLMToolkitStdCheckOutputSchema(
            id = input_data.id,
            result = check_dictionary
        ))
    except ValidationError as e:
        logger.error(f"Failed while trying to set output to {check_dictionary=}")
        return OutputSchema(statusCode=500, body=ErrorSchema(
            message="Check result not valid schema",
            reason=str(e),
        ))

def make_llm_call(openai_api_key: str, openai_model: str, user_prompt: str, system_prompt: str)->str:
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model=openai_model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        temperature=0,
    )
    return response['choices'][0]['message']['content'] # type: ignore