import type { Metadata, Viewport } from "next";
import { Bricolage_Grotesque, Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const bricolage = Bricolage_Grotesque({
  subsets: ["latin"],
  variable: "--font-bricolage",
  display: "swap",
});
const geist = Geist({ subsets: ["latin"], variable: "--font-geist", display: "swap" });
const geistMono = Geist_Mono({ subsets: ["latin"], variable: "--font-geist-mono", display: "swap" });

const title = "Solo & Starving? Dinner for one, sorted by how tired you are";
const description =
  "88 beginner recipes for one that cook in 10 to 30 minutes, tagged Normal, Tired or Dead Tired. Interactive PDF cookbook plus 2 free planners. Instant download.";

export const metadata: Metadata = {
  metadataBase: new URL("https://soloandstarving.store"),
  title,
  description,
  authors: [{ name: "Yassine & Nourhene" }],
  openGraph: {
    type: "website",
    url: "/",
    siteName: "Y&N Digital",
    title,
    description,
    locale: "en_US",
    images: [{ url: "/og-image.jpg", width: 1200, height: 630, alt: "Solo & Starving? cookbook: real dinners for one in 10 to 30 minutes" }],
  },
  twitter: { card: "summary_large_image", title, description, images: ["/og-image.jpg"] },
  alternates: { canonical: "/" },
};

export const viewport: Viewport = {
  themeColor: "#0f1012",
  colorScheme: "dark",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${bricolage.variable} ${geist.variable} ${geistMono.variable}`}>
      <body className="grain min-h-[100dvh]">{children}</body>
    </html>
  );
}
