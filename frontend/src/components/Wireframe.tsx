"use client";

/**
 * Deterministic composition wireframe renderer (PROD-CP-001 §5, LOG-CP-001 §3).
 *
 * The Concept Prompt Engine emits a STRUCTURED wireframe spec; this component
 * renders it as a TECHNICAL DRAWING — the LLM describes layout, it never draws
 * pixels, so the result is deterministic and reads as a drafting plate, not a
 * logo attempt. Ink-on-paper strokes, registration crosses at the corners, and
 * a figure caption (FIG. {label} — {ORIENTATION}) make the spec legible as a
 * blueprint the designer takes to their own tool.
 */

import { useRef, useState } from "react";

// ─── Types (mirror backend schemas) ───────────────────────────────────

export interface WireframeElement {
  kind: string;
  geometry: string;
  position: string;
  relative_size: string;
  notes?: string;
}

export interface WireframeSpec {
  orientation: string;
  balance: string;
  alignment: string;
  safe_margin: string;
  elements: WireframeElement[];
  favicon_note: string;
}

// ─── Geometry helpers (unchanged: deterministic) ─────────────────────

const CANVAS = 1024;
const SIZE_FACTOR: Record<string, number> = {
  dominant: 0.46,
  balanced: 0.32,
  accent: 0.18,
  small: 0.12,
};

function hexagonPoints(cx: number, cy: number, r: number): string {
  const pts: string[] = [];
  for (let i = 0; i < 6; i++) {
    const a = (Math.PI / 3) * i - Math.PI / 2;
    pts.push(`${(cx + r * Math.cos(a)).toFixed(1)},${(cy + r * Math.sin(a)).toFixed(1)}`);
  }
  return pts.join(" ");
}

function placeElement(
  el: WireframeElement,
  orientation: string,
  inner: number,
  margin: number
): { x: number; y: number; r: number } {
  const r = (inner * (SIZE_FACTOR[el.relative_size] ?? 0.3)) / 2;
  const mid = margin + inner / 2;
  if (el.position === "left-of-text") return { x: margin + inner * 0.22, y: mid, r };
  if (el.position === "above") return { x: mid, y: margin + inner * 0.3, r };
  if (el.position === "below") return { x: mid, y: margin + inner * 0.72, r };
  if (el.position === "integrated") return { x: mid + inner * 0.12, y: mid, r: r * 0.7 };
  if (el.kind === "wordmark" && orientation === "horizontal") return { x: margin + inner * 0.62, y: mid, r };
  return { x: mid, y: mid, r };
}

// ─── Element renderer (technical-drawing styling) ─────────────────────

const INK = "#1A1814";
const INK_LIGHT = "#5C564C";
const RULE = "#D8D0BF";

function ElementShape({ el, pos }: { el: WireframeElement; pos: { x: number; y: number; r: number } }) {
  const SW = 5; // a confident, single ink weight
  let shape = null;
  switch (el.geometry) {
    case "circle":
      shape = <circle cx={pos.x} cy={pos.y} r={pos.r} stroke={INK} strokeWidth={SW} fill="none" />;
      break;
    case "hexagon":
      shape = <polygon points={hexagonPoints(pos.x, pos.y, pos.r)} stroke={INK} strokeWidth={SW} fill="none" />;
      break;
    case "rectangle":
      shape = (
        <rect x={pos.x - pos.r} y={pos.y - pos.r * 0.6} width={pos.r * 2} height={pos.r * 1.2} stroke={INK} strokeWidth={SW} fill="none" />
      );
      break;
    case "baseline-bar":
      // wordmark stand-in: two ink rules (a cap-height line + baseline)
      shape = (
        <g stroke={INK} strokeWidth={SW}>
          <line x1={pos.x - pos.r * 1.4} y1={pos.y - pos.r * 0.35} x2={pos.x + pos.r * 1.4} y2={pos.y - pos.r * 0.35} />
          <line x1={pos.x - pos.r * 1.4} y1={pos.y + pos.r * 0.35} x2={pos.x + pos.r * 1.4} y2={pos.y + pos.r * 0.35} />
        </g>
      );
      break;
    case "monogram":
      shape = (
        <text x={pos.x} y={pos.y + pos.r * 0.35} textAnchor="middle" fontSize={pos.r * 1.4} fontFamily="var(--font-fraunces), Georgia, serif" fontWeight={600} fill={INK}>
          A
        </text>
      );
      break;
    default:
      // custom / container / negative-space — dashed placeholder
      shape = (
        <rect x={pos.x - pos.r} y={pos.y - pos.r} width={pos.r * 2} height={pos.r * 2} stroke={INK_LIGHT} strokeWidth={3} strokeDasharray="14 10" fill="none" />
      );
  }

  // Leader line + element tag, draughting-style.
  const tagX = pos.x + pos.r + 28;
  const tagY = pos.y + pos.r + 22;
  return (
    <g>
      <line x1={pos.x + pos.r * 0.7} y1={pos.y + pos.r * 0.7} x2={tagX - 6} y2={tagY - 6} stroke={RULE} strokeWidth={2} />
      {shape}
      <text x={tagX} y={tagY} fontSize={22} fontFamily="var(--font-jetbrains), monospace" fill={INK_LIGHT} letterSpacing="0.1em">
        {el.kind.toUpperCase()}
      </text>
    </g>
  );
}

// ─── Registration cross (corner mark) ─────────────────────────────────

