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
 * Styled in the specimen-sheet system (paper/ink/mono) so it matches the
 * redesigned views. The `tone` prop switches between the redesigned views
 * ("specimen") and the older gray views ("plain") that haven't been restyled.
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
  tone = "specimen",
}: {
  running: boolean;
  elapsed: number;
  error: StageErrorPayload | null;
  stageName: string; // e.g. "Concept Families"
  onRetry: () => void;
  tone?: "specimen" | "plain";
}) {
  if (!running && !error) return null;

  // ── Running: progress panel ──────────────────────────────────────────
  if (running) {
    const estimate = error?.estimate; // not set while running; kept for future
    const min = estimate?.[0];
    const max = estimate?.[1];
    return (
      <div
        className={
          tone === "specimen"
            ? "border border-ink/20 bg-stock p-4 font-mono text-xs"
            : "border border-gray-200 bg-white p-4 rounded-md text-sm"
        }
        role="status"
        aria-live="polite"
      >
        <div className="flex items-center gap-3">
          {/* spinner */}
          <svg className="animate-spin h-4 w-4 text-verified" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-90" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.4 0 0 5.4 0 12h4z" />
          </svg>
          <span className={tone === "specimen" ? "uppercase tracking-folio text-graphite" : "text-gray-700"}>
            {stageName} is reasoning
          </span>
          <span className={tone === "specimen" ? "ml-auto text-graphite" : "ml-auto text-gray-400"}>
            {fmt(elapsed)}
            {min && max ? ` · typically ${fmt(min)}–${fmt(max)}` : ""}
          </span>
        </div>
        <p className={tone === "specimen" ? "mt-2 text-graphite/80" : "mt-2 text-gray-500"}>
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
      className={
        tone === "specimen"
          ? "border border-stamp-reject/40 bg-stamp-reject/5 p-4"
          : "border border-red-200 bg-red-50 p-4 rounded-md"
      }
      role="alert"
    >
      <div className="flex items-start gap-3">
        <span
          className={
            tone === "specimen"
              ? "font-mono text-xs uppercase tracking-folio text-stamp-reject mt-0.5"
              : "text-sm font-medium text-red-800"
          }
        >
          {error?.stage_name ? `${error.stage_name} paused` : "Something went wrong"}
        </span>
      </div>
      <p className={tone === "specimen" ? "mt-1.5 text-sm text-ink/80" : "mt-1 text-sm text-red-700"}>
        {error?.detail ?? "An unexpected error occurred."}
      </p>
      {retryable && (
        <div className="mt-3 flex items-center gap-3">
          <button
            onClick={onRetry}
            className={
              tone === "specimen"
                ? "px-3 py-1.5 font-mono text-xs uppercase tracking-folio text-stock bg-ink hover:bg-ink/85"
                : "px-3 py-1.5 text-sm text-white bg-red-700 hover:bg-red-800 rounded-md"
            }
          >
            Retry {error?.stage_name ?? "stage"}
          </button>
          <span className={tone === "specimen" ? "text-xs text-graphite" : "text-xs text-red-500"}>
            Transient model failures usually clear on retry.
          </span>
        </div>
      )}
      {error?.technical && (
        <details className="mt-2">
          <summary className={tone === "specimen" ? "text-xs text-graphite cursor-pointer" : "text-xs text-red-400 cursor-pointer"}>
            Technical detail
          </summary>
          <pre
            className={
              tone === "specimen"
                ? "mt-1 text-[11px] text-graphite/70 bg-paper border border-rule p-2 overflow-auto font-mono"
                : "mt-1 text-[11px] text-red-500 bg-red-50 p-2 overflow-auto font-mono"
            }
          >
            {error.technical}
          </pre>
        </details>
      )}
    </div>
  );
}
