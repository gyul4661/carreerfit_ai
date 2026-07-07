# backend/Dockerfile

# 1. Python 3.11 기반 가벼운 이미지 사용
FROM python:3.11-slim

# 2. 컨테이너 안 작업 폴더 설정
WORKDIR /app

# 3. 패키지 목록 먼저 복사
COPY requirements.txt .

# 4. Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 백엔드 코드 복사
COPY . .

# 6. FastAPI 포트 공개
EXPOSE 8000

# 7. 서버 실행
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]