import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LogoMind — Think deeper. Sketch smarter.",
  description: "Strategic design intelligence for logo designers. Reason. Create. Refine.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 min-h-screen antialiased">
        <header className="border-b border-gray-200 bg-white">
          <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="/" className="text-xl font-semibold tracking-tight">
              LogoMind
            </a>
            <span className="text-sm text-gray-500 italic">Reason. Create. Refine.</span>
          </div>
        </header>
        <main className="max-w-6xl mx-auto px-6 py-8">{children}</main>
        <footer className="border-t border-gray-200 bg-white mt-16">
          <div className="max-w-6xl mx-auto px-6 py-4 text-sm text-gray-400">
            LogoMind — Strategic Design Intelligence Platform. The designer is sovereign.
          </div>
        </footer>
      </body>
    </html>
  );
}
