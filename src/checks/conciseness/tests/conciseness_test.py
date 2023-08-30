import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import conciseness
from conciseness import OutputSchema, QAPair

class TestYourLambdaScript(unittest.TestCase):

    #TODO there is almost no value in this test as the only thing it is tesing is OPENAI and that too is mocked.
    #It is fine to have one sanity test like this, but the real value is in testing the logic of YOUR code, and that
    # means you need to test all the failure conditions because that is the main logic you have written.
    @patch('conciseness.make_llm_call')
    def test_conciseness_check(self, mock_make_llm_call):
        mock_make_llm_call.return_value = '{"conciseness": "less"}'
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
        
        event = conciseness.LLMToolkitStdCheckInputSchema(
            old_qa_pair=old_qa_pair,
            new_qa_pair=new_qa_pair
        )

        response = conciseness.do("FAKE_OPENAI_API_KEY", event, "prompt.json")
        output = OutputSchema.parse_obj(response)
        self.assertEqual(output.statusCode, 200)
        self.assertIsInstance(output.body, conciseness.LLMToolkitStdCheckOutputSchema)
        if isinstance(output.body, conciseness.LLMToolkitStdCheckOutputSchema):
            self.assertEqual(output.body.result, {"conciseness": "less"})

    @patch('conciseness.make_llm_call')
    def test_non_json_output(self, mock_make_llm_call):
        mock_make_llm_call.return_value = 'The answer is less concise.'
        
        
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
        
        event = conciseness.LLMToolkitStdCheckInputSchema(
            old_qa_pair=old_qa_pair,
            new_qa_pair=new_qa_pair
        )

        response = conciseness.do("FAKE_OPENAI_API_KEY", event, "prompt.json")
        output = OutputSchema.parse_obj(response)
        self.assertEqual(output.statusCode, 500)
        self.assertIsInstance(output.body, conciseness.ErrorSchema)

if __name__ == '__main__':
    unittest.main()