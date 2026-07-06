function formatSkills(source) {
    const skills =
      source.required_skills ||
      source.requiredSkills ||
      source.skills ||
      source.matched_skills;
  
    if (!skills) return "정보 없음";
  
    if (Array.isArray(skills)) {
      return skills.length > 0 ? skills.join(", ") : "정보 없음";
    }
  
    return skills;
  }
  
  function SourceCard({ sources }) {
    if (!sources || sources.length === 0) {
      return (
        <div className="bg-slate-50 rounded-xl border border-slate-200 p-4 text-sm text-slate-500">
          참고한 공고 데이터가 없습니다.
        </div>
      );
    }
  
    return (
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-slate-700">
            참고한 공고 출처
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            AI가 답변을 만들 때 참고한 채용공고 목록입니다.
          </p>
        </div>
  
        <div className="space-y-3">
          {sources.map((source, index) => (
            <div
              key={index}
              className="border border-slate-200 rounded-lg p-4 bg-slate-50"
            >
              <p className="text-xs font-medium text-blue-600 mb-1">
                출처 {index + 1}
              </p>
  
              <p className="text-sm font-semibold text-slate-700">
                {source.company || "회사명 정보 없음"}
              </p>
  
              <p className="text-sm text-slate-600 mt-1">
                {source.title || "직무명 정보 없음"}
              </p>
  
              <p className="text-xs text-slate-500 mt-2">
                필수 스킬: {formatSkills(source)}
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  }
  
  export default SourceCard;