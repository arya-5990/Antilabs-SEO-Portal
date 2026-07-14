"use client";

import { useState } from "react";
import AnalyzerForm from "@/components/AnalyzerForm";
import ResultsDashboard from "@/components/ResultsDashboard";
import HistorySidebar from "@/components/HistorySidebar";
import { analyzeCompetitors } from "@/lib/api";
import Image from "next/image";
import Link from "next/link";

export default function CompetitorAnalyzerPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  const [results, setResults] =
    useState<import("@/components/ResultsDashboard").AnalysisResults | null>(
      null
    );

  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (
    ourUrl: string,
    competitorUrl: string
  ) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await analyzeCompetitors(
        ourUrl,
        competitorUrl
      );

      if (data.error) {
        setError(data.error);
      } else {
        setResults(data);
      }
    } catch (err: unknown) {
      setError(
        (err as Error).message ||
          "Failed to analyze. Please try again later."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-[#fafafa] bg-grid-pattern overflow-hidden font-sans">

      {/* NAVBAR */}

     <nav className="sticky top-0 z-50 bg-white border-b border-slate-200">

        <div className="max-w-7xl mx-auto flex items-center justify-between px-8 py-5">

          <div className="flex items-center">

            <Image
              src="/antilabs-logo.png"
              alt="SEO Optimizer"
              width={55}
              height={55}
            />

            <div className="w-px h-8 bg-gray-300 mx-4" />

            <span className="text-sm font-bold tracking-[0.15em] uppercase text-slate-900">
              SEO OPTIMIZER
            </span>

          </div>

          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">

            <Link
              href="/competitor-analyzer"
              className="text-[#12bafc]"
            >
              Competitor Analysis
            </Link>

            <Link
              href="/gbp-report"
              className="hover:text-slate-900 transition-colors"
            >
              GBP Report
            </Link>

            <a
              href="#"
              className="hover:text-slate-900 transition-colors"
            >
              About
            </a>

          </div>

          <div className="flex items-center gap-4">

            <button
              onClick={() => setIsHistoryOpen(true)}
              className="text-sm font-semibold text-slate-600 hover:text-[#12bafc] flex items-center gap-2 px-4 py-2 rounded-full hover:bg-slate-100 transition"
            >

              <svg
                className="w-4 h-4 text-[#12bafc]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2.5"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>

              History

            </button>

            <button className="hidden sm:block text-sm font-medium text-slate-700 hover:text-slate-900">
              Sign In
            </button>

            <button className="bg-[#12bafc] text-white text-xs font-bold px-5 py-2.5 rounded-md shadow-lg hover:opacity-90 transition">
              Start for Free
            </button>

          </div>

        </div>

      </nav>

      <main className="relative z-10 max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 pt-20 pb-24 flex flex-col items-center justify-center min-h-[calc(100vh-90px)]">

        {!results && (

          <div className="w-full flex flex-col items-center text-center">

            <div className="inline-flex items-center justify-center rounded-full border border-blue-200 bg-blue-50 px-6 py-3 text-sm font-bold uppercase tracking-wide text-[#12bafc] mb-8">

              ✨ Powered by AI

            </div>

            <h1 className="text-5xl md:text-7xl font-black leading-none tracking-tight text-slate-900">
              ANALYZE COMPETITOR SEO
              <br />
              <span className="text-[#12bafc]">
                FASTER.
              </span>
            </h1>

            <p className="mt-8 max-w-4xl text-xl leading-9 text-slate-600">
              Compare your website against top competitors.
              Identify high-value trending keywords,
              structure content quality gaps and receive
              actionable strategies to optimize ranking.
            </p>

            <div className="w-full mt-16">
              <AnalyzerForm
                onSubmit={handleAnalyze}
                isLoading={isLoading}
              />
            </div>

                      </div>
        )}

       {error && (
  <div className="mt-8 max-w-3xl w-full mx-auto bg-red-50 border border-red-200 rounded-xl p-6 text-red-600 text-center shadow-sm animate-slide-up">
    <p className="font-semibold text-lg flex items-center justify-center">
      <svg
        className="w-6 h-6 mr-2"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      {error}
    </p>
  </div>
)}
        {results && (
          <div className="mt-6 w-full animate-slide-up">

            <div className="mb-8 flex items-center justify-between">

              <h2 className="text-3xl font-bold text-slate-900">
                Analysis Results
              </h2>

              <button
                onClick={() => setResults(null)}
                className="btn-ghost px-4 py-2 text-xs"
              >
                ← New Analysis
              </button>

            </div>

            <ResultsDashboard
              results={results}
            />

          </div>
        )}

      </main>

      <HistorySidebar
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        onSelectReport={(reportData) =>
          setResults(reportData)
        }
      />

    </div>
  );
}