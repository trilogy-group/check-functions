from pydantic import ValidationError
import json
import openai

from utils.check_schema import LLMToolkitStdCheckInputSchema, LLMToolkitStdCheckOutputSchema, ErrorSchema
from prompt import compare_answers_prompt
from utils.secret_manager import get_secret
from utils.logger import get_logger


logger = get_logger(__name__)
openai_errors = (
    openai.error.Timeout,
    openai.error.APIError,
    openai.error.APIConnectionError,
    openai.error.InvalidRequestError,
    openai.error.AuthenticationError,
    openai.error.PermissionError,
    openai.error.RateLimitError,
)
def lambda_handler(event: dict, context: dict) -> dict:
    logger.info(f"Going to run conciseness check on {event=}")
    try:
        input_data = LLMToolkitStdCheckInputSchema(**event)
    except ValidationError  as ve:
        response = ErrorSchema(
            message="Bad Request Body",
            reason=str(ve),
        )
        return {"statusCode": 400, "body": response.model_dump()}
    
    user_prompt, system_prompt = compare_answers_prompt(
            question=input_data.question,
            old_answer = input_data.old_answer,
            new_answer=input_data.new_answer,
            criterion="How concise the answer is"
        )

    try:
        secrets = get_secret()
    except openai_errors as e:
        logger.error(f"Failed to retrieve secrets: {e}")
        response = ErrorSchema(
            message="Internal Server Error",
            reason=str(e),
        )
        return {"statusCode": 500, "body": response.model_dump()}

    try:
        openai_api_key = secrets["OPENAI_API_KEY"]
        openai.api_key = openai_api_key
        openai_model = 'gpt-3.5-turbo'
        response = openai.ChatCompletion.create(
            model=openai_model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            temperature=0,
        )
        
        check_result: str = response['choices'][0]['message']['content']
    except openai as e:
        logger.error(f"Failed to make call to openai: {e}")
        response = ErrorSchema(
            message="Internal Server Error",
            reason=str(e),
        )
        return {"statusCode": 500, "body": response.model_dump()}

    try:
        check_dictionary = json.loads(check_result)
        response = LLMToolkitStdCheckOutputSchema(
            id = input_data.id,
            result = check_dictionary
        )
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Failed while trying to parse response {check_result}: {e}")
        response = LLMToolkitStdCheckOutputSchema(
            id = input_data.id,
            result = {
                "conciseness": "Error while computing check"
            }
        )
    except ValidationError as e:
        logger.error(f"Failed while trying to set output to {check_dictionary=}")
        response = LLMToolkitStdCheckOutputSchema(
            id = input_data.id,
            result = {
                "conciseness": "Error while computing check"
            }
        )
    return {"statusCode": 200, "body": response.model_dump()}