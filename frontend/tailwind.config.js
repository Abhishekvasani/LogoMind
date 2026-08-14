/** @type {import('tailwindcss').Config} */
//
// LogoMind design tokens — theme-aware "specimen sheet".
//
// The product presents generated concept prompts as a designer's studio
// deliverable (a specimen / printout), not a SaaS dashboard. Every color below
// is a CSS variable defined in globals.css, so the whole palette flips between
// the warm PAPER light theme and the Claude-inspired "studio at night" dark
// theme via a single `html.dark` class. Type pairs a characterful display serif
// (Fraunces), a UI sans (Inter), and a technical mono (JetBrains Mono).
//
module.exports = {
  darkMode: "class",
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        // Neutrals — paper & ink substrate of a studio printout. RGB-triple
        // variables so Tailwind's /opacity modifiers compose (border-ink/15, …).
        paper: "rgb(var(--paper) / <alpha-value>)", // page background
        stock: "rgb(var(--stock) / <alpha-value>)", // raised card / header surface
        "surface-2": "rgb(var(--surface-2) / <alpha-value>)", // chips / input bg
        ink: "rgb(var(--ink) / <alpha-value>)", // primary text / frames
        graphite: "rgb(var(--graphite) / <alpha-value>)", // secondary text
        rule: "rgb(var(--rule) / <alpha-value>)", // hairline dividers

        // Accents — one brand accent + four semantic roles. All theme-aware.
        accent: "rgb(var(--accent) / <alpha-value>)", // amber (light) / coral (dark)
        verified: "rgb(var(--accent) / <alpha-value>)", // legacy alias used by existing views
        ok: "rgb(var(--ok) / <alpha-value>)", // drivers / liked / opportunity
        warn: "rgb(var(--warn) / <alpha-value>)", // honest caveat / contradiction
        bad: "rgb(var(--bad) / <alpha-value>)", // risk / disliked / cliché
        info: "rgb(var(--info) / <alpha-value>)", // share link / contemporary

        // Stage-classification stamps (used by the specimen Concept Prompt view).
        stamp: {
          recommended: "rgb(var(--stamp-recommended) / <alpha-value>)",
          develop: "rgb(var(--stamp-develop) / <alpha-value>)",
          reject: "rgb(var(--stamp-reject) / <alpha-value>)",
        },
      },
      fontFamily: {
        display: ["var(--font-fraunces)", "Georgia", "serif"],
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        mono: ["var(--font-jetbrains)", "ui-monospace", "monospace"],
      },
      letterSpacing: {
        folio: "0.2em", // folio numbers / technical labels
      },
    },
  },
  plugins: [],
};
