import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ESG & Thematic Investment Screener",
  description:
    "Screen, compare, and optimize ESG-focused portfolios with ML-powered insights. Built by Nhat Nguyen.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-gray-950 text-gray-100 min-h-screen antialiased">
        {/* Top nav */}
        <header className="sticky top-0 z-50 border-b border-gray-800 bg-gray-950/80 backdrop-blur-md">
          <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-600 font-bold text-sm">
                ESG
              </div>
              <span className="text-lg font-semibold tracking-tight">
                ESG & Thematic Investment Screener
              </span>
            </div>
            <nav className="flex items-center gap-1 text-sm">
              <a
                href="/"
                className="rounded-md px-3 py-1.5 transition hover:bg-gray-800"
              >
                Screener
              </a>
              <a
                href="/compare"
                className="rounded-md px-3 py-1.5 transition hover:bg-gray-800"
              >
                Compare
              </a>
              <a
                href="/optimizer"
                className="rounded-md px-3 py-1.5 transition hover:bg-gray-800"
              >
                Optimizer
              </a>
              <a
                href="/predictions"
                className="rounded-md px-3 py-1.5 transition hover:bg-gray-800"
              >
                ML Predictions
              </a>
            </nav>
          </div>
        </header>

        <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>

        {/* Footer */}
        <footer className="border-t border-gray-800 py-6 text-center text-xs text-gray-500">
          <p>
            Built by{" "}
            <a
              href="mailto:Nhatmn114@gmail.com"
              className="text-emerald-400 hover:underline"
            >
              Nhat Nguyen
            </a>{" "}
            &middot; ESG data is illustrative &middot; Not investment advice
          </p>
        </footer>
      </body>
    </html>
  );
}
