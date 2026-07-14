import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0fdfa', 100: '#ccfbf1', 200: '#99f6e4',
          300: '#5eead4', 400: '#4facfe', 500: '#00f2fe',
          600: '#0284c7', 700: '#0369a1', 800: '#075985', 900: '#0c4a6e',
        },
        dark: {
          50: '#f9fafb', 100: '#f3f4f6', 200: '#e5e7eb', 300: '#d1d5db',
          400: '#9ca3af', 500: '#6b7280', 600: '#4b5563', 700: '#374151',
          750: '#2d3748', 800: '#1e2433', 850: '#181e2e', 900: '#0f1623',
          950: '#090d18',
        },
      },
      fontFamily: {
        sans:    ['var(--font-plus-jakarta-sans)', 'sans-serif'],
        display: ['var(--font-syne)', 'sans-serif'],
        mono:    ['var(--font-jetbrains-mono)', 'monospace'],
      },
      boxShadow: {
        'premium':      '0 1px 3px rgba(0,0,0,0.05), 0 8px 24px rgba(0,0,0,0.08)',
        'premium-hover':'0 4px 12px rgba(0,0,0,0.08), 0 20px 40px rgba(0,0,0,0.12)',
        'glow':         '0 0 20px rgba(0,242,254,0.18)',
        'glow-brand':   '0 0 32px rgba(0,242,254,0.35), 0 4px 16px rgba(0,242,254,0.2)',
        'glow-sm':      '0 0 12px rgba(0,242,254,0.12)',
        'glass':        '0 8px 32px rgba(0,0,0,0.08)',
        'glass-dark':   '0 8px 40px rgba(0,0,0,0.5)',
        'card-dark':    '0 1px 0 rgba(255,255,255,0.04) inset, 0 8px 32px rgba(0,0,0,0.4)',
        'inset-dark':   'inset 0 1px 0 rgba(255,255,255,0.05)',
      },
      animation: {
        'aurora':       'aurora 18s ease infinite',
        'pulse-glow':   'pulse-glow 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float':        'float 6s ease-in-out infinite',
        'shimmer':      'shimmer 1.8s linear infinite',
        'slide-up':     'slideUp 0.5s cubic-bezier(0.22,1,0.36,1) forwards',
        'fade-in':      'fadeIn 0.4s ease forwards',
        'count-up':     'countUp 0.6s cubic-bezier(0.22,1,0.36,1) forwards',
        'spin-slow':    'spin 4s linear infinite',
        'border-spin':  'borderSpin 4s linear infinite',
      },
      keyframes: {
        aurora: {
          '0%,100%': { backgroundPosition: '0% 50%' },
          '50%':     { backgroundPosition: '100% 50%' },
        },
        'pulse-glow': {
          '0%,100%': { opacity: '1' },
          '50%':     { opacity: '0.4' },
        },
        float: {
          '0%,100%': { transform: 'translateY(0px)' },
          '50%':     { transform: 'translateY(-8px)' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        slideUp: {
          '0%':   { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        borderSpin: {
          '0%':   { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'noise': "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E\")",
      },
    },
  },
  plugins: [],
};

export default config;
