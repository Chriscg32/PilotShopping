import { AgentBase } from '../base/agent-base.mjs';
import mqtt from 'mqtt';
import axios from 'axios';

export class FinanceAgent extends AgentBase {
  constructor() {
    super('finance');
    this.mqttClient = null;
    this.paymentProcessors = {
      paystack: process.env.PAYSTACK_SECRET_KEY,
      paypal: {
        clientId: process.env.PAYPAL_CLIENT_ID,
        clientSecret: process.env.PAYPAL_CLIENT_SECRET
      }
    };
  }

  async initialize() {
    await super.initialize();
    
    // Connect to MQTT
    this.mqttClient = mqtt.connect(process.env.MQTT_URL || 'mqtt://localhost:1883');
    
    this.mqttClient.on('connect', () => {
      this.logger.info('Finance Agent connected to MQTT');
      this.mqttClient.subscribe('agents/finance/tasks/new');
      
      // Report status to boss
      this.mqttClient.publish('agents/finance/status', JSON.stringify({
        status: 'active',
        capabilities: ['payment_processing', 'invoice_generation', 'financial_analysis'],
        timestamp: new Date().toISOString()
      }));
    });

    this.mqttClient.on('message', async (topic, message) => {
      if (topic === 'agents/finance/tasks/new') {
        const task = JSON.parse(message.toString());
        const result = await this.processTask(task);
        
        // Report completion
        this.mqttClient.publish('agents/finance/tasks/completed', JSON.stringify(result));
      }
    });
  }

  async executeTask(task) {
    const { type, payload } = task;
    
    switch (type) {
      case 'financial':
        return await this.processFinancialTask(payload);
      case 'payment':
        return await this.processPayment(payload);
      case 'invoice':
        return await this.generateInvoice(payload);
      case 'analysis':
        return await this.performFinancialAnalysis(payload);
      default:
        return { 
          message: 'Financial task processed', 
          data: payload,
          timestamp: new Date().toISOString()
        };
    }
  }

