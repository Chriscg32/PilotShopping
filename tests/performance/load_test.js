// K6 Load Testing Script for ButterflyBlue Creations
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up
    { duration: '1m', target: 50 },   // Stay at 50 users
    { duration: '30s', target: 100 }, // Ramp to 100 users
    { duration: '2m', target: 100 },  // Stay at 100 users
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests under 2s
    http_req_failed: ['rate<0.1'],     // Error rate under 10%
    errors: ['rate<0.1'],
  },
};

const BASE_URL = 'http://localhost:8000';

export default function () {
  // Test health endpoint
  let healthResponse = http.get(`${BASE_URL}/health`);
  check(healthResponse, {
    'health check status is 200': (r) => r.status === 200,
    'health check response time < 500ms': (r) => r.timings.duration < 500,
  }) || errorRate.add(1);

  // Test agent status
  let agentResponse = http.get(`${BASE_URL}/api/agents/status`);
  check(agentResponse, {
    'agent status is 200': (r) => r.status === 200,
    'agent response has agents': (r) => JSON.parse(r.body).agents.length > 0,
  }) || errorRate.add(1);

  // Test marketing agent demo
  let marketingPayload = JSON.stringify({
    campaign_type: 'social_media',
    target_audience: 'small businesses',
    budget: 1000
  });
  
  let marketingResponse = http.post(`${BASE_URL}/api/agents/marketing/demo`, marketingPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(marketingResponse, {
    'marketing demo status is 200': (r) => r.status === 200,
    'marketing demo has result': (r) => JSON.parse(r.body).result !== undefined,
  }) || errorRate.add(1);

  // Test finance agent demo
  let financePayload = JSON.stringify({
    action: 'generate_invoice',
    amount: 299.00,
    currency: 'ZAR'
  });
  
  let financeResponse = http.post(`${BASE_URL}/api/agents/finance/demo`, financePayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(financeResponse, {
    'finance demo status is 200': (r) => r.status === 200,
    'finance demo has invoice': (r) => JSON.parse(r.body).result.invoice !== undefined,
  }) || errorRate.add(1);

  sleep(1); // Wait 1 second between iterations
}

export function handleSummary(data) {
  return {
    'performance-report.html': htmlReport(data),
    'performance-summary.json': JSON.stringify(data),
  };
}

function htmlReport(data) {
  return `
<!DOCTYPE html>
<html>
<head>
    <title>ButterflyBlue Performance Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .metric { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .pass { color: green; } .fail { color: red; }
    </style>
</head>
<body>
    <h1>🦋 ButterflyBlue Performance Test Report</h1>
    <div class="metric">
        <h3>Request Duration (95th percentile)</h3>
        <p class="${data.metrics.http_req_duration.values.p95 < 2000 ? 'pass' : 'fail'}">
            ${data.metrics.http_req_duration.values.p95.toFixed(2)}ms
        </p>
    </div>
    <div class="metric">
        <h3>Error Rate</h3>
        <p class="${data.metrics.http_req_failed.values.rate < 0.1 ? 'pass' : 'fail'}">
            ${(data.metrics.http_req_failed.values.rate * 100).toFixed(2)}%
        </p>
    </div>
    <div class="metric">
        <h3>Total Requests</h3>
        <p>${data.metrics.http_reqs.values.count}</p>
    </div>
</body>
</html>`;
}