import type { Metadata } from "next";
import { Syne, Plus_Jakarta_Sans, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const syne = Syne({
  variable: "--font-syne",
  subsets: ["latin"],
});

const plusJakartaSans = Plus_Jakarta_Sans({
  variable: "--font-plus-jakarta-sans",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Antilabs SEO Optimizer",
    template: "%s | Antilabs SEO Optimizer",
  },
  description: "Compare your website against competitors and get actionable SEO insights.",
  keywords: ["SEO", "Competitor Analysis", "Marketing", "Optimization", "Antilabs"],
  authors: [{ name: "Antilabs" }],
  creator: "Antilabs",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://antilabs-seo.com",
    title: "Antilabs SEO Optimizer",
    description: "Compare your website against competitors and get actionable SEO insights.",
    siteName: "Antilabs SEO Optimizer",
  },
  twitter: {
    card: "summary_large_image",
    title: "Antilabs SEO Optimizer",
    description: "Compare your website against competitors and get actionable SEO insights.",
    creator: "@antilabs",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`dark ${syne.variable} ${plusJakartaSans.variable} ${jetbrainsMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col font-sans dark:bg-[#090d18] dark:text-[#e2e8f0] bg-slate-50 text-slate-900 transition-colors duration-500 overflow-x-hidden">
        {children}
      </body>
    </html>
  );
}
