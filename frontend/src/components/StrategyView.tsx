"use client";

import { useState } from "react";
import { Project, runInsight } from "@/lib/api";

export function StrategyView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const [running, setRunning] = useState(false);
  const dna = project.brand_dna;

  const handleProceed = async () => {
    setRunning(true);
    try {
      await runInsight(project.id);
      onUpdate();
    } catch (e: any) {
      alert(e.message);
    } finally {
      setRunning(false);
    }
  };

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
            <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <h3 className="font-medium text-amber-900 mb-2">⚠ Contradictions Flagged</h3>
              {dna.contradictions_flagged.map((c: any, i: number) => (
                <p key={i} className="text-sm text-amber-800">{c.description || JSON.stringify(c)}</p>
              ))}
              <p className="text-xs text-amber-600 mt-2">LogoMind surfaces contradictions; the designer resolves them.</p>
            </div>
          )}

          <div className="pt-4">
            <button
              onClick={handleProceed}
              disabled={running}
              className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
            >
              {running ? "Generating Insight…" : "Continue to Insight →"}
            </button>
          </div>
        </>
      ) : (
        <p className="text-gray-500">Brand DNA not yet generated. (Strategy Engine should have run.)</p>
      )}
    </div>
  );
}

function DNACard({ label, value, confidence, sub }: { label: string; value: string; confidence?: string; sub?: string }) {
  const confidenceEmoji: Record<string, string> = { C5: "🟢", C4: "🔵", C3: "🟠", C2: "🟣", C1: "⚪" };
  return (
    <div className="p-4 bg-white border border-gray-200 rounded-lg">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">{label}</span>
        {confidence && (
          <span className="text-xs text-gray-400">{confidenceEmoji[confidence] || ""} {confidence}</span>
        )}
      </div>
      <p className="text-gray-900">{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
    </div>
  );
}
