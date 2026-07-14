import { Metadata } from "next";

export const metadata: Metadata = {
  title: "GBP Optimization Report",
  description: "Generate a comprehensive optimization report for your Google Business Profile with trending keywords, actionable recommendations, and quick wins.",
  openGraph: {
    title: "GBP Optimization Report | Antilabs",
    description: "Generate a comprehensive optimization report for your Google Business Profile.",
    url: "https://antilabs-seo.com/gbp-report",
  },
};

export default function GBPReportLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
