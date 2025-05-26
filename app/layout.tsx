import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Analytics } from '@vercel/analytics/react'
import { ErrorBoundary } from './components/ErrorBoundary'
import { initSentry } from './lib/monitoring'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

// Initialize monitoring
if (typeof window === 'undefined') {
  initSentry()
}

export const metadata: Metadata = {
  title: 'AI Landing Copy Generator | Professional Copy in Seconds',
  description: 'Generate compelling landing page copy with AI. Perfect for bootstrapped founders who need professional copy without the professional price tag. Just R9 per generation.',
  keywords: 'AI copywriting, landing page copy, startup copy, bootstrap, marketing copy, conversion copy',
  authors: [{ name: 'AI Landing Copy Generator' }],
  creator: 'AI Landing Copy Generator',
  publisher: 'AI Landing Copy Generator',
  robots: 'index, follow',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://ailandingcopy.com',
    title: 'AI Landing Copy Generator | Professional Copy in Seconds',
    description: 'Generate compelling landing page copy with AI. Perfect for bootstrapped founders.',
    siteName: 'AI Landing Copy Generator',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'AI Landing Copy Generator'
      }
    ]
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI Landing Copy Generator | Professional Copy in Seconds',
    description: 'Generate compelling landing page copy with AI. Perfect for bootstrapped founders.',
    images: ['/og-image.png'],
    creator: '@ailandingcopy'
  },
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#7c3aed'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
              new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
              j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
              'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
              })(window,document,'script','dataLayer','${process.env.NEXT_PUBLIC_GTM_ID}');
            `
          }}
        />
      </head>
      <body className={inter.className}>
        <noscript>
          <iframe
            src={`https://www.googletagmanager.com/ns.html?id=${process.env.NEXT_PUBLIC_GTM_ID}`}
            height="0"
            width="0"
            style={{ display: 'none', visibility: 'hidden' }}
          />
        </noscript>
        
        <ErrorBoundary>
          {children}
        </ErrorBoundary>
        
        <Analytics />
      </body>
    </html>
  )
}