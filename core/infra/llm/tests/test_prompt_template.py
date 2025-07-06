import pytest
from jinja2 import UndefinedError

from core.infra.llm.prompt_template import PromptTemplate


class DummyPromptTemplate:
    def __init__(self, system, user):
        self.system = system
        self.user = user


@pytest.fixture
def valid_prompt_template():
    return DummyPromptTemplate(system="You are a helpful assistant.", user="Hello, {{ name }}!")


def test_function_with_valid_input(valid_prompt_template):
    pt = PromptTemplate(valid_prompt_template)
    result = pt.format({"name": "Alice"})
    assert result == [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, Alice!"},
    ]


def test_function_multiple_calls(valid_prompt_template):
    pt = PromptTemplate(valid_prompt_template)
    result1 = pt.format({"name": "Bob"})
    result2 = pt.format({"name": "Carol"})
    assert result1 == [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, Bob!"},
    ]
    assert result2 == [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, Carol!"},
    ]


def test_function_empty_input():
    prompt_template = DummyPromptTemplate(system="System: {{ foo }}", user="User: {{ bar }}")
    pt = PromptTemplate(prompt_template)
    # No variables provided, should raise UndefinedError due to StrictUndefined
    with pytest.raises(UndefinedError):
        pt.format({})


def test_function_large_input():
    large_name = "A" * 1000000  # 1 million characters
    prompt_template = DummyPromptTemplate(system="System ready.", user="Hello, {{ name }}!")
    pt = PromptTemplate(prompt_template)
    result = pt.format({"name": large_name})
    assert result[1]["content"] == f"Hello, {large_name}!"
