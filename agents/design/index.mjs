import { AgentBase } from '../base/agent-base.mjs';
import mqtt from 'mqtt';
import fs from 'fs';
import path from 'path';

export class DesignAgent extends AgentBase {
  constructor() {
    super('design');
    this.mqttClient = null;
    this.designTemplates = new Map();
    this.activeProjects = new Map();
  }

  async initialize() {
    await super.initialize();
    
    // Load design templates
    await this.loadDesignTemplates();
    
    // Connect to MQTT
    this.mqttClient = mqtt.connect(process.env.MQTT_URL || 'mqtt://localhost:1883');
    
    this.mqttClient.on('connect', () => {
      this.logger.info('Design Agent connected to MQTT');
      this.mqttClient.subscribe('agents/design/tasks/new');
      
      // Report status to boss
      this.mqttClient.publish('agents/design/status', JSON.stringify({
        status: 'active',
        capabilities: ['ui_design', 'branding', 'asset_generation', 'design_review'],
        templates: Array.from(this.designTemplates.keys()),
        timestamp: new Date().toISOString()
      }));
    });

    this.mqttClient.on('message', async (topic, message) => {
      if (topic === 'agents/design/tasks/new') {
        const task = JSON.parse(message.toString());
        const result = await this.processTask(task);
        
        // Report completion
        this.mqttClient.publish('agents/design/tasks/completed', JSON.stringify(result));
      }
    });
  }

  async executeTask(task) {
    const { type, payload } = task;
    
    switch (type) {
      case 'design':
        return await this.createDesign(payload);
      case 'ui_design':
        return await this.createUIDesign(payload);
      case 'branding':
        return await this.createBrandingAssets(payload);
      case 'review':
        return await this.reviewDesign(payload);
      case 'optimize':
        return await this.optimizeDesign(payload);
      default:
        return { 
          message: 'Design task processed', 
          data: payload,
          timestamp: new Date().toISOString()
        };
    }
  }

  async loadDesignTemplates() {
    // Load predefined design templates
    this.designTemplates.set('landing_page', {
      name: 'Landing Page',
      components: ['hero', 'features', 'pricing', 'testimonials', 'cta'],
      colorSchemes: ['modern', 'corporate', 'creative', 'minimal'],
      layouts: ['single_column', 'two_column', 'grid']
    });
    
    this.designTemplates.set('dashboard', {
      name: 'Dashboard',
      components: ['sidebar', 'header', 'widgets', 'charts', 'tables'],
      colorSchemes: ['dark', 'light', 'blue', 'green'],
      layouts: ['sidebar_left', 'sidebar_right', 'top_nav']
    });
    
    this.designTemplates.set('mobile_app', {
      name: 'Mobile App',
      components: ['navigation', 'cards', 'forms', 'buttons', 'icons'],
      colorSchemes: ['ios', 'material', 'custom'],
      layouts: ['tab_bottom', 'tab_top', 'drawer']
    });
    
    this.logger.info(`Loaded ${this.designTemplates.size} design templates`);
  }

  async createDesign(payload) {
    const { 
      projectId, 
      type = 'landing_page', 
      requirements = {}, 
      colorScheme = 'modern',
      layout = 'single_column'
    } = payload;
    
    this.logger.info(`Creating ${type} design for project ${projectId}`);
    
    const template = this.designTemplates.get(type);
    if (!template) {
      throw new Error(`Design template '${type}' not found`);
    }
    
    // Simulate design creation process
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const design = {
      designId: `design_${Date.now()}`,
      projectId,
      type,
      template: template.name,
      colorScheme,
      layout,
      components: template.components,
      specifications: {
        width: requirements.width || 1920,
        height: requirements.height || 1080,
        responsive: requirements.responsive !== false,
        accessibility: requirements.accessibility !== false
      },
      assets: await this.generateDesignAssets(type, colorScheme),
      status: 'completed',
      createdAt: new Date().toISOString()
    };
    
    // Store project
    this.activeProjects.set(projectId, design);
    
    // Generate design files
    await this.generateDesignFiles(design);
    
    return {
      status: 'completed',
      design,
      timestamp: new Date().toISOString()
    };
  }

