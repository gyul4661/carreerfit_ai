import { useState } from "react";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import SourceCard from "./components/SourceCard";

const API_BASE = "http://localhost:8000";
// ⚠️ API Key는 절대 여기에 넣지 않습니다

function getClarifyingQuestions(formData) {
  const major = formData.major.trim();
  const jobType = formData.jobType.trim();
  const skills = formData.skills.map((skill) => skill.trim()).filter(Boolean);

  const questions = [];

  const vagueWords = [
    "개발자",
    "취업",
    "아직 모르겠음",
    "잘 모르겠음",
    "모르겠음",
    "모름",
    "아무거나",
    "추천",
  ];

  if (major.length < 3) {
    questions.push({
      title: "전공 정보 확인",
      question: "현재 전공이나 주전공을 조금 더 구체적으로 알려줄 수 있나요?",
      example: "예: 전자전기컴퓨터공학부, 컴퓨터공학과, 통계학과",
    });
  }

  if (
    skills.length < 2 ||
    skills.some((skill) => vagueWords.includes(skill))
  ) {
    questions.push({
      title: "보유 스킬 확인",
      question:
        "실제로 사용해본 언어, 프로그램, 전공 과목, 실험 경험은 무엇인가요?",
      example:
        "예: C언어, Python, MATLAB, LTspice, ANSYS, 회로해석, 전자회로, 반도체소자",
    });
  }

  if (jobType.length < 3 || vagueWords.includes(jobType)) {
    questions.push({
      title: "관심 직무 확인",
      question: "어떤 개발 분야나 직무에 더 관심이 있나요?",
      example:
        "예: 반도체 공정 엔지니어, 회로설계 엔지니어, 임베디드 개발자, AI/데이터, 전력전자 엔지니어",
    });
  }

  return questions;
}

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [clarifyingQuestions, setClarifyingQuestions] = useState([]);

  async function handleAnalyze(formData) {
    setIsLoading(false);
    setError(null);
    setResult(null);
    setClarifyingQuestions([]);

    const questions = getClarifyingQuestions(formData);

    if (questions.length > 0) {
      setClarifyingQuestions(questions);
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          major: formData.major,
          skills: formData.skills,
          job_type: formData.jobType,
        }),
      });

      if (!response.ok) throw new Error(`서버 오류: ${response.status}`);

      const data = await response.json();
      setResult(data);
    } catch (err) {
      if (err.message.includes("Failed to fetch")) {
        setError("FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.");
      } else {
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-slate-800 mb-2 text-center">
          CareerFit AI
        </h1>
        <p className="text-slate-500 text-sm mb-8 text-center">
          취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치
        </p>

        <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />

        {clarifyingQuestions.length > 0 && (
          <div className="mt-5 bg-amber-50 border border-amber-200 rounded-xl p-6">
            <h2 className="text-lg font-bold text-amber-800 mb-2">
              AI가 묻는 추가 질문
            </h2>

            <p className="text-sm text-amber-700 mb-4">
              입력 정보가 조금 애매해서 바로 분석하지 않았습니다. 아래 질문에 맞게 내용을 더 구체적으로 입력해주세요.
            </p>

            <div className="space-y-4">
              {clarifyingQuestions.map((item, index) => (
                <div
                  key={index}
                  className="bg-white border border-amber-100 rounded-lg p-4"
                >
                  <p className="text-xs font-semibold text-amber-600 mb-1">
                    질문 {index + 1}. {item.title}
                  </p>
                  <p className="text-sm font-medium text-slate-700">
                    {item.question}
                  </p>
                  <p className="text-xs text-slate-500 mt-2">
                    {item.example}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {isLoading && (
          <div className="mt-8 text-center text-slate-500">
            분석 중입니다...
          </div>
        )}

        {result && (
          <div className="mt-8 space-y-4">
            <ResultCard answer={result.answer} />
            {result.sources && result.sources.length > 0 && (
              <SourceCard sources={result.sources} />
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;