import { NextResponse } from 'next/server'
import { Redis } from '@upstash/redis'

export async function GET() {
  const startTime = Date.now()
  const checks = {
    timestamp: new Date().toISOString(),
    status: 'healthy',
    version: process.env.npm_package_version || '1.0.0',
    environment: process.env.NODE_ENV,
    checks: {
      huggingface: false,
      redis: false,
      database: false
    },
    responseTime: 0
  }

  try {
    // Check Hugging Face API
    try {
      const hfResponse = await fetch('https://api-inference.huggingface.co/models/gpt2', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.HUGGINGFACE_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          inputs: 'Health check',
          parameters: { max_new_tokens: 1 }
        }),
      })
      checks.checks.huggingface = hfResponse.ok
    } catch {
      checks.checks.huggingface = false
    }

    // Check Redis
    try {
      if (process.env.UPSTASH_REDIS_REST_URL) {
        const redis = new Redis({
          url: process.env.UPSTASH_REDIS_REST_URL,
          token: process.env.UPSTASH_REDIS_REST_TOKEN!,
        })
        await redis.ping()
        checks.checks.redis = true
      }
    } catch {
      checks.checks.redis = false
    }

    // Overall health status
    const allHealthy = Object.values(checks.checks).every(check => check === true)
    checks.status = allHealthy ? 'healthy' : 'degraded'
    checks.responseTime = Date.now() - startTime

    return NextResponse.json(checks, {
      status: allHealthy ? 200 : 503,
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    })

  } catch (error) {
    checks.status = 'unhealthy'
    checks.responseTime = Date.now() - startTime

    return NextResponse.json(checks, {
      status: 503,
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate'
      }
    })
  }
}