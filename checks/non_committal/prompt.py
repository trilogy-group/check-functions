def detect_noncommital_response(question: str, answer: str):
    system_prompt = f"""You are an AI assistant that evaluates answers to a question.
    Evaluate whether the answer is non-commital. Examples of non-commital answers are "I don't know", "I can't answer that question", "The documents don't contain information regarding this topic", etc.
    Your response should be a JSON object with non-commital as the key and the value being either true or false.
    """
    user_prompt = f"Question: {question}\nAnswer: {answer}\n. Make sure your response contains a single word, either true or false"

    return user_prompt, system_prompt