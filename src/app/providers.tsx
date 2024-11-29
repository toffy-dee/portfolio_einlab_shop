'use client'

import React from 'react'
import { Amplify } from 'aws-amplify'
import awsconfig from '@/aws-exports'

Amplify.configure(awsconfig)

export function Providers({ children }: { children: React.ReactNode }) {
  return <>{children}</>
} 