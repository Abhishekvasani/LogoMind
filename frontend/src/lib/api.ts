/**
 * LogoMind API Client.
 *
 * Thin wrapper around fetch for the LogoMind backend.
 * One function per pipeline stage (PROD-JOURNEY-001).
 */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

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
  ssb?: any;
  presentation?: any;
  workshop_state?: any;
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

async function apiCall<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `API error: ${response.status}`);
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

// Stage 4: Strategy
export const runStrategy = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/strategy`, { method: "POST" });

// Stage 5: Insight
export const runInsight = (projectId: number) =>
  apiCall<any>(`projects/${projectId}/insight`, { method: "POST" });

// Stage 6: Create
export const runCreate = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/create`, { method: "POST" });

// Stage 7: Judge
export const runJudge = (projectId: number) =>
  apiCall<any[]>(`/projects/${projectId}/judge`, { method: "POST" });

export const selectFamily = (projectId: number, label: string) =>
  apiCall<any>(`/projects/${projectId}/select-family/${label}`, { method: "POST" });

// Stage 8: SSB + Sketch
export const composeSSB = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/ssb`, { method: "POST" });

export const uploadSketch = (projectId: number, data: { description?: string; design_intent?: string; linked_concept_family?: string; image_url?: string }) =>
  apiCall<any>(`/projects/${projectId}/sketches`, { method: "POST", body: JSON.stringify(data) });

// Stage 9: Presentation
export const buildPresentation = (projectId: number) =>
  apiCall<any>(`/projects/${projectId}/presentation`, { method: "POST" });
