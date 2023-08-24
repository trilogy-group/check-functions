import unittest
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import new_answer_non_committal
from prompt import detect_noncommittal_response

class TestConciseness(unittest.TestCase):
    
    def test_make_llm_call_returns_json_string(self) -> None:
        question = "Tell me something"
        answer = "I don't know."
        openai_api_key: str = os.environ['OPENAI_API_KEY']
        openai_model: str = 'gpt-3.5-turbo'
        user_prompt, system_prompt = detect_noncommittal_response(question, answer)
        result = new_answer_non_committal.make_llm_call(openai_api_key, openai_model, user_prompt, system_prompt)
        try:
            json_data = json.loads(result)
            self.assertIsInstance(json_data, dict)
        except json.JSONDecodeError:
            self.fail("LLM output is not valid json.")


if __name__ == "__main__":
    unittest.main()