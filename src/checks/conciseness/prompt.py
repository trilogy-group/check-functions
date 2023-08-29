from typing import List
from jinja2 import Template
import json
from typing import Optional

def compare_answers_prompt(question: str, old_answer: str, new_answer: str, prompt_path: str):

    with open(prompt_path, "r") as f:
        prompts_string = f.read()
        try:
            prompts = json.loads(prompts_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse {prompts_string}")
        system_prompt_template: Optional[Template] = None
        user_prompt_template: Optional[Template] = None
        for prompt in prompts:
            if prompt.get('role') == 'system':
                system_prompt_template = Template(prompt.get('content'))
            elif prompt.get('role') == 'user':
                user_prompt_template = Template(prompt.get('content'))
            else:
                raise ValueError(f"Received prompt with unknown role: {prompt}")
        if system_prompt_template is None or user_prompt_template is None:
            raise ValueError("Could not parse prompts.")
        return \
            system_prompt_template.render(question=question, old_answer=old_answer, new_answer=new_answer),\
            user_prompt_template.render(question=question, old_answer=old_answer, new_answer=new_answer)