from core.infra.llm.token_handler import TokenHandler


class TextSplitter:
    def __init__(self, chunk_size=512, chunk_overlap=64, token_handler=TokenHandler()):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.token_handler = token_handler

    def split_text(self, text):
        tokens = self.token_handler.encode(text)
        text_list = []

        start = 0
        while start < len(tokens):
            end = start + self.chunk_size
            chunk = tokens[start:end]
            decoded = self.token_handler.decode_tokens(chunk)
            text_list.append(decoded)
            start += self.chunk_size - self.chunk_overlap
        return text_list
