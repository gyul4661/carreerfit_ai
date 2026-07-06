function ResultCard({ answer }) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-emerald-500 p-6">
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-slate-700">
            AI 분석 결과
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            입력한 정보와 관련 공고를 바탕으로 생성된 분석입니다.
          </p>
        </div>
  
        <div className="bg-emerald-50 border border-emerald-100 rounded-lg p-4">
          <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
            {answer}
          </p>
        </div>
      </div>
    );
  }
  
  export default ResultCard;