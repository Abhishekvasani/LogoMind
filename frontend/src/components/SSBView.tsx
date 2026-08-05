"use client";

import { useState } from "react";
import { Project, uploadSketch, buildPresentation } from "@/lib/api";
import { useStageAction } from "@/lib/useStageAction";
import { StageStatus } from "@/components/StageStatus";

export function SSBView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const [sketchDesc, setSketchDesc] = useState("");
  const [sketchIntent, setSketchIntent] = useState("");
  const ssb = project.ssb;
  const sketches = project.sketches || [];

  const handleUpload = () => {
    if (!sketchDesc.trim()) return;
    const desc = sketchDesc;
    const intent = sketchIntent;
    run(async () => {
      await uploadSketch(project.id, { description: desc, design_intent: intent });
      setSketchDesc("");
      setSketchIntent("");
    }, "sketch");
  };

  const handlePresentation = () => run(() => buildPresentation(project.id), "presentation");

  if (!ssb) return <p className="text-gray-500">SSB not yet composed.</p>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* SSB (left) */}
      <div className="space-y-4">
        <h2 className="text-lg font-medium">Strategic Sketch Brief</h2>

        <Section title="1. Project Essence" content={ssb.project_essence} />

        <Section title="2. Brand DNA Snapshot">
          <pre className="text-xs bg-gray-50 p-3 rounded overflow-auto max-h-40">
            {JSON.stringify(ssb.brand_dna_snapshot, null, 2)}
          </pre>
        </Section>

        <div className="p-4 bg-gray-900 text-white rounded-lg">
          <p className="text-xs uppercase tracking-wide text-gray-400 mb-1">3. Creative North Star</p>
          <p className="font-medium">{ssb.creative_north_star}</p>
        </div>

        <Section title="5. Opportunities & Warnings">
          <div className="space-y-2">
            {ssb.opportunities_and_warnings?.explore?.length > 0 && (
              <div>
                <p className="text-xs text-green-600 font-medium">EXPLORE:</p>
                <ul className="text-sm">{ssb.opportunities_and_warnings.explore.map((o: string, i: number) => <li key={i}>· {o}</li>)}</ul>
              </div>
            )}
            {ssb.opportunities_and_warnings?.avoid?.length > 0 && (
              <div>
                <p className="text-xs text-red-600 font-medium">AVOID:</p>
                <ul className="text-sm">{ssb.opportunities_and_warnings.avoid.map((a: string, i: number) => <li key={i}>· {a}</li>)}</ul>
              </div>
            )}
          </div>
        </Section>

        {ssb.sketch_missions?.length > 0 && (
          <Section title="7. Sketch Missions">
            <div className="space-y-3">
              {ssb.sketch_missions.map((m: any, i: number) => (
                <div key={i} className="p-3 border border-gray-200 rounded">
                  <p className="font-medium text-sm">Mission {i + 1}: {m.mission_name}</p>
                  <p className="text-sm text-gray-600 mt-1">{m.core_idea}</p>
                  <p className="text-xs text-gray-500 mt-1 italic">Start with: {m.start_with}</p>
                </div>
              ))}
            </div>
          </Section>
        )}

        <button
          onClick={handlePresentation}
          disabled={running}
          className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
        >
          {running ? "Building…" : "Request Presentation →"}
        </button>
      </div>

      {/* Sketch workspace (right) */}
      <div className="space-y-4">
        <h2 className="text-lg font-medium">Sketch Workspace</h2>

        <div className="p-4 border border-gray-200 rounded-lg bg-white">
          <label className="block text-sm font-medium mb-1">Upload Sketch (describe)</label>
          <textarea
            value={sketchDesc}
            onChange={(e) => setSketchDesc(e.target.value)}
            placeholder="Describe your sketch…"
            className="w-full p-2 border border-gray-300 rounded text-sm mb-2 min-h-[80px]"
          />
          <input
            value={sketchIntent}
            onChange={(e) => setSketchIntent(e.target.value)}
            placeholder="Design intent (optional)"
            className="w-full p-2 border border-gray-300 rounded text-sm mb-2"
          />
          <button
            onClick={handleUpload}
            disabled={running || !sketchDesc.trim()}
            className="px-3 py-1.5 bg-gray-100 rounded text-sm hover:bg-gray-200 disabled:opacity-50"
          >
            Submit for Coach Feedback
          </button>
        </div>

        {sketches.length > 0 && (
          <div className="space-y-3 mt-4">
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
              Coach Feedback ({sketches.length})
            </p>
            {sketches.map((sketch: any) => (
              <div key={sketch.id} className="p-3 border border-gray-200 rounded bg-white">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-gray-400">Sketch {sketch.sketch_number}</span>
                  {sketch.coach_confidence && (
                    <span className="text-xs text-gray-400">{sketch.coach_confidence}</span>
                  )}
                </div>
                {sketch.description && (
                  <p className="text-sm text-gray-600 mb-2">"{sketch.description}"</p>
                )}
                {sketch.coach_feedback && (
                  <div className="space-y-2">
                    <p className="text-sm text-gray-800">{sketch.coach_feedback.assessment}</p>
                    {sketch.coach_feedback.suggestions?.length > 0 && (
                      <div>
                        <p className="text-xs font-medium text-gray-500">Suggestions:</p>
                        <ul className="text-sm text-gray-600">
                          {sketch.coach_feedback.suggestions.map((s: string, i: number) => (
                            <li key={i}>· {s}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {sketch.coach_feedback.pitfalls_to_watch?.length > 0 && (
                      <div>
                        <p className="text-xs font-medium text-red-500">Pitfalls to watch:</p>
                        <ul className="text-sm text-gray-600">
                          {sketch.coach_feedback.pitfalls_to_watch.map((p: string, i: number) => (
                            <li key={i}>· {p}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="md:col-span-2">
        <StageStatus
          running={running}
          elapsed={elapsed}
          error={error}
          stageName={error?.stage_name ?? "Stage"}
          onRetry={retry}
        />
      </div>
    </div>
  );
}

function Section({ title, content, children }: { title: string; content?: string; children?: React.ReactNode }) {
  return (
    <div className="p-4 bg-white border border-gray-200 rounded-lg">
      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">{title}</p>
      {content && <p className="text-sm text-gray-700">{content}</p>}
      {children}
    </div>
  );
}
