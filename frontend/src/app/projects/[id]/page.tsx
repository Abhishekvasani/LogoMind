"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Project, getProject } from "@/lib/api";
import { StrategyView } from "@/components/StrategyView";
import { InsightView } from "@/components/InsightView";
import { ConceptFamiliesView } from "@/components/ConceptFamiliesView";
import { ConceptPromptView } from "@/components/ConceptPromptView";
import { SSBView } from "@/components/SSBView";
import { WorkshopView } from "@/components/WorkshopView";
import { PresentationView } from "@/components/PresentationView";
import { runStrategy as runStrategyApi, generateWorkshopLink } from "@/lib/api";

const STAGE_ORDER = ["entry", "discovery", "workshop", "strategy", "insight", "create", "judge", "concept_prompt", "ssb", "sketch", "presentation", "complete"];

const STAGE_LABELS: Record<string, string> = {
  entry: "Brief",
  discovery: "Discovery",
  workshop: "Workshop",
  strategy: "Strategy",
  insight: "Insight",
  create: "Create",
  judge: "Judge",
  concept_prompt: "Concept",
  ssb: "SSB",
  sketch: "Sketch",
  presentation: "Presentation",
  complete: "Complete",
};

export default function ProjectPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = Number(params.id);

  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // viewStage lets the user click a reached stage pill to review/modify it.
  // null = follow the project's real current stage.
  const [viewStage, setViewStage] = useState<string | null>(null);

  const loadProject = () => {
    getProject(projectId)
      .then(setProject)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  // After a stage action advances the project, drop the manual override so the
  // workspace follows the real current stage.
  const handleUpdate = () => {
    setViewStage(null);
    loadProject();
  };

  useEffect(() => {
    loadProject();
  }, [projectId]);

  if (loading) return <p className="text-gray-500">Loading project…</p>;
  if (error) return <div className="p-4 bg-red-50 rounded text-red-700">{error}</div>;
  if (!project) return <p>Project not found.</p>;

  const currentStageIndex = STAGE_ORDER.indexOf(project.stage);
  // The stage currently displayed: manual override (a reached stage the user
  // clicked) or the project's real current stage.
  const activeStage = viewStage ?? project.stage;
  const activeStageIndex = STAGE_ORDER.indexOf(activeStage);

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Link href="/" className="text-gray-400 hover:text-gray-600">← Dashboard</Link>
          <h1 className="text-xl font-semibold">{project.company_name}</h1>
          <span className="text-sm text-gray-400">{project.industry}</span>
        </div>
      </div>

      {/* Stage progress bar — each reached stage is clickable to jump back to it. */}
      <div className="flex items-center gap-1 mb-8 overflow-x-auto pb-2">
        {STAGE_ORDER.map((stage, idx) => {
          const reached = idx <= currentStageIndex;
          const isActive = stage === activeStage;
          const classNames = `px-3 py-1 text-xs rounded-full whitespace-nowrap ${
            isActive
              ? "bg-gray-900 text-white ring-2 ring-gray-900 ring-offset-1"
              : reached
                ? "bg-gray-900 text-white hover:bg-gray-700 cursor-pointer"
                : "bg-gray-100 text-gray-400"
          }`;
          if (reached) {
            return (
              <div key={stage} className="flex items-center">
                <button
                  type="button"
                  onClick={() => setViewStage(stage)}
                  aria-current={isActive ? "step" : undefined}
                  className={classNames}
                >
                  {STAGE_LABELS[stage]}
                </button>
                {idx < STAGE_ORDER.length - 1 && <div className="w-4 h-px bg-gray-200" />}
              </div>
            );
          }
          return (
            <div key={stage} className="flex items-center">
              <span className={classNames} aria-disabled="true">
                {STAGE_LABELS[stage]}
              </span>
              {idx < STAGE_ORDER.length - 1 && <div className="w-4 h-px bg-gray-200" />}
            </div>
          );
        })}
      </div>

      {/* Stage content */}
      <ProjectStageContent project={project} stage={activeStage} onUpdate={handleUpdate} />
    </div>
  );
}

