from jinja2 import Environment, StrictUndefined


class PromptTemplate:
    def __init__(self, prompt_template):
        self.prompt_template = prompt_template

    def format(self, variables: dict):
        environment = Environment(undefined=StrictUndefined)
        system_prompt = environment.from_string(self.prompt_template.system).render()
        user_prompt = environment.from_string(self.prompt_template.user).render(variables)
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
