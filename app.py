from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from pydantic import ValidationError

from utils.schema import InputSchema, OutputSchema, ErrorSchema

tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")


# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    try:
        body = InputSchema(**event)
        """
        Your code goes here 
        """
        response = OutputSchema(
            checks={"check": "empty check"},
            old_answer=body.old_answer,
            new_answer=body.new_answer,
            question=body.question,
            id=body.id,
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
