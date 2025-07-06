기존 README.md에 있던 과제 내용은 [ASSIGNMENT.md](./ASSIGNMENT.md)로 옮겼습니다.

## FlowChart

### LLM 기반 경험 판단 시스템 플로우
```mermaid
flowchart LR
    B1["1: JSON → YAML 변환<br />(YamlEmbeddingPreprocessor)"]
    C1["2: 토큰 기준 청킹<br />(TokenTextSplitter)"]
    D1["3: 참조 문서 검색 및 추출 <br />(PgVectorStoreRetriever)"]
    E1["4: LLM 호출<br />(OpenAIHandler)"]
    F1["5: 결과 파싱<br />YAML → dict 변환<br />(YAMLDictOutputParser)"]
    G1["6: 값 정규화로 의도한 값 추출<br />(SemanticNormalizer)"]
    
    subgraph S1["인재 데이터 전처리 프로세스"]
        B1 --> C1
    end
    
    C1 --> D1
    D1 --> E1
    E1 --> F1
    F1 --> G1
    
    style S1 fill:#fff2cc,stroke:#d6b656
```

### 사전 임베딩 플로우
```mermaid
flowchart LR
    A["Company 객체"] --> B["회사 데이터 + 뉴스 데이터 병합"]
    B --> C["임베딩 처리"]
```

## 사전 세팅
```
docker-compose up -d
poetry install
poetry run ./manage.py setuptables
poetry run ./manage.py embed # 임베딩 작업 실행 (약 2분)
poetry run ./manage.py runserver
```

## 테스트 방법

### 목표 데이터셋
```
make test-api FILE=example_datas/talent_ex4.json
```

### 성공 테스트셋
```
make test-api FILE=example_datas/talent_ex1.json
make test-api FILE=example_datas/talent_ex2.json
make test-api FILE=example_datas/talent_ex3.json
```