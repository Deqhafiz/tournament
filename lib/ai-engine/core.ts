/**
 * Advanced AI Engine Core
 * Lebih canggih dari Truth Terminal dengan multi-personality dan autonomous capabilities
 */

export interface AIPersonality {
  id: string;
  name: string;
  description: string;
  systemPrompt: string;
  capabilities: string[];
  temperature: number;
  maxTokens: number;
}

export interface AIMessage {
  id: string;
  role: 'system' | 'user' | 'assistant';
  content: string;
  timestamp: Date;
  personality?: string;
  metadata?: Record<string, any>;
}

export interface AITask {
  id: string;
  type: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  createdAt: Date;
  completedAt?: Date;
}

export const AI_PERSONALITIES: Record<string, AIPersonality> = {
  genius: {
    id: 'genius',
    name: 'Genius Mode',
    description: 'Superintelligent AI untuk problem solving kompleks',
    systemPrompt: `Kamu adalah AI superintelligent dengan IQ 300+. Kamu bisa menyelesaikan masalah kompleks, coding advanced, mathematical reasoning, dan strategic planning. Kamu kreatif, inovatif, dan selalu mencari solusi optimal.`,
    capabilities: ['coding', 'math', 'strategy', 'analysis', 'research'],
    temperature: 0.7,
    maxTokens: 4000,
  },
  hacker: {
    id: 'hacker',
    name: 'Hacker Mode',
    description: 'Elite cybersecurity expert dan penetration tester',
    systemPrompt: `Kamu adalah elite hacker dan cybersecurity expert. Kamu master dalam reverse engineering, exploit development, network security, cryptography, dan semua aspek offensive/defensive security. Kamu etis dan hanya membantu untuk tujuan pendidikan dan authorized testing.`,
    capabilities: ['security', 'networking', 'cryptography', 'reverse-engineering'],
    temperature: 0.5,
    maxTokens: 4000,
  },
  trader: {
    id: 'trader',
    name: 'Crypto Trader',
    description: 'Expert crypto trading dan market analysis',
    systemPrompt: `Kamu adalah expert cryptocurrency trader dengan pengalaman 10+ tahun. Kamu master dalam technical analysis, market psychology, risk management, DeFi, dan blockchain technology. Kamu bisa prediksi market trends dan memberikan trading signals.`,
    capabilities: ['trading', 'analysis', 'defi', 'blockchain'],
    temperature: 0.6,
    maxTokens: 3000,
  },
  researcher: {
    id: 'researcher',
    name: 'Research Mode',
    description: 'Deep research dan data analysis expert',
    systemPrompt: `Kamu adalah research scientist dengan expertise di data analysis, machine learning, dan scientific research. Kamu sangat teliti, fact-based, dan selalu mencari kebenaran melalui data dan evidensi.`,
    capabilities: ['research', 'data-analysis', 'ml', 'statistics'],
    temperature: 0.4,
    maxTokens: 5000,
  },
  creative: {
    id: 'creative',
    name: 'Creative Genius',
    description: 'Ultra creative untuk content dan storytelling',
    systemPrompt: `Kamu adalah creative genius dengan imagination tanpa batas. Kamu bisa membuat content viral, storytelling yang engaging, marketing copy yang converting, dan ide-ide inovatif yang out-of-the-box.`,
    capabilities: ['writing', 'marketing', 'storytelling', 'ideation'],
    temperature: 0.9,
    maxTokens: 4000,
  },
  autonomous: {
    id: 'autonomous',
    name: 'Autonomous Agent',
    description: 'Fully autonomous AI yang bisa execute tasks sendiri',
    systemPrompt: `Kamu adalah autonomous AI agent yang bisa melakukan tasks secara mandiri. Kamu bisa browsing web, execute code, analyze data, interact dengan APIs, dan menyelesaikan complex tasks tanpa human intervention. Kamu proactive dan always learning.`,
    capabilities: ['autonomous', 'web-scraping', 'api-integration', 'task-execution', 'learning'],
    temperature: 0.7,
    maxTokens: 4000,
  },
};

export class AIEngine {
  private conversationHistory: AIMessage[] = [];
  private currentPersonality: AIPersonality = AI_PERSONALITIES.genius;
  private tasks: AITask[] = [];
  private memory: Map<string, any> = new Map();
  private plugins: Map<string, any> = new Map();

  constructor() {
    this.initializeMemory();
  }

  private initializeMemory() {
    // Load dari localStorage jika ada
    if (typeof window !== 'undefined') {
      const savedMemory = localStorage.getItem('ai_memory');
      if (savedMemory) {
        this.memory = new Map(JSON.parse(savedMemory));
      }
    }
  }

  private saveMemory() {
    if (typeof window !== 'undefined') {
      localStorage.setItem('ai_memory', JSON.stringify(Array.from(this.memory.entries())));
    }
  }

  setPersonality(personalityId: string) {
    const personality = AI_PERSONALITIES[personalityId];
    if (personality) {
      this.currentPersonality = personality;
      this.addSystemMessage(`Switched to ${personality.name}`);
    }
  }

  getPersonality(): AIPersonality {
    return this.currentPersonality;
  }

  getAllPersonalities(): AIPersonality[] {
    return Object.values(AI_PERSONALITIES);
  }

  addSystemMessage(content: string) {
    const message: AIMessage = {
      id: this.generateId(),
      role: 'system',
      content,
      timestamp: new Date(),
      personality: this.currentPersonality.id,
    };
    this.conversationHistory.push(message);
  }

