"use client";

import { Project, runCreate } from "@/lib/api";
import { useStageAction } from "@/lib/useStageAction";
import { StageStatus } from "@/components/StageStatus";

export function InsightView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const report = project.insight_report;

  const handleProceed = () => run(() => runCreate(project.id), "create");

  if (!report) return <p className="text-gray-500">Insight report not generated.</p>;

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-medium">Insight Report — {project.industry}</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Clichés */}
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <h3 className="font-medium text-red-900 mb-2">Clichés to Avoid</h3>
          {report.cliche_avoidance?.length > 0 ? (
            <ul className="space-y-2">
              {report.cliche_avoidance.map((c: any, i: number) => (
                <li key={i} className="text-sm">
                  <span className="font-medium">{c.symbol}</span>
                  <span className="text-red-700"> — {c.why_cliche}</span>
                  {c.alternatives?.length > 0 && (
                    <span className="text-gray-500"> Alternatives: {c.alternatives.join(", ")}</span>
                  )}
                </li>
              ))}
            </ul>
          ) : <p className="text-sm text-gray-500">No major clichés identified.</p>}
        </div>

        {/* Opportunities */}
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="font-medium text-green-900 mb-2">Opportunities (White Space)</h3>
          {report.opportunities?.length > 0 ? (
            <ul className="space-y-1">
              {report.opportunities.map((o: string, i: number) => (
                <li key={i} className="text-sm text-green-800">· {o}</li>
              ))}
            </ul>
          ) : <p className="text-sm text-gray-500">None identified.</p>}
        </div>
      </div>

      {/* Trend Intelligence */}
      {report.trend_intelligence?.length > 0 && (
        <div className="p-4 bg-white border border-gray-200 rounded-lg">
          <h3 className="font-medium mb-2">Trend Intelligence</h3>
          {report.trend_vs_timeless_balance && (
            <div className="mb-3">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>Timeless</span>
                <span>Trend-forward</span>
              </div>
              <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden flex">
                <div className="bg-gray-800" style={{ width: `${report.trend_vs_timeless_balance.timeless * 100}%` }} />
                <div className="bg-blue-400" style={{ width: `${report.trend_vs_timeless_balance.contemporary * 100}%` }} />
              </div>
              <p className="text-xs text-gray-400 mt-1">
                Recommended: {(report.trend_vs_timeless_balance.timeless * 100).toFixed(0)}% timeless / {(report.trend_vs_timeless_balance.contemporary * 100).toFixed(0)}% contemporary
              </p>
            </div>
          )}
          <div className="space-y-1">
            {report.trend_intelligence.map((t: any, i: number) => (
              <div key={i} className="text-sm flex items-center gap-2">
                <span className={`text-xs px-2 py-0.5 rounded ${
                  t.classification === "timeless" ? "bg-gray-800 text-white" :
                  t.classification === "emerging" ? "bg-blue-100 text-blue-700" :
                  t.classification === "short_lived" ? "bg-yellow-100 text-yellow-700" :
                  "bg-red-100 text-red-700"
                }`}>{t.classification}</span>
                <span className="font-medium">{t.name}</span>
                <span className="text-gray-500">— {t.context_assessment}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={handleProceed}
        disabled={running}
        className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
      >
        {running ? "Generating Concept Families…" : "Continue to Create →"}
      </button>

      <StageStatus
        running={running}
        elapsed={elapsed}
        error={error}
        stageName="Concept Families"
        onRetry={retry}
      />
    </div>
  );
}