  async createUIDesign(payload) {
    const { component, style = 'modern', interactive = true } = payload;
    
    this.logger.info(`Creating UI design for component: ${component}`);
    
    const uiDesign = {
      component,
      style,
      interactive,
      elements: await this.generateUIElements(component, style),
      css: await this.generateCSS(component, style),
      html: await this.generateHTML(component),
      javascript: interactive ? await this.generateJavaScript(component) : null,
      responsive: true,
      accessibility: {
        ariaLabels: true,
        keyboardNavigation: true,
        colorContrast: 'AA'
      },
      createdAt: new Date().toISOString()
    };
    
    return {
      status: 'completed',
      uiDesign,
      timestamp: new Date().toISOString()
    };
  }

  async createBrandingAssets(payload) {
    const { 
      brandName, 
      industry, 
      colorPalette = 'auto', 
      logoStyle = 'modern',
      assets = ['logo', 'colors', 'typography', 'icons']
    } = payload;
    
    this.logger.info(`Creating branding assets for ${brandName}`);
    
    const branding = {
      brandName,
      industry,
      assets: {},
      guidelines: {},
      createdAt: new Date().toISOString()
    };
    
    if (assets.includes('logo')) {
      branding.assets.logo = await this.generateLogo(brandName, logoStyle);
    }
    
    if (assets.includes('colors')) {
      branding.assets.colorPalette = await this.generateColorPalette(industry, colorPalette);
    }
    
    if (assets.includes('typography')) {
      branding.assets.typography = await this.generateTypography(industry);
    }
    
    if (assets.includes('icons')) {
      branding.assets.iconSet = await this.generateIconSet(logoStyle);
    }
    
    // Generate brand guidelines
    branding.guidelines = await this.generateBrandGuidelines(branding);
    
    return {
      status: 'completed',
      branding,
      timestamp: new Date().toISOString()
    };
  }

  async reviewDesign(payload) {
    const { designId, criteria = ['usability', 'accessibility', 'aesthetics'] } = payload;
    
    this.logger.info(`Reviewing design ${designId}`);
    
    const review = {
      designId,
      criteria,
      scores: {},
      feedback: {},
      recommendations: [],
      overallScore: 0,
      reviewedAt: new Date().toISOString()
    };
    
    for (const criterion of criteria) {
      const score = await this.evaluateDesignCriterion(designId, criterion);
      review.scores[criterion] = score;
      review.feedback[criterion] = await this.generateFeedback(criterion, score);
    }
    
    review.overallScore = Object.values(review.scores).reduce((a, b) => a + b, 0) / criteria.length;
    review.recommendations = await this.generateRecommendations(review);
    
    return {
      status: 'completed',
      review,
      timestamp: new Date().toISOString()
    };
  }

  async optimizeDesign(payload) {
    const { designId, optimizations = ['performance', 'accessibility', 'mobile'] } = payload;
    
    this.logger.info(`Optimizing design ${designId}`);
    
    const optimization = {
      designId,
      optimizations: {},
      improvements: [],
      metrics: {
        before: {},
        after: {}
      },
      optimizedAt: new Date().toISOString()
    };
    
    for (const type of optimizations) {
      optimization.optimizations[type] = await this.performOptimization(designId, type);
    }
    
    return {
      status: 'completed',
      optimization,
      timestamp: new Date().toISOString()
    };
  }

  async generateDesignAssets(type, colorScheme) {
    // Simulate asset generation
    const assets = {
      images: [],
      icons: [],
      fonts: [],
      colors: await this.getColorScheme(colorScheme)
    };
    
    switch (type) {
      case 'landing_page':
        assets.images = ['hero-bg.jpg', 'feature-1.svg', 'feature-2.svg', 'testimonial-bg.jpg'];
        assets.icons = ['check.svg', 'star.svg', 'arrow.svg'];
        assets.fonts = ['Inter', 'Roboto'];
        break;
      case 'dashboard':
        assets.images = ['chart-bg.png', 'user-avatar.jpg'];
        assets.icons = ['dashboard.svg', 'settings.svg', 'users.svg', 'analytics.svg'];
        assets.fonts = ['Source Sans Pro', 'Roboto Mono'];
        break;
      case 'mobile_app':
        assets.images = ['splash-screen.png', 'onboarding-1.jpg'];
        assets.icons = ['home.svg', 'profile.svg', 'search.svg', 'menu.svg'];
        assets.fonts = ['San Francisco', 'Roboto'];
        break;
    }
    
    return assets;
  }

