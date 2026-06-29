from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["System"])
def health_check():
    """
    서버 상태를 확인하는 엔드포인트.
    """
    return {
        "status": "ok",
        "message": "CareerFit AI 서버가 정상 동작 중입니다."
    }