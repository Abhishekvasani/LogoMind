"use client";

import { Project, runInsight } from "@/lib/api";
import { useStageAction } from "@/lib/useStageAction";
import { StageStatus } from "@/components/StageStatus";

export function StrategyView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const dna = project.brand_dna;

  const handleProceed = () => run(() => runInsight(project.id), "insight");

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-medium">Brand DNA</h2>

      {dna ? (
        <>
          <DNACard label="Purpose" value={dna.purpose} confidence={dna.purpose_confidence} />
          <DNACard label="Positioning" value={dna.positioning_statement} confidence={dna.positioning_confidence} />
          <DNACard label="Differentiation" value={dna.differentiation_primary} confidence={dna.differentiation_defensibility} sub={`Dimension: ${dna.differentiation_dimension}`} />
          <DNACard label="Personality" value={dna.personality} confidence={dna.personality_coherence} />
          <DNACard label="Archetype" value={dna.archetype || "No clean archetype identified"} confidence={undefined} sub={`Finding: ${dna.archetype_finding}`} />
          <DNACard label="Emotional Goal" value={dna.emotional_goal} confidence={undefined} />

          {dna.contradictions_flagged?.length > 0 && (
            <div className="p-4 bg-warn/10 border border-warn/30 rounded-lg">
              <h3 className="font-medium text-warn mb-2">⚠ Contradictions Flagged</h3>
              {dna.contradictions_flagged.map((c: any, i: number) => (
                <p key={i} className="text-sm text-warn">{c.description || JSON.stringify(c)}</p>
              ))}
              <p className="text-xs text-warn/80 mt-2">LogoMind surfaces contradictions; the designer resolves them.</p>
            </div>
          )}

          <div className="pt-4">
            <button
              onClick={handleProceed}
              disabled={running}
              className="px-4 py-2 bg-ink text-stock rounded-md hover:bg-ink/85 disabled:opacity-50"
            >
              {running ? "Generating Insight…" : "Continue to Insight →"}
            </button>
          </div>

          <StageStatus
            running={running}
            elapsed={elapsed}
            error={error}
            stageName="Insight"
            onRetry={retry}
          />
        </>
      ) : (
        <p className="text-graphite">Brand DNA not yet generated. (Strategy Engine should have run.)</p>
      )}
    </div>
  );
}

function DNACard({ label, value, confidence, sub }: { label: string; value: string; confidence?: string; sub?: string }) {
  const confidenceEmoji: Record<string, string> = { C5: "🟢", C4: "🔵", C3: "🟠", C2: "🟣", C1: "⚪" };
  return (
    <div className="p-4 bg-stock border border-rule rounded-lg">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-medium text-graphite uppercase tracking-wide">{label}</span>
        {confidence && (
          <span className="text-xs text-graphite">{confidenceEmoji[confidence] || ""} {confidence}</span>
        )}
      </div>
      <p className="text-ink">{value}</p>
      {sub && <p className="text-xs text-graphite mt-1">{sub}</p>}
    </div>
  );
}
