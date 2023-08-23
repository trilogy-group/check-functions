import app

def lambda_context():
    class LambdaContext:
        def __init__(self):
            self.function_name = "test-func"
            self.memory_limit_in_mb = 128
            self.invoked_function_arn = "arn:aws:lambda:eu-west-1:809313241234:function:test-func"
            self.aws_request_id = "52fdfc07-2182-154f-163f-5f0f9a621d72"

        def get_remaining_time_in_millis(self) -> int:
            return 1000

    return LambdaContext()


def test_lambda_handler():
    apigw_event = {
      "id": "id",
      "question": "question",
      "old_answer": "old_answer",
      "new_answer": "new_answer"
    }
    resp = app.lambda_handler(apigw_event, context=lambda_context())  # type: ignore
    
    assert resp['statusCode'] == 200
    assert resp['body'] == {'id': 'id', 'question': 'question', 'new_answer': 'new_answer', 'old_answer': 'old_answer', 'checks': {'check': 'empty check'}}
    