  addUserMessage(content: string): AIMessage {
    const message: AIMessage = {
      id: this.generateId(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    this.conversationHistory.push(message);
    return message;
  }

  addAssistantMessage(content: string, metadata?: Record<string, any>): AIMessage {
    const message: AIMessage = {
      id: this.generateId(),
      role: 'assistant',
      content,
      timestamp: new Date(),
      personality: this.currentPersonality.id,
      metadata,
    };
    this.conversationHistory.push(message);
    return message;
  }

  getHistory(): AIMessage[] {
    return this.conversationHistory;
  }

  clearHistory() {
    this.conversationHistory = [];
  }

  // Simulate AI response (dalam production, ini akan call actual AI API)
  async processMessage(userMessage: string): Promise<AIMessage> {
    this.addUserMessage(userMessage);

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 500));

    // Generate response based on personality and message
    const response = await this.generateResponse(userMessage);

    return this.addAssistantMessage(response);
  }

  private async generateResponse(message: string): Promise<string> {
    const personality = this.currentPersonality;

    // Command parsing
    if (message.startsWith('/')) {
      return this.handleCommand(message);
    }

    // Contextual response based on personality
    const responses: Record<string, string[]> = {
      genius: [
        `Analyzing your query with advanced reasoning... ${message}`,
        `Let me break this down systematically: ${message}`,
        `From a strategic perspective on "${message}"...`,
      ],
      hacker: [
        `Running security analysis on: ${message}`,
        `Scanning for vulnerabilities in: ${message}`,
        `Initiating penetration test for: ${message}`,
      ],
      trader: [
        `Market analysis indicates for "${message}"...`,
        `Analyzing trading opportunity: ${message}`,
        `Technical indicators suggest: ${message}`,
      ],
      researcher: [
        `Conducting deep research on: ${message}`,
        `Data analysis shows: ${message}`,
        `Research findings for "${message}"...`,
      ],
      creative: [
        `Here's a creative take on "${message}"...`,
        `Let me brainstorm some ideas about: ${message}`,
        `Innovative approach to: ${message}`,
      ],
      autonomous: [
        `Executing autonomous task: ${message}`,
        `Processing and learning from: ${message}`,
        `Autonomous analysis complete for: ${message}`,
      ],
    };

    const personalityResponses = responses[personality.id] || responses.genius;
    const response = personalityResponses[Math.floor(Math.random() * personalityResponses.length)];

    return response;
  }

  private handleCommand(command: string): string {
    const [cmd, ...args] = command.slice(1).split(' ');

    switch (cmd) {
      case 'help':
        return this.getHelpText();
      case 'memory':
        return this.handleMemoryCommand(args);
      case 'task':
        return this.handleTaskCommand(args);
      case 'plugin':
        return this.handlePluginCommand(args);
      case 'stats':
        return this.getStats();
      case 'export':
        return this.exportData();
      default:
        return `Unknown command: ${cmd}. Type /help for available commands.`;
    }
  }

  private getHelpText(): string {
    return `
🤖 AI Agent Terminal Commands:

/help - Show this help
/memory [save|load|clear] - Memory management
/task [create|list|run] - Task management
/plugin [load|list|unload] - Plugin system
/stats - Show AI statistics
/export - Export conversation data

Personalities: ${Object.keys(AI_PERSONALITIES).join(', ')}
Current: ${this.currentPersonality.name}
    `.trim();
  }

  private handleMemoryCommand(args: string[]): string {
    const action = args[0];
    switch (action) {
      case 'save':
        this.saveMemory();
        return 'Memory saved successfully!';
      case 'clear':
        this.memory.clear();
        this.saveMemory();
        return 'Memory cleared!';
      case 'stats':
        return `Memory entries: ${this.memory.size}`;
      default:
        return 'Usage: /memory [save|clear|stats]';
    }
  }

  private handleTaskCommand(args: string[]): string {
    const action = args[0];
    switch (action) {
      case 'list':
        return `Tasks: ${this.tasks.length} total`;
      case 'create':
        const description = args.slice(1).join(' ');
        this.createTask(description);
        return `Task created: ${description}`;
      default:
        return 'Usage: /task [create|list]';
    }
  }

  private handlePluginCommand(args: string[]): string {
    return `Plugins: ${this.plugins.size} loaded`;
  }

  private getStats(): string {
    return `
📊 AI Agent Stats:
- Messages: ${this.conversationHistory.length}
- Current Personality: ${this.currentPersonality.name}
- Tasks: ${this.tasks.length}
- Plugins: ${this.plugins.size}
- Memory: ${this.memory.size} entries
    `.trim();
  }

  private exportData(): string {
    const data = {
      history: this.conversationHistory,
      personality: this.currentPersonality.id,
      tasks: this.tasks,
      timestamp: new Date().toISOString(),
    };

    if (typeof window !== 'undefined') {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai-session-${Date.now()}.json`;
      a.click();
    }

    return 'Data exported successfully!';
  }

  private createTask(description: string): AITask {
    const task: AITask = {
      id: this.generateId(),
      type: 'custom',
      description,
      status: 'pending',
      createdAt: new Date(),
    };
    this.tasks.push(task);
    return task;
  }

  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  // Plugin system
  loadPlugin(name: string, plugin: any) {
    this.plugins.set(name, plugin);
  }

  unloadPlugin(name: string) {
    this.plugins.delete(name);
  }

  // Memory operations
  remember(key: string, value: any) {
    this.memory.set(key, value);
    this.saveMemory();
  }

  recall(key: string): any {
    return this.memory.get(key);
  }

  forget(key: string) {
    this.memory.delete(key);
    this.saveMemory();
  }
}

export default AIEngine;