function ProjectStageContent({
  project,
  stage,
  onUpdate,
}: {
  project: Project;
  stage: string;
  onUpdate: () => void;
}) {
  switch (stage) {
    case "entry":
    case "discovery":
      return <DiscoveryStage project={project} onUpdate={onUpdate} />;
    case "workshop":
      return <WorkshopView project={project} onUpdate={onUpdate} />;
    case "strategy":
      return <StrategyView project={project} onUpdate={onUpdate} />;
    case "insight":
      return <InsightView project={project} onUpdate={onUpdate} />;
    case "create":
    case "judge":
      return <ConceptFamiliesView project={project} onUpdate={onUpdate} />;
    case "concept_prompt":
      return <ConceptPromptView project={project} onUpdate={onUpdate} />;
    case "ssb":
    case "sketch":
      return <SSBView project={project} onUpdate={onUpdate} />;
    case "presentation":
    case "complete":
      return <PresentationView project={project} onUpdate={onUpdate} />;
    default:
      return <p className="text-gray-500">Unknown stage: {stage}</p>;
  }
}

function DiscoveryStage({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const discovery = project.discovery_summary;
  const score = project.brand_confidence_score;
  const level = project.brand_confidence_level;
  const [proceeding, setProceeding] = useState(false);
  const [startingWorkshop, setStartingWorkshop] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleProceed = async () => {
    setProceeding(true);
    setError(null);
    try {
      await runStrategyApi(project.id);
      onUpdate(); // reload — project.stage will now be "strategy"
    } catch (e: any) {
      setError(e.message);
    } finally {
      setProceeding(false);
    }
  };

  const handleStartWorkshop = async () => {
    // generateWorkshopLink flips the project to the "workshop" stage, which
    // routes the workspace into WorkshopView (the designer-facing workshop).
    setStartingWorkshop(true);
    setError(null);
    try {
      await generateWorkshopLink(project.id);
      onUpdate(); // reload — project.stage will now be "workshop"
    } catch (e: any) {
      setError(e.message);
    } finally {
      setStartingWorkshop(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="p-6 bg-white border border-gray-200 rounded-lg">
        <h2 className="text-lg font-medium mb-4">Brief Analysis</h2>

        {score > 0 ? (
          <>
            <div className="mb-4">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm text-gray-500">Brand Confidence Score</span>
                <span className="text-sm font-medium">
                  {score.toFixed(0)}% — <span className="capitalize">{level}</span>
                </span>
              </div>
              <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${
                    score >= 90 ? "bg-green-500" : score >= 60 ? "bg-yellow-500" : "bg-red-400"
                  }`}
                  style={{ width: `${score}%` }}
                />
              </div>
            </div>

            {discovery?.discovery_summary && (
              <p className="text-gray-700 mb-4">{discovery.discovery_summary}</p>
            )}

            {discovery?.missing_info?.length > 0 && (
              <div className="mb-4">
                <h3 className="text-sm font-medium mb-2">Missing Information</h3>
                <ul className="space-y-2">
                  {discovery.missing_info.map((info: any, i: number) => (
                    <li key={i} className="text-sm bg-gray-50 p-3 rounded">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`text-xs px-2 py-0.5 rounded ${
                          info.impact === "high" ? "bg-red-100 text-red-700" : "bg-gray-200 text-gray-600"
                        }`}>
                          {info.impact}
                        </span>
                        <span className="font-medium">{info.field}</span>
                      </div>
                      {info.suggested_question && (
                        <p className="text-gray-600 italic">{info.suggested_question}</p>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex flex-col gap-3 pt-2 border-t border-gray-100">
              {score >= 70 ? (
                <button
                  onClick={handleProceed}
                  disabled={proceeding}
                  className="self-start px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
                >
                  {proceeding ? "Generating Brand DNA…" : "Proceed to Strategy →"}
                </button>
              ) : (
                <div className="flex flex-col gap-2">
                  <p className="text-sm text-gray-500">
                    Brand Confidence is below 70%. Run the Discovery Workshop to fill the gaps
                    before generating Brand DNA.
                  </p>
                  <button
                    onClick={handleStartWorkshop}
                    disabled={startingWorkshop}
                    className="self-start px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
                  >
                    {startingWorkshop ? "Starting…" : "Start Discovery Workshop →"}
                  </button>
                </div>
              )}

              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-700">
                  {error}
                </div>
              )}
            </div>
          </>
        ) : (
          <p className="text-gray-500">Brief not yet analysed.</p>
        )}
      </div>
    </div>
  );
}

