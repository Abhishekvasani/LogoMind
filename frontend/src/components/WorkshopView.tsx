"use client";

import { useState } from "react";
import { Project, generateWorkshopLink, completeWorkshop, runStrategy } from "@/lib/api";

export function WorkshopView({ project, onUpdate }: { project: Project; onUpdate: () => void }) {
  const [shareLink, setShareLink] = useState<string | null>(null);
  const [completing, setCompleting] = useState(false);

  const handleShare = async () => {
    try {
      const result = await generateWorkshopLink(project.id);
      setShareLink(`${window.location.origin}/workshop/${result.share_token}`);
    } catch (e: any) {
      alert(e.message);
    }
  };

  const handleComplete = async () => {
    setCompleting(true);
    try {
      await completeWorkshop(project.id);
      await runStrategy(project.id);
      onUpdate();
    } catch (e: any) {
      alert(e.message);
    } finally {
      setCompleting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="p-6 bg-white border border-gray-200 rounded-lg">
        <h2 className="text-lg font-medium mb-2">Discovery Workshop</h2>
        <p className="text-gray-600 mb-4">
          The brief needs enrichment. Run the Discovery Workshop with your client
          — a guided 10–15 minute experience that extracts strategic clarity.
        </p>

        <div className="flex flex-col gap-3">
          <button
            onClick={handleShare}
            className="px-4 py-2 bg-gray-100 text-gray-900 rounded-md hover:bg-gray-200 self-start"
          >
            Generate Client Workshop Link
          </button>

          {shareLink && (
            <div className="p-3 bg-blue-50 border border-blue-200 rounded text-sm">
              <p className="font-medium text-blue-900 mb-1">Share this link with your client:</p>
              <code className="text-blue-700 break-all">{shareLink}</code>
            </div>
          )}

          <div className="pt-4 border-t border-gray-100">
            <p className="text-sm text-gray-500 mb-2">
              Once the workshop is complete (or if you've gathered the information separately),
              proceed to Strategy.
            </p>
            <button
              onClick={handleComplete}
              disabled={completing}
              className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-700 disabled:opacity-50"
            >
              {completing ? "Processing…" : "Complete Workshop & Run Strategy →"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
