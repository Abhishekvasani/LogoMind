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
          className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 transition"
        >
          + New Project
        </Link>
      </div>

      {loading && <p className="text-gray-500">Loading projects…</p>}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
          {error}
          <p className="mt-2 text-gray-500">
            Is the backend running? Start it with: <code>cd backend && uvicorn app.main:app --reload</code>
          </p>
        </div>
      )}

      {!loading && !error && projects.length === 0 && (
        <div className="text-center py-16">
          <p className="text-gray-500 mb-4">No projects yet.</p>
          <Link
            href="/projects/new"
            className="inline-block px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 transition"
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
              className="block p-5 bg-white border border-gray-200 rounded-lg hover:border-gray-400 hover:shadow-sm transition"
            >
              <h3 className="font-medium text-gray-900">{project.company_name}</h3>
              <p className="text-sm text-gray-500 mt-1">{project.industry}</p>
              <div className="mt-3 flex items-center gap-2">
                <span className="text-xs px-2 py-1 bg-gray-100 rounded capitalize">
                  {project.stage}
                </span>
                {project.brand_confidence_score > 0 && (
                  <span className="text-xs text-gray-400">
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
