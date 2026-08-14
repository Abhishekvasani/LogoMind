"use client";

import { Project, runJudge, selectFamily, composeSSB, runClientFit } from "@/lib/api";
import { useStageAction } from "@/lib/useStageAction";
import { StageStatus } from "@/components/StageStatus";

export function ConceptFamiliesView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const families = project.concept_families || [];
  const judgeData = project.judge_report || [];

  const handleJudge = () => run(() => runJudge(project.id), "judge");
  const handleSelect = (label: string) => run(() => selectFamily(project.id, label), "judge");
  const handleClientFit = () => run(() => runClientFit(project.id), "client_fit");
  const handleComposeSSB = () => run(() => composeSSB(project.id), "ssb");

  // The stage name shown in the status depends on which action is in flight.
  const stageName = error?.stage_name ?? (running ? "Judge" : "Concept Families");

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-medium">Concept Families</h2>
        {project.stage === "create" && (
          <button onClick={handleJudge} disabled={running}
            className="px-3 py-1.5 bg-ink text-stock text-sm rounded hover:bg-ink/85 disabled:opacity-50">
            {running ? "Evaluating…" : "Evaluate All →"}
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {families.map((family: any) => {
          const judgment = judgeData.find((j: any) => j.family_label === family.family_label);
          return (
            <div key={family.family_label} className={`p-5 border rounded-lg ${
              judgment?.classification === "recommended" ? "border-ok/50 bg-ok/10" :
              judgment?.classification === "reject" ? "border-bad/40 bg-bad/10" :
              "border-rule bg-stock"
            }`}>
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-medium">Family {family.family_label} — {family.theme}</h3>
                {judgment && (
                  <span className={`text-xs px-2 py-1 rounded ${
                    judgment.classification === "recommended" ? "bg-ok/25 text-ok" :
                    judgment.classification === "develop" ? "bg-warn/20 text-warn" :
                    "bg-bad/20 text-bad"
                  }`}>
                    {judgment.composite?.toFixed(1)} — {judgment.classification}
                  </span>
                )}
              </div>

              <p className="text-sm text-graphite mb-2">{family.core_meaning_served}</p>

              {family.symbols?.length > 0 && (
                <div className="mb-2">
                  <p className="text-xs text-graphite uppercase mb-1">Symbols</p>
                  <div className="flex flex-wrap gap-1">
                    {family.symbols.map((s: any, i: number) => (
                      <span key={i} className="text-xs px-2 py-0.5 bg-surface-2 rounded">
                        {s.name} <span className="text-graphite">({s.meaning})</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <p className="text-sm text-graphite italic mt-2">{family.why_it_works}</p>

              {judgment?.refinement_recommendations?.length > 0 && (
                <div className="mt-3 pt-3 border-t border-rule">
                  <p className="text-xs font-medium text-graphite mb-1">Refinement:</p>
                  <ul className="text-xs text-graphite space-y-1">
                    {judgment.refinement_recommendations.map((r: string, i: number) => <li key={i}>· {r}</li>)}
                  </ul>
                </div>
              )}

              <button
                onClick={() => handleSelect(family.family_label)}
                className="mt-3 text-xs px-3 py-1 border border-rule rounded hover:bg-surface-2"
              >
                Select Family {family.family_label}
              </button>
            </div>
          );
        })}
      </div>

      {project.stage === "judge" && (
        <div className="flex flex-col gap-3">
          <div className="p-4 border border-accent/40 bg-accent/10 rounded-lg">
            <p className="text-sm text-ink/90 mb-2">
              <span className="font-medium">Next:</span> predict which family THIS client will
              actually pick — then compose concept prompts steered toward their taste.
            </p>
            <button
              onClick={handleClientFit}
              disabled={running}
              className="px-4 py-2 bg-ink text-stock rounded-md hover:bg-ink/85 disabled:opacity-50"
            >
              {running ? "Predicting…" : "Predict Client Appeal →"}
            </button>
          </div>
          <button
            onClick={handleComposeSSB}
            disabled={running}
            className="self-start px-4 py-2 border border-rule text-graphite rounded-md hover:bg-surface-2 disabled:opacity-50 text-sm"
          >
            {running ? "Composing SSB…" : "Skip to Strategic Sketch Brief →"}
          </button>
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
