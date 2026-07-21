"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createProject, analyseBrief } from "@/lib/api";

export default function NewProjectPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    company_name: "",
    industry: "",
    client_brief: "",
    client_contact: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.company_name || !form.industry || !form.client_brief) {
      setError("Company name, industry, and brief are required.");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const project = await createProject({
        company_name: form.company_name,
        industry: form.industry,
        client_brief: form.client_brief,
        client_contact: form.client_contact || undefined,
      });

      // Automatically run Discovery analysis
      await analyseBrief(project.id);

      router.push(`/projects/${project.id}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-semibold mb-2">New Project</h1>
      <p className="text-gray-500 mb-8">
        Paste whatever you have — even one sentence. LogoMind will work with it.
      </p>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Company Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={form.company_name}
            onChange={(e) => setForm({ ...form, company_name: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:border-transparent"
            placeholder="e.g., Northbridge Coffee"
            disabled={submitting}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Industry <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={form.industry}
            onChange={(e) => setForm({ ...form, industry: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:border-transparent"
            placeholder="e.g., Coffee / Hospitality"
            disabled={submitting}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Client Brief <span className="text-red-500">*</span>
          </label>
          <p className="text-xs text-gray-400 mb-2">
            Any completeness level. LogoMind will assess and help fill gaps.
          </p>
          <textarea
            value={form.client_brief}
            onChange={(e) => setForm({ ...form, client_brief: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:border-transparent min-h-[150px]"
            placeholder="They're an independent coffee roaster in the city. They want something warm and crafted…"
            disabled={submitting}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Client Contact <span className="text-gray-400 font-normal">(optional)</span>
          </label>
          <input
            type="email"
            value={form.client_contact}
            onChange={(e) => setForm({ ...form, client_contact: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-900 focus:border-transparent"
            placeholder="client@example.com — for Workshop link sharing"
            disabled={submitting}
          />
        </div>

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
            {error}
          </div>
        )}

        <div className="flex items-center gap-4">
          <button
            type="submit"
            disabled={submitting}
            className="px-6 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 transition disabled:opacity-50"
          >
            {submitting ? "Analysing brief…" : "Analyse Project →"}
          </button>
          <button
            type="button"
            onClick={() => router.push("/")}
            className="px-4 py-2 text-gray-500 hover:text-gray-700"
            disabled={submitting}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
