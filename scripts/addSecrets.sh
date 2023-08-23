#!/bin/bash
set -e

SECRET_NAME="sahil-test-4-process-bp-project-secrets"
ENV_FILE=".env"

# Check if the .env file exists
if [ ! -f $ENV_FILE ]; then
    echo "File $ENV_FILE does not exist."
    exit 1
fi

# Convert .env file to JSON
JSON_CONTENT="{"
while IFS='=' read -r key value
do
  if [ ! -z "$key" ]; then
    JSON_CONTENT+="\"$key\":\"$value\","
  fi
done < "$ENV_FILE"
JSON_CONTENT=${JSON_CONTENT%?}
JSON_CONTENT+="}"

# Check if the secret exists
if aws secretsmanager describe-secret --secret-id $SECRET_NAME >/dev/null 2>&1; then
  echo "Secret $SECRET_NAME exists, updating..."
  aws secretsmanager put-secret-value --secret-id $SECRET_NAME --secret-string "$JSON_CONTENT"
else
  echo "Secret $SECRET_NAME does not exist, creating..."
  aws secretsmanager create-secret --name $SECRET_NAME --secret-string "$JSON_CONTENT"
fi