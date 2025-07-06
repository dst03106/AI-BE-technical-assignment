import json
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Any


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor, RealDictRow, execute_values
from pgvector.psycopg2 import register_vector

from config.settings.env_settings import settings


@dataclass
class Embedding:
    content: str
    embedding_vector: list[float]
    source_type: str  # 참조하는 테이블 이름 (ex. company)
    source_id: int  # 참조하는 테이블의 PK 값

    # default argument
    metadata: dict | None = field(default_factory=dict)
    model: str = settings.embedding_model

    @property
    def embedding_hash(self) -> str:
        # 멱등성 보장을 위한 해시값
        data = json.dumps({"content": self.content, "model": self.model}, sort_keys=True)
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def to_db_tuple(self):
        return (
            self.content,
            self.embedding_vector,
            self.embedding_hash,
            json.dumps(self.metadata),
            self.model,
            self.source_type,
            self.source_id,
        )


class BaseVectorStore(ABC):
    @abstractmethod
    def add_embeddings(self, id: str, embedding: list[float], metadata: dict = None):
        """임베딩 벡터를 저장"""
        pass

    @abstractmethod
    def search_similar(self, embedding: list[float], top_k: int = 5) -> List[Any]:
        """유사도 검색"""
        pass

    @abstractmethod
    def delete_embedding(self, id: str):
        """벡터 삭제"""
        pass


class PgVectorStore(BaseVectorStore):
    # TODO : 임베딩 모델마다 다른 차원 수 가져오는 메서드 구현
    dim = settings.embedding_model_dim
    table_name = f"documents_{dim}"
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PgVectorStore, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        self.conn = self.get_db_connection()
        self.ensure_table_exists()
        register_vector(self.conn)  # DB에서 가져온 vector 타입을 Python list로 파싱

    @classmethod
    def get_db_connection(cls, uri=settings.postgres_uri):
        try:
            conn = psycopg2.connect(uri)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            return conn
        except psycopg2.Error:
            raise

    def ensure_table_exists(self):
        with self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id SERIAL PRIMARY KEY,
                    source_type VARCHAR NOT NULL,
                    source_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    embedding_vector VECTOR({self.dim}) NOT NULL,
                    model TEXT NOT NULL,
                    embedding_hash CHAR(64) UNIQUE NOT NULL,  -- (model+content) 해시값으로 멱등성 보장
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT now()
                );
                """
            )
            self.conn.commit()

    def _drop_table_if_exists(self):
        with self.conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {self.table_name};")
            self.conn.commit()

    def add_embeddings(self, embeddings: list[Embedding], batch_size=200):
        with self.conn.cursor() as cur:
            for i in range(0, len(embeddings), batch_size):
                print(i)
                batch = embeddings[i : i + batch_size]
                execute_values(
                    cur,
                    f"""
                    INSERT INTO {self.table_name} (
                        content,
                        embedding_vector,
                        embedding_hash,
                        metadata,
                        model,
                        source_type,
                        source_id
                    )
                    VALUES %s
                    ON CONFLICT (embedding_hash) DO NOTHING;
                    """,
                    [e.to_db_tuple() for e in batch],
                )
            self.conn.commit()

    def search_similar(self, embedding, top_k=5) -> list[RealDictRow]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                f"""
                SELECT id, metadata, embedding <#> %s AS distance
                FROM {self.table_name}
                ORDER BY embedding <#> %s
                LIMIT %s;
                """,
                (embedding, embedding, top_k),
            )
        return cur.fetchall()

    def delete_embedding(self, id):
        # SQL로 삭제
        pass
