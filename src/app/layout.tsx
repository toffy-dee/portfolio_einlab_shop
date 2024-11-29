import React from 'react'
import "@/app/globals.css"
import { Oswald, Pinyon_Script } from "next/font/google"
import { SiteHeader } from "@/components/site-header"
import { Providers } from "./providers"

const oswald = Oswald({
  subsets: ["latin"],
  variable: "--font-oswald",
})

const pinyonScript = Pinyon_Script({
  weight: '400',
  subsets: ["latin"],
  variable: "--font-pinyon-script",
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${oswald.variable} ${pinyonScript.variable} font-sans`}>
        <Providers>
          <SiteHeader />
          {children}
        </Providers>
      </body>
    </html>
  )
}

