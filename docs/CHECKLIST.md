# CareerFit AI — 일차별 체크리스트

## 1일차

- [x] carreerfit_ai 폴더 구조 생성 완료
- [x] .gitignore에 .env 포함 확인
- [x] .env.example 파일 생성 완료
- [x] .cursor/rules/project-rules.mdc 작성 완료
- [x] docs/AI_TA_RULES.md 또는 하네스 규칙 파일 작성 완료
- [x] docs/PROMPTS.md 또는 하네스 기반 프롬프트 규칙 작성 완료
- [x] docs/CHECKLIST.md 작성 완료
- [x] docs/EVAL_QUESTIONS.md 작성 완료
- [x] docs/PROJECT_PLAN.md 작성 완료
- [x] GitHub Repository 생성 및 초기 커밋 완료
- [x] 피어그룹 멤버 이름·GitHub URL 기록 또는 프로젝트 협업 기록 확인 완료

---

## 2일차

- [x] Python 가상환경(venv) 생성 및 활성화 확인
- [x] requirements.txt 생성 및 패키지 설치 완료
- [x] .env 파일 생성 및 GEMINI_API_KEY 입력 완료
- [x] FastAPI /health 실행 확인 (localhost:8000/health)
- [x] FastAPI /docs 접속 확인 (localhost:8000/docs)
- [x] /jobs API 목업 응답 확인
- [x] /analyze API 기본 구조 작성 완료
- [x] Gemini API 최초 응답 확인
- [x] README.md 골격 작성 완료
- [x] GitHub 커밋 완료 (.env 미포함 확인)

---

## 3일차

- [x] 강사 제공 CSV 데이터 확인 완료
- [x] Pandas로 CSV 읽기 성공
- [x] 결측치·중복 확인 완료
- [x] 스킬 키워드 표준화 완료
- [x] SQLite DB 생성 및 저장 확인
- [x] SQLite 조회 확인
- [x] RAG 문서 구조로 변환 완료
- [x] ChromaDB 컬렉션 생성 및 문서 저장 확인
- [x] metadata 설계 완료
- [x] GitHub 커밋 완료

---

## 4일차

- [x] ChromaDB 질문 기반 검색 확인
- [x] 검색 결과 품질 점검 완료
- [x] /analyze API RAG 응답으로 변경 완료
- [x] React 프로젝트 생성 및 실행 확인 (localhost:5173)
- [x] /analyze API 연결 완료
- [x] 결과 카드 화면 출력 확인
- [x] 출처 카드 화면 출력 확인
- [x] 로컬 통합 테스트 완료
- [x] 하네스 엔지니어링 설정 추가 완료
- [x] UI 디자인 규칙 문서 작성 완료
- [x] CareerFit AI 입력폼·결과카드·출처카드 개선 완료
- [x] GitHub 커밋 완료

---

## 5일차

- [x] Docker Desktop 설치 및 docker 명령어 확인 완료
- [x] docker --version 확인 완료
- [x] docker ps 실행 확인 완료
- [x] Dockerfile 작성 완료
- [x] .dockerignore 작성 완료
- [x] requirements.txt 최종 패키지 확인 완료
- [x] Docker build 성공
- [x] Docker run 후 /health 접속 확인
- [x] Docker run 후 /docs 접속 확인
- [x] Dockerfile 개선 완료
  - [x] pip install 재시도 옵션 추가
  - [x] 컨테이너 헬스체크 추가
  - [x] 비루트 사용자 실행 설정
  - [x] ChromaDB 폴더 권한 문제 해결
- [x] README 최종화 완료 (문제정의·데이터·구현·검증 4단계)
- [x] .env 미포함 보안 확인
- [x] 최종 하네스 파일 업데이트 완료
- [x] docs/EVAL_QUESTIONS.md 자기 평가 답변 작성 완료
- [x] docs/CHECKLIST.md 최종 체크리스트 업데이트 완료
- [x] GitHub 최종 커밋 완료
- [x] 팀 리플렉션 발표 준비 완료

---

## 최종 제출 전 확인

### GitHub Repository

- [x] Repository가 Public으로 설정되어 있는지 확인
- [x] README.md가 GitHub에서 정상 렌더링되는지 확인
- [x] backend, frontend, docs, harness 폴더가 모두 있는지 확인
- [x] backend/Dockerfile이 존재하는지 확인
- [x] backend/.dockerignore가 존재하는지 확인
- [x] frontend React/Vite 프로젝트 파일이 존재하는지 확인

### 보안

- [x] .env 파일이 GitHub에 올라가지 않았는지 확인
- [x] backend/.env 파일이 GitHub에 올라가지 않았는지 확인
- [x] API Key가 코드에 직접 포함되어 있지 않은지 확인
- [x] .env.example 파일에는 실제 Key가 아닌 예시 값만 있는지 확인
- [x] node_modules 폴더가 GitHub에 올라가지 않았는지 확인
- [x] venv 폴더가 GitHub에 올라가지 않았는지 확인
- [x] chroma_db 폴더가 GitHub에 올라가지 않았는지 확인

### 코드 동작

- [x] uvicorn으로 FastAPI 실행 후 /health 응답 확인
- [x] /docs Swagger UI 접속 확인
- [x] /jobs API 응답 확인
- [x] /analyze API가 answer와 sources를 포함해 응답하는지 확인
- [x] React UI에서 입력폼 표시 확인
- [x] React UI에서 결과 카드 출력 확인
- [x] React UI에서 출처 카드 출력 확인
- [x] Docker build 성공 확인
- [x] Docker run 후 /health 응답 확인
- [x] Docker run 후 /docs 접속 확인

### 문서

- [x] README.md에 프로젝트 개요 작성 완료
- [x] README.md에 기술 스택 작성 완료
- [x] README.md에 아키텍처 작성 완료
- [x] README.md에 실행 방법 작성 완료
- [x] README.md에 데이터 파이프라인 작성 완료
- [x] README.md에 주요 기능 작성 완료
- [x] README.md에 보안 관리 내용 작성 완료
- [x] README.md에 향후 개선점 작성 완료
- [x] docs/EVAL_QUESTIONS.md 작성 완료
- [x] docs/CHECKLIST.md 작성 완료
- [x] docs/MODEL_BENCHMARK.md 작성 완료
- [x] harness 파일 업데이트 완료

### 발표 준비

- [x] 프로젝트가 해결하는 문제 설명 가능
- [x] RAG를 사용한 이유 설명 가능
- [x] SQLite와 ChromaDB를 함께 사용한 이유 설명 가능
- [x] /analyze API 흐름 설명 가능
- [x] Docker를 사용한 이유 설명 가능
- [x] .env를 GitHub에 올리면 안 되는 이유 설명 가능
- [x] 향후 개선 방향 설명 가능