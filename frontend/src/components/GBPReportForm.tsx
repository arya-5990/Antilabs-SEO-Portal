"use client";

import { useState, useEffect } from "react";

interface GBPReportFormProps {
  onSubmit: (profileUrl: string) => void;
  isLoading: boolean;
}

const loadingSteps = [
  "Scraping your Business Profile...",
  "Extracting profile data...",
  "Analyzing with AI...",
  "Identifying trending keywords...",
  "Generating optimization report..."
];

export default function GBPReportForm({ onSubmit, isLoading }: GBPReportFormProps) {
  const [profileUrl, setProfileUrl] = useState("");
  const [loadingStepIndex, setLoadingStepIndex] = useState(0);

  useEffect(() => {
    if (isLoading) {
      const timer = setTimeout(() => {
        setLoadingStepIndex(0);
      }, 0);
      const interval = setInterval(() => {
        setLoadingStepIndex((prev) => Math.min(prev + 1, loadingSteps.length - 1));
      }, 4000);
      return () => {
        clearTimeout(timer);
        clearInterval(interval);
      };
    }
  }, [isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!profileUrl) return;
    onSubmit(profileUrl);
  };

  return (
    <div className="relative z-10 w-full max-w-4xl mx-auto glass-card p-8 sm:p-10 rounded-3xl">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col sm:flex-row items-end gap-4 w-full"
      >
        <div className="w-full sm:flex-1">
          <label className="block text-xs font-semibold uppercase text-slate-400 mb-2">
            Google Business Profile URL
          </label>
          <input
            type="url"
            value={profileUrl}
            onChange={(e) => setProfileUrl(e.target.value)}
            required
            className="input-base"
            placeholder="https://www.google.com/maps/place/your-business..."
          />
          <p className="text-[11px] text-slate-500 mt-2">
            Paste your Google Maps or Google Business Profile link
          </p>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary w-full sm:w-auto flex items-center justify-center gap-2 whitespace-nowrap"
        >
          {isLoading ? (
            <div className="flex flex-col items-center justify-center min-w-[240px]">
              <div className="flex items-center gap-2 mb-2">
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span className="text-xs font-semibold">{loadingSteps[loadingStepIndex]}</span>
              </div>
              <div className="w-full bg-black/20 h-1.5 rounded-full overflow-hidden">
                <div
                  className="bg-white h-full transition-all duration-500 ease-out"
                  style={{ width: `${((loadingStepIndex + 1) / loadingSteps.length) * 100}%` }}
                ></div>
              </div>
            </div>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>Generate Report</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
