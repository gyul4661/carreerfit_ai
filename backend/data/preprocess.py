# backend/data/preprocess.py

# 데이터 전처리 파이프라인
# 실행 위치: backend 폴더
# 실행 명령어: python data/preprocess.py

import json
import os
import sqlite3

import pandas as pd


# ===== 1. 파일 경로 설정 =====

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOBS_CSV = os.path.join(BASE_DIR, "jobs.csv")
DB_PATH = os.path.join(BASE_DIR, "careerfit.db")
RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")


# ===== 2. 스킬 키워드 표준화 사전 =====

SKILL_NORMALIZATION = {
    "python": "Python",
    "sql": "SQL",
    "ai": "AI",
    "ml": "머신러닝",
    "machine learning": "머신러닝",
    "deep learning": "딥러닝",
    "r": "R",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "tableau": "Tableau",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "matlab": "MATLAB",
    "mosfet": "MOSFET",
    "excel": "Excel",
}


# ===== 3. CSV 읽기 =====

def load_data(filepath: str) -> pd.DataFrame:
    """
    CSV 파일을 읽어 DataFrame으로 변환합니다.
    인코딩 오류가 발생하면 cp949로 재시도합니다.
    """
    try:
        df = pd.read_csv(filepath, encoding="utf-8-sig")
        print(f"✅ 파일 읽기 성공 (UTF-8): {filepath}")

    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="cp949")
        print(f"✅ 파일 읽기 성공 (CP949): {filepath}")

    print(f"행 수: {len(df)}, 열 수: {len(df.columns)}")
    print(f"컬럼: {df.columns.tolist()}")

    return df


# ===== 4. 결측치 확인 =====

