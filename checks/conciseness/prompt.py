def compare_answers_prompt(question: str, old_answer: str, new_answer: str, criterion: str, labels: List[str] = ["more", "less", "unchanged"]):

    system_prompt = f"""You are an AI assistant that compares two different answers to the same question. 
    You are to compare the second answer against the first on the following criterion: {criterion}. 
    For each criteria, classify the content in second answer as compared to the first answer, with one of the following labels: {', '.join(labels)}
    Your answer should be a JSON object with the criterion as the key and the label as the value.
    """

    user_prompt = f"Question: {question}\nFirst answer: {old_answer}\nSecond answer: {new_answer}\n. Make sure your response contains a single word"
    return user_prompt, system_prompt