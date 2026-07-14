"use client";

export interface AnalysisResults {
  our_score: number;
  competitor_score: number;
  content_quality: {
    our_website: string;
    competitor_website: string;
  };
  trending_keywords: string[];
  comparison_table: Array<{
    feature: string;
    our_status: string;
    competitor_status: string;
  }>;
  strengths_weaknesses: {
    our_strengths: string[];
    our_weaknesses: string[];
    competitor_strengths: string[];
    competitor_weaknesses: string[];
  };
  actionable_suggestions: Array<{
    priority: string;
    suggestion: string;
  }>;
}

interface ResultsDashboardProps {
  results: AnalysisResults;
}

export default function ResultsDashboard({ results }: ResultsDashboardProps) {
  if (!results) return null;

  const handleDownloadPDF = () => {
    try {
      // html2canvas (used by html2pdf) doesn't support modern CSS color functions like oklab/oklch
      // used natively by Tailwind v4. We use the browser's native print functionality which
      // perfectly handles all modern CSS and allows users to "Save as PDF".
      window.print();
    } catch (error) {
      console.error("Failed to generate PDF", error);
      alert("Failed to generate PDF. Please try again.");
    }
  };

  return (
    <div
  id="dashboard-container"
  className="space-y-10 animate-fade-in-up font-sans bg-white border border-slate-200 shadow-xl rounded-3xl p-8 relative"
>
      <div className="absolute top-4 right-4 z-10 hidden sm:block">
        <button
          onClick={handleDownloadPDF}
          className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-sm font-semibold rounded-lg transition-all shadow-sm"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Download PDF
        </button>
      </div>
      {/* Mobile Download button */}
      <div className="sm:hidden flex justify-end mb-4">
        <button
          onClick={handleDownloadPDF}
          className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-sm font-semibold rounded-lg transition-all shadow-sm"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          PDF
        </button>
      </div>
      {/* Scores */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white border border-slate-200 shadow-lg hover:shadow-xl transition-all p-8 rounded-3xl text-center">
          <h3 className="text-xl font-display font-semibold mb-4 text-slate-700">Our SEO Score</h3>
          <p className={`text-7xl font-display font-extrabold  ${results.our_score >= 80 ? 'text-emerald-400' : results.our_score >= 50 ? 'text-amber-400' : 'text-[#00f2fe]'}`}>
            {results.our_score}
          </p>
        </div>
        <div className="bg-white border border-slate-200 shadow-lg hover:shadow-xl transition-all p-8 rounded-3xl text-center">
          <h3 className="text-xl font-display font-semibold mb-4 text-slate-700">Competitor Score</h3>
          <p className={`text-7xl font-display font-extrabold text-glow ${results.competitor_score >= 80 ? 'text-emerald-400' : results.competitor_score >= 50 ? 'text-amber-400' : 'text-[#00f2fe]'}`}>
            {results.competitor_score}
          </p>
        </div>
      </div>

      {/* Content Quality */}
      <div className="bg-white border border-slate-200 shadow-lg rounded-3xl p-10">
        <h3 className="text-3xl font-bold mb-8 text-slate-900">Content Quality Analysis</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <div>
            <h4 className="text-xl font-semibold text-[#00f2fe] mb-4">Our Website</h4>
            <p className="text-slate-600 leading-relaxed text-lg">{results.content_quality.our_website}</p>
          </div>
          <div>
            <h4 className="text-xl font-semibold text-[#4facfe] mb-4">Competitor Website</h4>
            <p className="text-slate-600 leading-relaxed text-lg">{results.content_quality.competitor_website}</p>
          </div>
        </div>
      </div>

     {/* Trending Keywords */}
<div className="bg-white border border-slate-200 shadow-lg rounded-3xl p-10">
  <h3 className="text-3xl font-bold mb-8 text-slate-900">
    Trending Keywords
  </h3>

  <div className="flex flex-wrap gap-3">
    {results.trending_keywords.map((keyword: string, index: number) => (
      <span
        key={index}
        className="px-5 py-2.5 bg-sky-50 border border-sky-200 text-sky-600 rounded-full text-sm font-semibold shadow-sm hover:bg-sky-100 hover:shadow-md transition-all duration-200 cursor-default"
      >
        {keyword}
      </span>
    ))}
  </div>
</div>
{/* Comparison Table */}
<div className="bg-white border border-slate-200 shadow-lg rounded-3xl p-10 overflow-x-auto">
  <h3 className="text-3xl font-bold mb-8 text-slate-900">
    Side-by-Side Comparison
  </h3>

  <table className="w-full min-w-[600px] border-collapse">
    <thead>
      <tr className="bg-slate-50 border-b border-slate-200">
        <th className="py-5 px-6 text-left text-slate-700 font-semibold">
          Feature
        </th>
        <th className="py-5 px-6 text-left text-slate-700 font-semibold">
          Our Status
        </th>
        <th className="py-5 px-6 text-left text-slate-700 font-semibold">
          Competitor Status
        </th>
      </tr>
    </thead>

    <tbody>
      {results.comparison_table.map((row, i: number) => (
        <tr
          key={i}
          className="border-b border-slate-200 hover:bg-slate-50 transition-colors"
        >
          <td className="py-5 px-6 text-slate-700 font-medium">
            {row.feature}
          </td>

          <td className="py-5 px-6 text-sky-600 font-medium">
            {row.our_status}
          </td>

          <td className="py-5 px-6 text-blue-600 font-medium">
            {row.competitor_status}
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>

     {/* Strengths & Weaknesses */}
<div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

  {/* Our Profile */}
  <div className="bg-white border border-slate-200 shadow-lg rounded-3xl p-10">

    <h3 className="text-3xl font-bold mb-8 text-slate-900">
      Our Profile
    </h3>

    <div className="mb-10">

      <h4 className="badge-approved text-sm px-4 py-2 mb-5 uppercase tracking-wide">
        Strengths
      </h4>

      <ul className="space-y-4">

        {results.strengths_weaknesses.our_strengths.map((s, i) => (
          <li
            key={i}
            className="flex items-start text-slate-700"
          >
            <span className="mr-3 mt-1 text-emerald-500 font-bold">
              ✓
            </span>

            <span>{s}</span>
          </li>
        ))}

      </ul>

    </div>

    <div>

      <h4 className="badge-rejected text-sm px-4 py-2 mb-5 uppercase tracking-wide">
        Weaknesses
      </h4>

      <ul className="space-y-4">

        {results.strengths_weaknesses.our_weaknesses.map((w, i) => (
          <li
            key={i}
            className="flex items-start text-slate-700"
          >
            <span className="mr-3 mt-1 text-red-500 font-bold">
              ✕
            </span>

            <span>{w}</span>
          </li>
        ))}

      </ul>

    </div>

  </div>

  {/* Competitor Profile */}

  <div className="bg-white border border-slate-200 shadow-lg rounded-3xl p-10">

    <h3 className="text-3xl font-bold mb-8 text-slate-900">
      Competitor Profile
    </h3>

    <div className="mb-10">

      <h4 className="badge-approved text-sm px-4 py-2 mb-5 uppercase tracking-wide">
        Strengths
      </h4>

      <ul className="space-y-4">

        {results.strengths_weaknesses.competitor_strengths.map((s, i) => (
          <li
            key={i}
            className="flex items-start text-slate-700"
          >
            <span className="mr-3 mt-1 text-emerald-500 font-bold">
              ✓
            </span>

            <span>{s}</span>
          </li>
        ))}

      </ul>

    </div>

    <div>

      <h4 className="badge-rejected text-sm px-4 py-2 mb-5 uppercase tracking-wide">
        Weaknesses
      </h4>

      <ul className="space-y-4">

        {results.strengths_weaknesses.competitor_weaknesses.map((w, i) => (
          <li
            key={i}
            className="flex items-start text-slate-700"
          >
            <span className="mr-3 mt-1 text-red-500 font-bold">
              ✕
            </span>

            <span>{w}</span>
          </li>
        ))}

      </ul>

    </div>

  </div>

</div>
     
     {/* Actionable Suggestions */}
<div className="bg-white border border-slate-200 shadow-lg rounded-3xl p-10">

  <h3 className="text-3xl font-bold mb-8 text-slate-900">
    Actionable Suggestions
  </h3>

  <div className="space-y-5">

    {results.actionable_suggestions.map((action, i: number) => (

      <div
        key={i}
        className="flex flex-col lg:flex-row lg:items-start gap-5 p-6 rounded-2xl border border-slate-200 bg-slate-50 hover:bg-white hover:shadow-md transition-all duration-300"
      >

        <span
          className={`shrink-0 ${
            action.priority.toLowerCase() === "high"
              ? "badge-rejected"
              : action.priority.toLowerCase() === "medium"
              ? "badge-pending"
              : "badge-approved"
          }`}
        >
          {action.priority} Priority
        </span>

        <p className="text-slate-700 text-lg leading-8">
          {action.suggestion}
        </p>

      </div>

    ))}

  </div>

</div>
    </div>
  );
}
