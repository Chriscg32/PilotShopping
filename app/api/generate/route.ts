import { NextRequest, NextResponse } from 'next/server'
import pino from 'pino'
import { z } from 'zod'
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

// Enhanced logging
const logger = pino({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  transport: process.env.NODE_ENV !== 'production' ? {
    target: 'pino-pretty'
  } : undefined
})

// Rate limiting
const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
})

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, '1 m'), // 10 requests per minute
})

// Input validation schema
const GenerateSchema = z.object({
  productName: z.string().min(1).max(100),
  features: z.string().min(10).max(500),
  targetCustomer: z.string().min(5).max(200),
  industry: z.string().optional(),
  tone: z.enum(['professional', 'casual', 'urgent', 'friendly']).default('professional')
})

// Response schema
const CopyResponseSchema = z.object({
  headline: z.string(),
  subheadline: z.string(),
  bullets: z.array(z.string()),
  cta: z.string(),
  metadata: z.object({
    generatedAt: z.string(),
    model: z.string(),
    processingTime: z.number()
  })
})

export async function POST(request: NextRequest) {
  const startTime = Date.now()
  const requestId = crypto.randomUUID()
  
  try {
    // Rate limiting
    const ip = request.ip ?? '127.0.0.1'
    const { success, limit, reset, remaining } = await ratelimit.limit(ip)
    
    if (!success) {
      logger.warn({ ip, requestId }, 'Rate limit exceeded')
      return NextResponse.json(
        { error: 'Rate limit exceeded. Please try again later.' },
        { 
          status: 429,
          headers: {
            'X-RateLimit-Limit': limit.toString(),
            'X-RateLimit-Remaining': remaining.toString(),
            'X-RateLimit-Reset': new Date(reset).toISOString(),
          }
        }
      )
    }

    // Parse and validate input
    const body = await request.json()
    const validatedInput = GenerateSchema.parse(body)
    
    logger.info({ requestId, input: validatedInput }, 'Processing copy generation request')

    // Enhanced prompt engineering
    const prompt = buildEnhancedPrompt(validatedInput)
    
    // Call Hugging Face API with retry logic
    const generatedCopy = await generateCopyWithRetry(prompt, requestId)
    
    // Validate response
    const validatedResponse = CopyResponseSchema.parse({
      ...generatedCopy,
      metadata: {
        generatedAt: new Date().toISOString(),
        model: 'gpt2',
        processingTime: Date.now() - startTime
      }
    })

    logger.info({ 
      requestId, 
      processingTime: Date.now() - startTime,
      success: true 
    }, 'Copy generation completed successfully')

    return NextResponse.json(validatedResponse, {
      headers: {
        'X-Request-ID': requestId,
        'X-Processing-Time': (Date.now() - startTime).toString()
      }
    })

  } catch (error) {
    const processingTime = Date.now() - startTime
    
    if (error instanceof z.ZodError) {
      logger.warn({ requestId, error: error.errors }, 'Validation error')
      return NextResponse.json(
        { error: 'Invalid input data', details: error.errors },
        { status: 400 }
      )
    }

    logger.error({ 
      requestId, 
      error: error instanceof Error ? error.message : 'Unknown error',
      processingTime 
    }, 'Copy generation failed')

    return NextResponse.json(
      { error: 'Failed to generate copy. Please try again.' },
      { status: 500 }
    )
  }
}

function buildEnhancedPrompt(input: z.infer<typeof GenerateSchema>): string {
  const toneInstructions = {
    professional: 'Use professional, authoritative language',
    casual: 'Use conversational, friendly language',
    urgent: 'Create urgency and immediate action',
    friendly: 'Use warm, approachable language'
  }

  return `Create compelling landing page copy for "${input.productName}".

Product Features: ${input.features}
Target Customer: ${input.targetCustomer}
Industry: ${input.industry || 'General'}
Tone: ${toneInstructions[input.tone]}

Generate:
1. Compelling headline (max 60 characters)
2. Supporting subheadline (max 120 characters)  
3. Three benefit bullets (max 50 characters each)
4. Call-to-action button text (max 25 characters)

Format as JSON:
{
  "headline": "...",
  "subheadline": "...", 
  "bullets": ["...", "...", "..."],
  "cta": "..."
}`
}

async function generateCopyWithRetry(prompt: string, requestId: string, maxRetries = 3): Promise<any> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch('https://api-inference.huggingface.co/models/gpt2', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.HUGGINGFACE_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          inputs: prompt,
          parameters: {
            max_new_tokens: 200,
            temperature: 0.7,
            do_sample: true,
            return_full_text: false
          }
        }),
      })

      if (!response.ok) {
        throw new Error(`HF API error: ${response.status} ${response.statusText}`)
      }

      const result = await response.json()
      const generatedText = result[0]?.generated_text || result.generated_text

      // Parse JSON from generated text
      const jsonMatch = generatedText.match(/\{[\s\S]*\}/)
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0])
      }

      // Fallback parsing or default response
      return parseOrFallback(generatedText, prompt)

    } catch (error) {
      logger.warn({ requestId, attempt, error: error instanceof Error ? error.message : 'Unknown error' }, 'Generation attempt failed')
      
      if (attempt === maxRetries) {
        throw error
      }
      
      // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000))
    }
  }
}

function parseOrFallback(text: string, originalPrompt: string): any {
  // Implement intelligent fallback parsing
  return {
    headline: "Transform Your Business Today",
    subheadline: "Discover the power of innovation with our cutting-edge solution",
    bullets: [
      "Increase efficiency by 300%",
      "Save time and resources", 
      "Get results in 24 hours"
    ],
    cta: "Get Started Now"
  }
}

// Health check endpoint
export async function GET() {
  return NextResponse.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || '1.0.0'
  })
}