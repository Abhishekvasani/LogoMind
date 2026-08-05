"use client";

/**
 * useStageAction — shared hook for running a pipeline stage action against a
 * (slow, sometimes-flaky) AI model.
 *
 * Replaces the duplicated `running`/`error`/try-catch-finally boilerplate in
 * every stage view, and adds:
 *   - an elapsed timer while the action runs (so the UI can show real progress
 *     instead of a frozen gerund),
 *   - structured error capture (StageApiError → rich payload; plain Error →
 *     string), and
 *   - a `retry` that re-runs the last action.
 *
 * The caller passes the stage id (for estimate lookup) and a factory for the
 * API call; the hook returns { run, retry, running, elapsed, error }.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { StageApiError, StageErrorPayload } from "./api";

interface UseStageAction {
  running: boolean;
  elapsed: number; // seconds since the current run started
  error: StageErrorPayload | null;
  // Run an action. The factory receives no args; close over what you need.
  // `stageId` is optional metadata for estimate lookup if the backend didn't
  // return one in the error payload.
  run: (fn: () => Promise<unknown>, stageId?: string) => Promise<void>;
  retry: () => Promise<void>;
}

const ESTIMATES: Record<string, [number, number]> = {
  strategy: [20, 90],
  insight: [30, 120],
  create: [60, 240],
  judge: [180, 540],
  concept_prompt: [180, 720],
  ssb: [30, 120],
  sketch: [20, 60],
  presentation: [30, 90],
};

function toPayload(e: unknown, stageId?: string): StageErrorPayload {
  if (e instanceof StageApiError) return e.payload;
  // Network failure (fetch rejected) — browser-native, no backend body.
  const msg = e instanceof Error ? e.message : "Unexpected error.";
  return {
    stage: stageId ?? "",
    stage_name: stageId ? stageId : "engine",
    kind: "transient",
    detail:
      msg === "Failed to fetch"
        ? "Couldn't reach the LogoMind server. Check both dev servers are running, then retry."
        : `Something went wrong while running this stage. ${msg}`,
    retryable: true,
    estimate: stageId ? ESTIMATES[stageId] : undefined,
  };
}

export function useStageAction(onSuccess: () => void): UseStageAction {
  const [running, setRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [error, setError] = useState<StageErrorPayload | null>(null);

  const lastFn = useRef<(() => Promise<unknown>) | null>(null);
  const lastStageId = useRef<string | undefined>(undefined);
  const startedAt = useRef<number>(0);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  const stopTimer = useCallback(() => {
    if (timer.current) {
      clearInterval(timer.current);
      timer.current = null;
    }
  }, []);

  const run = useCallback(
    async (fn: () => Promise<unknown>, stageId?: string) => {
      lastFn.current = fn;
      lastStageId.current = stageId;
      setError(null);
      setRunning(true);
      setElapsed(0);
      startedAt.current = Date.now();
      stopTimer();
      timer.current = setInterval(() => {
        setElapsed(Math.floor((Date.now() - startedAt.current) / 1000));
      }, 1000);
      try {
        await fn();
        onSuccess();
      } catch (e) {
        setError(toPayload(e, stageId));
      } finally {
        stopTimer();
        setRunning(false);
      }
    },
    [onSuccess, stopTimer]
  );

  const retry = useCallback(async () => {
    if (lastFn.current) await run(lastFn.current, lastStageId.current);
  }, [run]);

  // Clean up the timer if the component unmounts mid-run.
  useEffect(() => stopTimer, [stopTimer]);

  return { running, elapsed, error, run, retry };
}

export { ESTIMATES };
