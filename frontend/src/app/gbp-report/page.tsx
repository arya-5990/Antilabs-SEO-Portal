"use client";

import { useState } from "react";
import GBPReportForm from "@/components/GBPReportForm";
import GBPReportDashboard from "@/components/GBPReportDashboard";
import { generateGBPReport } from "@/lib/api";
import Image from "next/image";
import Link from "next/link";
import type { GBPReportResults } from "@/components/GBPReportDashboard";

export default function GBPReportPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<GBPReportResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateReport = async (profileUrl: string) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await generateGBPReport(profileUrl);
      if (data.error) {
        setError(data.error);
      } else {
        setResults(data);
      }
    } catch (err: unknown) {
      setError((err as Error).message || "Failed to generate report. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-[#f8fafc] bg-grid-pattern overflow-hidden font-sans">

      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-white border-b border-slate-200">
        <div className="flex items-center justify-between py-6 px-8 max-w-7xl mx-auto">
          <div className="flex items-center">
            <Image
              src="/antilabs-logo.png"
              alt="SEO Optimizer"
              width={55}
              height={55}
            />
            <div className="w-px h-8 bg-slate-300 mx-4"></div>
            <span className="text-sm font-bold tracking-[0.15em] uppercase text-slate-900">
              SEO OPTIMIZER
            </span>
          </div>

          <div className="hidden md:flex gap-8 text-sm font-medium text-slate-600">
            <Link
  href="/competitor-analyzer"
  className="hover:text-slate-900 transition-colors"
>
              Competitor Analysis
            </Link>
           <Link
  href="/gbp-report"
  className="text-sky-600 font-semibold transition-colors"
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
            <button className="text-sm font-medium text-slate-700 hover:text-slate-900 hidden sm:block">
              Sign In
            </button>
            <button className="bg-[#12bafc] text-white text-xs font-bold px-5 py-2.5 rounded-md hover:opacity-90 transition-all shadow-lg">
              Start for Free
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto pt-16 pb-20 px-6 sm:px-8 lg:px-12 relative z-10 flex flex-col items-center justify-center min-h-[calc(100vh-100px)]">

        {!results && (
          <div className="text-center space-y-6 w-full animate-slide-up flex flex-col items-center">

            <div className="inline-flex items-center justify-center px-6 py-3 bg-emerald-50 border border-emerald-200 text-emerald-600 text-sm font-bold uppercase tracking-wide mb-6 rounded-full">
              📊 GBP Optimization
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold uppercase tracking-tight leading-none text-slate-900">
              OPTIMIZE YOUR
              <br className="hidden md:block" />
             <span className="text-sky-500">GOOGLE BUSINESS PROFILE</span>
            </h1>

            <p className="text-[22px] text-slate-600 max-w-4xl mx-auto leading-relaxed mb-12">
              Paste your Google Business Profile link and get a comprehensive report with
              trending keywords, actionable recommendations, and quick wins to boost your local visibility.
            </p>

            <div className="w-full mt-8 animate-fade-in">
              <GBPReportForm
                onSubmit={handleGenerateReport}
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
          <div className="w-full mt-4 animate-slide-up">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-slate-900">
                {results.business_name
                  ? `${results.business_name} — Report`
                  : "Optimization Report"}
              </h2>

              <button
                onClick={() => setResults(null)}
                className="btn-ghost text-xs py-2 px-4"
              >
                ← New Report
              </button>
            </div>

            <GBPReportDashboard results={results} />
          </div>
        )}
      </div>
    </div>
  );
}
