import type { Metadata } from "next";
import { Fraunces, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const fraunces = Fraunces({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-fraunces",
  axes: ["opsz", "SOFT"], // optical sizing + a touch of softness for character
});

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-jetbrains",
});

export const metadata: Metadata = {
  title: "LogoMind — Think deeper. Sketch smarter.",
  description: "Strategic design intelligence for logo designers. Reason. Create. Refine.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${fraunces.variable} ${inter.variable} ${jetbrains.variable}`}>
      <body className="bg-paper text-ink min-h-screen antialiased font-sans selection:bg-verified/20">
        <header className="border-b border-ink/15 bg-stock">
          <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="/" className="font-display text-2xl tracking-tight">
              LogoMind
            </a>
            <span className="font-display italic text-sm text-graphite">Reason. Create. Refine.</span>
          </div>
        </header>
        <main className="max-w-6xl mx-auto px-6 py-8">{children}</main>
        <footer className="border-t border-ink/15 bg-stock mt-16">
          <div className="max-w-6xl mx-auto px-6 py-4 text-xs text-graphite font-mono">
            LOGOMIND — STRATEGIC DESIGN INTELLIGENCE · THE DESIGNER IS SOVEREIGN
          </div>
        </footer>
      </body>
    </html>
  );
}
