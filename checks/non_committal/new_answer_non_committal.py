from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from pydantic import ValidationError
import json
import openai

from utils.schema import InputSchema, OutputSchema, ErrorSchema
from prompt import detect_noncommital_response
from utils.secret_manager import get_secret

tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")


# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    logger.info(f"Going to check if new answer is non committal for {event=}")
    try:
        body = InputSchema(**event)
        user_prompt, system_prompt = detect_noncommital_response(
            question=body.question,
            answer = body.new_answer
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
            response = OutputSchema(
                id = body.id,
                result = check_dictionary
            )
        except Exception as e:
            logger.error(f"Failed while trying to parse response {check_result}: {e}")
            response = OutputSchema(
                id = body.id,
                result = {
                    "non-committal": "Error while computing check"
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

