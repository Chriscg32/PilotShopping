import mqtt from 'mqtt';
import { QdrantClient } from '@qdrant/js-client-rest';
import axios from 'axios';
import { createLogger } from '../../services/logger.mjs';
import { AgentBase } from '../base/agent-base.mjs';

export class BossAgent extends AgentBase {
  constructor() {
    super('boss');
    this.subordinateAgents = [
      'finance', 'design', 'engineering', 
      'legal', 'marketing', 'customer-success', 'security'
    ];
    this.taskQueue = [];
    this.agentPerformance = new Map();
    this.mqttClient = null;
    this.qdrantClient = null;
  }

  async initialize() {
    await super.initialize();
    
    try {
      // Connect to MQTT
      this.mqttClient = mqtt.connect(process.env.MQTT_URL || 'mqtt://localhost:1883');
      
      // Connect to Qdrant
      this.qdrantClient = new QdrantClient({
        url: process.env.QDRANT_URL || 'http://localhost:6333'
      });

      // Setup MQTT listeners
      this.setupMQTTListeners();
      
      // Initialize Qdrant collections
      await this.initializeQdrantCollections();
      
      // Start task delegation loop
      this.startTaskDelegationLoop();
      
      // Send a test event
      setTimeout(() => {
        this.sendTestEvent();
      }, 5000);
      
      this.logger.info('Boss Agent initialized successfully');
    } catch (error) {
      this.logger.error('Error initializing Boss Agent:', error);
    }
  }

  async initializeQdrantCollections() {
    try {
      // Create tasks collection if it doesn't exist
      const collections = await this.qdrantClient.getCollections();
      const hasTasksCollection = collections.collections.some(c => c.name === 'tasks');
      
      if (!hasTasksCollection) {
        await this.qdrantClient.createCollection('tasks', {
          vectors: {
            size: 384,
            distance: 'Cosine'
          }
        });
        this.logger.info('Created tasks collection in Qdrant');
      }
    } catch (error) {
      this.logger.error('Error initializing Qdrant collections:', error);
    }
  }

  setupMQTTListeners() {
    this.mqttClient.on('connect', () => {
      this.logger.info('Connected to MQTT broker');
      
      // Subscribe to all agent channels
      this.mqttClient.subscribe('agents/+/status');
      this.mqttClient.subscribe('agents/+/tasks/completed');
      this.mqttClient.subscribe('events/+');
      this.mqttClient.subscribe('tasks/new');
    });

    this.mqttClient.on('message', async (topic, message) => {
      try {
        const data = JSON.parse(message.toString());
        await this.handleMessage(topic, data);
      } catch (error) {
        this.logger.error('Error processing MQTT message:', error);
      }
    });

    this.mqttClient.on('error', (error) => {
      this.logger.error('MQTT connection error:', error);
    });
  }

  async handleMessage(topic, data) {
    const topicParts = topic.split('/');
    
    if (topic.startsWith('agents/') && topic.endsWith('/status')) {
      const agentName = topicParts[1];
      this.updateAgentStatus(agentName, data);
    } else if (topic.startsWith('agents/') && topic.includes('/tasks/completed')) {
      const agentName = topicParts[1];
      await this.handleTaskCompletion(agentName, data);
    } else if (topic.startsWith('events/')) {
      await this.processEvent(data);
    } else if (topic === 'tasks/new') {
      await this.addTask(data);
    }
  }

  async processEvent(eventData) {
    // Process incoming events and create tasks
    const { type, payload, priority = 'medium' } = eventData;
    
    // Use AI to classify and route the event
    const classification = await this.classifyEvent(eventData);
    
    const task = {
      id: this.generateTaskId(),
      type: classification.taskType,
      assignedAgent: classification.bestAgent,
      payload,
      priority,
      createdAt: new Date().toISOString(),
      status: 'pending'
    };

    await this.addTask(task);
  }

  async classifyEvent(eventData) {
    try {
      // Simple classification logic (enhance with better AI model)
      const text = eventData.type?.toLowerCase() || '';
      
      if (text.includes('payment') || text.includes('invoice')) {
        return { taskType: 'financial', bestAgent: 'finance' };
      } else if (text.includes('design') || text.includes('ui')) {
        return { taskType: 'design', bestAgent: 'design' };
      } else if (text.includes('customer') || text.includes('support')) {
        return { taskType: 'support', bestAgent: 'customer-success' };
      } else if (text.includes('marketing') || text.includes('campaign')) {
        return { taskType: 'marketing', bestAgent: 'marketing' };
      } else {
        return { taskType: 'general', bestAgent: 'engineering' };
      }
    } catch (error) {
      this.logger.error('Error classifying event:', error);
      return { taskType: 'general', bestAgent: 'engineering' };
    }
  }

  async addTask(task) {
    this.taskQueue.push(task);
    this.logger.info(`Added task ${task.id} to queue for agent ${task.assignedAgent}`);
    
    // Store task in vector database
    try {
      const embedding = await this.generateEmbedding(JSON.stringify(task));
      await this.qdrantClient.upsert('tasks', {
        points: [{
          id: task.id,
          vector: embedding,
          payload: task
        }]
      });
    } catch (error) {
      this.logger.error('Error storing task in vector DB:', error);
    }
  }

