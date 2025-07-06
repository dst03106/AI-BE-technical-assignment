import pytest
import re
import yaml

from core.infra.llm.output_parser import YAMLDictOutputParser


class DummyBaseOutputParser:
    pass


class TestYAMLDictOutputParser:
    @pytest.fixture(autouse=True)
    def setup_parser(self, monkeypatch):
        # Patch BaseOutputParser to DummyBaseOutputParser for test instantiation
        import core.infra.llm.output_parser as output_parser_module

        output_parser_module.BaseOutputParser = DummyBaseOutputParser
        self.parser = YAMLDictOutputParser()

    def test_function_executes_with_valid_input(self):
        text = "Here is the config:\n```yaml\nfoo: bar\nbaz: 1\n```"
        result = self.parser._parse(text)
        assert isinstance(result, dict)
        assert result == {"foo": "bar", "baz": 1}

    def test_function_returns_expected_output(self):
        text = "Output:\n```yaml\nkey1: value1\nkey2: 42\n```"
        expected = {"key1": "value1", "key2": 42}
        assert self.parser._parse(text) == expected

    def test_function_handles_multiple_valid_inputs(self):
        texts = [
            "```yaml\nx: 10\ny: 20\n```",
            "Some text\n```yaml\na: b\nc: d\n```",
            "Header\n```yaml\nlist:\n  - 1\n  - 2\n```",
        ]
        expected = [{"x": 10, "y": 20}, {"a": "b", "c": "d"}, {"list": [1, 2]}]
        for t, exp in zip(texts, expected):
            assert self.parser._parse(t) == exp

    def test_function_raises_error_on_invalid_input(self):
        # Invalid YAML inside code block
        text = "```yaml\nfoo: [unclosed_list\n```"
        with pytest.raises(yaml.YAMLError):
            self.parser._parse(text)

    def test_function_handles_empty_input(self):
        text = ""
        assert self.parser._parse(text) is None

    def test_function_handles_large_input(self):
        large_dict = {f"key{i}": i for i in range(10000)}
        yaml_str = yaml.dump(large_dict)
        text = f"```yaml\n{yaml_str}```"
        result = self.parser._parse(text)
        assert isinstance(result, dict)
        assert result == large_dict
