"""
LLM 호출을 담당하는 서비스 파일.

이 파일은 라우터가 직접 Gemini API를 호출하지 않도록
AI 호출 로직을 분리하는 역할을 한다.

사용하는 환경변수:
- GEMINI_API_KEY
- MOCK_MODE
- LLM_MODEL
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


def _is_mock_mode() -> bool:
    """
    MOCK_MODE가 true이면 실제 API를 호출하지 않고
    테스트용 응답을 반환한다.
    """
    return os.getenv("MOCK_MODE", "false").lower() == "true"


def _get_gemini_api_key() -> str:
    """
    .env에서 Gemini API Key를 가져온다.
    API Key를 코드에 직접 쓰면 보안 문제가 생기므로 반드시 .env에서 읽는다.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY가 .env에 없습니다.")

    return api_key


def _get_model_name() -> str:
    """
    사용할 Gemini 모델명을 가져온다.
    .env에 없으면 기본값을 사용한다.
    """
    return os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")


def _get_mock_response(user_text: str) -> str:
    """
    개발/테스트용 가짜 응답.
    API Key 없이 기능 흐름을 확인할 때 사용한다.
    """
    return f"""
[MOCK 응답]

입력한 내용:
{user_text}

분석 결과:
이 사용자는 취업·공모전 준비를 위해 포트폴리오 방향 설정이 필요합니다.
현재 입력 내용을 바탕으로 강점, 부족한 점, 추천 활동을 정리할 수 있습니다.
"""


def generate_analysis(user_text: str) -> str:
    """
    사용자의 입력을 받아 Gemini로 분석 결과를 생성한다.

    Args:
        user_text: 사용자가 입력한 자기소개, 경험, 관심 직무 등의 텍스트

    Returns:
        AI가 생성한 분석 결과 문자열
    """
    if not user_text or not user_text.strip():
        raise ValueError("분석할 텍스트가 비어 있습니다.")

    if _is_mock_mode():
        return _get_mock_response(user_text)

    api_key = _get_gemini_api_key()
    model_name = _get_model_name()

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)

    prompt = f"""
너는 대학생 취업·공모전 포트폴리오 코치야.

아래 사용자의 정보를 바탕으로 다음 항목을 분석해줘.

1. 현재 강점
2. 부족한 점
3. 추천할 활동
4. 포트폴리오 방향

사용자 정보:
{user_text}
"""

    try:
        response = model.generate_content(prompt)
    except Exception as error:
        raise RuntimeError(f"Gemini API 호출 중 오류가 발생했습니다: {error}") from error

    if not response.text:
        return "AI 응답이 비어 있습니다."

    return response.text