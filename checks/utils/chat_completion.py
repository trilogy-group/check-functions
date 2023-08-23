import openai
from aws_lambda_powertools import Logger


logger = Logger()
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