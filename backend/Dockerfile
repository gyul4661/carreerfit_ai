# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# pip 설치 안정성 개선
COPY requirements.txt .
RUN pip install --no-cache-dir --retries 5 --timeout 60 -r requirements.txt

# 백엔드 코드 복사
COPY . .

# 보안 강화를 위해 비루트 사용자 생성
# ChromaDB가 /app/chroma_db 폴더를 만들 수 있도록 /app 권한 부여
RUN adduser --disabled-password --gecos "" appuser \
    && mkdir -p /app/chroma_db \
    && chown -R appuser:appuser /app

USER appuser

# 컨테이너 내부 포트 문서화
EXPOSE 8000

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import os, urllib.request; port=os.getenv('PORT','8000'); urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=5)"

# Render에서는 PORT 환경변수를 사용할 수 있고, 로컬에서는 기본 8000 사용
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]