/** @type {import('tailwindcss').Config} */
//
// LogoMind design tokens — "specimen sheet" system.
// The product presents generated concept prompts as a designer's studio
// deliverable (a specimen / printout), not a SaaS dashboard. Palette is
// paper-and-ink (warm), with one amber "verified" accent used sparingly.
// Type pairs a characterful display serif (Fraunces), a UI sans (Inter),
// and a technical mono (JetBrains Mono) for prompts/specs.
//
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        // Paper & ink — the substrate of a studio printout.
        paper: "#F2EEE5", // warm manila paper (page bg)
        stock: "#FBF8F1", // lighter sheet surface (cards/plates)
        ink: "#1A1814", // primary text / hairline frames
        graphite: "#5C564C", // secondary text
        rule: "#D8D0BF", // hairline dividers, registration marks
        verified: "#B8732A", // single accent — the "stamp"
        // Semantic aliases used by stage classification.
        stamp: {
          recommended: "#3F6B43", // muted forest
          develop: "#B8732A", // amber
          reject: "#9A3B2E", // oxblood
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
