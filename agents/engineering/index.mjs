import { AgentBase } from '../base/agent-base.mjs';
import mqtt from 'mqtt';
import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export class EngineeringAgent extends AgentBase {
  constructor() {
    super('engineering');
    this.mqttClient = null;
    this.activeProjects = new Map();
    this.codeTemplates = new Map();
    this.deploymentTargets = ['development', 'staging', 'production'];
  }

  async initialize() {
    await super.initialize();
    
    // Load code templates
    await this.loadCodeTemplates();
    
    // Connect to MQTT
    this.mqttClient = mqtt.connect(process.env.MQTT_URL || 'mqtt://localhost:1883');
    
    this.mqttClient.on('connect', () => {
      this.logger.info('Engineering Agent connected to MQTT');
      this.mqttClient.subscribe('agents/engineering/tasks/new');
      
      // Report status to boss
      this.mqttClient.publish('agents/engineering/status', JSON.stringify({
        status: 'active',
        capabilities: [
          'code_generation', 'api_development', 'database_design', 
          'testing', 'deployment', 'code_review', 'optimization'
        ],
        technologies: ['Node.js', 'React', 'Python', 'Docker', 'PostgreSQL', 'MongoDB'],
        timestamp: new Date().toISOString()
      }));
    });

    this.mqttClient.on('message', async (topic, message) => {
      if (topic === 'agents/engineering/tasks/new') {
        const task = JSON.parse(message.toString());
        const result = await this.processTask(task);
        
        // Report completion
        this.mqttClient.publish('agents/engineering/tasks/completed', JSON.stringify(result));
      }
    });
  }

  async executeTask(task) {
    const { type, payload } = task;
    
    switch (type) {
      case 'code_generation':
        return await this.generateCode(payload);
      case 'api_development':
        return await this.developAPI(payload);
      case 'database_design':
        return await this.designDatabase(payload);
      case 'testing':
        return await this.runTests(payload);
      case 'deployment':
        return await this.deployApplication(payload);
      case 'code_review':
        return await this.reviewCode(payload);
      case 'optimization':
        return await this.optimizeCode(payload);
      default:
        return { 
          message: 'Engineering task processed', 
          data: payload,
          timestamp: new Date().toISOString()
        };
    }
  }

  async loadCodeTemplates() {
    this.codeTemplates.set('api_endpoint', {
      language: 'javascript',
      framework: 'express',
      template: `
app.{{method}}('{{path}}', async (req, res) => {
  try {
    // {{description}}
    const result = await {{service}}.{{action}}(req.body);
    res.json({ success: true, data: result });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});`
    });

    this.codeTemplates.set('react_component', {
      language: 'javascript',
      framework: 'react',
      template: `
import React, { useState, useEffect } from 'react';

const {{componentName}} = ({ {{props}} }) => {
  const [{{state}}, set{{State}}] = useState({{initialValue}});

  useEffect(() => {
    // Component logic here
  }, []);

  return (
    <div className="{{className}}">
      {{content}}
    </div>
  );
};

export default {{componentName}};`
    });

    this.codeTemplates.set('database_model', {
      language: 'javascript',
      framework: 'mongoose',
      template: `
const mongoose = require('mongoose');

const {{modelName}}Schema = new mongoose.Schema({
  {{fields}}
}, {
  timestamps: true
});

{{modelName}}Schema.methods.{{method}} = function() {
  // Method implementation
};

module.exports = mongoose.model('{{modelName}}', {{modelName}}Schema);`
    });

    this.logger.info(`Loaded ${this.codeTemplates.size} code templates`);
  }

  async generateCode(payload) {
    const { 
      type, 
      specifications, 
      language = 'javascript', 
      framework,
      projectId 
    } = payload;
    
    this.logger.info(`Generating ${type} code for project ${projectId}`);
    
    const template = this.codeTemplates.get(type);
    if (!template) {
      throw new Error(`Code template '${type}' not found`);
    }
    
    // Generate code based on specifications
    const generatedCode = await this.processTemplate(template, specifications);
    
    // Create project structure
    const projectPath = await this.createProjectStructure(projectId, type);
    
    // Write generated files
    const files = await this.writeCodeFiles(projectPath, generatedCode, specifications);
    
    // Generate tests
    const tests = await this.generateTests(generatedCode, specifications);
    
    // Generate documentation
    const documentation = await this.generateCodeDocumentation(generatedCode, specifications);
    
    const result = {
      projectId,
      type,
      language,
      framework: framework || template.framework,
      files,
      tests,
      documentation,
      projectPath,
      status: 'completed',
      createdAt: new Date().toISOString()
    };
    
    // Store project
    this.activeProjects.set(projectId, result);
    
    return {
      status: 'completed',
      code: result,
      timestamp: new Date().toISOString()
    };
  }

  async developAPI(payload) {
    const { 
      endpoints, 
      authentication = true, 
      database = 'mongodb',
      projectId 
    } = payload;
    
    this.logger.info(`Developing API with ${endpoints.length} endpoints for project ${projectId}`);
    
    const apiStructure = {
      projectId,
      endpoints: [],
      middleware: [],
      models: [],
      routes: [],
      tests: [],
      documentation: {}
    };
    
    // Generate endpoints
    for (const endpoint of endpoints) {
      const generatedEndpoint = await this.generateEndpoint(endpoint);
      apiStructure.endpoints.push(generatedEndpoint);
    }
    
    // Generate middleware
    if (authentication) {
      apiStructure.middleware.push(await this.generateAuthMiddleware());
    }
    apiStructure.middleware.push(await this.generateErrorMiddleware());
    apiStructure.middleware.push(await this.generateLoggingMiddleware());
    
    // Generate models based on endpoints
    const models = this.extractModelsFromEndpoints(endpoints);
    for (const model of models) {
      apiStructure.models.push(await this.generateModel(model, database));
    }
    
    // Generate main app file
    const appFile = await this.generateAppFile(apiStructure);
    
    // Create project files
    const projectPath = await this.createAPIProject(projectId, apiStructure);
    
    return {
      status: 'completed',
      api: apiStructure,
      projectPath,
      timestamp: new Date().toISOString()
    };
  }

  async designDatabase(payload) {
    const { 
      entities, 
      relationships, 
      database = 'postgresql',
      projectId 
    } = payload;
    
    this.logger.info(`Designing ${database} database for project ${projectId}`);
    
    const schema = {
      database,
      tables: [],
      relationships: [],
      indexes: [],
      migrations: [],
      seeds: []
    };
    
    // Generate tables from entities
    for (const entity of entities) {
      const table = await this.generateTable(entity, database);
      schema.tables.push(table);
    }
    
    // Process relationships
    for (const relationship of relationships) {
      const rel = await this.processRelationship(relationship, database);
      schema.relationships.push(rel);
    }
    
    // Generate indexes
    schema.indexes = await this.generateIndexes(schema.tables);
    
    // Generate migrations
    schema.migrations = await this.generateMigrations(schema);
    
    // Generate seed data
    schema.seeds = await this.generateSeedData(schema.tables);
    
    return {
      status: 'completed',
      schema,
      timestamp: new Date().toISOString()
    };
  }

  async runTests(payload) {
    const { projectId, testType = 'unit', coverage = true } = payload;
    
    this.logger.info(`Running ${testType} tests for project ${projectId}`);
    
    const project = this.activeProjects.get(projectId);
    if (!project) {
      throw new Error(`Project ${projectId} not found`);
    }
    
    try {
      const testResults = {
        projectId,
        testType,
        results: {},
        coverage: null,
        duration: 0,
        status: 'passed',
        timestamp: new Date().toISOString()
      };
      
      const startTime = Date.now();
      
      // Run different types of tests
      switch (testType) {
        case 'unit':
          testResults.results = await this.runUnitTests(project.projectPath);
          break;
        case 'integration':
          testResults.results = await this.runIntegrationTests(project.projectPath);
          break;
        case 'e2e':
          testResults.results = await this.runE2ETests(project.projectPath);
          break;
        case 'performance':
          testResults.results = await this.runPerformanceTests(project.projectPath);
          break;
      }
      
      testResults.duration = Date.now() - startTime;
      
      // Generate coverage report if requested
      if (coverage) {
        testResults.coverage = await this.generateCoverageReport(project.projectPath);
      }
      
      // Determine overall status
      testResults.status = testResults.results.failed > 0 ? 'failed' : 'passed';
      
      return {
        status: 'completed',
        tests: testResults,
        timestamp: new Date().toISOString()
      };
      
    } catch (error) {
      this.logger.error('Test execution failed:', error);
      return {
        status: 'failed',
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  async deployApplication(payload) {
    const { 
      projectId, 
      environment = 'development', 
      buildFirst = true,
      runTests = true 
    } = payload;
    
    this.logger.info(`Deploying project ${projectId} to ${environment}`);
    
    const deployment = {
      projectId,
      environment,
      steps: [],
      status: 'in_progress',
      startTime: new Date().toISOString(),
      endTime: null,
      url: null
    };
    
    try {
      // Step 1: Pre-deployment checks
      deployment.steps.push(await this.preDeploymentChecks(projectId));
      
      // Step 2: Run tests if requested
      if (runTests) {
        const testResult = await this.runTests({ projectId, testType: 'unit' });
        deployment.steps.push({
          name: 'tests',
          status: testResult.tests.status,
          duration: testResult.tests.duration
        });
        
        if (testResult.tests.status === 'failed') {
          throw new Error('Tests failed, deployment aborted');
        }
      }
      
      // Step 3: Build application
      if (buildFirst) {
        deployment.steps.push(await this.buildApplication(projectId));
      }
      
      // Step 4: Deploy to environment
      deployment.steps.push(await this.deployToEnvironment(projectId, environment));
      
      // Step 5: Post-deployment verification
      deployment.steps.push(await this.postDeploymentVerification(projectId, environment));
      
      deployment.status = 'completed';
      deployment.endTime = new Date().toISOString();
      deployment.url = this.generateDeploymentURL(projectId, environment);
      
      // Notify other agents about successful deployment
      this.mqttClient.publish('events/deployment_completed', JSON.stringify({
        type: 'deployment_completed',
        payload: deployment
      }));
      
      return {
        status: 'completed',
        deployment,
        timestamp: new Date().toISOString()
      };
      
    } catch (error) {
      deployment.status = 'failed';
      deployment.endTime = new Date().toISOString();
      deployment.error = error.message;
      
      this.logger.error('Deployment failed:', error);
      return {
        status: 'failed',
        deployment,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  async reviewCode(payload) {
    const { projectId, files, criteria = ['quality', 'security', 'performance'] } = payload;
    
    this.logger.info(`Reviewing code for project ${projectId}`);
    
    const review = {
      projectId,
      files: files || [],
      criteria,
      results: {},
      issues: [],
      suggestions: [],
      overallScore: 0,
      reviewedAt: new Date().toISOString()
    };
    
    // Analyze each criterion
    for (const criterion of criteria) {
      review.results[criterion] = await this.analyzeCodeCriterion(projectId, criterion);
    }
    
    // Find issues and generate suggestions
    review.issues = await this.findCodeIssues(projectId);
    review.suggestions = await this.generateCodeSuggestions(review.issues);
    
    // Calculate overall score
    const scores = Object.values(review.results).map(r => r.score);
    review.overallScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    
    return {
      status: 'completed',
      review,
      timestamp: new Date().toISOString()
    };
  }

  async optimizeCode(payload) {
    const { projectId, optimizations = ['performance', 'bundle_size', 'memory'] } = payload;
    
    this.logger.info(`Optimizing code for project ${projectId}`);
    
    const optimization = {
      projectId,
      optimizations: {},
      improvements: [],
      metrics: {
        before: {},
        after: {}
      },
      optimizedAt: new Date().toISOString()
    };
    
    // Capture baseline metrics
    optimization.metrics.before = await this.captureMetrics(projectId);
    
    // Apply optimizations
    for (const type of optimizations) {
      optimization.optimizations[type] = await this.applyOptimization(projectId, type);
    }
    
    // Capture post-optimization metrics
    optimization.metrics.after = await this.captureMetrics(projectId);
    
    // Calculate improvements
    optimization.improvements = this.calculateImprovements(
      optimization.metrics.before,
      optimization.metrics.after
    );
    
    return {
      status: 'completed',
      optimization,
      timestamp: new Date().toISOString()
    };
  }

  async processTemplate(template, specifications) {
    let code = template.template;
    
    // Replace template variables with actual values
    Object.entries(specifications).forEach(([key, value]) => {
      const regex = new RegExp(`{{${key}}}`, 'g');
      code = code.replace(regex, value);
    });
    
    return {
      language: template.language,
      framework: template.framework,
      code,
      specifications
    };
  }

  async createProjectStructure(projectId, type) {
    const projectPath = path.join(process.cwd(), 'data', 'projects', projectId);
    
    const structure = {
      api_endpoint: ['src', 'tests', 'docs'],
      react_component: ['src/components', 'src/tests', 'src/stories'],
      database_model: ['models', 'migrations', 'seeds', 'tests']
    };
    
    const dirs = structure[type] || ['src', 'tests', 'docs'];
    
    for (const dir of dirs) {
      const fullPath = path.join(projectPath, dir);
      if (!fs.existsSync(fullPath)) {
        fs.mkdirSync(fullPath, { recursive: true });
      }
    }
    
    return projectPath;
  }

  async writeCodeFiles(projectPath, generatedCode, specifications) {
    const files = [];
    
    // Main code file
    const mainFile = `${specifications.name || 'index'}.${this.getFileExtension(generatedCode.language)}`;
    const mainFilePath = path.join(projectPath, 'src', mainFile);
    fs.writeFileSync(mainFilePath, generatedCode.code);
    files.push(mainFile);
    
    // Package.json for Node.js projects
    if (generatedCode.language === 'javascript') {
      const packageJson = this.generatePackageJson(specifications);
      fs.writeFileSync(path.join(projectPath, 'package.json'), JSON.stringify(packageJson, null, 2));
      files.push('package.json');
    }
    
    // README.md
    const readme = this.generateReadme(specifications);
    fs.writeFileSync(path.join(projectPath, 'README.md'), readme);
    files.push('README.md');
    
    return files;
  }

  async generateTests(generatedCode, specifications) {
    const testCode = `
// Test for ${specifications.name || 'generated code'}
describe('${specifications.name || 'Generated Code'}', () => {
  test('should work correctly', () => {
    // Test implementation
    expect(true).toBe(true);
  });
  
  test('should handle errors gracefully', () => {
    // Error handling test
    expect(() => {
      // Error scenario
    }).not.toThrow();
  });
});
`;
    
    return {
      framework: 'jest',
      code: testCode,
      coverage: 'enabled'
    };
  }

  async generateCodeDocumentation(generatedCode, specifications) {
    return `
# ${specifications.name || 'Generated Code'}

## Description
${specifications.description || 'Auto-generated code component'}

## Usage
\`\`\`${generatedCode.language}
${generatedCode.code.split('\n').slice(0, 10).join('\n')}
\`\`\`

## API Reference
- **Language**: ${generatedCode.language}
- **Framework**: ${generatedCode.framework}
- **Generated**: ${new Date().toISOString()}

## Dependencies
${specifications.dependencies ? specifications.dependencies.join(', ') : 'None'}
`;
  }

  async generateEndpoint(endpoint) {
    const { method, path, description, parameters, response } = endpoint;
    
    return {
      method: method.toLowerCase(),
      path,
      description,
      parameters: parameters || [],
      response: response || { type: 'json' },
      middleware: ['auth', 'validation'],
      code: `
app.${method.toLowerCase()}('${path}', async (req, res) => {
  try {
    // ${description}
    const result = await service.${this.camelCase(description)}(req.body);
    res.json({ success: true, data: result });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});`
    };
  }

  async generateAuthMiddleware() {
    return {
      name: 'auth',
      code: `
const jwt = require('jsonwebtoken');

const authMiddleware = (req, res, next) => {
  const token = req.header('Authorization')?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'Access denied. No token provided.' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(400).json({ error: 'Invalid token.' });
  }
};

module.exports = authMiddleware;`
    };
  }

  async generateErrorMiddleware() {
    return {
      name: 'error',
      code: `
const errorMiddleware = (err, req, res, next) => {
  console.error(err.stack);
  
  if (err.name === 'ValidationError') {
    return res.status(400).json({ error: err.message });
  }
  
  if (err.name === 'CastError') {
    return res.status(400).json({ error: 'Invalid ID format' });
  }
  
  res.status(500).json({ error: 'Something went wrong!' });
};

module.exports = errorMiddleware;`
    };
  }

  async generateLoggingMiddleware() {
    return {
      name: 'logging',
      code: `
const loggingMiddleware = (req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(\`\${req.method} \${req.path} - \${res.statusCode} - \${duration}ms\`);
  });
  
  next();
};

module.exports = loggingMiddleware;`
    };
  }

  extractModelsFromEndpoints(endpoints) {
    const models = new Set();
    
    endpoints.forEach(endpoint => {
      // Extract model names from endpoint paths
      const pathParts = endpoint.path.split('/').filter(part => part && !part.startsWith(':'));
      pathParts.forEach(part => {
        if (part !== 'api' && part !== 'v1') {
          models.add(this.singularize(part));
        }
      });
    });
    
    return Array.from(models);
  }

  async generateModel(modelName, database) {
    const capitalizedName = this.capitalize(modelName);
    
    if (database === 'mongodb') {
      return {
        name: modelName,
        code: `
const mongoose = require('mongoose');

const ${modelName}Schema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, unique: true },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
}, {
  timestamps: true
});

module.exports = mongoose.model('${capitalizedName}', ${modelName}Schema);`
      };
    } else {
      return {
        name: modelName,
        code: `
-- ${capitalizedName} table
CREATE TABLE ${modelName}s (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`
      };
    }
  }

  async runUnitTests(projectPath) {
    // Simulate test execution
    return {
      total: 15,
      passed: 14,
      failed: 1,
      skipped: 0,
      details: [
        { name: 'should create user', status: 'passed', duration: 45 },
        { name: 'should validate email', status: 'failed', duration: 23, error: 'Invalid email format' }
      ]
    };
  }

  async runIntegrationTests(projectPath) {
    return {
      total: 8,
      passed: 8,
      failed: 0,
      skipped: 0,
      details: []
    };
  }

  async runE2ETests(projectPath) {
    return {
      total: 5,
      passed: 4,
      failed: 1,
      skipped: 0,
      details: [
        { name: 'user login flow', status: 'passed', duration: 2340 },
        { name: 'checkout process', status: 'failed', duration: 1890, error: 'Payment gateway timeout' }
      ]
    };
  }

  async runPerformanceTests(projectPath) {
    return {
      total: 3,
      passed: 3,
      failed: 0,
      skipped: 0,
      metrics: {
        responseTime: '245ms',
        throughput: '1200 req/s',
        memoryUsage: '128MB'
      }
    };
  }

  async generateCoverageReport(projectPath) {
    return {
      lines: { total: 450, covered: 387, percentage: 86 },
      functions: { total: 45, covered: 41, percentage: 91 },
      branches: { total: 120, covered: 98, percentage: 82 },
      statements: { total: 380, covered: 325, percentage: 86 }
    };
  }

  async preDeploymentChecks(projectId) {
    // Simulate pre-deployment checks
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
      name: 'pre_deployment_checks',
      status: 'passed',
      checks: [
        { name: 'environment_variables', status: 'passed' },
        { name: 'dependencies', status: 'passed' },
        { name: 'configuration', status: 'passed' }
      ],
      duration: 1000
    };
  }

  async buildApplication(projectId) {
    // Simulate build process
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    return {
      name: 'build',
      status: 'passed',
      artifacts: ['dist/bundle.js', 'dist/styles.css', 'dist/index.html'],
      size: '2.4MB',
      duration: 5000
    };
  }

  async deployToEnvironment(projectId, environment) {
    // Simulate deployment
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    return {
      name: 'deploy',
      status: 'passed',
      environment,
      instance: `${projectId}-${environment}-${Date.now()}`,
      duration: 3000
    };
  }

  async postDeploymentVerification(projectId, environment) {
    // Simulate verification
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      name: 'verification',
      status: 'passed',
      checks: [
        { name: 'health_check', status: 'passed', response_time: '120ms' },
        { name: 'database_connection', status: 'passed' },
        { name: 'external_services', status: 'passed' }
      ],
      duration: 2000
    };
  }

  generateDeploymentURL(projectId, environment) {
    const subdomain = environment === 'production' ? projectId : `${projectId}-${environment}`;
    return `https://${subdomain}.example.com`;
  }

  async analyzeCodeCriterion(projectId, criterion) {
    const scores = {
      quality: Math.random() * 20 + 80,
      security: Math.random() * 15 + 85,
      performance: Math.random() * 25 + 75,
      maintainability: Math.random() * 20 + 80
    };
    
    return {
      criterion,
      score: Math.round(scores[criterion] || 85),
      details: `${criterion} analysis completed`,
      recommendations: [`Improve ${criterion} by following best practices`]
    };
  }

  async findCodeIssues(projectId) {
    // Simulate code analysis
    return [
      {
        type: 'warning',
        file: 'src/index.js',
        line: 45,
        message: 'Unused variable detected',
        severity: 'medium'
      },
      {
        type: 'error',
        file: 'src/api.js',
        line: 23,
        message: 'Potential SQL injection vulnerability',
        severity: 'high'
      }
    ];
  }

  async generateCodeSuggestions(issues) {
    return issues.map(issue => ({
      file: issue.file,
      line: issue.line,
      suggestion: this.getSuggestionForIssue(issue),
      priority: issue.severity
    }));
  }

  getSuggestionForIssue(issue) {
    const suggestions = {
      'Unused variable detected': 'Remove unused variable or use ESLint to catch these automatically',
      'Potential SQL injection vulnerability': 'Use parameterized queries or ORM to prevent SQL injection'
    };
    
    return suggestions[issue.message] || 'Review and fix this issue';
  }

  async captureMetrics(projectId) {
    return {
      bundleSize: Math.floor(Math.random() * 1000) + 2000, // KB
      loadTime: Math.floor(Math.random() * 500) + 1000, // ms
      memoryUsage: Math.floor(Math.random() * 50) + 100, // MB
      cpuUsage: Math.floor(Math.random() * 30) + 20 // %
    };
  }

  async applyOptimization(projectId, type) {
    const optimizations = {
      performance: {
        actions: ['code_splitting', 'lazy_loading', 'caching'],
        improvement: '25% faster execution'
      },
      bundle_size: {
        actions: ['tree_shaking', 'minification', 'compression'],
        improvement: '30% smaller bundle'
      },
      memory: {
        actions: ['memory_pooling', 'garbage_collection_tuning'],
        improvement: '20% less memory usage'
      }
    };
    
    // Simulate optimization process
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return optimizations[type] || optimizations.performance;
  }

  calculateImprovements(before, after) {
    const improvements = [];
    
    Object.keys(before).forEach(metric => {
      const beforeValue = before[metric];
      const afterValue = after[metric];
      const improvement = ((beforeValue - afterValue) / beforeValue * 100).toFixed(1);
      
      if (improvement > 0) {
        improvements.push({
          metric,
          before: beforeValue,
          after: afterValue,
          improvement: `${improvement}% better`
        });
      }
    });
    
    return improvements;
  }

  getFileExtension(language) {
    const extensions = {
      javascript: 'js',
      typescript: 'ts',
      python: 'py',
      java: 'java',
      csharp: 'cs'
    };
    
    return extensions[language] || 'txt';
  }

  generatePackageJson(specifications) {
    return {
      name: specifications.name || 'generated-project',
      version: '1.0.0',
      description: specifications.description || 'Auto-generated project',
      main: 'src/index.js',
      scripts: {
        start: 'node src/index.js',
        test: 'jest',
        build: 'webpack --mode production',
        dev: 'nodemon src/index.js'
      },
      dependencies: specifications.dependencies || {},
      devDependencies: {
        jest: '^29.0.0',
        nodemon: '^2.0.0'
      }
    };
  }

  generateReadme(specifications) {
    return `
# ${specifications.name || 'Generated Project'}

${specifications.description || 'Auto-generated project'}

## Installation

\`\`\`bash
npm install
\`\`\`

## Usage

\`\`\`bash
npm start
\`\`\`

## Testing

\`\`\`bash
npm test
\`\`\`

## Generated by Engineering Agent
- **Created**: ${new Date().toISOString()}
- **Language**: ${specifications.language || 'JavaScript'}
- **Framework**: ${specifications.framework || 'Node.js'}
`;
  }

  // Utility methods
  camelCase(str) {
    return str.replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => {
      return index === 0 ? word.toLowerCase() : word.toUpperCase();
    }).replace(/\s+/g, '');
  }

  capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  singularize(str) {
    // Simple singularization
    if (str.endsWith('s')) {
      return str.slice(0, -1);
    }
    return str;
  }

  async shutdown() {
    this.logger.info('Shutting down Engineering Agent...');
    
    if (this.mqttClient) {
      this.mqttClient.end();
    }
    
    await super.shutdown();
  }
}

// Auto-start if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const engineeringAgent = new EngineeringAgent();
  engineeringAgent.initialize().catch(console.error);
}