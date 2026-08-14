"use client";

import { Project } from "@/lib/api";

export function PresentationView({ project }: { project: Project; onUpdate: () => void }) {
  const presentation = project.presentation;

  if (!presentation) {
    return <p className="text-graphite">Presentation not yet built.</p>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-medium">Client Presentation — {project.company_name}</h2>
        <div className="flex gap-2">
          <button
            onClick={() => window.print()}
            className="px-3 py-1.5 text-sm border border-rule rounded hover:bg-surface-2"
          >
            Print / PDF
          </button>
        </div>
      </div>

      {/* Presentation sections */}
      {presentation.sections?.length > 0 ? (
        <div className="space-y-4">
          {presentation.sections.map((section: any, i: number) => (
            <div key={i} className="p-6 bg-stock border border-rule rounded-lg">
              <p className="text-xs text-graphite uppercase tracking-wide mb-2">
                Slide {i + 1} of {presentation.sections.length}
              </p>
              <h3 className="text-lg font-medium mb-2">{section.title}</h3>
              <p className="text-ink/90 whitespace-pre-wrap">{section.content}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-6 bg-stock border border-rule rounded-lg">
          <p className="text-ink/90">{JSON.stringify(presentation, null, 2)}</p>
        </div>
      )}

      {/* Objection Handling (designer-only) */}
      {presentation.objection_handling?.length > 0 && (
        <div className="p-4 bg-warn/10 border border-warn/30 rounded-lg">
          <h3 className="font-medium text-warn mb-2">🎯 Objection-Handling Notes (Designer Only — Not in Export)</h3>
          <div className="space-y-2">
            {presentation.objection_handling.map((o: any, i: number) => (
              <div key={i} className="text-sm">
                <p className="font-medium text-warn">"{o.concern}"</p>
                <p className="text-warn/90 ml-4">→ {o.response}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Project complete */}
      <div className="p-6 bg-ink text-stock rounded-lg text-center">
        <p className="text-lg font-medium mb-1">Project Complete ✓</p>
        <p className="text-graphite text-sm">
          {project.company_name} has moved through the full LOGOS pipeline.
        </p>
        <p className="text-graphite text-xs mt-2 italic">Reason. Create. Refine.</p>
      </div>
    </div>
  );
}
