import http from 'k6/http'
import { check, sleep } from 'k6'
import { Rate } from 'k6/metrics'

export const errorRate = new Rate('errors')

export const options = {
  stages: [
    { duration: '2m', target: 10 }, // Ramp up to 10 users
    { duration: '5m', target: 10 }, // Stay at 10 users
    { duration: '2m', target: 20 }, // Ramp up to 20 users
    { duration: '5m', target: 20 }, // Stay at 20 users
    { duration: '2m', target: 50 }, // Ramp up to 50 users
    { duration: '5m', target: 50 }, // Stay at 50 users
    { duration: '5m', target: 0 },  // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<5000'], // 95% of requests must complete below 5s
    http_req_failed: ['rate<0.1'],     // Error rate must be below 10%
    errors: ['rate<0.1'],
  },
}

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000'

export default function () {
  const payload = JSON.stringify({
    productName: 'TaskMaster Pro',
    features: 'Advanced task management with AI-powered prioritization, team collaboration tools, and automated reporting features that save 5+ hours per week.',
    targetCustomer: 'Busy entrepreneurs and small business owners who struggle with task prioritization and team coordination.',
    industry: 'SaaS',
    tone: 'professional'
  })

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  }

  // Test API endpoint
  const response = http.post(`${BASE_URL}/api/generate`, payload, params)
  
  const success = check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 5000ms': (r) => r.timings.duration < 5000,
    'response has headline': (r) => {
      try {
        const body = JSON.parse(r.body)
        return body.headline && body.headline.length > 0
      } catch {
        return false
      }
    },
    'response has valid structure': (r) => {
      try {
        const body = JSON.parse(r.body)
        return body.headline && body.subheadline && body.bullets && body.cta
      } catch {
        return false
      }
    }
  })

  errorRate.add(!success)

  // Test health endpoint
  const healthResponse = http.get(`${BASE_URL}/api/generate`)
  check(healthResponse, {
    'health check status is 200': (r) => r.status === 200,
  })

  sleep(1)
}