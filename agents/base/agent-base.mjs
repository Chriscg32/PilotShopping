import { EventEmitter } from 'events';
import { createLogger } from '../../services/logger.mjs';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

export class AgentBase extends EventEmitter {
  constructor(agentType) {
    super();
    this.agentType = agentType;
    this.id = uuidv4();
    this.status = 'initializing';
    this.logger = createLogger(agentType);
    this.tasks = new Map();
    this.performance = {
      tasksCompleted: 0,
      tasksSuccessful: 0,
      tasksFailed: 0,
      averageResponseTime: 0,
      lastActive: new Date()
    };
  }

  async initialize() {
    this.status = 'active';
    this.logger.info(`${this.agentType} agent initialized with ID: ${this.id}`);
    
    // Start health monitoring
    this.startHealthMonitoring();
    
    // Start self-learning loop
    this.startSelfLearning();
  }

  async processTask(task) {
    const startTime = Date.now();
    
    try {
      this.logger.info(`Processing task: ${task.id}`);
      this.tasks.set(task.id, { ...task, status: 'processing', startTime });
      
      // Override this method in child classes
      const result = await this.executeTask(task);
      
      const endTime = Date.now();
      const responseTime = endTime - startTime;
      
      // Update performance metrics
      this.updatePerformance(true, responseTime);
      
      // Mark task as completed
      this.tasks.set(task.id, { 
        ...task, 
        status: 'completed', 
        result, 
        responseTime,
        completedAt: new Date()
      });
      
      this.logger.info(`Task ${task.id} completed successfully in ${responseTime}ms`);
      
      return {
        success: true,
        taskId: task.id,
        result,
        responseTime,
        agentId: this.id,
        agentType: this.agentType
      };
      
    } catch (error) {
      this.logger.error(`Task ${task.id} failed:`, error);
      this.updatePerformance(false, Date.now() - startTime);
      
      return {
        success: false,
        taskId: task.id,
        error: error.message,
        agentId: this.id,
        agentType: this.agentType
      };
    }
  }

  async executeTask(task) {
    // Override this method in child classes
    throw new Error('executeTask method must be implemented by child class');
  }

  async generateEmbedding(text) {
    try {
      // For development, return a dummy embedding
      // In production, use Hugging Face API
      if (!process.env.HUGGINGFACE_API_KEY) {
        this.logger.warn('No Hugging Face API key found, using dummy embedding');
        return new Array(384).fill(0).map(() => Math.random() - 0.5);
      }

      const response = await axios.post(
        'https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2',
        { inputs: text },
        {
          headers: {
            'Authorization': `Bearer ${process.env.HUGGINGFACE_API_KEY}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      return response.data;
    } catch (error) {
      this.logger.error('Error generating embedding:', error);
      // Return dummy embedding for development
      return new Array(384).fill(0).map(() => Math.random() - 0.5);
    }
  }

  updatePerformance(success, responseTime) {
    this.performance.tasksCompleted++;
    this.performance.lastActive = new Date();
    
    if (success) {
      this.performance.tasksSuccessful++;
    } else {
      this.performance.tasksFailed++;
    }
    
    // Update average response time
    const totalTasks = this.performance.tasksCompleted;
    this.performance.averageResponseTime = 
      (this.performance.averageResponseTime * (totalTasks - 1) + responseTime) / totalTasks;
  }

  startHealthMonitoring() {
    setInterval(() => {
      this.reportHealth();
    }, 30000); // Report health every 30 seconds
  }

  reportHealth() {
    const healthReport = {
      agentId: this.id,
      agentType: this.agentType,
      status: this.status,
      performance: this.performance,
      activeTasks: this.tasks.size,
      timestamp: new Date().toISOString()
    };
    
    this.emit('health-report', healthReport);
  }

  startSelfLearning() {
    setInterval(async () => {
      await this.analyzePastPerformance();
    }, 300000); // Analyze every 5 minutes
  }

  async analyzePastPerformance() {
    const completedTasks = Array.from(this.tasks.values())
      .filter(task => task.status === 'completed');
    
    if (completedTasks.length < 5) return; // Need minimum data
    
    // Analyze patterns and optimize
    const avgResponseTime = completedTasks.reduce((sum, task) => 
      sum + task.responseTime, 0) / completedTasks.length;
    
    if (avgResponseTime > this.performance.averageResponseTime * 1.2) {
      this.logger.warn('Performance degradation detected, initiating self-optimization');
      await this.optimizePerformance();
    }
  }

  async optimizePerformance() {
    // Override in child classes for specific optimizations
    this.logger.info('Running generic performance optimization');
  }

  generateTaskId() {
    return `${this.agentType}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  getStatus() {
    return {
      id: this.id,
      type: this.agentType,
      status: this.status,
      performance: this.performance,
      activeTasks: this.tasks.size
    };
  }

  async shutdown() {
    this.logger.info(`Shutting down ${this.agentType} agent`);
    this.status = 'shutdown';
  }
}