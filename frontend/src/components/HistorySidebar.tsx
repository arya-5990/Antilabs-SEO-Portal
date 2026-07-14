"use client";

import { useEffect, useState } from "react";
import { getHistory, getReportById } from "@/lib/api";

interface HistoryItem {
  id: number;
  our_url: string;
  competitor_url: string;
  our_score: number;
  competitor_score: number;
  created_at: string;
}

interface HistorySidebarProps {
  isOpen: boolean;
  onClose: () => void;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onSelectReport: (reportData: any) => void;
}

export default function HistorySidebar({ isOpen, onClose, onSelectReport }: HistorySidebarProps) {
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingReportId, setLoadingReportId] = useState<number | null>(null);

  const fetchHistory = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getHistory();
      setHistoryItems(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load history");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      const timer = setTimeout(() => {
        fetchHistory();
      }, 0);
      return () => clearTimeout(timer);
    }
  }, [isOpen]);

  const handleSelectReport = async (item: HistoryItem) => {
    setLoadingReportId(item.id);
    try {
      const reportData = await getReportById(item.id);
      onSelectReport(reportData);
      onClose();
    } catch {
      alert("Failed to fetch full report details. Please try again.");
    } finally {
      setLoadingReportId(null);
    }
  };

  const cleanUrl = (url: string) => {
    try {
      const parsed = new URL(url);
      return parsed.hostname.replace("www.", "");
    } catch {
      return url.replace("https://", "").replace("http://", "").replace("www.", "");
    }
  };

  const formatDate = (dateStr: string) => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <>
      {/* Backdrop overlay */}
      <div
        className={`fixed inset-0 z-40 bg-slate-900/30 backdrop-blur-md transition-opacity duration-300 ${
          isOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
        }`}
        onClick={onClose}
      />

      {/* Sidebar Drawer */}
      <div
        className={`fixed top-0 right-0 z-50 h-full w-full max-w-md bg-white border-l border-slate-200 shadow-[0_20px_60px_rgba(15,23,42,0.18)] transition-transform duration-300 ease-out transform ${
          isOpen ? "translate-x-0" : "translate-x-full"
        } flex flex-col`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-slate-200 bg-slate-50">
          <h3 className="text-xl font-bold text-slate-900">
            Analysis History
          </h3>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-slate-500 hover:bg-slate-200 hover:text-slate-900 transition"
            aria-label="Close history sidebar"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {isLoading ? (
            // Loading skeleton list
            Array.from({ length: 4 }).map((_, i) => (
              <div
                key={i}
                className="h-24 rounded-xl bg-slate-100 animate-pulse"
              />
            ))
          ) : error ? (
            <div className="text-center py-10 space-y-2">
              <p className="text-rose-400 font-medium">Failed to load history</p>
              <button
                onClick={fetchHistory}
                className="text-xs bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-full border border-transparent transition-all font-semibold"
              >
                Retry
              </button>
            </div>
          ) : historyItems.length === 0 ? (
            <div className="text-center py-20 text-slate-400">
              <svg
                className="w-12 h-12 mx-auto text-slate-500 mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="1.5"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
                />
              </svg>
              <p className="font-semibold text-lg">No history found</p>
              <p className="text-sm text-slate-500 mt-1">
                Run an SEO analysis to save it in history.
              </p>
            </div>
          ) : (
            // History list
            historyItems.map((item) => (
              <div
                key={item.id}
                onClick={() => !loadingReportId && handleSelectReport(item)}
                className={`w-full p-5 rounded-2xl bg-white border border-slate-200 text-left hover:border-sky-300 hover:shadow-lg transition-all duration-300 cursor-pointer flex flex-col gap-3 relative overflow-hidden group ${
                  loadingReportId === item.id ? "opacity-50 pointer-events-none" : ""
                }`}
              >
                {/* URLs comparison */}
                <div className="flex flex-col gap-1 pr-16">
                  <div className="flex items-center gap-1.5 text-sm font-semibold text-slate-900">
                    <span className="w-1.5 h-1.5 rounded-full bg-sky-500" />
                    <span className="truncate max-w-[180px]">{cleanUrl(item.our_url)}</span>
                  </div>
                  <div className="text-[10px] text-slate-500 font-bold uppercase tracking-wider pl-3">vs</div>
                  <div className="flex items-center gap-1.5 text-sm font-semibold text-slate-700">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                    <span className="truncate max-w-[180px]">{cleanUrl(item.competitor_url)}</span>
                  </div>
                </div>

                {/* Score indicators */}
                <div className="absolute right-5 top-5 flex flex-col items-end">
                  <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Scores</span>
                  <div className="flex gap-1.5 items-center mt-1">
                    <span className={`text-base font-bold font-display ${item.our_score >= 80 ? "text-emerald-400" : item.our_score >= 50 ? "text-amber-400" : "text-sky-500"}`}>
                      {item.our_score}
                    </span>
                    <span className="text-slate-600 text-xs font-semibold">/</span>
                    <span className={`text-base font-bold font-display ${item.competitor_score >= 80 ? "text-emerald-400" : item.competitor_score >= 50 ? "text-amber-400" : "text-blue-500"}`}>
                      {item.competitor_score}
                    </span>
                  </div>
                </div>

                {/* Footer details */}
                <div className="flex items-center justify-between border-t border-slate-200 pt-3 text-[11px] text-slate-400">
                  <span>{formatDate(item.created_at)}</span>
                  
                  {loadingReportId === item.id ? (
                    <span className="flex items-center gap-1 text-sky-600 font-semibold">
                      <svg className="animate-spin h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Loading...
                    </span>
                  ) : (
                    <span className="text-sky-600 font-semibold opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center gap-0.5">
                      View report →
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
