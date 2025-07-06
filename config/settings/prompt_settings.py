from dynaconf import Dynaconf

settings = Dynaconf(settings_files=["core/infra/llm/talent_experience_prompts.toml"])
