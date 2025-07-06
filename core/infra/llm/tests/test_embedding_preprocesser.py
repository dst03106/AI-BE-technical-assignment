import yaml

from core.infra.llm.embedding_preprocesser import YamlEmbeddingPreprocessor


class DummySplitter:
    def split_text(self, text: str) -> list[str]:
        # Splits text into chunks of 5 characters for testing
        return [text[i : i + 5] for i in range(0, len(text), 5)]


class InvalidSplitter:
    # Does not implement split_text
    pass


def test_yaml_embedding_preprocessor_to_text_with_dict():
    data = {"a": 1, "b": 2}
    preprocessor = YamlEmbeddingPreprocessor(DummySplitter())
    yaml_str = preprocessor.to_text(data)
    expected = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    assert yaml_str == expected


def test_base_embedding_preprocessor_preprocess_with_valid_splitter():
    data = {"foo": "bar", "baz": 42}
    preprocessor = YamlEmbeddingPreprocessor(DummySplitter())
    result = preprocessor.preprocess(data)
    expected_text = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    expected_chunks = [expected_text[i : i + 5] for i in range(0, len(expected_text), 5)]
    assert result == expected_chunks


def test_yaml_embedding_preprocessor_to_text_with_nested_data():
    data = {"outer": {"inner": [1, 2, {"deep": "value"}], "another": {"x": 10}}, "list": [1, 2, 3]}
    preprocessor = YamlEmbeddingPreprocessor(DummySplitter())
    yaml_str = preprocessor.to_text(data)
    expected = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    assert yaml_str == expected


def test_base_embedding_preprocessor_preprocess_with_empty_data():
    data = {}
    preprocessor = YamlEmbeddingPreprocessor(DummySplitter())
    result = preprocessor.preprocess(data)
    expected_text = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    expected_chunks = [expected_text[i : i + 5] for i in range(0, len(expected_text), 5)]
    assert result == expected_chunks
