describe('AI Landing Copy Generator E2E', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should generate landing copy successfully', () => {
    // Fill out the form
    cy.get('[data-testid="product-name"]').type('TaskMaster Pro')
    cy.get('[data-testid="features"]').type('Advanced task management with AI-powered prioritization, team collaboration tools, and automated reporting features that save 5+ hours per week.')
    cy.get('[data-testid="target-customer"]').type('Busy entrepreneurs and small business owners who struggle with task prioritization and team coordination.')
    cy.get('[data-testid="industry"]').type('SaaS')
    cy.get('[data-testid="tone"]').select('professional')

    // Mock the API response
    cy.intercept('POST', '/api/generate', {
      statusCode: 200,
      body: {
        headline: 'Master Your Tasks, Master Your Business',
        subheadline: 'AI-powered task management that saves entrepreneurs 5+ hours weekly',
        bullets: [
          'Prioritize tasks with AI intelligence',
          'Collaborate seamlessly with your team',
          'Generate automated progress reports'
        ],
        cta: 'Start Free Trial',
        metadata: {
          generatedAt: '2024-01-15T10:30:00.000Z',
          model: 'gpt2',
          processingTime: 1250
        }
      }
    }).as('generateCopy')

    // Submit the form
    cy.get('[data-testid="generate-button"]').click()

    // Wait for API call
    cy.wait('@generateCopy')

    // Verify results are displayed
    cy.get('[data-testid="copy-result"]').should('be.visible')
    cy.get('[data-testid="headline"]').should('contain', 'Master Your Tasks, Master Your Business')
    cy.get('[data-testid="subheadline"]').should('contain', 'AI-powered task management')
    cy.get('[data-testid="bullets"]').should('contain', 'Prioritize tasks with AI intelligence')
    cy.get('[data-testid="cta"]').should('contain', 'Start Free Trial')

    // Verify live preview
    cy.get('[data-testid="live-preview"]').should('be.visible')
    cy.get('[data-testid="live-preview"] h1').should('contain', 'Master Your Tasks, Master Your Business')

    // Test copy functionality
    cy.get('[data-testid="copy-headline"]').click()
    cy.window().its('navigator.clipboard').invoke('readText').should('contain', 'Master Your Tasks')

    // Verify payment button is present
    cy.get('[data-testid="payment-button"]').should('be.visible').and('contain', 'Purchase for R9')
  })

  it('should handle API errors gracefully', () => {
    // Mock API error
    cy.intercept('POST', '/api/generate', {
      statusCode: 500,
      body: { error: 'Failed to generate copy. Please try again.' }
    }).as('generateError')

    // Fill minimal form data
    cy.get('[data-testid="product-name"]').type('Test Product')
    cy.get('[data-testid="features"]').type('Test features description')
    cy.get('[data-testid="target-customer"]').type('Test customers')

    // Submit form
    cy.get('[data-testid="generate-button"]').click()

    // Wait for error
    cy.wait('@generateError')

    // Verify error message is displayed
    cy.get('[data-testid="error-alert"]').should('be.visible')
      .and('contain', 'Failed to generate copy. Please try again.')

    // Verify form is still visible for retry
    cy.get('[data-testid="generate-form"]').should('be.visible')
  })

  it('should validate form inputs', () => {
    // Try to submit empty form
    cy.get('[data-testid="generate-button"]').click()

    // Check validation errors
    cy.get('[data-testid="product-name-error"]').should('contain', 'Product name is required')
    cy.get('[data-testid="features-error"]').should('contain', 'Please provide more details')
    cy.get('[data-testid="target-customer-error"]').should('contain', 'Please describe your target customer')

    // Test character limits
    cy.get('[data-testid="features"]').type('a'.repeat(501))
    cy.get('[data-testid="features-error"]').should('contain', 'maximum')
  })

  it('should handle payment flow', () => {
    // First generate copy
    cy.get('[data-testid="product-name"]').type('Test Product')
    cy.get('[data-testid="features"]').type('Amazing features that solve problems')
    cy.get('[data-testid="target-customer"]').type('Target customers who need solutions')

    cy.intercept('POST', '/api/generate', { fixture: 'copy-response.json' }).as('generateCopy')
    cy.get('[data-testid="generate-button"]').click()
    cy.wait('@generateCopy')

    // Mock Paystack
    cy.window().then((win) => {
      win.PaystackPop = {
        setup: cy.stub().returns({
          openIframe: cy.stub()
        })
      }
    })

    // Mock webhook call
    cy.intercept('POST', '**/webhook/payment-success', {
      statusCode: 200,
      body: { status: 'success' }
    }).as('webhookCall')

    // Click payment button
    cy.get('[data-testid="payment-button"]').click()

    // Verify Paystack was called with correct parameters
    cy.window().its('PaystackPop.setup').should('have.been.called')
  })
})