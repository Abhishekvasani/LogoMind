"use client";

import { useState } from "react";
import {
  Project,
  runClientFit,
  composeConceptPrompts,
  decodeContestBrief,
  attachContestBrief,
  refineClientFit,
  decodeIntent,
} from "@/lib/api";
import { useStageAction } from "@/lib/useStageAction";
import { StageStatus } from "@/components/StageStatus";

/**
 * Client Fit — the Client Preference Predictor view.
 *
 * The decision screen: which Concept Family is the safest bet to win THIS
 * client, and why. Shows the modelled client persona, ranks families by
 * predicted appeal, and surfaces the honest caveat (brief-only inference,
 * not literal neuroscience).
 *
 * Two contest-intelligence inputs feed the prediction (both filed under this
 * stage by the backend): a decoded contest brief (paste a freelancer.com brief
 * → structured signals, attached before predicting) and a revealed-preference
 * refine loop (log what the client liked/disliked mid-contest → re-predict).
 */
export function ClientFitView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const report = project.appeal_report;
  const persona = report?.persona || project.client_persona;
  const families = project.concept_families || [];

  const handlePredict = () => run(() => runClientFit(project.id), "client_fit");
  const handleCompose = () => run(() => composeConceptPrompts(project.id), "concept_prompt");

  const stageName = error?.stage_name ?? "Client Fit";

  // ── Contest Brief Decoder (input) ──────────────────────────────────
  const attached = project.contest_brief;
  const [showContest, setShowContest] = useState(!attached);
  const [rawBrief, setRawBrief] = useState("");
  const [preview, setPreview] = useState<any>(null);
  const [decoding, setDecoding] = useState(false);
  const [decodeError, setDecodeError] = useState<string | null>(null);

  const handleDecodePreview = async () => {
    if (!rawBrief.trim()) return;
    setDecoding(true);
    setDecodeError(null);
    setPreview(null);
    try {
      setPreview(await decodeContestBrief(rawBrief));
    } catch (e: any) {
      setDecodeError(e?.message ?? "Couldn't decode that brief.");
    } finally {
      setDecoding(false);
    }
  };

  const handleAttach = () =>
    run(() => attachContestBrief(project.id, rawBrief), "client_fit").then(() => {
      setRawBrief("");
      setPreview(null);
    });

  // ── Intent Extraction mini-tool ────────────────────────────────────
  const [intentInput, setIntentInput] = useState("");
  const [intentResult, setIntentResult] = useState<any>(null);
  const [decodingIntent, setDecodingIntent] = useState(false);

  const handleDecodeIntent = async () => {
    if (!intentInput.trim()) return;
    setDecodingIntent(true);
    setIntentResult(null);
    try {
      setIntentResult(await decodeIntent(intentInput));
    } catch {
      setIntentResult(null);
    } finally {
      setDecodingIntent(false);
    }
  };

  // ── Revealed-preference refine loop ────────────────────────────────
  const feedback = project.contest_feedback || [];
  const [sigKind, setSigKind] = useState<"liked" | "disliked" | "comment">("liked");
  const [sigTrait, setSigTrait] = useState("");
  const [sigNote, setSigNote] = useState("");

  const handleRefine = () => {
    if (!sigTrait.trim()) return;
    run(
      () =>
        refineClientFit(project.id, [
          { kind: sigKind, trait: sigTrait.trim(), note: sigNote.trim() || undefined },
        ]),
      "client_fit"
    );
    setSigTrait("");
    setSigNote("");
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-medium">Client Fit — what will THIS client love?</h2>
          <p className="text-sm text-graphite">
            Predicts which direction the decision-maker is most likely to pick — based on their
            brief, not generic &ldquo;good design&rdquo;.
          </p>
        </div>
        <button
          onClick={handlePredict}
          disabled={running}
          className="px-3 py-1.5 bg-ink text-stock text-sm rounded hover:bg-ink/85 disabled:opacity-50"
        >
          {running ? "Predicting…" : report ? "Re-run Prediction" : "Predict Client Appeal →"}
        </button>
      </div>

      {/* ── Contest Brief Decoder (an input to the prediction) ────── */}
      <div className="border border-rule bg-stock rounded-lg overflow-hidden">
        <button
          onClick={() => setShowContest((s) => !s)}
          className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-surface-2"
        >
          <span className="text-sm font-medium">
            Contest brief {attached && <span className="text-xs text-ok ml-1">· attached</span>}
          </span>
          <span className="text-xs text-graphite">{showContest ? "hide ▲" : "paste a freelancer.com brief to sharpen the prediction ▼"}</span>
        </button>

        {showContest && (
          <div className="px-4 pb-4 space-y-3 border-t border-rule">
            {attached && (
              <ContestFields brief={attached} />
            )}

            <div>
              <textarea
                value={rawBrief}
                onChange={(e) => setRawBrief(e.target.value)}
                placeholder={"Paste a raw contest brief here (e.g. the freelancer.com description):\n\nCompany name: …\nDo you have colors in mind: …\nAnything to avoid: …"}
                rows={6}
                className="w-full text-sm border border-rule rounded p-2 font-mono bg-paper text-ink focus:outline-none focus:border-ink/40"
              />
              <div className="flex items-center gap-2 mt-2">
                <button
                  onClick={handleDecodePreview}
                  disabled={decoding || !rawBrief.trim()}
                  className="px-3 py-1.5 text-sm border border-rule rounded hover:bg-surface-2 disabled:opacity-50"
                >
                  {decoding ? "Decoding…" : "Decode preview"}
                </button>
                <button
                  onClick={handleAttach}
                  disabled={running || !rawBrief.trim()}
                  className="px-3 py-1.5 text-sm bg-ink text-stock rounded hover:bg-ink/85 disabled:opacity-50"
                >
                  {running ? "Attaching…" : "Attach to project →"}
                </button>
                {decodeError && <span className="text-xs text-bad">{decodeError}</span>}
              </div>
            </div>

            {preview && (
              <div className="border border-accent/40 bg-accent/10 rounded p-3">
                <p className="text-xs text-accent font-medium mb-2">Decoded preview (not yet attached)</p>
                <ContestFields brief={preview} />
              </div>
            )}

            {/* Intent Extraction mini-tool — "I want blue" -> "I want trust" */}
            <div className="border-t border-rule pt-3">
              <p className="text-xs text-graphite uppercase mb-1">Decode a client preference</p>
              <div className="flex items-center gap-2">
                <input
                  value={intentInput}
                  onChange={(e) => setIntentInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleDecodeIntent()}
                  placeholder='e.g. "I want blue" or "a shield"'
                  className="flex-1 text-sm border border-rule rounded px-2 py-1.5 bg-paper text-ink focus:outline-none focus:border-ink/40"
                />
                <button
                  onClick={handleDecodeIntent}
                  disabled={decodingIntent || !intentInput.trim()}
                  className="px-3 py-1.5 text-sm border border-rule rounded hover:bg-surface-2 disabled:opacity-50"
                >
                  {decodingIntent ? "…" : "Decode"}
                </button>
              </div>
              {intentResult && (
                <p className="text-xs text-graphite mt-2">
                  <span className="italic">&ldquo;{intentResult.preference}&rdquo;</span>{" "}
                  → <span className="font-medium text-ink">{intentResult.intent}</span>
                  {intentResult.reasoning && <span className="text-graphite/80"> — {intentResult.reasoning}</span>}
                </p>
              )}
            </div>
          </div>
        )}
      </div>

      {report && persona && (
        <>
          {/* Persona card */}
          <div className="p-5 border border-rule bg-stock rounded-lg">
            <div className="flex items-center gap-2 mb-3">
              <h3 className="font-medium">Modelled client</h3>
              <span className="text-xs px-2 py-0.5 bg-surface-2 rounded">{persona.archetype}</span>
              <span className="text-xs px-2 py-0.5 bg-accent/15 text-accent rounded capitalize">
                {persona.aesthetic_lean}
              </span>
              <span className="text-xs px-2 py-0.5 bg-surface-2 text-graphite rounded capitalize">
                {persona.boldness_tolerance} boldness
              </span>
            </div>
            <p className="text-sm text-ink/90 mb-3">{persona.one_line}</p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
              {persona.decoded_intents?.length > 0 && (
                <div>
                  <p className="text-xs text-graphite/80 uppercase mb-1">Decoded intents</p>
                  <div className="flex flex-wrap gap-1">
                    {persona.decoded_intents.map((di: any, i: number) => (
                      <span key={i} className="text-xs px-2 py-0.5 bg-surface-2 rounded">
                        &ldquo;{di.stated}&rdquo; → {di.intent}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {persona.taste_signals?.length > 0 && (
                <div>
                  <p className="text-xs text-graphite/80 uppercase mb-1">Taste signals</p>
                  <div className="flex flex-wrap gap-1">
                    {persona.taste_signals.map((s: string, i: number) => (
                      <span key={i} className="text-xs px-2 py-0.5 bg-surface-2 rounded">{s}</span>
                    ))}
                  </div>
                </div>
              )}
              {persona.must_haves?.length > 0 && (
                <div>
                  <p className="text-xs text-graphite/80 uppercase mb-1">Must have</p>
                  <p className="text-xs text-graphite">{persona.must_haves.join(", ")}</p>
                </div>
              )}
              {persona.must_avoids?.length > 0 && (
                <div>
                  <p className="text-xs text-graphite/80 uppercase mb-1">Must avoid</p>
                  <p className="text-xs text-graphite">{persona.must_avoids.join(", ")}</p>
                </div>
              )}
            </div>
          </div>

          {/* Ranked families */}
          <div className="space-y-3">
            <p className="text-sm text-graphite">
              Recommended: <span className="font-medium text-ink">Family {report.recommended_family}</span> — {report.reasoning}
            </p>

            {(report.family_appeal || [])
              .slice()
              .sort((a: any, b: any) => a.rank - b.rank)
              .map((fa: any) => {
                const family = families.find((f: any) => f.family_label === fa.family_label);
                const isTop = fa.rank === 1;
                const score = Math.round(fa.client_appeal_score);
                return (
                  <div
                    key={fa.family_label}
                    className={`p-5 border rounded-lg ${isTop ? "border-accent/50 bg-accent/10" : "border-rule bg-stock"}`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium">
                        {isTop && <span className="text-accent mr-1">★</span>}
                        Family {fa.family_label}
                        {family?.theme ? ` — ${family.theme}` : ""}
                      </h3>
                      <span className={`text-xs px-2 py-1 rounded ${isTop ? "bg-accent/25 text-accent" : "bg-surface-2 text-graphite"}`}>
                        Predicted appeal {score}/100
                      </span>
                    </div>

                    <div className="w-full h-1.5 bg-surface-2 rounded-full overflow-hidden mb-3">
                      <div
                        className={isTop ? "h-full bg-accent" : "h-full bg-graphite/60"}
                        style={{ width: `${score}%` }}
                      />
                    </div>

                    <p className="text-sm text-ink/90 italic mb-2">{fa.predicted_response}</p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                      <div>
                        <p className="text-ok font-medium mb-0.5">Drivers</p>
                        <ul className="text-graphite space-y-0.5">
                          {(fa.appeal_drivers || []).map((d: string, i: number) => <li key={i}>+ {d}</li>)}
                        </ul>
                      </div>
                      <div>
                        <p className="text-bad font-medium mb-0.5">Risks</p>
                        <ul className="text-graphite space-y-0.5">
                          {(fa.appeal_risks || []).map((r: string, i: number) => <li key={i}>− {r}</li>)}
                        </ul>
                      </div>
                    </div>
                  </div>
                );
              })}
          </div>

          {/* Honest caveat */}
          <div className="p-4 bg-warn/10 border border-warn/30 rounded-lg text-sm text-warn">
            <span className="font-medium">Honest limit:</span> {report.caveat} This is a
            reasoning-based preference prediction, not a literal brain-response measurement — it
            sharpens considerably once you fold in the client&rsquo;s contest ratings and comments.
          </div>

          {/* Revealed-preference refine loop — sharpen with in-contest feedback */}
          <div className="p-4 border border-rule bg-stock rounded-lg">
            <h3 className="font-medium mb-1">Sharpen the prediction</h3>
            <p className="text-xs text-graphite mb-3">
              As the contest unfolds, log what the client actually reacted to. Each signal re-runs
              the predictor with that feedback weighted highest.
            </p>

            {feedback.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mb-3">
                {feedback.map((s: any, i: number) => (
                  <span
                    key={i}
                    className={`text-xs px-2 py-0.5 rounded ${
                      s.kind === "liked"
                        ? "bg-ok/15 text-ok"
                        : s.kind === "disliked"
                        ? "bg-bad/15 text-bad"
                        : "bg-surface-2 text-ink"
                    }`}
                    title={s.note}
                  >
                    {s.kind === "liked" ? "👍" : s.kind === "disliked" ? "👎" : "💬"} {s.trait}
                  </span>
                ))}
              </div>
            )}

            <div className="flex flex-wrap items-center gap-2">
              <select
                value={sigKind}
                onChange={(e) => setSigKind(e.target.value as "liked" | "disliked" | "comment")}
                className="text-sm border border-rule rounded px-2 py-1.5 bg-paper text-ink focus:outline-none focus:border-ink/40"
              >
                <option value="liked">Liked</option>
                <option value="disliked">Disliked</option>
                <option value="comment">Comment</option>
              </select>
              <input
                value={sigTrait}
                onChange={(e) => setSigTrait(e.target.value)}
                placeholder="trait, e.g. minimal layouts"
                className="flex-1 min-w-[160px] text-sm border border-rule rounded px-2 py-1.5 bg-paper text-ink focus:outline-none focus:border-ink/40"
              />
              <input
                value={sigNote}
                onChange={(e) => setSigNote(e.target.value)}
                placeholder="note (optional)"
                className="flex-1 min-w-[140px] text-sm border border-rule rounded px-2 py-1.5 bg-paper text-ink focus:outline-none focus:border-ink/40"
              />
              <button
                onClick={handleRefine}
                disabled={running || !sigTrait.trim()}
                className="px-3 py-1.5 text-sm bg-ink text-stock rounded hover:bg-ink/85 disabled:opacity-50"
              >
                {running ? "Re-predicting…" : "Add & re-predict →"}
              </button>
            </div>
          </div>

          {/* Proceed — concept prompts are steered by this persona */}
          <button
            onClick={handleCompose}
            disabled={running}
            className="px-4 py-2 bg-ink text-stock rounded-md hover:bg-ink/85 disabled:opacity-50"
          >
            {running ? "Composing prompts…" : "Compose Concept Prompts (steered by this client) →"}
          </button>
        </>
      )}

      {!report && (
        <div className="p-6 border border-dashed border-rule rounded-lg text-center">
          <p className="text-sm text-graphite mb-3">
            No prediction yet. Run the predictor to rank the {families.length} concept families by
            how strongly they&rsquo;ll resonate with this specific client.
          </p>
        </div>
      )}

      <StageStatus
        running={running}
        elapsed={elapsed}
        error={error}
        stageName={stageName}
        onRetry={retry}
      />
    </div>
  );
}

/** Render the structured fields of a ContestBrief (attached or previewed). */
function ContestFields({ brief }: { brief: any }) {
  const groups: Array<[string, string[]]> = [
    ["Preferred colors", brief.colors_preferred],
    ["Avoid colors", brief.colors_avoided],
    ["Style", brief.style_keywords],
    ["Do", brief.dos],
    ["Don't", brief.donts],
    ["Must include", brief.must_include],
    ["Must avoid", brief.must_avoid],
    ["References", brief.references],
  ].filter(([, v]) => Array.isArray(v) && v.length > 0) as Array<[string, string[]]>;

  return (
    <div className="space-y-2">
      {(brief.company_name || brief.industry || brief.tagline) && (
        <p className="text-sm text-ink">
          {brief.company_name && <span className="font-medium">{brief.company_name}</span>}
          {brief.industry && <span className="text-graphite"> · {brief.industry}</span>}
          {brief.tagline && <span className="text-graphite/80 italic"> — &ldquo;{brief.tagline}&rdquo;</span>}
        </p>
      )}
      {brief.decoded_summary && <p className="text-xs text-graphite italic">{brief.decoded_summary}</p>}
      {groups.length > 0 && (
        <div className="space-y-1.5">
          {groups.map(([label, items]) => (
            <div key={label} className="flex flex-wrap items-baseline gap-1.5">
              <span className="text-xs text-graphite/80 uppercase">{label}</span>
              {items.map((item, i) => (
                <span key={i} className="text-xs px-2 py-0.5 bg-surface-2 rounded">{item}</span>
              ))}
            </div>
          ))}
        </div>
      )}
      {brief.confidence && (
        <span className="inline-block text-xs px-2 py-0.5 bg-surface-2 text-graphite rounded">
          confidence {brief.confidence}
        </span>
      )}
    </div>
  );
}
