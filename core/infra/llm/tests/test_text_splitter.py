import pytest

from core.infra.llm.text_splitter import TokenTextSplitter


class DummyTokenHandler:
    """A simple token handler for deterministic testing."""

    def encode(self, text):
        # Each character is a token (simulate tokenization)
        return [ord(c) for c in text]

    def decode_tokens(self, tokens):
        # Each token is a character
        return "".join(chr(t) for t in tokens)


@pytest.fixture
def dummy_token_handler():
    return DummyTokenHandler()


def test_split_text_splits_into_chunks(dummy_token_handler):
    text = "abcdefghij" * 10  # 100 chars
    chunk_size = 20
    chunk_overlap = 5
    splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, token_handler=dummy_token_handler)
    chunks = splitter.split_text(text)
    # Each chunk should be 20 chars, and overlap by 5 chars
    assert all(len(chunk) == chunk_size or len(chunk) == len(text) % (chunk_size - chunk_overlap) for chunk in chunks)
    # Overlap check
    for i in range(1, len(chunks)):
        assert chunks[i - 1][-chunk_overlap:] == chunks[i][:chunk_overlap]
    # Reconstruct text (with overlaps removed)
    reconstructed = chunks[0]
    for chunk in chunks[1:]:
        reconstructed += chunk[chunk_overlap:]
    assert reconstructed == text


def test_split_text_returns_single_chunk_for_short_text(dummy_token_handler):
    text = "short text"
    chunk_size = 50
    splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=10, token_handler=dummy_token_handler)
    chunks = splitter.split_text(text)
    assert chunks == [text]


def test_split_text_handles_empty_input(dummy_token_handler):
    splitter = TokenTextSplitter(chunk_size=10, chunk_overlap=2, token_handler=dummy_token_handler)
    assert splitter.split_text("") == []
