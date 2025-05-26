'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { CreditCard, Loader2 } from 'lucide-react'

interface PayButtonProps {
  amount: number // in cents
  email: string
  copyData: any
  onSuccess: () => void
}

export function PayButton({ amount, email, copyData, onSuccess }: PayButtonProps) {
  const [isProcessing, setIsProcessing] = useState(false)

  const handlePayment = async () => {
    setIsProcessing(true)
    
    try {
      // Load Paystack script dynamically
      const script = document.createElement('script')
      script.src = 'https://js.paystack.co/v1/inline.js'
      document.body.appendChild(script)

      script.onload = () => {
        const handler = (window as any).PaystackPop.setup({
          key: process.env.NEXT_PUBLIC_PAYSTACK_KEY,
          email: email,
          amount: amount,
          currency: 'ZAR',
          ref: `copy_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          metadata: {
            copyData: JSON.stringify(copyData),
            product: 'AI Landing Copy',
            generatedAt: copyData.metadata.generatedAt
          },
          callback: async function(response: any) {
            console.log('Payment successful:', response)
            
            // Trigger n8n webhook
            try {
              await fetch(process.env.NEXT_PUBLIC_N8N_WEBHOOK_URL || '/api/webhook/payment-success', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  reference: response.reference,
                  status: 'success',
                  amount: amount,
                  email: email,
                  copyData: copyData,
                  timestamp: new Date().toISOString()
                })
              })
              
              onSuccess()
              setIsProcessing(false)
            } catch (error) {
              console.error('Webhook error:', error)
              // Still call onSuccess as payment was successful
              onSuccess()
              setIsProcessing(false)
            }
          },
          onClose: function() {
            console.log('Payment window closed')
            setIsProcessing(false)
          }
        })
        
        handler.openIframe()
      }
    } catch (error) {
      console.error('Payment initialization error:', error)
      setIsProcessing(false)
    }
  }

  return (
    <Button 
      onClick={handlePayment}
      disabled={isProcessing}
      className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700"
      size="lg"
    >
      {isProcessing ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Processing Payment...
        </>
      ) : (
        <>
          <CreditCard className="mr-2 h-4 w-4" />
          Purchase for R9
        </>
      )}
    </Button>
  )
}