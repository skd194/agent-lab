/** @type {import('tailwindcss').Config} */
// AOEN design tokens (§41). Futuristic, restrained, information-dense (§54).
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "rgb(var(--aoen-bg) / <alpha-value>)",
        surface: "rgb(var(--aoen-surface) / <alpha-value>)",
        "surface-elevated": "rgb(var(--aoen-surface-elevated) / <alpha-value>)",
        border: "rgb(var(--aoen-border) / <alpha-value>)",
        primary: "rgb(var(--aoen-primary) / <alpha-value>)",
        secondary: "rgb(var(--aoen-secondary) / <alpha-value>)",
        success: "rgb(var(--aoen-success) / <alpha-value>)",
        warning: "rgb(var(--aoen-warning) / <alpha-value>)",
        danger: "rgb(var(--aoen-danger) / <alpha-value>)",
        "text-primary": "rgb(var(--aoen-text-primary) / <alpha-value>)",
        "text-secondary": "rgb(var(--aoen-text-secondary) / <alpha-value>)",
        muted: "rgb(var(--aoen-muted) / <alpha-value>)",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "Segoe UI", "sans-serif"],
        mono: ["JetBrains Mono", "SFMono-Regular", "Menlo", "monospace"],
      },
      borderRadius: {
        card: "16px",
        pill: "999px",
      },
      boxShadow: {
        glow: "0 0 24px -4px rgb(var(--aoen-primary) / 0.35)",
        "glow-strong": "0 0 40px -2px rgb(var(--aoen-primary) / 0.55)",
        card: "0 8px 30px -12px rgba(0, 0, 0, 0.6)",
      },
      backdropBlur: {
        glass: "14px",
      },
      keyframes: {
        "pulse-ring": {
          "0%": { transform: "scale(0.9)", opacity: "0.7" },
          "100%": { transform: "scale(1.6)", opacity: "0" },
        },
        breathe: {
          "0%, 100%": { opacity: "0.55", transform: "scale(1)" },
          "50%": { opacity: "1", transform: "scale(1.04)" },
        },
        "spin-slow": {
          to: { transform: "rotate(360deg)" },
        },
        shimmer: {
          "100%": { transform: "translateX(100%)" },
        },
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "pulse-ring": "pulse-ring 2.4s ease-out infinite",
        breathe: "breathe 4s ease-in-out infinite",
        "spin-slow": "spin-slow 14s linear infinite",
        shimmer: "shimmer 1.8s infinite",
        "fade-up": "fade-up 0.4s ease-out both",
      },
      transitionDuration: {
        250: "250ms",
      },
    },
  },
  plugins: [],
};
