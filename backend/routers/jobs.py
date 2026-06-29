from fastapi import APIRouter, HTTPException

router = APIRouter()

# 목업 채용 데이터
# 나중에 CSV 데이터로 교체할 예정
MOCK_JOBS = [
    {
        "id": 1,
        "company": "삼성전자",
        "title": "반도체 공정 R&D 인턴",
        "required_skills": ["반도체 공정", "Python", "데이터 분석"],
        "preferred_skills": ["MOSFET", "공정 실험", "통계 분석"],
        "description": "반도체 공정 데이터를 분석하고 공정 개선 방향을 도출합니다.",
        "deadline": "2026-08-31"
    },
    {
        "id": 2,
        "company": "SK하이닉스",
        "title": "소자/공정 개발 연구원",
        "required_skills": ["반도체 소자", "전자회로", "Python"],
        "preferred_skills": ["TCAD", "데이터 분석", "논문 작성"],
        "description": "메모리 반도체 소자 특성 분석 및 공정 최적화 업무를 수행합니다.",
        "deadline": "2026-09-15"
    },
    {
        "id": 3,
        "company": "현대오토에버",
        "title": "로봇 비전/AI 개발 인턴",
        "required_skills": ["Python", "컴퓨터 비전", "딥러닝"],
        "preferred_skills": ["OpenCV", "YOLO", "센서 데이터 처리"],
        "description": "로봇 비전 데이터를 활용한 객체 인식 및 위치 추정 기능을 개발합니다.",
        "deadline": "2026-08-20"
    }
]


@router.get("/jobs", tags=["Jobs"])
def get_jobs():
    """
    취업 공고 목록을 반환하는 엔드포인트.
    현재는 목업 데이터를 반환한다.
    """
    return {
        "count": len(MOCK_JOBS),
        "jobs": MOCK_JOBS
    }


@router.get("/jobs/{job_id}", tags=["Jobs"])
def get_job_by_id(job_id: int):
    """
    특정 공고의 상세 정보를 반환한다.
    """
    for job in MOCK_JOBS:
        if job["id"] == job_id:
            return job

    raise HTTPException(
        status_code=404,
        detail=f"공고 ID {job_id}를 찾을 수 없습니다."
    )