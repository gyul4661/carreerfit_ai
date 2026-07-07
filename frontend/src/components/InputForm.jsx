import { useState } from "react";

function InputForm({ onSubmit, isLoading }) {
  const [major, setMajor] = useState("");
  const [skillsInput, setSkillsInput] = useState("");
  const [jobType, setJobType] = useState("");

  const isDisabled = isLoading || !major.trim() || !skillsInput.trim() || !jobType.trim();

  function handleSubmit(e) {
    e.preventDefault();

    const skills = skillsInput
      .split(",")
      .map((skill) => skill.trim())
      .filter(Boolean);

    onSubmit({
      major: major.trim(),
      skills,
      jobType: jobType.trim(),
    });
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow-sm border border-slate-200 p-6"
    >
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-slate-700">내 정보 입력</h2>
        <p className="text-sm text-slate-500 mt-1">
          전공, 보유 스킬, 관심 직무를 입력하면 관련 공고를 바탕으로 역량을 분석합니다.
        </p>
      </div>

      <div className="space-y-5">
        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1">
            전공
          </label>
          <input
            type="text"
            value={major}
            onChange={(e) => setMajor(e.target.value)}
            placeholder="예: 전자전기컴퓨터공학부"
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1">
            보유 스킬
          </label>
          <input
            type="text"
            value={skillsInput}
            onChange={(e) => setSkillsInput(e.target.value)}
            placeholder="예: Python,MATLAB, C언어,LTspice, ANSYS, 3D CAD "
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <p className="text-xs text-slate-500 mt-1">
            여러 개의 스킬은 쉼표로 구분해서 입력하세요.
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1">
            관심 직무
          </label>
          <input
            type="text"
            value={jobType}
            onChange={(e) => setJobType(e.target.value)}
            placeholder="예: 반도체 공정 엔지니어"
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <button
          type="submit"
          disabled={isDisabled}
          className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium py-2.5 px-4 rounded-lg transition-colors text-sm"
        >
          {isLoading ? "분석 중..." : "역량 분석 요청"}
        </button>
      </div>
    </form>
  );
}

export default InputForm;