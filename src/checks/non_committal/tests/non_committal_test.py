import unittest
from unittest.mock import patch, Mock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import old_answer_non_committal

class TestYourLambdaScript(unittest.TestCase):

    @patch('old_answer_non_committal.get_secret')
    @patch('old_answer_non_committal.make_llm_call')
    def test_non_committal_check(self, mock_make_llm_call, mock_get_secret):
        mock_get_secret.return_value = {
            "OPENAI_API_KEY": "mocked_api_key"
        }
        
        mock_make_llm_call.return_value = '{"non_committal": "true"}'
        
        event = {
            "id": "123",
            "question": "What is the meaning of life?",
            "old_answer": "42",
            "new_answer": "The meaning of life is 42."
        }

        context = {}

        response = old_answer_non_committal.lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)
        self.assertTrue('result' in response['body'])
        self.assertEqual(type(response['body']['result']), dict)

if __name__ == '__main__':
    unittest.main()