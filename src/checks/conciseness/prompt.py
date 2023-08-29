from typing import List
from jinja2 import Template
import json
from typing import Optional

def compare_answers_prompt(question: str, old_answer: str, new_answer: str, prompt_path: str):

    with open(prompt_path, "r") as f:
        prompts = json.loads(f.read())
        system_prompt_template: Optional[Template] = None
        user_prompt_template: Optional[Template] = None
        for prompt in prompts:
            if prompt.get('role') == 'system':
                system_prompt_template = Template(prompt.get('content'))
            elif prompt.get('role') == 'user':
                user_prompt_template = Template(prompt.get('content'))
        if system_prompt_template is None or user_prompt_template is None:
            raise ValueError("Could not parse prompts.")
        return \
            system_prompt_template.render(question=question, old_answer=old_answer, new_answer=new_answer),\
            user_prompt_template.render(question=question, old_answer=old_answer, new_answer=new_answer)