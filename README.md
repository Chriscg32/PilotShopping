# 🚀 AI Landing Copy Generator

A powerful, production-ready application that generates compelling landing page copy using AI. Built for bootstrapped founders who need professional copy without the professional price tag.

## ✨ Features

- **AI-Powered Copy Generation** - Uses Hugging Face transformers for high-quality copy
- **Instant Payment Processing** - Integrated with Paystack for seamless R9 payments
- **Automated Workflows** - n8n automation for email delivery and customer management
- **Real-time Preview** - See how your copy looks on an actual landing page
- **Export Options** - Download copy in multiple formats
- **Performance Optimized** - Built with Next.js 14 and optimized for speed
- **Comprehensive Testing** - Unit, integration, and E2E tests included
- **Production Ready** - Full CI/CD pipeline with monitoring and error tracking

## 🛠️ Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes, Hugging Face API
- **Payments**: Paystack
- **Automation**: n8n
- **Database**: Upstash Redis
- **Deployment**: Vercel
- **Monitoring**: Sentry, Vercel Analytics
- **Testing**: Jest, Cypress, k6

## 🚀 Quick Start

1. **Clone and setup**
```bash
git clone <repository-url>
cd ai-landing-copy-generator
chmod +x scripts/setup.sh
./scripts/setup.sh
```

2. **Configure environment variables**
```bash
cp .env.example .env.local
# Edit .env.local with your API keys
```

3. **Start development server**
```bash
npm run dev
```

4. **Visit http://localhost:3000**

## 📋 Environment Variables

Create a `.env.local` file with the following variables:

```env
# Hugging Face API
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Paystack
NEXT_PUBLIC_PAYSTACK_KEY=pk_test_your_paystack_public_key
PAYSTACK_SECRET_KEY=sk_test_your_paystack_secret_key

# Redis (Optional - for caching)
UPSTASH_REDIS_REST_URL=your_redis_url
UPSTASH_REDIS_REST_TOKEN=your_redis_token

# Monitoring (Optional)
SENTRY_DSN=your_sentry_dsn
NEXT_PUBLIC_GTM_ID=your_google_tag_manager_id

# n8n Webhook URL
N8N_WEBHOOK_URL=http://localhost:5678/webhook/paystack-success
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e

# Load testing
npm run test:load

# Type checking
npm run type-check
```

## 🚀 Deployment

### Automatic Deployment (Recommended)

Push to `main` branch for production or `develop` for staging. GitHub Actions will handle the rest.

### Manual Deployment

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 🤖 n8n Automation Setup

1. **Start n8n locally**
```bash
npm run docker:n8n
```

2. **Access n8n at http://localhost:5678**
   - Username: `admin`
   - Password: `changeme123`

3. **Import workflow**
   - Go to Workflows → Import
   - Upload `n8n/workflows/paystack-payment-automation.json`

4. **Configure credentials**
   - Paystack API credentials
   - Email service credentials
   - MailerLite API key
   - Slack webhook URL

## 📊 Monitoring & Analytics

- **Health Check**: `/api/health`
- **Sentry**: Error tracking and performance monitoring
- **Vercel Analytics**: User behavior and conversion tracking
- **Custom Metrics**: API response times, generation success rates

## 🔧 Development

### Project Structure

```
├── app/                    # Next.js 14 app directory
│   ├── api/               # API routes
│   ├── components/        # React components
│   ├── lib/              # Utility functions
│   └── globals.css       # Global styles
├── cypress/              # E2E tests
├── k6/                   # Load tests
├── n8n/                  # Automation workflows
├── scripts/              # Deployment scripts
└── __tests__/            # Unit tests
```

### Key Components

- **GenerateForm**: Main form for copy generation
- **CopyResult**: Displays generated copy with preview
- **PayButton**: Handles Paystack payment integration
- **ErrorBoundary**: Catches and handles React errors

### API Endpoints

- `POST /api/generate` - Generate landing copy
- `GET /api/health` - Health check endpoint
- `POST /webhook/payment-success` - Payment webhook (n8n)

## 💰 Business Model

- **Price**: R9 per copy generation
- **Payment**: Paystack (supports South African Rand)
- **Delivery**: Instant via email after payment
- **Target**: Bootstrapped founders and small businesses

## 🔒 Security

- Input validation with Zod schemas
- Rate limiting on API endpoints
- Secure payment processing with Paystack
- Environment variable protection
- CORS configuration
- Error boundary implementation

## 📈 Performance

- **Lighthouse Score**: 95+ on all metrics
- **API Response Time**: <2s for copy generation
- **Caching**: Redis for frequently requested content
- **CDN**: Vercel Edge Network
- **Image Optimization**: Next.js automatic optimization

## 🐛 Troubleshooting

### Common Issues

1. **Hugging Face API Timeout**
   - Check API key validity
   - Verify model availability
   - Implement retry logic

2. **Payment Not Processing**
   - Verify Paystack credentials
   - Check webhook URL configuration
   - Ensure n8n is running

3. **n8n Workflow Not Triggering**
   - Check webhook URL in environment
   - Verify n8n is accessible
   - Check workflow activation status

### Debug Mode

```bash
# Enable debug logging
DEBUG=* npm run dev

# Check API health
curl http://localhost:3000/api/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Hugging Face for AI models
- Paystack for payment processing
- n8n for automation workflows
- Vercel for hosting and deployment
- The open-source community

## 📞 Support

- **Email**: support@ailandingcopy.com
- **Documentation**: [docs.ailandingcopy.com](https://docs.ailandingcopy.com)
- **Issues**: GitHub Issues
- **Discord**: [Join our community](https://discord.gg/ailandingcopy)

---

Built with ❤️ for the bootstrap community