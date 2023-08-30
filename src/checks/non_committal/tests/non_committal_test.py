import unittest
from unittest.mock import patch, Mock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import old_answer_non_committal
from old_answer_non_committal import OutputSchema, QAPair

class TestYourLambdaScript(unittest.TestCase):
    @patch('old_answer_non_committal.make_llm_call')
    def test_non_committal_check(self, mock_make_llm_call):
        mock_make_llm_call.return_value = '{"old_answer_non_committal": true}'

        
        old_qa_pair = QAPair(
            id="123",
            question="What is the meaning of life?",
            answer="I don't know",
            version="v0.9",
            sources=[]
        )
        new_qa_pair = QAPair(
            id="456",
            question="What is the meaning of life?",
            answer="The meaning of life is 42.",
            version="v1.0",
            sources=[]
        )
        
        event = old_answer_non_committal.LLMToolkitStdCheckInputSchema(
            old_qa_pair=old_qa_pair,
            new_qa_pair=new_qa_pair
        )

        response = old_answer_non_committal.do("FAKE_OPENAI_API_KEY", event, "prompt.json", "old_answer_non_committal")
        output = OutputSchema.parse_obj(response)

        self.assertEqual(output.statusCode, 200)
        self.assertIsInstance(output.body, old_answer_non_committal.LLMToolkitStdCheckOutputSchema)
        if isinstance(output.body, old_answer_non_committal.LLMToolkitStdCheckOutputSchema):
            self.assertEqual(output.body.result, {"old_answer_non_committal": True})

    @patch('old_answer_non_committal.make_llm_call')
    def test_non_json_output(self, mock_make_llm_call):
        mock_make_llm_call.return_value = 'The answer is less non-committal.'

        
        old_qa_pair = QAPair(
            id="123",
            question="What is the meaning of life?",
            answer="42",
            version="v0.9",
            sources=[]
        )
        new_qa_pair = QAPair(
            id="456",
            question="What is the meaning of life?",
            answer="The meaning of life is 42.",
            version="v1.0",
            sources=[]
        )
        
        event = old_answer_non_committal.LLMToolkitStdCheckInputSchema(
            old_qa_pair=old_qa_pair,
            new_qa_pair=new_qa_pair
        )
        
        response = old_answer_non_committal.do("FAKE_OPENAI_API_KEY", event, "prompt.json", "old_answer_non_committal")
        output = OutputSchema.parse_obj(response)


        self.assertEqual(output.statusCode, 500)
        self.assertIsInstance(output.body, old_answer_non_committal.ErrorSchema)

if __name__ == '__main__':
    unittest.main()