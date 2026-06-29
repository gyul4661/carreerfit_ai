from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


# 요청 본문 모델
# 사용자가 서버에 보내는 데이터 형식
class AnalyzeRequest(BaseModel):
    major: str
    skills: List[str]
    job_type: str
    experience_years: int = 0
    preferred_company_size: str = "무관"


# 응답 본문 모델
# 서버가 사용자에게 돌려주는 데이터 형식
class AnalyzeResponse(BaseModel):
    answer: str
    sources: List[dict]


@router.post("/analyze", response_model=AnalyzeResponse, tags=["Analyze"])
def analyze_career(request: AnalyzeRequest):
    """
    사용자의 전공, 보유 스킬, 관심 직무를 기반으로
    취업·공모전 맞춤 분석을 제공한다.

    현재는 목업 응답을 반환하고,
    나중에 Gemini API와 연결할 예정이다.
    """

    skill_text = ", ".join(request.skills)

    mock_answer = (
        f"{request.major} 학생으로서 {request.job_type} 직무에 지원하려면, "
        f"현재 보유하신 {skill_text} 역량을 바탕으로 준비하면 좋습니다.\n\n"
        f"경력 연수: {request.experience_years}년\n"
        f"희망 회사 규모: {request.preferred_company_size}\n\n"
        "추천 준비 방향:\n"
        "1. 관심 직무와 연결되는 프로젝트 경험을 정리하세요.\n"
        "2. 사용 가능한 기술 스택을 포트폴리오에 명확히 작성하세요.\n"
        "3. 부족한 기술은 공모전, 인턴, 개인 프로젝트로 보완하세요."
    )

    mock_sources = [
        {
            "title": "목업 데이터 - 취업 공고 분석",
            "content": f"요구 스킬: {skill_text}"
        }
    ]

    return AnalyzeResponse(
        answer=mock_answer,
        sources=mock_sources
    )