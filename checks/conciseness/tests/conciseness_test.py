import unittest
from unittest.mock import patch, Mock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import conciseness

class TestYourLambdaScript(unittest.TestCase):

    #TODO there is almost no value in this test as the only thing it is tesing is OPENAI and that too is mocked.
    #It is fine to have one sanity test like this, but the real value is in testing the logic of YOUR code, and that
    # means you need to test all the failure conditions because that is the main logic you have written.
    @patch('conciseness.get_secret')
    @patch('conciseness.make_llm_call')
    def test_conciseness_check(self, mock_make_llm_call, mock_get_secret):
        mock_get_secret.return_value = {
            "OPENAI_API_KEY": "mocked_api_key"
        }
        
        mock_make_llm_call.return_value = '{"conciseness": "less"}'
        
        event = {
            "id": "123",
            "question": "What is the meaning of life?",
            "old_answer": "42",
            "new_answer": "The meaning of life is 42."
        }

        context = {}

        response = conciseness.lambda_handler(event, context)

        self.assertEqual(response.statusCode, 200)
        self.assertIsInstance(response.body, conciseness.LLMToolkitStdCheckOutputSchema)
        if isinstance(response.body, conciseness.LLMToolkitStdCheckOutputSchema):
            self.assertEqual(response.body.result, {"conciseness": "less"})

if __name__ == '__main__':
    unittest.main()