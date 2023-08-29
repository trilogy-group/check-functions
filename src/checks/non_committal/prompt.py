from typing import Tuple, Optional
import json

from jinja2 import Template

def detect_noncommittal_response(question: str, answer: str, prompt_path: str) -> Tuple[str, str]:

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
            system_prompt_template.render(question=question, answer=answer),\
            user_prompt_template.render(question=question, answer=answer)