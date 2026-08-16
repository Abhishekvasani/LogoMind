"use client";

import { useState } from "react";
import { Project, uploadSketch, uploadSketchImage, buildPresentation } from "@/lib/api";
import { useStageAction } from "@/lib/useStageAction";
import { StageStatus } from "@/components/StageStatus";

export function SSBView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const { run, retry, running, elapsed, error } = useStageAction(onUpdate);
  const [sketchDesc, setSketchDesc] = useState("");
  const [sketchIntent, setSketchIntent] = useState("");
  const [sketchFile, setSketchFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);
  const ssb = project.ssb;
  const sketches = project.sketches || [];

  const pickFile = (file: File | null) => {
    setSketchFile(file);
    if (filePreview) URL.revokeObjectURL(filePreview);
    setFilePreview(file ? URL.createObjectURL(file) : null);
  };

  const handleUpload = () => {
    if (!sketchFile && !sketchDesc.trim()) return;
    const desc = sketchDesc;
    const intent = sketchIntent;
    const file = sketchFile;
    run(async () => {
      if (file) {
        await uploadSketchImage(project.id, file, { description: desc, design_intent: intent });
      } else {
        await uploadSketch(project.id, { description: desc, design_intent: intent });
      }
      setSketchDesc("");
      setSketchIntent("");
      pickFile(null);
    }, "sketch");
  };

  const handlePresentation = () => run(() => buildPresentation(project.id), "presentation");

  if (!ssb) return <p className="text-graphite">SSB not yet composed.</p>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* SSB (left) */}
      <div className="space-y-4">
        <h2 className="text-lg font-medium">Strategic Sketch Brief</h2>

        <Section title="1. Project Essence" content={ssb.project_essence} />

        <Section title="2. Brand DNA Snapshot">
          <dl className="space-y-1.5 text-sm">
            <SnapRow label="Purpose" value={ssb.brand_dna_snapshot?.purpose} />
            <SnapRow label="Positioning" value={ssb.brand_dna_snapshot?.positioning} />
            <SnapRow label="Differentiation" value={ssb.brand_dna_snapshot?.differentiation} />
            <SnapRow label="Personality" value={ssb.brand_dna_snapshot?.personality} />
            <SnapRow label="Archetype" value={ssb.brand_dna_snapshot?.archetype} />
            <SnapRow label="Emotional Goal" value={ssb.brand_dna_snapshot?.emotional_goal} />
          </dl>
        </Section>

        <div className="p-4 bg-ink text-stock rounded-lg">
          <p className="text-xs uppercase tracking-wide text-graphite mb-1">3. Creative North Star</p>
          <p className="font-medium">{ssb.creative_north_star}</p>
        </div>

        {/* 4. Selected Territory */}
        {ssb.selected_territory ? (
          <Section title="4. Selected Territory">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-medium text-sm">Family {ssb.selected_territory.family_label} — {ssb.selected_territory.theme}</span>
                  {ssb.selected_territory.core_meaning_served && (
                    <p className="text-xs text-graphite mt-0.5">Serves: {ssb.selected_territory.core_meaning_served}</p>
                  )}
                </div>
                {ssb.selected_territory.composite != null && (
                  <span className="text-xs px-2 py-1 rounded bg-accent/20 text-accent">
                    {typeof ssb.selected_territory.composite === 'number' ? ssb.selected_territory.composite.toFixed(1) : ssb.selected_territory.composite}
                    {ssb.selected_territory.classification ? ` — ${ssb.selected_territory.classification}` : ''}
                  </span>
                )}
              </div>
              {ssb.selected_territory.visual_language && Object.keys(ssb.selected_territory.visual_language).length > 0 && (
                <div className="grid grid-cols-2 gap-2 text-xs">
                  {Object.entries(ssb.selected_territory.visual_language).map(([k, v]) => (
                    <div key={k} className="bg-surface-2 p-2 rounded">
                      <p className="font-medium text-graphite uppercase">{k}</p>
                      <p className="text-ink/90">{v as string}</p>
                    </div>
                  ))}
                </div>
              )}
              {ssb.selected_territory.symbols?.length > 0 && (
                <div>
                  <p className="text-xs font-medium text-graphite mb-1">SYMBOLS</p>
                  <div className="flex flex-wrap gap-1">
                    {ssb.selected_territory.symbols.map((s: any, i: number) => (
                      <span key={i} className="text-xs px-2 py-0.5 bg-surface-2 rounded">
                        {s.name} <span className="text-graphite">({s.meaning})</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {ssb.selected_territory.why_it_works && (
                <p className="text-sm text-graphite italic">{ssb.selected_territory.why_it_works}</p>
              )}
              {ssb.selected_territory.pitfalls && (
                <p className="text-xs text-warn">⚠ {ssb.selected_territory.pitfalls}</p>
              )}
              {ssb.selected_territory.refinement_recommendations?.length > 0 && (
                <div className="pt-2 border-t border-rule">
                  <p className="text-xs font-medium text-graphite mb-1">Refinement:</p>
                  <ul className="text-xs text-graphite space-y-0.5">
                    {ssb.selected_territory.refinement_recommendations.map((r: string, i: number) => <li key={i}>· {r}</li>)}
                  </ul>
                </div>
              )}
            </div>
          </Section>
        ) : (
          <Section title="4. Creative Territories">
            <div className="space-y-1">
              {(ssb.creative_territories || []).map((t: any, i: number) => (
                <p key={i} className="text-sm text-graphite">
                  Family {t.family_label} — {t.theme}
                  <span className="text-xs text-graphite/80 ml-2">({t.recommendation})</span>
                </p>
              ))}
            </div>
          </Section>
        )}

        <Section title="5. Opportunities & Warnings">
          <div className="space-y-2">
            {ssb.opportunities_and_warnings?.explore?.length > 0 && (
              <div>
                <p className="text-xs text-ok font-medium">EXPLORE:</p>
                <ul className="text-sm">{ssb.opportunities_and_warnings.explore.map((o: string, i: number) => <li key={i}>· {o}</li>)}</ul>
              </div>
            )}
            {ssb.opportunities_and_warnings?.avoid?.length > 0 && (
              <div>
                <p className="text-xs text-bad font-medium">AVOID:</p>
                <ul className="text-sm">{ssb.opportunities_and_warnings.avoid.map((a: string, i: number) => <li key={i}>· {a}</li>)}</ul>
              </div>
            )}
          </div>
        </Section>

        {/* 6. Creative Council Advice */}
        {ssb.council_advice ? (
          <Section title="6. Creative Council Advice">
            {ssb.council_advice.synthesised_verdict && (
              <p className="text-sm font-medium text-ink mb-2 p-2 bg-surface-2 rounded">{ssb.council_advice.synthesised_verdict}</p>
            )}
            <dl className="space-y-1 text-xs">
              {['meaning_mind','simplicity_mind','differentiation_mind','context_mind','memorability_mind','systems_mind','emotion_mind','longevity_mind','boldness_mind']
                .filter((m) => (ssb.council_advice as any)[m])
                .map((m) => (
                  <div key={m} className="flex gap-2">
                    <dt className="text-graphite capitalize w-36 flex-shrink-0">{m.replace(/_mind$/, '').replace(/_/g, ' ')}:</dt>
                    <dd className="text-ink/90">{(ssb.council_advice as any)[m]}</dd>
                  </div>
                ))}
            </dl>
          </Section>
        ) : null}

        {ssb.sketch_missions?.length > 0 && (
          <Section title="7. Sketch Missions">
            <div className="space-y-3">
              {ssb.sketch_missions.map((m: any, i: number) => {
                const chosenSymbols = (ssb.selected_territory?.symbols || []).map((s: any) => s.name);
                return (
                <div key={i} className="p-3 border border-rule rounded">
                  <p className="font-medium text-sm">Mission {i + 1}: {m.mission_name}</p>
                  <p className="text-sm text-graphite mt-1">{m.core_idea}</p>
                  {m.combine?.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {m.combine.map((c: string, j: number) => (
                        <span key={j} className={`text-xs px-1.5 py-0.5 rounded ${
                          chosenSymbols.includes(c) ? 'bg-info/20 text-info' : 'bg-surface-2 text-graphite'
                        }`}>{c}</span>
                      ))}
                    </div>
                  )}
                  {m.why_it_works && <p className="text-xs text-graphite mt-2 italic">{m.why_it_works}</p>}
                  {m.potential_pitfalls?.length > 0 && (
                    <ul className="text-xs text-bad mt-1">
                      {m.potential_pitfalls.map((p: string, j: number) => <li key={j}>· {p}</li>)}
                    </ul>
                  )}
                  {m.start_with && (
                    <p className="text-xs text-ink/90 mt-2 bg-surface-2 p-2 rounded">▸ {m.start_with}</p>
                  )}
                </div>
                );
              })}
            </div>
          </Section>
        )}

        <button
          onClick={handlePresentation}
          disabled={running}
          className="px-4 py-2 bg-ink text-stock rounded-md hover:bg-ink/85 disabled:opacity-50"
        >
          {running ? "Building…" : "Request Presentation →"}
        </button>
      </div>

      {/* Sketch workspace (right) */}
      <div className="space-y-4">
        <h2 className="text-lg font-medium">Sketch Workspace</h2>

        <div className="p-4 border border-rule rounded-lg bg-stock">
          <label className="block text-sm font-medium mb-1">Upload Sketch</label>
          {filePreview && (
            <div className="mb-2 relative">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={filePreview} alt="Sketch preview" className="w-full rounded border border-rule bg-paper" />
              <button
                onClick={() => pickFile(null)}
                className="absolute top-2 right-2 px-2 py-0.5 text-xs bg-ink/80 text-stock rounded"
              >
                Remove
              </button>
            </div>
          )}
          <input
            type="file"
            accept="image/png,image/jpeg,image/webp,image/gif,image/svg+xml"
            onChange={(e) => pickFile(e.target.files?.[0] ?? null)}
            className="w-full text-sm text-graphite file:mr-3 file:px-3 file:py-1.5 file:border file:border-rule file:rounded file:text-sm file:text-ink file:bg-surface-2 file:cursor-pointer mb-2"
          />
          <textarea
            value={sketchDesc}
            onChange={(e) => setSketchDesc(e.target.value)}
            placeholder="Describe your sketch (required without an image)…"
            className="w-full p-2 border border-rule rounded text-sm mb-2 min-h-[80px] bg-paper text-ink focus:outline-none focus:border-ink/40"
          />
          <input
            value={sketchIntent}
            onChange={(e) => setSketchIntent(e.target.value)}
            placeholder="Design intent (optional)"
            className="w-full p-2 border border-rule rounded text-sm mb-2 bg-paper text-ink focus:outline-none focus:border-ink/40"
          />
          <button
            onClick={handleUpload}
            disabled={running || (!sketchFile && !sketchDesc.trim())}
            className="px-3 py-1.5 bg-surface-2 rounded text-sm text-ink hover:bg-ink/15 disabled:opacity-50"
          >
            Submit for Coach Feedback
          </button>
        </div>

        {sketches.length > 0 && (
          <div className="space-y-3 mt-4">
            <p className="text-xs font-medium text-graphite uppercase tracking-wide">
              Coach Feedback ({sketches.length})
            </p>
            {sketches.map((sketch: any) => (
              <div key={sketch.id} className="p-3 border border-rule rounded bg-stock">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-graphite">Sketch {sketch.sketch_number}</span>
                  {sketch.coach_confidence && (
                    <span className="text-xs text-graphite">{sketch.coach_confidence}</span>
                  )}
                </div>
                {sketch.image_url && (
                  /* eslint-disable-next-line @next/next/no-img-element */
                  <img src={sketch.image_url} alt={`Sketch ${sketch.sketch_number}`} className="w-full rounded border border-rule mb-2 bg-paper" />
                )}
                {sketch.description && (
                  <p className="text-sm text-graphite mb-2">"{sketch.description}"</p>
                )}
                {sketch.coach_feedback && (
                  <div className="space-y-2">
                    <p className="text-sm text-ink">{sketch.coach_feedback.assessment}</p>
                    {sketch.coach_feedback.suggestions?.length > 0 && (
                      <div>
                        <p className="text-xs font-medium text-graphite">Suggestions:</p>
                        <ul className="text-sm text-graphite">
                          {sketch.coach_feedback.suggestions.map((s: string, i: number) => (
                            <li key={i}>· {s}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {sketch.coach_feedback.pitfalls_to_watch?.length > 0 && (
                      <div>
                        <p className="text-xs font-medium text-bad">Pitfalls to watch:</p>
                        <ul className="text-sm text-graphite">
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
    <div className="p-4 bg-stock border border-rule rounded-lg">
      <p className="text-xs font-medium text-graphite uppercase tracking-wide mb-2">{title}</p>
      {content && <p className="text-sm text-ink/90">{content}</p>}
      {children}
    </div>
  );
}

function SnapRow({ label, value }: { label: string; value?: string }) {
  if (!value) return null;
  return (
    <div className="flex gap-2">
      <dt className="text-graphite w-28 flex-shrink-0">{label}:</dt>
      <dd className="text-ink/90">{value}</dd>
    </div>
  );
}
