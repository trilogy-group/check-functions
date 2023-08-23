from typing import List

def compare_answers_prompt(question: str, old_answer: str, new_answer: str, criterion: str, labels: List[str] = ["more", "less", "unchanged"]):

    system_prompt = f"""You are an AI assistant that compares two different answers to the same question. 
    You are to compare the second answer against the first on the following criterion: {criterion}. 
    For each criteria, classify the content in second answer as compared to the first answer, with one of the following labels: {', '.join(labels)}
    Your answer should be a JSON object with the criterion as the key and the label as the value.
    """

    user_prompt = f"Question: {question}\nFirst answer: {old_answer}\nSecond answer: {new_answer}\n. Make sure your response contains a single word"
    return user_prompt, system_prompt

def detect_noncommital_response(question: str, answer: str):
    system_prompt = f"""You are an AI assistant that evaluates answers to a question.
    Evaluate whether the answer is non-commital. Examples of non-commital answers are "I don't know", "I can't answer that question", "The documents don't contain information regarding this topic", etc.
    Your response should be a JSON object with non-commital as the key and the value being either true or false.
    """
    user_prompt = f"Question: {question}\nAnswer: {answer}\n. Make sure your response contains a single word, either true or false"

    return user_prompt, system_prompt