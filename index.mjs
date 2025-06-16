import dotenv from 'dotenv';
import { createLogger } from './services/logger.mjs';
import { BossAgent } from './agents/boss/index.mjs';

// Load environment variables
dotenv.config();

const logger = createLogger('main');

async function startAISaaSPlatform() {
  try {
    logger.info('🚀 Starting AI SaaS Platform...');
    
    // Initialize Boss Agent (orchestrates everything)
    const bossAgent = new BossAgent();
    await bossAgent.initialize();
    
    // Handle graceful shutdown
    process.on('SIGINT', async () => {
      logger.info('Shutting down AI SaaS Platform...');
      await bossAgent.shutdown();
      process.exit(0);
    });
    
    logger.info('✅ AI SaaS Platform started successfully!');
    logger.info('🌐 Services available at:');
    logger.info('  - n8n Workflow Editor: http://localhost:5678 (admin/admin123)');
    logger.info('  - Qdrant Vector DB: http://localhost:6333');
    logger.info('  - MQTT Broker: mqtt://localhost:1883');
    
  } catch (error) {
    logger.error('Failed to start AI SaaS Platform:', error);
    process.exit(1);
  }
}

// Start the platform
startAISaaSPlatform();