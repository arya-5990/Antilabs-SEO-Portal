"use client";

export interface GBPReportResults {
  business_name: string;
  overall_score: number;
  category_scores: {
    profile_completeness: number;
    keyword_optimization: number;
    reviews_engagement: number;
    visual_content: number;
    local_seo: number;
  };
  trending_keywords: string[];
  recommended_changes: Array<{
    area: string;
    current_state: string;
    recommendation: string;
    priority: string;
    estimated_impact: string;
  }>;
  quick_wins: string[];
  competitor_keywords_to_target: string[];
  summary: string;
}

interface GBPReportDashboardProps {
  results: GBPReportResults;
}

function ScoreRing({ score, size = 140 }: { score: number; size?: number }) {
  const radius = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;
 const color =
  score >= 80
    ? "#10b981"
    : score >= 60
      ? "#0ea5e9"
      : score >= 40
        ? "#f59e0b"
        : "#ef4444";
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#E2E8F0"
          strokeWidth="8"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          style={{ transition: "stroke-dashoffset 1s ease-out" }}
        />
      </svg>
      <span
        className="absolute text-4xl font-extrabold font-display"
        style={{ color }}
      >
        {score}
      </span>
    </div>
  );
}

function CategoryBar({ label, score }: { label: string; score: number }) {
  const color =
  score >= 80
    ? "#10b981"
    : score >= 60
      ? "#0ea5e9"
      : score >= 40
        ? "#f59e0b"
        : "#ef4444";

 const textColor =
  score >= 80
    ? "text-emerald-600"
    : score >= 60
      ? "text-sky-600"
      : score >= 40
        ? "text-amber-600"
        : "text-rose-600";

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium text-slate-700">{label}</span>
        <span className={`text-sm font-bold ${textColor}`}>{score}/100</span>
      </div>
      <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${color} transition-all duration-1000 ease-out`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

const categoryLabels: Record<string, string> = {
  profile_completeness: "Profile Completeness",
  keyword_optimization: "Keyword Optimization",
  reviews_engagement: "Reviews & Engagement",
  visual_content: "Visual Content",
  local_seo: "Local SEO",
};

export default function GBPReportDashboard({ results }: GBPReportDashboardProps) {
  if (!results) return null;

  const handleDownloadPDF = () => {
    try {
      window.print();
    } catch (error) {
      console.error("Failed to generate PDF", error);
      alert("Failed to generate PDF. Please try again.");
    }
  };

  return (
    <div
  id="gbp-dashboard-container"
  className="max-w-7xl mx-auto space-y-8 animate-fade-in-up font-sans bg-slate-50 p-6 rounded-3xl relative"
>

      {/* Download PDF Button */}
      <div className="absolute top-4 right-4 z-10 hidden sm:block">
        <button
          onClick={handleDownloadPDF}
          className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 text-sm font-semibold rounded-lg transition-all shadow-sm hover:shadow-md"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Download PDF
        </button>
      </div>
      {/* Mobile Download */}
      <div className="sm:hidden flex justify-end mb-4">
        <button
          onClick={handleDownloadPDF}
          className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 text-sm font-semibold rounded-lg transition-all shadow-sm hover:shadow-md"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          PDF
        </button>
      </div>

      {/* Executive Summary */}
      <div className="bg-white border border-slate-200 shadow-sm p-8 rounded-3xl border-l-4 border-sky-500">
        <div className="flex items-start gap-4">
         <div className="shrink-0 w-10 h-10 rounded-xl bg-sky-100 flex items-center justify-center">
  <svg className="w-5 h-5 text-sky-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-display font-bold text-slate-900 mb-2">Executive Summary</h3>
            <p className="text-slate-600 leading-relaxed text-[15px]">{results.summary}</p>
          </div>
        </div>
      </div>

      {/* Overall Score + Category Scores */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Overall Score */}
        <div className="bg-white border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 p-8 rounded-3xl flex flex-col items-center justify-center text-center">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-6">Overall Score</h3>
          <ScoreRing score={results.overall_score} size={160} />
          <p className="text-sm text-slate-600 mt-4 font-medium">
            {results.business_name}
          </p>
        </div>

        {/* Category Scores */}
        <div className="lg:col-span-2 bg-white border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 p-8 rounded-3xl">
          <h3 className="text-xl font-display font-bold text-slate-900 mb-6">Category Breakdown</h3>
          <div className="space-y-5">
            {Object.entries(results.category_scores).map(([key, score]) => (
              <CategoryBar
                key={key}
                label={categoryLabels[key] || key}
                score={score}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Trending Keywords */}
      <div className="bg-white border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 p-8 rounded-3xl">
      <h3 className="text-xl font-display font-bold text-slate-900 mb-6">
          <span className="mr-2">🔥</span>
          Trending Keywords to Target
        </h3>
        <div className="flex flex-wrap gap-3">
          {results.trending_keywords.map((keyword: string, index: number) => (
            <span
              key={index}
              className="px-5 py-2.5 bg-sky-100 border border-sky-200 text-sky-700 rounded-full text-sm font-semibold shadow-sm hover:bg-sky-200 hover:scale-105 transition-all cursor-default"
            >
              {keyword}
            </span>
          ))}
        </div>
        {results.competitor_keywords_to_target && results.competitor_keywords_to_target.length > 0 && (
          <div className="mt-6 pt-6 border-t border-slate-200">
            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-4">
              Competitor Keywords to Target
            </h4>
            <div className="flex flex-wrap gap-3">
              {results.competitor_keywords_to_target.map((keyword: string, index: number) => (
                <span
                  key={index}
                  className="px-4 py-2 bg-blue-100 border border-blue-200 text-blue-700 rounded-full text-sm font-medium hover:bg-blue-200 transition-colors"
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Recommended Changes */}
      <div className="bg-white border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 p-8 rounded-3xl">
        <h3 className="text-xl font-display font-bold text-slate-900 mb-6">
          <span className="mr-2">📋</span>
          Recommended Changes
        </h3>
        <div className="space-y-4">
          {results.recommended_changes.map((change, i: number) => (
            <div
              key={i}
             className="p-6 rounded-2xl bg-slate-50 border border-slate-200 hover:border-sky-300 hover:shadow-md transition-all duration-300"
            >
              <div className="flex flex-col sm:flex-row sm:items-center gap-3 mb-4">
                <h4 className="text-lg font-semibold text-slate-900">{change.area}</h4>
                <div className="flex items-center gap-2">
                  <span
                    className={`shrink-0 ${
                      change.priority.toLowerCase() === "high"
                        ? "badge-rejected"
                        : change.priority.toLowerCase() === "medium"
                          ? "badge-pending"
                          : "badge-approved"
                    }`}
                  >
                    {change.priority} Priority
                  </span>
                  {change.estimated_impact && (
                    <span className="text-xs font-medium text-emerald-400/80 bg-emerald-400/10 px-2.5 py-1 rounded-full border border-emerald-400/15">
                      ↑ {change.estimated_impact}
                    </span>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-rose-50 border border-rose-200">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-rose-600 mb-1.5">Current State</p>
                  <p className="text-sm text-slate-700 leading-relaxed">{change.current_state}</p>
                </div>
                <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-emerald-600 mb-1.5">Recommendation</p>
                  <p className="text-sm text-slate-700 leading-relaxed">{change.recommendation}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Wins */}
      <div className="bg-white border border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 p-8 rounded-3xl">
        <h3 className="text-xl font-display font-bold text-slate-900 mb-6">
          <span className="mr-2">⚡</span>
          Quick Wins
          <span className="text-sm font-normal text-slate-500 ml-2">(do these in 10 minutes)</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {results.quick_wins.map((win: string, index: number) => (
            <div
              key={index}
              className="flex items-start gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200 hover:border-emerald-300 hover:shadow-sm transition-all duration-300"
            >
              <div className="shrink-0 w-6 h-6 rounded-md bg-emerald-100 border border-emerald-200 flex items-center justify-center mt-0.5">
                <span className="text-emerald-600 text-xs font-bold">✓</span>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed">{win}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