  async processFinancialTask(payload) {
    this.logger.info('Processing financial task:', payload);
    
    // Simulate financial processing
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
      status: 'completed',
      type: 'financial_processing',
      result: {
        processed: true,
        amount: payload.amount || 0,
        currency: payload.currency || 'USD',
        transactionId: `txn_${Date.now()}`,
        timestamp: new Date().toISOString()
      }
    };
  }

  async processPayment(payload) {
    const { amount, currency = 'USD', customerId, paymentMethod = 'paystack' } = payload;
    
    this.logger.info(`Processing payment: ${amount} ${currency} for customer ${customerId}`);
    
    try {
      let paymentResult;
      
      if (paymentMethod === 'paystack' && this.paymentProcessors.paystack) {
        paymentResult = await this.processPaystackPayment(payload);
      } else if (paymentMethod === 'paypal' && this.paymentProcessors.paypal.clientId) {
        paymentResult = await this.processPayPalPayment(payload);
      } else {
        // Simulate payment for development
        paymentResult = await this.simulatePayment(payload);
      }
      
      // Trigger invoice generation
      await this.triggerInvoiceGeneration(paymentResult);
      
      return paymentResult;
      
    } catch (error) {
      this.logger.error('Payment processing failed:', error);
      return {
        status: 'failed',
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  async processPaystackPayment(payload) {
    const { amount, currency, customerId, email } = payload;
    
    try {
      const response = await axios.post(
        'https://api.paystack.co/transaction/initialize',
        {
          amount: amount * 100, // Paystack uses kobo
          currency,
          email,
          reference: `ref_${Date.now()}_${customerId}`,
          callback_url: process.env.PAYSTACK_CALLBACK_URL
        },
        {
          headers: {
            Authorization: `Bearer ${this.paymentProcessors.paystack}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      return {
        status: 'success',
        provider: 'paystack',
        reference: response.data.data.reference,
        authorization_url: response.data.data.authorization_url,
        amount,
        currency,
        customerId,
        timestamp: new Date().toISOString()
      };
      
    } catch (error) {
      throw new Error(`Paystack payment failed: ${error.message}`);
    }
  }

  async processPayPalPayment(payload) {
    // PayPal implementation would go here
    // For now, simulate PayPal payment
    return await this.simulatePayment({ ...payload, provider: 'paypal' });
  }

  async simulatePayment(payload) {
    const { amount, currency = 'USD', customerId, provider = 'simulation' } = payload;
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Simulate 95% success rate
    const isSuccess = Math.random() > 0.05;
    
    if (!isSuccess) {
      throw new Error('Simulated payment failure');
    }
    
    return {
      status: 'success',
      provider,
      transactionId: `sim_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      amount,
      currency,
      customerId,
      timestamp: new Date().toISOString()
    };
  }

  async generateInvoice(payload) {
    const { customerId, items, amount, currency = 'USD', dueDate } = payload;
    
    this.logger.info(`Generating invoice for customer ${customerId}`);
    
    const invoice = {
      invoiceId: `inv_${Date.now()}`,
      customerId,
      items: items || [{ description: 'Service', amount }],
      subtotal: amount,
      tax: amount * 0.1, // 10% tax
      total: amount * 1.1,
      currency,
      issueDate: new Date().toISOString(),
      dueDate: dueDate || new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days
      status: 'pending'
    };
    
    // Store invoice (in production, save to database)
    this.logger.info('Invoice generated:', invoice);
    
    // Notify customer service
    this.mqttClient.publish('events/invoice_generated', JSON.stringify({
      type: 'invoice_generated',
      payload: invoice
    }));
    
    return {
      status: 'completed',
      invoice,
      timestamp: new Date().toISOString()
    };
  }

  async performFinancialAnalysis(payload) {
    const { period = '30d', metrics = ['revenue', 'transactions', 'customers'] } = payload;
    
    this.logger.info(`Performing financial analysis for period: ${period}`);
    
    // Simulate financial analysis
    const analysis = {
      period,
      metrics: {},
      timestamp: new Date().toISOString()
    };
    
    if (metrics.includes('revenue')) {
      analysis.metrics.revenue = {
        total: Math.floor(Math.random() * 100000) + 50000,
        growth: (Math.random() * 20 - 10).toFixed(2) + '%',
        currency: 'USD'
      };
    }
    
    if (metrics.includes('transactions')) {
      analysis.metrics.transactions = {
        total: Math.floor(Math.random() * 1000) + 500,
        successful: Math.floor(Math.random() * 950) + 450,
        failed: Math.floor(Math.random() * 50) + 10,
        averageAmount: (Math.random() * 200 + 50).toFixed(2)
      };
    }
    
    if (metrics.includes('customers')) {
      analysis.metrics.customers = {
        total: Math.floor(Math.random() * 500) + 200,
        new: Math.floor(Math.random() * 50) + 10,
        returning: Math.floor(Math.random() * 100) + 50
      };
    }
    
    return {
      status: 'completed',
      analysis,
      timestamp: new Date().toISOString()
    };
  }

  async triggerInvoiceGeneration(paymentResult) {
    if (paymentResult.status === 'success') {
      const invoiceTask = {
        id: this.generateTaskId(),
        type: 'invoice',
        payload: {
          customerId: paymentResult.customerId,
          amount: paymentResult.amount,
          currency: paymentResult.currency,
          transactionId: paymentResult.transactionId
        }
      };
      
      // Self-delegate invoice generation
      setTimeout(() => {
        this.processTask(invoiceTask);
      }, 1000);
    }
  }

  async shutdown() {
    this.logger.info('Shutting down Finance Agent...');
    
    if (this.mqttClient) {
      this.mqttClient.end();
    }
    
    await super.shutdown();
  }
}

// Auto-start if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const financeAgent = new FinanceAgent();
  financeAgent.initialize().catch(console.error);
}