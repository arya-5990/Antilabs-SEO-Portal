import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Analyze Competitor SEO",
  description: "Analyze and compare your SEO performance against top competitors to discover actionable strategies.",
  openGraph: {
    title: "Analyze Competitor SEO | Antilabs",
    description: "Analyze and compare your SEO performance against top competitors to discover actionable strategies.",
    url: "https://antilabs-seo.com/competitor-analyzer",
  },
};

export default function CompetitorAnalyzerLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
