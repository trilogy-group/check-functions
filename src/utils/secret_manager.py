
import json
from typing import Dict, Optional
import os
from functools import lru_cache

import boto3
from utils.logger import get_logger

class SecretManagerClient:
    def __init__(
        self, access_key: Optional[str] = None, secret_key: Optional[str] = None, session_token: Optional[str] = None):
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = secret_key
        self.session_token = session_token
        self.secret_manager_client = boto3.client("secretsmanager",
                                                  aws_access_key_id=access_key,
                                                  aws_secret_access_key=secret_key,
                                                  aws_session_token=session_token
                                                  )
        self.logger = get_logger(__name__)

    def get_secret_value(self, secret_name: str) -> Dict[str, str]:
        try:
            response = self.secret_manager_client.get_secret_value(SecretId=secret_name)
            secret_value = response["SecretString"]
            return json.loads(secret_value)
        except Exception as e:
            self.logger.error(f"Error while retrieving secret value: {e}")
            raise e

@lru_cache
def get_secret():
    secret_name = os.environ.get("SECRET_NAME")

    ## To debug locally provide SecretManagerClient with access_id and access_key
    secret_manager_client = SecretManagerClient()
    secret_values =secret_manager_client.get_secret_value(secret_name)
    return secret_values
    
