"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listProjects, ProjectSummary } from "@/lib/api";

export default function Dashboard() {
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listProjects()
      .then(setProjects)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-semibold">Projects</h1>
        <Link
          href="/projects/new"
          className="px-4 py-2 bg-ink text-stock rounded-md hover:bg-ink/85 transition"
        >
          + New Project
        </Link>
      </div>

      {loading && <p className="text-graphite">Loading projects…</p>}
      {error && (
        <div className="p-4 bg-bad/10 border border-bad/30 rounded-md text-bad text-sm">
          {error}
          <p className="mt-2 text-graphite">
            Is the backend running? Start it with: <code>cd backend && uvicorn app.main:app --reload</code>
          </p>
        </div>
      )}

      {!loading && !error && projects.length === 0 && (
        <div className="text-center py-16">
          <p className="text-graphite mb-4">No projects yet.</p>
          <Link
            href="/projects/new"
            className="inline-block px-4 py-2 bg-ink text-stock rounded-md hover:bg-ink/85 transition"
          >
            Start your first project
          </Link>
        </div>
      )}

      {!loading && projects.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project) => (
            <Link
              key={project.id}
              href={`/projects/${project.id}`}
              className="block p-5 bg-stock border border-rule rounded-lg hover:border-ink/40 hover:shadow-sm transition"
            >
              <h3 className="font-medium text-ink">{project.company_name}</h3>
              <p className="text-sm text-graphite mt-1">{project.industry}</p>
              <div className="mt-3 flex items-center gap-2">
                <span className="text-xs px-2 py-1 bg-surface-2 rounded capitalize">
                  {project.stage}
                </span>
                {project.brand_confidence_score > 0 && (
                  <span className="text-xs text-graphite">
                    {project.brand_confidence_score.toFixed(0)}% confidence
                  </span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