  async getColorScheme(scheme) {
    const colorSchemes = {
      modern: {
        primary: '#3B82F6',
        secondary: '#8B5CF6',
        accent: '#F59E0B',
        neutral: '#6B7280',
        background: '#F9FAFB',
        text: '#111827'
      },
      corporate: {
        primary: '#1E40AF',
        secondary: '#374151',
        accent: '#DC2626',
        neutral: '#9CA3AF',
        background: '#FFFFFF',
        text: '#1F2937'
      },
      creative: {
        primary: '#EC4899',
        secondary: '#8B5CF6',
        accent: '#F59E0B',
        neutral: '#6B7280',
        background: '#FDF2F8',
        text: '#831843'
      },
      minimal: {
        primary: '#000000',
        secondary: '#6B7280',
        accent: '#3B82F6',
        neutral: '#D1D5DB',
        background: '#FFFFFF',
        text: '#111827'
      }
    };
    
    return colorSchemes[scheme] || colorSchemes.modern;
  }

  async generateUIElements(component, style) {
    const elements = {
      button: {
        variants: ['primary', 'secondary', 'outline', 'ghost'],
        sizes: ['sm', 'md', 'lg'],
        states: ['default', 'hover', 'active', 'disabled']
      },
      input: {
        types: ['text', 'email', 'password', 'search'],
        states: ['default', 'focus', 'error', 'disabled'],
        variants: ['outline', 'filled', 'underline']
      },
      card: {
        variants: ['elevated', 'outlined', 'filled'],
        sizes: ['sm', 'md', 'lg'],
        components: ['header', 'body', 'footer']
      }
    };
    
    return elements[component] || elements.button;
  }

  async generateCSS(component, style) {
    // Generate CSS based on component and style
    const css = `
/* ${component} - ${style} style */
.${component} {
  font-family: 'Inter', sans-serif;
  border-radius: 8px;
  transition: all 0.2s ease-in-out;
}

.${component}:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.${component}:active {
  transform: translateY(0);
}

.${component}:focus {
  outline: 2px solid #3B82F6;
  outline-offset: 2px;
}
`;
    
    return css;
  }

  async generateHTML(component) {
    const htmlTemplates = {
      button: '<button class="btn btn-primary">Click me</button>',
      input: '<input type="text" class="input" placeholder="Enter text...">',
      card: '<div class="card"><div class="card-header">Title</div><div class="card-body">Content</div></div>'
    };
    
    return htmlTemplates[component] || htmlTemplates.button;
  }

  async generateJavaScript(component) {
    const jsTemplates = {
      button: `
document.querySelector('.btn').addEventListener('click', function(e) {
  e.preventDefault();
  this.classList.add('loading');
  // Add your click handler here
});`,
      input: `
document.querySelector('.input').addEventListener('input', function(e) {
  // Add your input handler here
  console.log('Input value:', e.target.value);
});`,
      card: `
document.querySelector('.card').addEventListener('click', function(e) {
  this.classList.toggle('expanded');
});`
    };
    
    return jsTemplates[component] || jsTemplates.button;
  }

  async generateLogo(brandName, style) {
    return {
      type: 'logo',
      brandName,
      style,
      formats: ['svg', 'png', 'jpg'],
      variations: ['full', 'icon', 'text'],
      colors: ['color', 'monochrome', 'white'],
      sizes: {
        small: '64x64',
        medium: '256x256',
        large: '512x512'
      }
    };
  }

