# backend/data/test_search.py

# ChromaDB 저장 및 검색 테스트
# 실행 위치: backend 폴더
# 실행 명령어: python data/test_search.py

import json
import os

import chromadb


# ===== 1. 파일 경로 설정 =====

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")


# ===== 2. RAG 문서 불러오기 =====

def load_rag_documents(json_path: str) -> list:
    """
    저장된 RAG 문서 JSON을 불러옵니다.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    print(f"✅ RAG 문서 {len(documents)}개 로드됨")
    return documents


# ===== 3. ChromaDB 저장 =====

def save_to_chromadb(documents: list, chroma_path: str):
    """
    RAG 문서를 ChromaDB에 저장합니다.
    """
    print("\n=== ChromaDB 저장 ===")

    client = chromadb.PersistentClient(path=chroma_path)

    collection = client.get_or_create_collection(
        name="careerfit_jobs",
        metadata={
            "description": "CareerFit AI 취업·공모전 데이터"
        }
    )

    # 기존 데이터가 있으면 초기화
    existing_count = collection.count()

    if existing_count > 0:
        print(f"기존 문서 {existing_count}개 발견 → 초기화 후 재저장합니다.")

        existing = collection.get()

        if existing.get("ids"):
            collection.delete(ids=existing["ids"])

    texts = [doc["text"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]
    ids = [doc["doc_id"] for doc in documents]

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ {collection.count()}개 문서 저장 완료")
    print(f"저장 위치: {chroma_path}")

    return collection


# ===== 4. 검색 테스트 =====

def test_search(collection) -> None:
    """
    저장된 문서로 질문 기반 검색을 테스트합니다.
    """
    print("\n=== ChromaDB 검색 테스트 ===")

    test_queries = [
        "반도체 공정 엔지니어 공고",
        "Python이 필요한 공고",
        "전력반도체 관련 직무",
    ]

    for query in test_queries:
        print(f"\n질문: {query}")

        results = collection.query(
            query_texts=[query],
            n_results=2
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i, (doc, meta, distance) in enumerate(
            zip(documents, metadatas, distances),
            start=1
        ):
            print(f"\n결과 {i}:")
            print(f"회사: {meta.get('company', '?')}")
            print(f"직무: {meta.get('title', '?')}")
            print(f"직무 유형: {meta.get('job_type', '?')}")
            print(f"마감월: {meta.get('deadline_month', '?')}")
            print(f"거리: {distance:.4f}")
            print(f"문서: {doc[:120]}...")


# ===== 5. 실행 =====

if __name__ == "__main__":
    documents = load_rag_documents(RAG_JSON)

    collection = save_to_chromadb(
        documents=documents,
        chroma_path=CHROMA_PATH
    )

    test_search(collection)

    print("\n✅ ChromaDB 저장 및 검색 테스트 완료")