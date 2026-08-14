/**
 * LogoMind API Client.
 *
 * Thin wrapper around fetch for the LogoMind backend.
 * One function per pipeline stage (PROD-JOURNEY-001).
 */

// Same-origin by default: requests go to "/api/..." and are proxied to the
// FastAPI backend by next.config.js rewrites (server-side, so this works even
// inside sandboxed browsers whose loopback can't reach the backend host).
// Set NEXT_PUBLIC_API_BASE to an absolute URL to bypass the proxy (direct
// cross-origin calls) for deployments that prefer it.
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "/api";

// ─── Types ────────────────────────────────────────────────────────────

export interface ProjectSummary {
  id: number;
  company_name: string;
  industry: string;
  stage: string;
  brand_confidence_score: number;
  created_at: string;
  updated_at: string;
}

export interface Project extends ProjectSummary {
  client_brief: string;
  client_contact?: string;
  brand_confidence_level: string;
  discovery_summary?: any;
  brand_dna?: any;
  insight_report?: any;
  concept_families?: any[];
  judge_report?: any;
  concept_prompts?: any[];
  ssb?: any;
  presentation?: any;
  client_persona?: any;
  appeal_report?: any;
  contest_brief?: any;
  contest_feedback?: any[];
  workshop_state?: any;
  sketches?: any[];
}

export interface BriefAnalysisResult {
  brand_confidence_score: number;
  brand_confidence_level: string;
  recommended_mode: string;
  discovery_summary: string;
  missing_info: Array<{ field: string; impact: string; suggested_question?: string }>;
  next_action: string;
}

// ─── API Functions ────────────────────────────────────────────────────

// A structured stage error from the backend's @with_stage_error wrapper.
// When the backend returns HTTP 503 with this shape, apiCall throws a
// StageApiError carrying it, so views can present a polished message + Retry
// instead of a raw "Internal Server Error".
export interface StageErrorPayload {
  stage: string;
  stage_name: string;
  kind: "transient" | "validation";
  detail: string; // human-readable explanation
  retryable: boolean;
  technical?: string;
  estimate?: [number, number]; // [minSeconds, maxSeconds] typical wall-clock
}

export class StageApiError extends Error {
  payload: StageErrorPayload;
  status: number;
  constructor(payload: StageErrorPayload, status: number) {
    // Keep .message backward-compatible for any caller that still reads it.
    super(payload.detail);
    this.payload = payload;
    this.status = status;
  }
}

async function apiCall<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: response.statusText }));
    const detail = body?.detail;
    // Structured stage error (from @with_stage_error): present it richly.
    if (detail && typeof detail === "object" && detail.stage && detail.detail) {
      throw new StageApiError(detail as StageErrorPayload, response.status);
    }
    // Plain HTTPException detail (guard failures, 4xx): a simple string.
    throw new Error(typeof detail === "string" ? detail : `API error: ${response.status}`);
  }
  return response.json();
}


// Projects
export const listProjects = () => apiCall<ProjectSummary[]>("/projects");
export const getProject = (id: number) => apiCall<Project>(`/projects/${id}`);
export const createProject = (data: { company_name: string; industry: string; client_brief: string; client_contact?: string }) =>
  apiCall<Project>("/projects", { method: "POST", body: JSON.stringify(data) });
export const deleteProject = (id: number) =>
  apiCall<void>(`/projects/${id}`, { method: "DELETE" });

// Stage 2: Discovery
export const analyseBrief = (projectId: number) =>
  apiCall<BriefAnalysisResult>(`/projects/${projectId}/analyse`, { method: "POST" });

// Stage 3: Workshop
export const generateWorkshopLink = (projectId: number) =>
  apiCall<{ share_token: string; url: string }>(`/projects/${projectId}/workshop/share`, { method: "POST" });

export const completeWorkshop = (projectId: number) =>
  apiCall<Project>(`/projects/${projectId}/workshop/complete`, { method: "POST" });

export const submitWorkshopAnswer = (
  projectId: number,
  data: { stage: number; question_id: string; answer: string; answer_type?: string }
) =>
  apiCall<any>(`/projects/${projectId}/workshop/answer`, { method: "POST", body: JSON.stringify(data) });

// Stage 4: Strategy
export const runStrategy = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/strategy`, { method: "POST" });

// Stage 5: Insight
export const runInsight = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/insight`, { method: "POST" });

// Stage 6: Create
export const runCreate = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/create`, { method: "POST" });

// Stage 7: Judge
export const runJudge = (projectId: number) =>
  apiCall<any[]>(`/projects/${projectId}/judge`, { method: "POST" });

export const selectFamily = (projectId: number, label: string) =>
  apiCall<any>(`/projects/${projectId}/select-family/${label}`, { method: "POST" });

// Stage: Client Fit (Client Preference Predictor)
export const runClientFit = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/client-fit`, { method: "POST" });

// Stage 4: refine Client Fit with revealed in-contest preferences
export const refineClientFit = (
  projectId: number,
  signals: Array<{ kind: "liked" | "disliked" | "comment"; trait: string; note?: string }>
) =>
  apiCall<any>(`/projects/${projectId}/client-fit/refine`, { method: "POST", body: JSON.stringify({ signals }) });

// Stage 3: Contest Brief Decoder
export const decodeContestBrief = (rawText: string) =>
  apiCall<any>(`/decode-contest-brief`, { method: "POST", body: JSON.stringify({ raw_text: rawText }) });

export const attachContestBrief = (projectId: number, rawText: string) =>
  apiCall<Project>(`/projects/${projectId}/contest-brief`, { method: "POST", body: JSON.stringify({ raw_text: rawText }) });

// Intent Extraction utility (LOG-DISC-001) — "I want blue" -> "I want trust".
export const decodeIntent = (preference: string) =>
  apiCall<{ preference: string; intent: string; reasoning: string }>(`/decode-intent`, {
    method: "POST",
    body: JSON.stringify({ preference }),
  });

// Stage: Concept Prompt
export const composeConceptPrompts = (projectId: number) =>
  apiCall<any[]>(`/projects/${projectId}/concept-prompts`, { method: "POST" });

// Stage 8: SSB + Sketch
export const composeSSB = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/ssb`, { method: "POST" });

export const uploadSketch = (projectId: number, data: { description?: string; design_intent?: string; linked_concept_family?: string; image_url?: string }) =>
  apiCall<any>(`/projects/${projectId}/sketches`, { method: "POST", body: JSON.stringify(data) });

// Stage 9: Presentation
export const buildPresentation = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/presentation`, { method: "POST" });