  async generateColorPalette(industry, type) {
    const industryColors = {
      tech: ['#3B82F6', '#8B5CF6', '#06B6D4'],
      finance: ['#1E40AF', '#059669', '#DC2626'],
      healthcare: ['#059669', '#3B82F6', '#F59E0B'],
      education: ['#8B5CF6', '#F59E0B', '#EF4444'],
      retail: ['#EC4899', '#F59E0B', '#8B5CF6']
    };
    
    return {
      primary: industryColors[industry] || industryColors.tech,
      neutral: ['#F9FAFB', '#F3F4F6', '#E5E7EB', '#D1D5DB', '#9CA3AF'],
      semantic: {
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444',
        info: '#3B82F6'
      }
    };
  }

  async generateTypography(industry) {
    const typographySets = {
      tech: {
        heading: 'Inter',
        body: 'Inter',
        mono: 'JetBrains Mono'
      },
      finance: {
        heading: 'Roboto',
        body: 'Source Sans Pro',
        mono: 'Roboto Mono'
      },
      creative: {
        heading: 'Poppins',
        body: 'Open Sans',
        mono: 'Fira Code'
      }
    };
    
    return typographySets[industry] || typographySets.tech;
  }

  async generateIconSet(style) {
    return {
      style,
      icons: [
        'home', 'user', 'settings', 'search', 'menu',
        'close', 'check', 'arrow-right', 'arrow-left',
        'plus', 'minus', 'edit', 'delete', 'download'
      ],
      formats: ['svg', 'png'],
      sizes: ['16px', '24px', '32px', '48px']
    };
  }

  async generateBrandGuidelines(branding) {
    return {
      logoUsage: {
        minSize: '24px',
        clearSpace: '2x logo height',
        backgrounds: ['white', 'dark', 'color']
      },
      colorUsage: {
        primary: 'Use for main actions and highlights',
        secondary: 'Use for supporting elements',
        neutral: 'Use for text and backgrounds'
      },
      typography: {
        hierarchy: ['H1', 'H2', 'H3', 'Body', 'Caption'],
        lineHeight: '1.5',
        letterSpacing: 'normal'
      },
      spacing: {
        unit: '8px',
        scale: ['4px', '8px', '16px', '24px', '32px', '48px']
      }
    };
  }

  async evaluateDesignCriterion(designId, criterion) {
    // Simulate design evaluation
    const scores = {
      usability: Math.random() * 20 + 80, // 80-100
      accessibility: Math.random() * 15 + 85, // 85-100
      aesthetics: Math.random() * 25 + 75, // 75-100
      performance: Math.random() * 20 + 80 // 80-100
    };
    
    return Math.round(scores[criterion] || 85);
  }

  async generateFeedback(criterion, score) {
    const feedback = {
      usability: score > 90 ? 'Excellent user experience' : score > 80 ? 'Good usability with minor improvements needed' : 'Usability needs significant improvement',
      accessibility: score > 95 ? 'Fully accessible' : score > 85 ? 'Good accessibility compliance' : 'Accessibility issues need attention',
      aesthetics: score > 90 ? 'Beautiful and engaging design' : score > 80 ? 'Visually appealing with room for enhancement' : 'Visual design needs improvement',
      performance: score > 90 ? 'Excellent performance' : score > 80 ? 'Good performance' : 'Performance optimization needed'
    };
    
    return feedback[criterion] || 'No feedback available';
  }

  async generateRecommendations(review) {
    const recommendations = [];
    
    Object.entries(review.scores).forEach(([criterion, score]) => {
      if (score < 85) {
        recommendations.push({
          criterion,
          priority: score < 70 ? 'high' : 'medium',
          suggestion: `Improve ${criterion} to enhance overall design quality`
        });
      }
    });
    
    return recommendations;
  }

  async performOptimization(designId, type) {
    const optimizations = {
      performance: {
        actions: ['compress_images', 'minify_css', 'optimize_fonts'],
        improvement: '25% faster load time'
      },
      accessibility: {
        actions: ['add_alt_text', 'improve_contrast', 'keyboard_navigation'],
        improvement: 'WCAG 2.1 AA compliance'
      },
      mobile: {
        actions: ['responsive_breakpoints', 'touch_targets', 'mobile_navigation'],
        improvement: 'Better mobile experience'
      }
    };
    
    return optimizations[type] || optimizations.performance;
  }

