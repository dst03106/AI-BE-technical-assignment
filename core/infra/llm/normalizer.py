from difflib import get_close_matches


class SemanticNormalizer:
    def __init__(
        self,
        standard_values: list[str],
        alias_mapping: dict[str, str] | None = None,
        embedding_model=None,  # Optional: 임베딩 유사도 기반
        similarity_threshold: float = 0.85,
    ):
        self.standard_values = standard_values
        self.alias_mapping = alias_mapping or {}
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold

    def normalize(self, raw_value: str) -> str:
        raw_value = raw_value.strip()

        # 1. Exact match
        if raw_value in self.standard_values:
            return raw_value

        # 2. Alias mapping (e.g. '대기업 경험' → '대규모 회사 경험')
        if raw_value in self.standard_values:
            return self.alias_mapping[raw_value]

        # 3. Fuzzy matching
        fuzzy_matches = get_close_matches(raw_value, self.standard_values, n=1, cutoff=self.similarity_threshold)
        if fuzzy_matches:
            return fuzzy_matches[0]

        # 4 No match found
        return raw_value  # 그대로 반환하거나 None 반환 가능
