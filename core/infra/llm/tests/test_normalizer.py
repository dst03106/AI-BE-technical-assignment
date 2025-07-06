import pytest

from core.infra.llm.normalizer import SemanticNormalizer


class TestSemanticNormalizer:
    def test_function_with_valid_input(self):
        standard_values = ["apple", "banana", "orange"]
        alias_mapping = {"appl": "apple"}
        normalizer = SemanticNormalizer(standard_values, alias_mapping)
        assert normalizer.normalize("apple") == "apple"
        assert normalizer.normalize("appl") == "apple"
        assert normalizer.normalize("banana") == "banana"
        assert normalizer.normalize(" orange ") == "orange"

    def test_function_multiple_invocations(self):
        standard_values = ["cat", "dog"]
        alias_mapping = {"kitten": "cat"}
        normalizer = SemanticNormalizer(standard_values, alias_mapping)
        inputs = ["cat", "kitten", "dog", "cat", "kitten"]
        expected = ["cat", "cat", "dog", "cat", "cat"]
        for inp, exp in zip(inputs, expected):
            print(inp, exp)
            assert normalizer.normalize(inp) == exp

    def test_function_with_empty_input(self):
        standard_values = ["empty", ""]
        alias_mapping = {" ": ""}
        normalizer = SemanticNormalizer(standard_values, alias_mapping)
        assert normalizer.normalize("") == ""
        assert normalizer.normalize(" ") == ""

    def test_function_with_invalid_input_type(self):
        standard_values = ["test"]
        normalizer = SemanticNormalizer(standard_values)
        with pytest.raises(AttributeError):
            normalizer.normalize(None)
        with pytest.raises(AttributeError):
            normalizer.normalize(123)