  startTaskDelegationLoop() {
    setInterval(async () => {
      await this.delegateTasks();
    }, 5000); // Check every 5 seconds
  }

  async delegateTasks() {
    if (this.taskQueue.length === 0) return;

    // Sort tasks by priority
    this.taskQueue.sort((a, b) => {
      const priorityOrder = { high: 3, medium: 2, low: 1 };
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    });

    for (const task of this.taskQueue.slice(0, 5)) { // Process up to 5 tasks at once
      await this.delegateTask(task);
      this.taskQueue = this.taskQueue.filter(t => t.id !== task.id);
    }
  }

  async delegateTask(task) {
    const agentTopic = `agents/${task.assignedAgent}/tasks/new`;
    
    this.mqttClient.publish(agentTopic, JSON.stringify(task));
    this.logger.info(`Delegated task ${task.id} to ${task.assignedAgent} agent`);
  }

  updateAgentStatus(agentName, statusData) {
    this.agentPerformance.set(agentName, {
      ...this.agentPerformance.get(agentName),
      ...statusData,
      lastUpdate: new Date()
    });
  }

  async handleTaskCompletion(agentName, taskData) {
    this.logger.info(`Task ${taskData.taskId} completed by ${agentName} agent`);
    
    // Update agent performance
    const currentPerf = this.agentPerformance.get(agentName) || {};
    this.agentPerformance.set(agentName, {
      ...currentPerf,
      tasksCompleted: (currentPerf.tasksCompleted || 0) + 1,
      lastTaskCompletion: new Date()
    });

    // Analyze task completion for learning
    await this.analyzeTaskCompletion(taskData);
  }

  async analyzeTaskCompletion(taskData) {
    // Use this data to improve future task routing
    try {
      const embedding = await this.generateEmbedding(JSON.stringify(taskData));
      
      // Store completion data for future analysis
      await this.qdrantClient.upsert('tasks', {
        points: [{
          id: `${taskData.taskId}-completion`,
          vector: embedding,
          payload: {
            ...taskData,
            type: 'completion',
            timestamp: new Date().toISOString()
          }
        }]
      });
    } catch (error) {
      this.logger.error('Error analyzing task completion:', error);
    }
  }

  sendTestEvent() {
    const testEvents = [
      {
        type: 'customer_inquiry',
        payload: { message: 'Customer needs help with billing', customerId: '12345' },
        priority: 'high'
      },
      {
        type: 'design_request',
        payload: { request: 'Update landing page design', projectId: 'proj-001' },
        priority: 'medium'
      },
      {
        type: 'payment_received',
        payload: { amount: 99.99, customerId: '12345', planId: 'premium' },
        priority: 'high'
      }
    ];

    testEvents.forEach((event, index) => {
      setTimeout(() => {
        this.mqttClient.publish('events/test', JSON.stringify(event));
        this.logger.info(`Sent test event: ${event.type}`);
      }, index * 2000);
    });
  }

  async executeTask(task) {
    // Boss agent handles high-level coordination tasks
    switch (task.type) {
      case 'coordinate':
        return await this.coordinateAgents(task.payload);
      case 'analyze':
        return await this.analyzeSystemPerformance();
      case 'optimize':
        return await this.optimizeSystemPerformance();
      default:
        return { message: 'Task delegated to appropriate agent' };
    }
  }

  async coordinateAgents(payload) {
    const { agents, objective } = payload;
    
    // Create coordination plan
    const plan = {
      objective,
      agents,
      steps: [],
      estimatedCompletion: new Date(Date.now() + 3600000) // 1 hour from now
    };

    // Send coordination instructions to each agent
    for (const agent of agents) {
      const coordinationTask = {
        id: this.generateTaskId(),
        type: 'coordination',
        objective,
        assignedAgent: agent,
        priority: 'high'
      };

      await this.addTask(coordinationTask);
    }

    return plan;
  }

  async analyzeSystemPerformance() {
    const performance = {
      totalAgents: this.subordinateAgents.length,
      activeAgents: this.agentPerformance.size,
      totalTasksProcessed: Array.from(this.agentPerformance.values())
        .reduce((sum, agent) => sum + (agent.tasksCompleted || 0), 0),
      averageResponseTime: this.performance.averageResponseTime,
      systemHealth: this.calculateSystemHealth()
    };

    this.logger.info('System performance analysis:', performance);
    return performance;
  }

  calculateSystemHealth() {
    const activeAgents = this.agentPerformance.size;
    const totalAgents = this.subordinateAgents.length;
    const healthScore = (activeAgents / totalAgents) * 100;
    
    if (healthScore >= 80) return 'excellent';
    if (healthScore >= 60) return 'good';
    if (healthScore >= 40) return 'fair';
    return 'poor';
  }

  async optimizeSystemPerformance() {
    // Implement system optimization logic
    const optimizations = [];

    // Check for overloaded agents
    for (const [agentName, performance] of this.agentPerformance.entries()) {
      if (performance.tasksCompleted > 100) { // Threshold
        optimizations.push({
          type: 'load_balancing',
          agent: agentName,
          action: 'redistribute_tasks'
        });
      }
    }

    return { optimizations, timestamp: new Date().toISOString() };
  }

  async shutdown() {
    this.logger.info('Shutting down Boss Agent...');
    
    if (this.mqttClient) {
      this.mqttClient.end();
    }
    
    await super.shutdown();
  }
}