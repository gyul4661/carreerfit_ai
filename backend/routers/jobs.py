from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter()

# backend/data/jobs.csv 경로
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "jobs.csv"


def load_jobs():
    """
    jobs.csv 파일을 읽어서 API 응답용 리스트로 변환한다.
    """
    df = pd.read_csv(DATA_PATH)

    jobs = df.to_dict(orient="records")

    for idx, job in enumerate(jobs, start=1):
        job["id"] = idx

        # "반도체소자; 전자회로; 데이터 분석" 형태를 리스트로 변환
        if isinstance(job.get("required_skills"), str):
            job["required_skills"] = [
                skill.strip()
                for skill in job["required_skills"].split(";")
            ]

        if isinstance(job.get("preferred_skills"), str):
            job["preferred_skills"] = [
                skill.strip()
                for skill in job["preferred_skills"].split(";")
            ]

    return jobs


@router.get("/jobs", tags=["Jobs"])
def get_jobs():
    """
    취업 공고 목록을 반환하는 엔드포인트.
    data/jobs.csv 파일의 데이터를 읽어서 반환한다.
    """
    jobs = load_jobs()

    return {
        "count": len(jobs),
        "jobs": jobs
    }


@router.get("/jobs/{job_id}", tags=["Jobs"])
def get_job_by_id(job_id: int):
    """
    특정 공고의 상세 정보를 반환한다.
    """
    jobs = load_jobs()

    for job in jobs:
        if job["id"] == job_id:
            return job

    raise HTTPException(
        status_code=404,
        detail=f"공고 ID {job_id}를 찾을 수 없습니다."
    )