def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    각 컬럼의 결측치 수와 비율을 확인합니다.
    """
    print("\n=== 결측치 확인 ===")

    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(1)

    result = pd.DataFrame({
        "결측치 수": missing,
        "결측치 비율(%)": missing_pct
    })

    missing_result = result[result["결측치 수"] > 0]

    if missing_result.empty:
        print("✅ 결측치 없음")
    else:
        print(missing_result)
        print(f"⚠️ 총 {missing.sum()}개 결측치 발견")

    return df


# ===== 5. 결측치 처리 =====

def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    결측치를 처리합니다.
    - 핵심 컬럼이 비어있는 행은 제거
    - 나머지 텍스트 컬럼은 빈 문자열로 채움
    """
    print("\n=== 결측치 처리 ===")

    before = len(df)

    df = df.dropna(subset=["title", "required_skills"])

    text_cols = [
        "company",
        "preferred_skills",
        "description",
        "job_type",
        "deadline",
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")

    after = len(df)

    print(f"처리 전: {before}행")
    print(f"처리 후: {after}행")
    print(f"제거된 행: {before - after}행")

    return df


# ===== 6. 중복 제거 =====

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    중복 행을 확인하고 제거합니다.
    company + title 조합이 같으면 중복으로 판단합니다.
    """
    print("\n=== 중복 확인 ===")

    before = len(df)

    duplicated = df.duplicated(subset=["company", "title"], keep=False)

    if duplicated.sum() > 0:
        print(f"⚠️ 중복 발견: {duplicated.sum()}행")
        print(df[duplicated][["company", "title"]])
    else:
        print("✅ 중복 없음")

    df = df.drop_duplicates(subset=["company", "title"], keep="first")
    df = df.reset_index(drop=True)

    after = len(df)

    print(f"제거 후: {after}행")
    print(f"제거된 중복: {before - after}행")

    return df


# ===== 7. 스킬 키워드 표준화 =====

def normalize_skills(skills_str: str) -> str:
    """
    스킬 키워드 문자열을 표준화합니다.

    예:
    "python; sql; mosfet" -> "Python; SQL; MOSFET"
    """
    if not isinstance(skills_str, str) or not skills_str.strip():
        return ""

    skills = [s.strip() for s in skills_str.split(";")]

    normalized = []

    for skill in skills:
        lower = skill.lower()
        normalized.append(SKILL_NORMALIZATION.get(lower, skill))

    return "; ".join(normalized)


def standardize_skills(df: pd.DataFrame) -> pd.DataFrame:
    """
    required_skills, preferred_skills 컬럼에 스킬 표준화를 적용합니다.
    """
    print("\n=== 스킬 키워드 표준화 ===")

    df = df.copy()

    for col in ["required_skills", "preferred_skills"]:
        if col in df.columns:
            df[col] = df[col].apply(normalize_skills)

    print("✅ 스킬 표준화 완료")

    print("\n[표준화 전후 확인용 샘플]")
    print(df[["title", "required_skills", "preferred_skills"]].head(3).to_string())

    return df


# ===== 8. SQLite DB 저장 =====

def save_to_sqlite(df: pd.DataFrame) -> None:
    """
    전처리된 데이터를 SQLite DB에 저장합니다.
    """
    print("\n=== SQLite 저장 ===")

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "jobs",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(f"✅ DB 저장 완료: {DB_PATH}")


# ===== 9. SQLite 조회 테스트 =====

def query_sqlite(db_path: str) -> None:
    """
    SQLite에서 데이터를 조회해 저장 결과를 확인합니다.
    """
    print("\n=== SQLite 조회 테스트 ===")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. 전체 행 수
    cursor.execute("SELECT COUNT(*) FROM jobs")
    print(f"전체 공고 수: {cursor.fetchone()[0]}개")

    # 2. 직무 분류별 개수
    print("\n[직무 분류별 공고 수]")
    cursor.execute("""
        SELECT job_type, COUNT(*) as count
        FROM jobs
        GROUP BY job_type
        ORDER BY count DESC
    """)

    for row in cursor.fetchall():
        print(f"- {row[0]}: {row[1]}개")

    # 3. Python이 포함된 공고 조회
    print("\n[Python 관련 공고]")
    cursor.execute("""
        SELECT company, title, required_skills, preferred_skills
        FROM jobs
        WHERE required_skills LIKE '%Python%'
           OR preferred_skills LIKE '%Python%'
        LIMIT 5
    """)

    rows = cursor.fetchall()

    if not rows:
        print("- Python 관련 공고 없음")
    else:
        for row in rows:
            print(f"- {row[0]} | {row[1]}")
            print(f"  필수 스킬: {row[2]}")
            print(f"  우대 스킬: {row[3]}")

    conn.close()


# ===== 10. RAG 문서 변환 =====

def convert_to_rag_documents(df: pd.DataFrame) -> list[dict]:
    """
    DataFrame의 각 행을 RAG 검색에 적합한 자연어 문서로 변환합니다.
    """
    print("\n=== RAG 문서 변환 ===")

    documents = []

    for idx, row in df.iterrows():
        job_id = idx + 1

        doc_text = (
            f"{row.get('company', '')}에서 "
            f"{row.get('title', '')}을 제공하고 있습니다. "
            f"직무 유형은 {row.get('job_type', '정보 없음')}입니다. "
            f"필수 스킬은 {row.get('required_skills', '정보 없음')}입니다. "
            f"우대 스킬은 {row.get('preferred_skills', '정보 없음')}입니다. "
            f"업무 내용은 {row.get('description', '정보 없음')}입니다. "
            f"마감일은 {row.get('deadline', '정보 없음')}입니다."
        )

        metadata = {
            "id": str(job_id),
            "company": str(row.get("company", "")),
            "title": str(row.get("title", "")),
            "job_type": str(row.get("job_type", "")),
            "deadline": str(row.get("deadline", "")),
            "source": "jobs.csv"
        }

        documents.append({
            "text": doc_text,
            "metadata": metadata,
            "doc_id": f"job_{job_id}"
        })

    print(f"✅ {len(documents)}개 문서 변환 완료")

    if documents:
        print("\n[첫 번째 문서 미리보기]")
        print(f"ID: {documents[0]['doc_id']}")
        print(f"텍스트: {documents[0]['text'][:100]}...")
        print(f"메타데이터: {documents[0]['metadata']}")

    return documents


# ===== 11. RAG JSON 저장 =====

def save_rag_documents(documents: list[dict]) -> None:
    """
    RAG 문서를 JSON 파일로 저장합니다.
    """
    with open(RAG_JSON, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print(f"✅ RAG JSON 저장 완료: {RAG_JSON}")


# ===== 12. 실행 =====

if __name__ == "__main__":
    # 1. 읽기
    df_jobs = load_data(JOBS_CSV)

    print("\n=== 처음 3행 미리보기 ===")
    print(df_jobs.head(3).to_string())

    # 2. 결측치 확인
    df_jobs = check_missing(df_jobs)

    # 3. 결측치 처리
    df_jobs = handle_missing(df_jobs)

    # 4. 중복 제거
    df_jobs = remove_duplicates(df_jobs)

    # 5. 스킬 키워드 표준화
    df_jobs = standardize_skills(df_jobs)

    # 6. SQLite 저장
    save_to_sqlite(df_jobs)

    # 7. SQLite 조회 테스트
    query_sqlite(DB_PATH)

    # 8. RAG 문서 변환
    rag_docs = convert_to_rag_documents(df_jobs)

    # 9. RAG JSON 저장
    save_rag_documents(rag_docs)

    print(f"\n✅ 전처리 완료: 최종 {len(df_jobs)}행, RAG 문서 {len(rag_docs)}개")