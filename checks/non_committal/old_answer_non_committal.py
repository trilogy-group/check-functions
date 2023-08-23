from pydantic import ValidationError
import json
import openai

from utils.check_schema import LLMToolkitStdCheckInputSchema, LLMToolkitStdCheckOutputSchema, ErrorSchema
from prompt import detect_noncommittal_response
from utils.secret_manager import get_secret
from utils.logger import get_logger


logger = get_logger(__name__)
def lambda_handler(event: dict, context: dict) -> dict:
    logger.info(f"Going to check if old answer is non committal for {event=}")

    try:
        body = LLMToolkitStdCheckInputSchema(**event)
    except ValidationError  as ve:
        response = ErrorSchema(
            message="Bad Request Body",
            reason=str(ve),
        )
        return {"statusCode": 400, "body": response.model_dump()}
    
    user_prompt, system_prompt = detect_noncommittal_response(
        question=body.question,
        answer = body.old_answer
    )

    try:
        secrets = get_secret()
    except Exception as e:
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
    except Exception as e:
        logger.error(f"Failed to make call to openai: {e}")
        response = ErrorSchema(
            message="Internal Server Error",
            reason=str(e),
        )
        return {"statusCode": 500, "body": response.model_dump()}

    try:
        check_dictionary = json.loads(check_result)
        response = LLMToolkitStdCheckOutputSchema(
            id = body.id,
            result = check_dictionary
        )
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Failed while trying to parse response {check_result}: {e}")
        response = LLMToolkitStdCheckOutputSchema(
            id = body.id,
            result = {
                "non-committal": "Error while computing check"
            }
        )
    except ValidationError as e:
        logger.error(f"Failed while trying to set output to {check_dictionary=}")
        response = LLMToolkitStdCheckOutputSchema(
            id = body.id,
            result = {
                "non-committal": "Error while computing check"
            }
        )
    return {"statusCode": 200, "body": response.model_dump()}
        

