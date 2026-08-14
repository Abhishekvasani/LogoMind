"use client";

import { useEffect, useState } from "react";

/**
 * ThemeToggle — flips the LogoMind substrate between the warm PAPER light theme
 * and the Claude-inspired "studio at night" dark theme.
 *
 * The active theme is driven by the `dark` class on <html> (see globals.css).
 * A no-flash inline script in layout.tsx sets it before first paint from
 * localStorage("lm-theme"); this button just flips + persists the choice.
 */
export function ThemeToggle() {
  const [dark, setDark] = useState(true);

  // Sync the React state with whatever the no-flash script established.
  useEffect(() => {
    setDark(document.documentElement.classList.contains("dark"));
  }, []);

  const toggle = () => {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
    try {
      localStorage.setItem("lm-theme", next ? "dark" : "light");
    } catch {
      /* storage may be unavailable (private mode) — class still applied */
    }
  };

  return (
    <button
      onClick={toggle}
      aria-label={dark ? "Switch to light theme" : "Switch to dark theme"}
      title={dark ? "Light theme" : "Dark theme"}
      className="ml-4 inline-flex items-center justify-center w-9 h-9 rounded-full border border-rule text-ink hover:bg-surface-2 transition-colors"
    >
      {dark ? (
        // Sun — shown in dark mode (click for light)
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round">
          <circle cx="12" cy="12" r="4.2" />
          <path d="M12 2v2.4M12 19.6V22M2 12h2.4M19.6 12H22M4.6 4.6l1.7 1.7M17.7 17.7l1.7 1.7M19.4 4.6l-1.7 1.7M6.3 17.7l-1.7 1.7" />
        </svg>
      ) : (
        // Moon — shown in light mode (click for dark)
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
          <path d="M20 14.5A8 8 0 1 1 9.5 4a6.3 6.3 0 0 0 10.5 10.5z" />
        </svg>
      )}
    </button>
  );
}
