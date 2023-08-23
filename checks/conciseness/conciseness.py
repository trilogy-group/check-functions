from pydantic import ValidationError
import json
import openai

from utils.check_schema import LLMToolkitStdCheckInputSchema, LLMToolkitStdCheckOutputSchema, ErrorSchema
from prompt import compare_answers_prompt
from utils.secret_manager import get_secret
from utils.logger import get_logger


logger = get_logger(__name__)
def lambda_handler(event: dict, context: dict) -> dict:
    logger.info(f"Going to run conciseness check on {event=}")
    try:
        body = LLMToolkitStdCheckInputSchema(**event)
        user_prompt, system_prompt = compare_answers_prompt(
            question=body.question,
            old_answer = body.old_answer,
            new_answer=body.new_answer,
            criterion="How concise the answer is"
        )

        secrets = get_secret()
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

        try:
            check_dictionary = json.loads(check_result)
            response = LLMToolkitStdCheckOutputSchema(
                id = body.id,
                result = check_dictionary
            )
        except Exception as e:
            logger.error(f"Failed while trying to parse response {check_result}: {e}")
            response = LLMToolkitStdCheckOutputSchema(
                id = body.id,
                result = {
                    "conciseness": "Error while computing check"
                }
            )
        return {"statusCode": 200, "body": response.model_dump()}
    except ValidationError  as ve:
        response = ErrorSchema(
            message="Bad Request Body",
            reason=str(ve),
        )
        return {"statusCode": 400, "body": response.model_dump()}
    except Exception as e:
        response = ErrorSchema(
            message="Internal Server Error",
            reason=str(e),
        )
        return {"statusCode": 500, "body": response.model_dump()}

def get_chat_completion(system_prompt: str, user_prompt: str, api_key: str, model: str = 'gpt-3.5-turbo'):
    openai.api_key=api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        temperature=0,
    )
    return response['choices'][0]['message']['content']