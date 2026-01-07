import type { Metadata } from "next";
import { Lexend } from "next/font/google";
import PlausibleProvider from "next-plausible";
import { GoogleAnalytics } from '@next/third-parties/google'
import { ResearchHistoryProvider } from "@/hooks/ResearchHistoryContext";
import "./globals.css";
import Script from 'next/script';
import { MINIMAL_UI } from "@/config/ui";

const isMinimal = (process.env.NEXT_PUBLIC_MINIMAL_UI ?? 'true').toLowerCase() === 'true';

const inter = Lexend({ subsets: ["latin"] });

let title = "VentureProof";
let description =
  "Generate structured venture/industry analysis with citations from your brief.";
let url = "https://github.com/assafelovic/gpt-researcher";
let ogimage = "/favicon.ico";
let sitename = "VentureProof";

export const metadata: Metadata = {
  metadataBase: new URL(url),
  title,
  description,
  manifest: '/manifest.json',
  icons: isMinimal ? undefined : {
    icon: "/img/gptr-black-logo.png",
    apple: '/img/gptr-black-logo.png',
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: title,
  },
  openGraph: {
    images: [ogimage],
    title,
    description,
    url: url,
    siteName: sitename,
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    images: [ogimage],
    title,
    description,
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
    userScalable: false,
  },
  themeColor: '#111827',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html className={`gptr-root ${MINIMAL_UI ? 'minimal-ui' : ''}`} lang="en" suppressHydrationWarning>
      <head>
        {!MINIMAL_UI && <PlausibleProvider domain="localhost:3000" />}
        {!MINIMAL_UI && <GoogleAnalytics gaId={process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID!} />}
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        {!MINIMAL_UI && <link rel="apple-touch-icon" href="/img/gptr-black-logo.png" />}
        {MINIMAL_UI && (
          <>
            {/* Use a transparent favicon (effectively no icon) */}
            <link
              rel="icon"
              href={'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22></svg>'}
            />
          </>
        )}
      </head>
      <body
        className={`app-container ${MINIMAL_UI ? '' : inter.className} flex min-h-screen flex-col justify-between`}
        suppressHydrationWarning
      >
        <ResearchHistoryProvider>
          {children}
        </ResearchHistoryProvider>
      </body>
    </html>
  );
}
