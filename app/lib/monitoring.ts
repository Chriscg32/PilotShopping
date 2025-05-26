import * as Sentry from '@sentry/nextjs'
import { Analytics } from '@vercel/analytics/react'

// Initialize Sentry
export function initSentry() {
  Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV,
    tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
    beforeSend(event) {
      // Filter out non-critical errors in production
      if (process.env.NODE_ENV === 'production') {
        if (event.exception) {
          const error = event.exception.values?.[0]
          if (error?.type === 'ChunkLoadError' || error?.type === 'ResizeObserver loop limit exceeded') {
            return null
          }
        }
      }
      return event
    },
  })
}

// Custom analytics tracking
export class AppAnalytics {
  static trackCopyGeneration(data: {
    productName: string
    industry?: string
    tone: string
    processingTime: number
    success: boolean
  }) {
    // Track with Vercel Analytics
    if (typeof window !== 'undefined') {
      window.va?.track('copy_generated', {
        industry: data.industry || 'unknown',
        tone: data.tone,
        processing_time: data.processingTime,
        success: data.success
      })
    }

    // Track with Sentry
    Sentry.addBreadcrumb({
      category: 'copy_generation',
      message: 'Copy generation attempt',
      data,
      level: data.success ? 'info' : 'error'
    })
  }

  static trackPayment(data: {
    amount: number
    reference: string
    email: string
    success: boolean
  }) {
    if (typeof window !== 'undefined') {
      window.va?.track('payment_attempt', {
        amount: data.amount,
        success: data.success
      })

      if (data.success) {
        window.va?.track('purchase', {
          amount: data.amount,
          currency: 'ZAR'
        })
      }
    }

    Sentry.addBreadcrumb({
      category: 'payment',
      message: data.success ? 'Payment successful' : 'Payment failed',
      data,
      level: data.success ? 'info' : 'warning'
    })
  }

  static trackError(error: Error, context?: Record<string, any>) {
    Sentry.captureException(error, {
      tags: {
        component: context?.component || 'unknown'
      },
      extra: context
    })

    if (typeof window !== 'undefined') {
      window.va?.track('error', {
        error_type: error.name,
        component: context?.component
      })
    }
  }
}

// Performance monitoring
export class PerformanceMonitor {
  private static marks: Map<string, number> = new Map()

  static startTiming(label: string) {
    this.marks.set(label, performance.now())
  }

  static endTiming(label: string): number {
    const startTime = this.marks.get(label)
    if (!startTime) return 0

    const duration = performance.now() - startTime
    this.marks.delete(label)

    // Track performance metrics
    if (typeof window !== 'undefined') {
      window.va?.track('performance', {
        metric: label,
        duration: Math.round(duration)
      })
    }

    return duration
  }

  static measureApiCall<T>(
    apiCall: () => Promise<T>,
    endpoint: string
  ): Promise<T> {
    const startTime = performance.now()
    
    return apiCall()
      .then((result) => {
        const duration = performance.now() - startTime
        
        if (typeof window !== 'undefined') {
          window.va?.track('api_call', {
            endpoint,
            duration: Math.round(duration),
            success: true
          })
        }
        
        return result
      })
      .catch((error) => {
        const duration = performance.now() - startTime
        
        if (typeof window !== 'undefined') {
          window.va?.track('api_call', {
            endpoint,
            duration: Math.round(duration),
            success: false
          })
        }
        
        throw error
      })
  }
}