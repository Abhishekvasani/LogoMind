"use client";

/**
 * Concept Prompt view — redesigned as a SPECIMEN SHEET (PROD-CP-001).
 *
 * Each concept family is presented as a studio plate: a folio number, an
 * italic Fraunces title (the core concept), a hairline rule, then the four
 * prompt variants set as MONO SPECIMENS on paper (the copyable artifact) and
 * a technical-drawing wireframe plate with model adaptations. Clichés avoided
 * appear as a strike-through margin list. The register is a designer's
 * printout, not a SaaS dashboard.
 */

import { useState } from "react";
import { Project, composeConceptPrompts, composeSSB } from "@/lib/api";
import { Wireframe } from "@/components/Wireframe";
import { StageStatus } from "@/components/StageStatus";
import { useStageAction } from "@/lib/useStageAction";

const STAMP_TEXT: Record<string, string> = {
  recommended: "RECOMMENDED",
  develop: "DEVELOP",
  reject: "RECONCEIVE",
};

export function ConceptPromptView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const [activeVariant, setActiveVariant] = useState<Record<string, number>>({});
  const [showSpec, setShowSpec] = useState<Record<string, boolean>>({});
  const [copied, setCopied] = useState<string | null>(null);

  const conceptPrompts = project.concept_prompts || [];
  const judgeByLabel: Record<string, any> = {};
  for (const j of project.judge_report || []) judgeByLabel[j.family_label] = j;

  const handleCompose = () => run(() => composeConceptPrompts(project.id), "concept_prompt");
  const handleContinue = () => run(() => composeSSB(project.id), "ssb");

  const copy = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopied(key);
    setTimeout(() => setCopied(null), 1500);
  };

  // ── Empty state: not yet composed ──────────────────────────────────
  if (conceptPrompts.length === 0) {
    return (
      <section className="space-y-6">
        <header className="border-b border-ink/15 pb-6">
          <p className="font-mono text-xs tracking-folio text-graphite uppercase">Stage · Concept Prompt</p>
          <h2 className="font-display text-4xl mt-2 tracking-tight">Executable concepts.</h2>
          <p className="text-graphite mt-2 max-w-2xl">
            Each evaluated Concept Family becomes a model-ready concept — four prompt variants, per-model
            adaptations, and a composition wireframe. Copy a prompt into your own image model.
          </p>
        </header>
        {/* Compose is reachable once families have been judged. The happy path
            routes through Client Fit (judge → client_fit → concept_prompt), but
            a designer may also arrive here straight from judge, so accept both. */}
        {project.stage === "judge" || project.stage === "client_fit" ? (
          <button
            onClick={handleCompose}
            disabled={running}
            className="px-5 py-3 bg-ink text-stock font-mono text-sm uppercase tracking-folio hover:bg-ink/85 disabled:opacity-50"
          >
            {running ? "Composing…" : "Generate concept prompts →"}
          </button>
        ) : (
          <p className="text-sm text-graphite italic">
            Concept Families must pass the Judge engine before concepts can be composed.
          </p>
        )}
        <StageStatus
          running={running}
          elapsed={elapsed}
          error={error}
          stageName="Concept Prompt"
          onRetry={retry}
        />
      </section>
    );
  }

  // ── Specimen plates ────────────────────────────────────────────────
  return (
    <section className="space-y-10">
      <header className="border-b border-ink/15 pb-6">
        <div className="flex items-end justify-between gap-6">
          <div>
            <p className="font-mono text-xs tracking-folio text-graphite uppercase">Stage · Concept Prompt</p>
            <h2 className="font-display text-4xl mt-2 tracking-tight">Executable concepts.</h2>
          </div>
          <p className="font-mono text-xs text-graphite text-right">
            {conceptPrompts.length} PLATE{conceptPrompts.length === 1 ? "" : "S"}
            <br />
            <span className="text-graphite/70">Take a prompt to your own model.</span>
          </p>
        </div>
      </header>

      {conceptPrompts.map((cp: any) => {
        const judgment = judgeByLabel[cp.family_label];
        const stamp = judgment?.classification; // recommended | develop | reject
        const variantIdx = activeVariant[cp.family_label] ?? 0;
        const variant = cp.variants[variantIdx];

        return (
          <article
            key={cp.family_label}
            className="relative bg-stock border border-ink/25 rounded-sm p-6 md:p-10"
          >
            {/* Classification stamp, top-right */}
            {stamp && (
              <span
                className={`absolute top-0 right-6 -translate-y-1/2 px-3 py-1 font-mono text-[10px] tracking-folio uppercase border bg-stock ${
                  stamp === "recommended"
                    ? "text-stamp-recommended border-stamp-recommended"
                    : stamp === "reject"
                    ? "text-stamp-reject border-stamp-reject"
                    : "text-stamp-develop border-stamp-develop"
                }`}
              >
                {STAMP_TEXT[stamp] ?? stamp}
              </span>
            )}

            {/* Folio + title */}
            <div className="flex items-baseline gap-4">
              <span className="font-mono text-sm tracking-folio text-graphite">FAMILY {cp.family_label}</span>
              <span className="font-mono text-[10px] tracking-folio text-graphite/70">· {cp.confidence}</span>
            </div>
            <h3 className="font-display italic text-2xl md:text-3xl leading-snug mt-2 max-w-3xl">
              {cp.core_concept}
            </h3>
            <hr className="border-rule mt-6" />

            {/* Body: specimens (left) + plate (right) */}
            <div className="grid grid-cols-1 lg:grid-cols-[1.15fr_1fr] gap-8 mt-6">
              {/* ── Prompt specimens ── */}
              <div>
                <p className="font-mono text-[10px] tracking-folio text-graphite uppercase mb-3">
                  Prompt Specimens · Four Variants
                </p>

                {/* variant selector — labelled chips */}
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {cp.variants.map((v: any, i: number) => (
                    <button
                      key={v.style}
                      onClick={() => setActiveVariant({ ...activeVariant, [cp.family_label]: i })}
                      className={`px-3 py-1 font-mono text-[11px] tracking-folio uppercase border transition-colors ${
                        i === variantIdx
                          ? "bg-ink text-stock border-ink"
                          : "bg-transparent text-ink border-ink/30 hover:border-ink"
                      }`}
                    >
                      {v.style}
                    </button>
                  ))}
                </div>

                {/* the specimen itself — mono on paper, the hero */}
                <div className="relative bg-paper border border-ink/15 p-5">
                  <p className="font-display italic text-sm text-graphite mb-3">{variant.intent}</p>
                  <pre className="font-mono text-[13px] leading-relaxed text-ink whitespace-pre-wrap">
                    {variant.prompt}
                  </pre>
                  <button
                    onClick={() => copy(variant.prompt, `${cp.family_label}-v${variantIdx}`)}
                    className="absolute top-3 right-3 px-2.5 py-1 font-mono text-[10px] uppercase tracking-folio bg-stock border border-ink/40 hover:bg-ink hover:text-stock transition-colors"
                  >
                    {copied === `${cp.family_label}-v${variantIdx}` ? "Copied ✓" : "Copy"}
                  </button>
                </div>

                {/* model adaptations — compact reference table */}
                <p className="font-mono text-[10px] tracking-folio text-graphite uppercase mt-6 mb-2">
                  Model Adaptations
                </p>
                <dl className="border-t border-rule">
                  {cp.model_adaptations.map((a: any) => (
                    <div
                      key={a.model_family}
                      className="grid grid-cols-[7.5rem_1fr_auto] gap-3 items-baseline py-2 border-b border-rule"
                    >
                      <dt className="font-mono text-[11px] uppercase tracking-folio text-ink">{a.model_family}</dt>
                      <dd className="text-[13px] text-graphite leading-snug">{a.notes}</dd>
                      <button
                        onClick={() => copy(a.example_suffix, `${cp.family_label}-${a.model_family}`)}
                        title="Copy suffix"
                        className="font-mono text-[11px] text-verified hover:text-ink transition-colors whitespace-nowrap"
                      >
                        {copied === `${cp.family_label}-${a.model_family}` ? "✓" : a.example_suffix}
                      </button>
                    </div>
                  ))}
                </dl>
              </div>

              {/* ── Wireframe plate ── */}
              <div>
                <p className="font-mono text-[10px] tracking-folio text-graphite uppercase mb-3">
                  Composition Wireframe
                </p>
                <Wireframe spec={cp.wireframe} familyLabel={cp.family_label} />

                {/* collapsible raw spec */}
                <div className="mt-4">
                  <button
                    onClick={() => setShowSpec({ ...showSpec, [cp.family_label]: !showSpec[cp.family_label] })}
                    className="font-mono text-[10px] tracking-folio text-graphite uppercase hover:text-ink"
                  >
                    {showSpec[cp.family_label] ? "− Hide raw spec" : "+ Show raw spec"}
                  </button>
                  {showSpec[cp.family_label] && (
                    <pre className="font-mono text-[11px] text-graphite bg-paper border border-rule mt-2 p-3 overflow-auto max-h-56 leading-relaxed">
                      {JSON.stringify(cp.wireframe, null, 2)}
                    </pre>
                  )}
                </div>
              </div>
            </div>

            {/* Footer: rationale + clichés avoided (strike-through list) */}
            <div className="grid grid-cols-1 md:grid-cols-[1.5fr_1fr] gap-8 mt-8 pt-6 border-t border-rule">
              <div>
                <p className="font-mono text-[10px] tracking-folio text-graphite uppercase mb-2">Rationale</p>
                <p className="font-display italic text-[15px] text-ink/80 leading-relaxed">{cp.rationale}</p>
              </div>
              {cp.cliches_avoided?.length > 0 && (
                <div>
                  <p className="font-mono text-[10px] tracking-folio text-graphite uppercase mb-2">
                    Clichés Avoided
                  </p>
                  <ul className="space-y-1">
                    {cp.cliches_avoided.map((c: string, i: number) => (
                      <li
                        key={i}
                        className="font-mono text-[12px] text-graphite/70 line-through decoration-stamp-reject/60 decoration-1"
                      >
                        {c}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </article>
        );
      })}

      {/* Continue to SSB */}
      {project.stage === "concept_prompt" && (
        <div className="flex justify-end pt-2">
          <button
            onClick={handleContinue}
            disabled={running}
            className="px-5 py-3 bg-ink text-stock font-mono text-sm uppercase tracking-folio hover:bg-ink/85 disabled:opacity-50"
          >
            {running ? "Composing…" : "Compose strategic sketch brief →"}
          </button>
        </div>
      )}

      <StageStatus
        running={running}
        elapsed={elapsed}
        error={error}
        stageName="Concept Prompt"
        onRetry={retry}
      />
    </section>
  );
}
