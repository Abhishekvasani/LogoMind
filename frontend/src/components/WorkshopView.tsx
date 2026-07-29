"use client";

import { useState } from "react";
import {
  Project,
  generateWorkshopLink,
  submitWorkshopAnswer,
  completeWorkshop,
  runStrategy,
} from "@/lib/api";

/**
 * Designer-facing Discovery Workshop (LOG-DISC-001, Workshop Mode).
 *
 * The brief did not yet reach the 70% Brand Confidence bar. This view presents
 * the gaps Discovery identified (`discovery_summary.missing_info`) as questions,
 * captures the designer's answers via the existing workshop plumbing, then
 * completes the workshop — which re-analyses the enriched brief — and runs
 * Strategy.
 *
 * The client-shareable `/workshop/[token]` page remains a deferred (Phase 6)
 * feature; the optional "Generate Client Workshop Link" affordance is kept here
 * for when that page exists.
 */
export function WorkshopView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const discovery = project.discovery_summary;
  // The questions are the missing-info gaps Discovery surfaced. Each has a
  // field id and a human-readable suggested_question.
  const questions = (discovery?.missing_info || []) as Array<{
    field: string;
    impact: string;
    suggested_question?: string;
  }>;

  // stage maps to the workshop step number (1-7); we assign sequentially.
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [shareLink, setShareLink] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleShare = async () => {
    setError(null);
    try {
      const result = await generateWorkshopLink(project.id);
      setShareLink(`${window.location.origin}/workshop/${result.share_token}`);
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleComplete = async () => {
    setRunning(true);
    setError(null);
    try {
      // Persist each non-empty answer so completion re-analyses an enriched brief.
      for (let i = 0; i < questions.length; i++) {
        const q = questions[i];
        const value = (answers[q.field] || "").trim();
        if (!value) continue;
        await submitWorkshopAnswer(project.id, {
          stage: i + 1,
          question_id: q.field,
          answer: value,
          answer_type: "text",
        });
      }
      // Complete re-analyses the brief (with answers appended) and resets stage
      // to "discovery"; then Strategy can run.
      await completeWorkshop(project.id);
      await runStrategy(project.id);
      onUpdate();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="p-6 bg-white border border-gray-200 rounded-lg">
        <h2 className="text-lg font-medium mb-2">Discovery Workshop</h2>
        <p className="text-gray-600 mb-4">
          The brief needs enrichment. Answer the questions below to fill the strategic gaps
          Discovery identified, then complete the workshop to rebuild Brand DNA.
        </p>

        {questions.length > 0 ? (
          <div className="space-y-4">
            {questions.map((q, i) => (
              <div key={q.field} className="p-4 border border-gray-200 rounded-lg bg-gray-50/50">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs px-2 py-0.5 rounded bg-gray-200 text-gray-600">
                    Step {i + 1}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded ${
                      q.impact === "high"
                        ? "bg-red-100 text-red-700"
                        : "bg-gray-200 text-gray-600"
                    }`}
                  >
                    {q.impact} impact
                  </span>
                  <span className="font-medium text-sm">{q.field.replace(/_/g, " ")}</span>
                </div>
                <p className="text-sm text-gray-700 mb-2 italic">
                  {q.suggested_question || `Tell us about ${q.field.replace(/_/g, " ")}.`}
                </p>
                <textarea
                  value={answers[q.field] || ""}
                  onChange={(e) => setAnswers({ ...answers, [q.field]: e.target.value })}
                  placeholder="Your answer…"
                  className="w-full p-2 border border-gray-300 rounded text-sm min-h-[70px]"
                />
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500 mb-4">
            No specific gaps were surfaced. If you have already gathered the strategic context
            separately, you can proceed directly.
          </p>
        )}

        <div className="flex flex-col gap-3 pt-4 border-t border-gray-100 mt-4">
          <button
            onClick={handleComplete}
            disabled={running}
            className="self-start px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
          >
            {running ? "Processing…" : "Complete Workshop & Run Strategy →"}
          </button>
          <p className="text-xs text-gray-400">
            Completing re-analyses the enriched brief and advances to Strategy.
          </p>
        </div>
      </div>

      {/* Optional: client-shareable link (deferred page). Kept for Phase 6. */}
      <div className="p-4 bg-white border border-gray-200 rounded-lg">
        <p className="text-sm text-gray-500 mb-2">
          Optionally, generate a link for your client to answer the workshop themselves.
          (The public workshop page is a deferred feature.)
        </p>
        <button
          onClick={handleShare}
          className="px-4 py-2 bg-gray-100 text-gray-900 rounded-md hover:bg-gray-200 self-start"
        >
          Generate Client Workshop Link
        </button>
        {shareLink && (
          <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded text-sm">
            <p className="font-medium text-blue-900 mb-1">Share this link with your client:</p>
            <code className="text-blue-700 break-all">{shareLink}</code>
          </div>
        )}
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-700">
          {error}
        </div>
      )}
    </div>
  );
}
