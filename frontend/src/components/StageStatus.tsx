"use client";

/**
 * StageStatus — shared UI for a running/failed pipeline stage.
 *
 * While running: a quiet "working" panel with the stage name, an animated
 * hairline progress meter bounded by the stage's honest estimate, and live
 * elapsed time — so a 5-minute Create/Judge/Concept call never feels frozen.
 *
 * On failure: a polished, natural-language message (never a raw "Internal
 * Server Error"), the kind of failure, and a Retry button when retryable.
 *
 * Styled in the specimen-sheet token system (ink/stock/graphite/stamp-reject)
 * so it matches the theme-aware views and flips with the light/dark substrate.
 */

import { StageErrorPayload } from "@/lib/api";

function fmt(s: number): string {
  const m = Math.floor(s / 60);
  const r = s % 60;
  return m > 0 ? `${m}m ${r}s` : `${r}s`;
}

export function StageStatus({
  running,
  elapsed,
  error,
  stageName,
  onRetry,
}: {
  running: boolean;
  elapsed: number;
  error: StageErrorPayload | null;
  stageName: string; // e.g. "Concept Families"
  onRetry: () => void;
}) {
  if (!running && !error) return null;

  // ── Running: progress panel ──────────────────────────────────────────
  if (running) {
    const estimate = error?.estimate; // not set while running; kept for future
    const min = estimate?.[0];
    const max = estimate?.[1];
    return (
      <div
        className="border border-ink/20 bg-stock p-4 font-mono text-xs"
        role="status"
        aria-live="polite"
      >
        <div className="flex items-center gap-3">
          {/* spinner */}
          <svg className="animate-spin h-4 w-4 text-accent" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-90" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.4 0 0 5.4 0 12h4z" />
          </svg>
          <span className="uppercase tracking-folio text-graphite">
            {stageName} is reasoning
          </span>
          <span className="ml-auto text-graphite">
            {fmt(elapsed)}
            {min && max ? ` · typically ${fmt(min)}–${fmt(max)}` : ""}
          </span>
        </div>
        <p className="mt-2 text-graphite/80">
          LogoMind is calling the model and working through the strategy. Long stages like Judge and
          Concept Prompt can take several minutes — this is normal. Keep this tab open.
        </p>
      </div>
    );
  }

  // ── Failed: polished error + retry ───────────────────────────────────
  const retryable = error?.retryable !== false;
  return (
    <div
      className="border border-bad/40 bg-bad/5 p-4"
      role="alert"
    >
      <div className="flex items-start gap-3">
        <span className="font-mono text-xs uppercase tracking-folio text-bad mt-0.5">
          {error?.stage_name ? `${error.stage_name} paused` : "Something went wrong"}
        </span>
      </div>
      <p className="mt-1.5 text-sm text-ink/80">
        {error?.detail ?? "An unexpected error occurred."}
      </p>
      {retryable && (
        <div className="mt-3 flex items-center gap-3">
          <button
            onClick={onRetry}
            className="px-3 py-1.5 font-mono text-xs uppercase tracking-folio text-stock bg-ink hover:bg-ink/85"
          >
            Retry {error?.stage_name ?? "stage"}
          </button>
          <span className="text-xs text-graphite">
            Transient model failures usually clear on retry.
          </span>
        </div>
      )}
      {error?.technical && (
        <details className="mt-2">
          <summary className="text-xs text-graphite cursor-pointer">
            Technical detail
          </summary>
          <pre className="mt-1 text-[11px] text-graphite/70 bg-paper border border-rule p-2 overflow-auto font-mono">
            {error.technical}
          </pre>
        </details>
      )}
    </div>
  );
}
