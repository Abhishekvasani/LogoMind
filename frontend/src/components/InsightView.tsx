"use client";

import { Project, runCreate } from "@/lib/api";
import { useStageAction } from "@/lib/useStageAction";
import { StageStatus } from "@/components/StageStatus";

export function InsightView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const report = project.insight_report;

  const handleProceed = () => run(() => runCreate(project.id), "create");

  if (!report) return <p className="text-graphite">Insight report not generated.</p>;

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-medium">Insight Report — {project.industry}</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Clichés */}
        <div className="p-4 bg-bad/10 border border-bad/30 rounded-lg">
          <h3 className="font-medium text-bad mb-2">Clichés to Avoid</h3>
          {report.cliche_avoidance?.length > 0 ? (
            <ul className="space-y-2">
              {report.cliche_avoidance.map((c: any, i: number) => (
                <li key={i} className="text-sm">
                  <span className="font-medium">{c.symbol}</span>
                  <span className="text-bad/90"> — {c.why_cliche}</span>
                  {c.alternatives?.length > 0 && (
                    <span className="text-graphite"> Alternatives: {c.alternatives.join(", ")}</span>
                  )}
                </li>
              ))}
            </ul>
          ) : <p className="text-sm text-graphite">No major clichés identified.</p>}
        </div>

        {/* Opportunities */}
        <div className="p-4 bg-ok/10 border border-ok/30 rounded-lg">
          <h3 className="font-medium text-ok mb-2">Opportunities (White Space)</h3>
          {report.opportunities?.length > 0 ? (
            <ul className="space-y-1">
              {report.opportunities.map((o: string, i: number) => (
                <li key={i} className="text-sm text-ok/90">· {o}</li>
              ))}
            </ul>
          ) : <p className="text-sm text-graphite">None identified.</p>}
        </div>
      </div>

      {/* Trend Intelligence */}
      {report.trend_intelligence?.length > 0 && (
        <div className="p-4 bg-stock border border-rule rounded-lg">
          <h3 className="font-medium mb-2">Trend Intelligence</h3>
          {report.trend_vs_timeless_balance && (
            <div className="mb-3">
              <div className="flex justify-between text-xs text-graphite mb-1">
                <span>Timeless</span>
                <span>Trend-forward</span>
              </div>
              <div className="w-full h-2 bg-surface-2 rounded-full overflow-hidden flex">
                <div className="bg-ink" style={{ width: `${report.trend_vs_timeless_balance.timeless * 100}%` }} />
                <div className="bg-info" style={{ width: `${report.trend_vs_timeless_balance.contemporary * 100}%` }} />
              </div>
              <p className="text-xs text-graphite mt-1">
                Recommended: {(report.trend_vs_timeless_balance.timeless * 100).toFixed(0)}% timeless / {(report.trend_vs_timeless_balance.contemporary * 100).toFixed(0)}% contemporary
              </p>
            </div>
          )}
          <div className="space-y-1">
            {report.trend_intelligence.map((t: any, i: number) => (
              <div key={i} className="text-sm flex items-center gap-2">
                <span className={`text-xs px-2 py-0.5 rounded ${
                  t.classification === "timeless" ? "bg-ink text-stock" :
                  t.classification === "emerging" ? "bg-info/20 text-info" :
                  t.classification === "short_lived" ? "bg-warn/20 text-warn" :
                  "bg-bad/20 text-bad"
                }`}>{t.classification}</span>
                <span className="font-medium">{t.name}</span>
                <span className="text-graphite">— {t.context_assessment}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={handleProceed}
        disabled={running}
        className="px-4 py-2 bg-ink text-stock rounded-md hover:bg-ink/85 disabled:opacity-50"
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
