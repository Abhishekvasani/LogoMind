"use client";

import { Project, runJudge, selectFamily, composeSSB } from "@/lib/api";
import { useStageAction } from "@/lib/useStageAction";
import { StageStatus } from "@/components/StageStatus";

export function ConceptFamiliesView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const families = project.concept_families || [];
  const judgeData = project.judge_report || [];

  const handleJudge = () => run(() => runJudge(project.id), "judge");
  const handleSelect = (label: string) => run(() => selectFamily(project.id, label), "judge");
  const handleComposeSSB = () => run(() => composeSSB(project.id), "ssb");

  // The stage name shown in the status depends on which action is in flight.
  const stageName = error?.stage_name ?? (running ? "Judge" : "Concept Families");

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-medium">Concept Families</h2>
        {project.stage === "create" && (
          <button onClick={handleJudge} disabled={running}
            className="px-3 py-1.5 bg-gray-900 text-white text-sm rounded hover:bg-gray-700 disabled:opacity-50">
            {running ? "Evaluating…" : "Evaluate All →"}
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {families.map((family: any) => {
          const judgment = judgeData.find((j: any) => j.family_label === family.family_label);
          return (
            <div key={family.family_label} className={`p-5 border rounded-lg ${
              judgment?.classification === "recommended" ? "border-green-300 bg-green-50/30" :
              judgment?.classification === "reject" ? "border-red-200 bg-red-50/20" :
              "border-gray-200 bg-white"
            }`}>
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-medium">Family {family.family_label} — {family.theme}</h3>
                {judgment && (
                  <span className={`text-xs px-2 py-1 rounded ${
                    judgment.classification === "recommended" ? "bg-green-200 text-green-800" :
                    judgment.classification === "develop" ? "bg-yellow-100 text-yellow-700" :
                    "bg-red-100 text-red-700"
                  }`}>
                    {judgment.composite?.toFixed(1)} — {judgment.classification}
                  </span>
                )}
              </div>

              <p className="text-sm text-gray-600 mb-2">{family.core_meaning_served}</p>

              {family.symbols?.length > 0 && (
                <div className="mb-2">
                  <p className="text-xs text-gray-400 uppercase mb-1">Symbols</p>
                  <div className="flex flex-wrap gap-1">
                    {family.symbols.map((s: any, i: number) => (
                      <span key={i} className="text-xs px-2 py-0.5 bg-gray-100 rounded">
                        {s.name} <span className="text-gray-400">({s.meaning})</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <p className="text-sm text-gray-600 italic mt-2">{family.why_it_works}</p>

              {judgment?.refinement_recommendations?.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <p className="text-xs font-medium text-gray-500 mb-1">Refinement:</p>
                  <ul className="text-xs text-gray-600 space-y-1">
                    {judgment.refinement_recommendations.map((r: string, i: number) => <li key={i}>· {r}</li>)}
                  </ul>
                </div>
              )}

              <button
                onClick={() => handleSelect(family.family_label)}
                className="mt-3 text-xs px-3 py-1 border border-gray-300 rounded hover:bg-gray-50"
              >
                Select Family {family.family_label}
              </button>
            </div>
          );
        })}
      </div>

      {project.stage === "judge" && (
        <button
          onClick={handleComposeSSB}
          disabled={running}
          className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
        >
          {running ? "Composing SSB…" : "Compose Strategic Sketch Brief →"}
        </button>
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
