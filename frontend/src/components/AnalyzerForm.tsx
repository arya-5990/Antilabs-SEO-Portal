"use client";

import { useState, useEffect } from "react";

interface AnalyzerFormProps {
  onSubmit: (ourUrl: string, competitorUrl: string) => void;
  isLoading: boolean;
}

const loadingSteps = [
  "Scraping Your Website...",
  "Scraping Competitor's Website...",
  "Extracting Content & Headings...",
  "Generating AI Insights...",
  "Finalizing Report..."
];

export default function AnalyzerForm({
  onSubmit,
  isLoading,
}: AnalyzerFormProps) {
  const [ourUrl, setOurUrl] = useState("https://example-edtech.com");
  const [competitorUrl, setCompetitorUrl] = useState("");
  const [loadingStepIndex, setLoadingStepIndex] = useState(0);

  useEffect(() => {
    if (isLoading) {
      const timer = setTimeout(() => {
        setLoadingStepIndex(0);
      }, 0);

      const interval = setInterval(() => {
        setLoadingStepIndex((prev) =>
          Math.min(prev + 1, loadingSteps.length - 1)
        );
      }, 3500);

      return () => {
        clearTimeout(timer);
        clearInterval(interval);
      };
    }
  }, [isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!ourUrl || !competitorUrl) return;

    onSubmit(ourUrl, competitorUrl);
  };

  return (
    <div className="relative z-10 w-full max-w-6xl mx-auto">

      <div className="bg-white border border-slate-200 rounded-3xl shadow-2xl p-8 md:p-10">

        <form
          onSubmit={handleSubmit}
          className="flex flex-col lg:flex-row items-end gap-6 w-full"
        >

          <div className="flex-1 w-full">

            <label className="block text-sm font-semibold text-slate-700 mb-3">
              Your Website URL
            </label>

            <input
              type="url"
              value={ourUrl}
              onChange={(e) => setOurUrl(e.target.value)}
              required
              className="input-base"
              placeholder="https://yourwebsite.com"
            />

          </div>

          <div className="hidden lg:flex items-center justify-center w-14 h-14 rounded-full bg-slate-50 border border-slate-300 text-slate-500 font-bold shadow-sm">
            VS
          </div>

          <div className="flex-1 w-full">

            <label className="block text-sm font-semibold text-slate-700 mb-3">
              Competitor Website URL
            </label>

            <input
              type="url"
              value={competitorUrl}
              onChange={(e) => setCompetitorUrl(e.target.value)}
              required
              className="input-base"
              placeholder="https://competitor.com"
            />

          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="btn-primary w-full lg:w-auto flex items-center justify-center gap-2 whitespace-nowrap min-w-[220px]"
          >
            {isLoading ? (
              <div className="flex flex-col items-center justify-center w-full">

                              <div className="flex items-center gap-2 mb-3">

                <svg
                  className="animate-spin h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />

                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373
                    0 0 5.373 0 12h4zm2
                    5.291A7.962 7.962 0
                    014 12H0c0 3.042
                    1.135 5.824
                    3 7.938l3-2.647z"
                  />

                </svg>

                <span className="text-xs font-semibold text-white">
                  {loadingSteps[loadingStepIndex]}
                </span>

              </div>

              <div className="w-full h-2 rounded-full bg-slate-200 overflow-hidden">

                <div
                  className="h-full bg-sky-500 transition-all duration-500 ease-out"
                  style={{
                    width: `${
                      ((loadingStepIndex + 1) /
                        loadingSteps.length) *
                      100
                    }%`,
                  }}
                />

              </div>

            </div>
          ) : (
            <>
              <span>Analyze SEO</span>

              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </>
          )}
          </button>

        </form>

      </div>

    </div>
  );
}