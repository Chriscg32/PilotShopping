'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Copy, Download, Share2, CheckCircle, Edit3 } from 'lucide-react'
import { PayButton } from './PayButton'

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

interface CopyResultProps {
  copyData: CopyData
  onPaymentSuccess: () => void
}

export function CopyResult({ copyData, onPaymentSuccess }: CopyResultProps) {
  const [copiedField, setCopiedField] = useState<string | null>(null)

  const copyToClipboard = async (text: string, field: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedField(field)
      setTimeout(() => setCopiedField(null), 2000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  const exportAsJSON = () => {
    const dataStr = JSON.stringify(copyData, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
    
    const exportFileDefaultName = `landing-copy-${Date.now()}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
  }

  const shareResults = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AI Generated Landing Copy',
          text: `Headline: ${copyData.headline}\n\nSubheadline: ${copyData.subheadline}`,
          url: window.location.href
        })
      } catch (err) {
        console.error('Error sharing:', err)
      }
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Results Header */}
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="flex items-center justify-center gap-2">
            <CheckCircle className="h-6 w-6 text-green-600" />
            Your Landing Copy is Ready!
          </CardTitle>
          <CardDescription>
            Generated in {copyData.metadata.processingTime}ms using {copyData.metadata.model}
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Copy Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Generated Copy */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Generated Copy</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Headline */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Badge variant="secondary">Headline</Badge>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(copyData.headline, 'headline')}
                  >
                    {copiedField === 'headline' ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </Button>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <h2 className="text-xl font-bold text-gray-900">{copyData.headline}</h2>
                </div>
              </div>

              {/* Subheadline */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Badge variant="secondary">Subheadline</Badge>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(copyData.subheadline, 'subheadline')}
                  >
                    {copiedField === 'subheadline' ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </Button>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-gray-700">{copyData.subheadline}</p>
                </div>
              </div>

              {/* Bullets */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Badge variant="secondary">Key Benefits</Badge>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(copyData.bullets.join('\n• '), 'bullets')}
                  >
                    {copiedField === 'bullets' ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </Button>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <ul className="space-y-1">
                    {copyData.bullets.map((bullet, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-purple-600 mr-2">•</span>
                        <span className="text-gray-700">{bullet}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* CTA */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Badge variant="secondary">Call to Action</Badge>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => copyToClipboard(copyData.cta, 'cta')}
                  >
                    {copiedField === 'cta' ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </Button>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <Button className="w-full bg-gradient-to-r from-purple-600 to-blue-600">
                    {copyData.cta}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Actions */}
          <div className="flex flex-wrap gap-2">
            <Button variant="outline" onClick={exportAsJSON}>
              <Download className="mr-2 h-4 w-4" />
              Export JSON
            </Button>
            <Button variant="outline" onClick={shareResults}>
              <Share2 className="mr-2 h-4 w-4" />
              Share
            </Button>
            <Button variant="outline">
              <Edit3 className="mr-2 h-4 w-4" />
              Regenerate
            </Button>
          </div>
        </div>

        {/* Live Preview */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Live Preview</CardTitle>
              <CardDescription>How your copy looks on a landing page</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-white border rounded-lg p-6 shadow-sm">
                <div className="text-center space-y-4">
                  <h1 className="text-3xl font-bold text-gray-900 leading-tight">
                    {copyData.headline}
                  </h1>
                  <p className="text-xl text-gray-600 leading-relaxed">
                    {copyData.subheadline}
                  </p>
                  
                  <div className="my-6">
                    <ul className="text-left space-y-3 max-w-md mx-auto">
                      {copyData.bullets.map((bullet, index) => (
                        <li key={index} className="flex items-start">
                          <CheckCircle className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700">{bullet}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <Button 
                    size="lg" 
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-8"
                  >
                    {copyData.cta}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Payment Section */}
          <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-blue-50">
            <CardHeader className="text-center">
              <CardTitle className="text-lg text-purple-800">Love Your Copy?</CardTitle>
              <CardDescription>
                Get the full package for just <span className="font-bold text-purple-600">R9</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 text-sm text-gray-600 mb-4">
                <div className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                  <span>Instant email delivery</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                  <span>Multiple format exports</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                  <span>Commercial usage rights</span>
                </div>
              </div>
              
              <PayButton 
                amount={900} // R9 in cents
                email="customer@example.com"
                copyData={copyData}
                onSuccess={onPaymentSuccess}
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}