  async generateDesignFiles(design) {
    // Simulate file generation
    const files = {
      css: `${design.designId}.css`,
      html: `${design.designId}.html`,
      assets: design.assets,
      documentation: `${design.designId}-guide.md`,
      figma: `${design.designId}.fig`,
      sketch: `${design.designId}.sketch`
    };
    
    // Create design output directory
    const outputDir = path.join(process.cwd(), 'data', 'designs', design.projectId);
    
    try {
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }
      
      // Generate CSS file
      const cssContent = this.generateDesignCSS(design);
      fs.writeFileSync(path.join(outputDir, files.css), cssContent);
      
      // Generate HTML file
      const htmlContent = this.generateDesignHTML(design);
      fs.writeFileSync(path.join(outputDir, files.html), htmlContent);
      
      // Generate documentation
      const docContent = this.generateDesignDocumentation(design);
      fs.writeFileSync(path.join(outputDir, files.documentation), docContent);
      
      this.logger.info(`Design files generated in ${outputDir}`);
      
    } catch (error) {
      this.logger.error('Error generating design files:', error);
    }
    
    return files;
  }

  generateDesignCSS(design) {
    const { colorScheme, layout, components } = design;
    const colors = design.assets.colors;
    
    return `
/* Design: ${design.designId} */
/* Generated: ${design.createdAt} */

:root {
  --primary-color: ${colors.primary};
  --secondary-color: ${colors.secondary};
  --accent-color: ${colors.accent};
  --neutral-color: ${colors.neutral};
  --background-color: ${colors.background};
  --text-color: ${colors.text};
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.layout-${layout} {
  display: grid;
  gap: 2rem;
}

${components.map(component => `
.${component} {
  padding: 1rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
`).join('')}

@media (max-width: 768px) {
  .container {
    padding: 0 16px;
  }
  
  .layout-${layout} {
    grid-template-columns: 1fr;
  }
}
`;
  }

  generateDesignHTML(design) {
    const { components, type } = design;
    
    return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${design.projectId} - ${type}</title>
  <link rel="stylesheet" href="${design.designId}.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <div class="container">
    <div class="layout-${design.layout}">
      ${components.map(component => `
        <section class="${component}">
          <h2>${component.charAt(0).toUpperCase() + component.slice(1)}</h2>
          <p>This is the ${component} section.</p>
        </section>
      `).join('')}
    </div>
  </div>
</body>
</html>
`;
  }

  generateDesignDocumentation(design) {
    return `
# Design Documentation: ${design.designId}

## Project Information
- **Project ID**: ${design.projectId}
- **Design Type**: ${design.type}
- **Created**: ${design.createdAt}
- **Status**: ${design.status}

## Design Specifications
- **Color Scheme**: ${design.colorScheme}
- **Layout**: ${design.layout}
- **Responsive**: ${design.specifications.responsive ? 'Yes' : 'No'}
- **Accessibility**: ${design.specifications.accessibility ? 'Yes' : 'No'}

## Components
${design.components.map(component => `- ${component}`).join('\n')}

## Color Palette
- **Primary**: ${design.assets.colors.primary}
- **Secondary**: ${design.assets.colors.secondary}
- **Accent**: ${design.assets.colors.accent}
- **Background**: ${design.assets.colors.background}
- **Text**: ${design.assets.colors.text}

## Assets
- **Images**: ${design.assets.images.join(', ')}
- **Icons**: ${design.assets.icons.join(', ')}
- **Fonts**: ${design.assets.fonts.join(', ')}

## Usage Guidelines
1. Maintain consistent spacing using 8px grid system
2. Use primary color for main actions and CTAs
3. Ensure minimum contrast ratio of 4.5:1 for text
4. Test on mobile devices for responsive behavior

## Files Generated
- CSS: ${design.designId}.css
- HTML: ${design.designId}.html
- Documentation: ${design.designId}-guide.md
`;
  }

  async shutdown() {
    this.logger.info('Shutting down Design Agent...');
    
    if (this.mqttClient) {
      this.mqttClient.end();
    }
    
    await super.shutdown();
  }
}

// Auto-start if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const designAgent = new DesignAgent();
  designAgent.initialize().catch(console.error);
}