function RegMark({ x, y }: { x: number; y: number }) {
  return (
    <g stroke={RULE} strokeWidth={2}>
      <line x1={x - 14} y1={y} x2={x + 14} y2={y} />
      <line x1={x} y1={y - 14} x2={x} y2={y + 14} />
      <circle cx={x} cy={y} r={2} fill={RULE} stroke="none" />
    </g>
  );
}

// ─── Main component ───────────────────────────────────────────────────

export function Wireframe({ spec, familyLabel }: { spec: WireframeSpec; familyLabel?: string }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [copied, setCopied] = useState<string | null>(null);

  const marginPct = parseFloat(spec.safe_margin) || 12;
  const margin = (CANVAS * marginPct) / 100;
  const inner = CANVAS - margin * 2;

  const flash = (k: string) => {
    setCopied(k);
    setTimeout(() => setCopied(null), 1500);
  };

  const downloadSvg = () => {
    const svg = svgRef.current;
    if (!svg) return;
    const xml = new XMLSerializer().serializeToString(svg);
    const url = URL.createObjectURL(new Blob([xml], { type: "image/svg+xml" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `wireframe-${familyLabel || "concept"}.svg`;
    a.click();
    URL.revokeObjectURL(url);
    flash("svg");
  };

  const copyPng = () => {
    const svg = svgRef.current;
    if (!svg) return;
    const xml = new XMLSerializer().serializeToString(svg);
    const img = new Image();
    const url = URL.createObjectURL(new Blob([xml], { type: "image/svg+xml" }));
    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = CANVAS;
      canvas.height = CANVAS;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      ctx.fillStyle = "#FBF8F1";
      ctx.fillRect(0, 0, CANVAS, CANVAS);
      ctx.drawImage(img, 0, 0);
      canvas.toBlob((blob) => {
        if (!blob) return;
        blob.arrayBuffer().then((buf) => {
          navigator.clipboard.write([new ClipboardItem({ "image/png": new Blob([buf], { type: "image/png" }) })]);
          flash("png");
        });
      });
      URL.revokeObjectURL(url);
    };
    img.src = url;
  };

  const figLabel = `FIG. ${familyLabel || "•"} — ${spec.orientation.toUpperCase()}`;

  return (
    <div className="space-y-3">
      {/* The plate */}
      <div className="relative bg-stock border border-ink/30 rounded-sm p-3">
        <svg ref={svgRef} viewBox={`0 0 ${CANVAS} ${CANVAS}`} className="w-full h-auto" role="img" aria-label="Composition wireframe">
          <rect x={0} y={0} width={CANVAS} height={CANVAS} fill="#FBF8F1" />
          {/* registration crosses at the inner corners */}
          <RegMark x={margin - 24} y={margin - 24} />
          <RegMark x={CANVAS - margin + 24} y={margin - 24} />
          <RegMark x={margin - 24} y={CANVAS - margin + 24} />
          <RegMark x={CANVAS - margin + 24} y={CANVAS - margin + 24} />
          {/* safe-margin frame */}
          <rect x={margin} y={margin} width={inner} height={inner} fill="none" stroke={RULE} strokeWidth={2} />
          {/* optical-centre guides */}
          <line x1={CANVAS / 2} y1={margin} x2={CANVAS / 2} y2={CANVAS - margin} stroke={RULE} strokeWidth={1.5} strokeDasharray="6 10" />
          <line x1={margin} y1={CANVAS / 2} x2={CANVAS - margin} y2={CANVAS / 2} stroke={RULE} strokeWidth={1.5} strokeDasharray="6 10" />

          {spec.elements.map((el, i) => (
            <ElementShape key={i} el={el} pos={placeElement(el, spec.orientation, inner, margin)} />
          ))}
        </svg>
      </div>

      {/* Figure caption + metadata strip */}
      <div className="flex items-baseline justify-between gap-4 border-t border-rule pt-2">
        <p className="font-mono text-[11px] tracking-folio text-graphite uppercase">{figLabel}</p>
        <p className="font-mono text-[11px] text-graphite">
          {spec.alignment} · {spec.balance}
        </p>
      </div>

      {/* Scale test (favicon) — framed as a small-size degradation probe */}
      <div className="flex items-center gap-3 pt-1">
        <div className="w-9 h-9 border border-ink/40 bg-stock flex items-center justify-center">
          <svg viewBox={`0 0 ${CANVAS} ${CANVAS}`} className="w-full h-full">
            {spec.elements
              .filter((e) => e.kind === "symbol")
              .map((el, i) => (
                <ElementShape key={i} el={el} pos={placeElement(el, spec.orientation, inner, margin)} />
              ))}
          </svg>
        </div>
        <p className="text-xs text-graphite">
          <span className="font-mono uppercase tracking-folio text-[10px] text-ink/70 mr-1">Scale 16px —</span>
          {spec.favicon_note}
        </p>
      </div>

      {/* Export */}
      <div className="flex gap-2 pt-1">
        <button onClick={downloadSvg} className="px-3 py-1.5 text-xs font-mono uppercase tracking-folio text-ink border border-ink/40 hover:bg-ink hover:text-stock transition-colors">
          {copied === "svg" ? "Saved ✓" : "↓ SVG"}
        </button>
        <button onClick={copyPng} className="px-3 py-1.5 text-xs font-mono uppercase tracking-folio text-ink border border-ink/40 hover:bg-ink hover:text-stock transition-colors">
          {copied === "png" ? "Copied ✓" : "⧉ PNG"}
        </button>
      </div>
    </div>
  );
}
