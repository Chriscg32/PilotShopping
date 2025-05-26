'use client'

import { useState } from 'react'
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Loader2, Sparkles, Zap } from 'lucide-react'

const FormSchema = z.object({
  productName: z.string().min(1, 'Product name is required').max(100),
  features: z.string().min(10, 'Please provide more details about features').max(500),
  targetCustomer: z.string().min(5, 'Please describe your target customer').max(200),
  industry: z.string().optional(),
  tone: z.enum(['professional', 'casual', 'urgent', 'friendly']).default('professional')
})

type FormData = z.infer<typeof FormSchema>

interface GenerateFormProps {
  onGenerate: (data: FormData) => Promise<void>
  isLoading: boolean
}

export function GenerateForm({ onGenerate, isLoading }: GenerateFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch
  } = useForm<FormData>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      tone: 'professional'
    }
  })

  const watchedFields = watch()

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader className="text-center">
        <CardTitle className="flex items-center justify-center gap-2 text-2xl">
          <Sparkles className="h-6 w-6 text-purple-600" />
          AI Landing Copy Generator
        </CardTitle>
        <CardDescription>
          Generate compelling landing page copy in seconds with AI
        </CardDescription>
      </CardHeader>
      
      <CardContent>
        <form onSubmit={handleSubmit(onGenerate)} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="productName">Product Name *</Label>
            <Input
              id="productName"
              placeholder="e.g., TaskMaster Pro"
              {...register('productName')}
              className={errors.productName ? 'border-red-500' : ''}
            />
            {errors.productName && (
              <p className="text-sm text-red-500">{errors.productName.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="features">Key Features & Benefits *</Label>
            <Textarea
              id="features"
              placeholder="Describe your product's main features and benefits..."
              rows={4}
              {...register('features')}
              className={errors.features ? 'border-red-500' : ''}
            />
            <div className="flex justify-between text-sm text-gray-500">
              <span>{errors.features?.message}</span>
              <span>{watchedFields.features?.length || 0}/500</span>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="targetCustomer">Target            <Label htmlFor="targetCustomer">Target Customer *</Label>
            <Textarea
              id="targetCustomer"
              placeholder="Describe your ideal customer (demographics, pain points, goals)..."
              rows={3}
              {...register('targetCustomer')}
              className={errors.targetCustomer ? 'border-red-500' : ''}
            />
            <div className="flex justify-between text-sm text-gray-500">
              <span>{errors.targetCustomer?.message}</span>
              <span>{watchedFields.targetCustomer?.length || 0}/200</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="industry">Industry (Optional)</Label>
              <Input
                id="industry"
                placeholder="e.g., SaaS, E-commerce, Healthcare"
                {...register('industry')}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="tone">Tone & Style</Label>
              <Select onValueChange={(value) => setValue('tone', value as any)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select tone" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="professional">Professional</SelectItem>
                  <SelectItem value="casual">Casual & Friendly</SelectItem>
                  <SelectItem value="urgent">Urgent & Action-Oriented</SelectItem>
                  <SelectItem value="friendly">Warm & Approachable</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button 
            type="submit" 
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
            disabled={isLoading}
            size="lg"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating Copy...
              </>
            ) : (
              <>
                <Zap className="mr-2 h-4 w-4" />
                Generate Landing Copy
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}