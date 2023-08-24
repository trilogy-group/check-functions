import unittest
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import conciseness
from prompt import compare_answers_prompt

class TestConciseness(unittest.TestCase):
    
    def test_make_llm_call_returns_json_string(self) -> None:
        question = "What is 1+1?"
        old_answer = "1+1 is 2."
        new_answer = "2."
        openai_api_key: str = os.environ['OPENAI_API_KEY']
        openai_model: str = 'gpt-3.5-turbo'
        user_prompt, system_prompt = compare_answers_prompt(question, old_answer, new_answer)
        result = conciseness.make_llm_call(openai_api_key, openai_model, user_prompt, system_prompt)
        try:
            json_data = json.loads(result)
            self.assertIsInstance(json_data, dict)
        except json.JSONDecodeError:
            self.fail("LLM output is not valid json.")


if __name__ == "__main__":
    unittest.main()