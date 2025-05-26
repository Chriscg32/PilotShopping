'use client'

import { useState } from 'react'
import { GenerateForm } from './components/GenerateForm'
import { CopyResult } from './components/CopyResult'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertCircle, CheckCircle } from 'lucide-react'

interface CopyData {
  headline: string
  subheadline: string
  bullets: string[]
  cta: string
  metadata: {
    generatedAt: string
    model: string
    processingTime: number
  }
}

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false)
  const [copyData, setCopyData] = useState<CopyData | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isPaid, setIsPaid] = useState(false)

  const handleGenerate = async (formData: any) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to generate copy')
      }

      const data = await response.json()
      setCopyData(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const handlePaymentSuccess = () => {
    setIsPaid(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Landing Copy Generator
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Generate compelling landing page copy in seconds. Perfect for bootstrapped founders 
            who need professional copy without the professional price tag.
          </p>
        </div>

        {/* Success Alert */}
        {isPaid && (
          <Alert className="mb-6 border-green-200 bg-green-50">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-800">
              Payment successful! Check your email for the complete copy package.
            </AlertDescription>
          </Alert>
        )}

        {/* Error Alert */}
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Main Content */}
        <div className="space-y-8">
          {!copyData ? (
            <GenerateForm onGenerate={handleGenerate} isLoading={isLoading} />
          ) : (
            <>
              <CopyResult copyData={copyData} onPaymentSuccess={handlePaymentSuccess} />
              
              {/* Generate Another */}
              <div className="text-center">
                <Card className="max-w-md mx-auto">
                  <CardContent className="pt-6">
                    <p className="text-gray-600 mb-4">Want to generate another copy?</p>
                    <button
                      onClick={() => {
                        setCopyData(null)
                        setError(null)
                        setIsPaid(false)
                      }}
                      className="text-purple-600 hover:text-purple-700 font-medium"
                    >
                      Start Over
                    </button>
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-500 text-sm">
          <p>© 2024 AI Landing Copy Generator. Built for bootstrapped founders.</p>
          <p className="mt-2">
            Powered by Hugging Face • Payments by Paystack • Made with ❤️
          </p>
        </footer>
      </div>
    </div>
  )
}