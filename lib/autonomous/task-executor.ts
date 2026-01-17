/**
 * Autonomous Task Executor
 * Sistem untuk menjalankan tasks secara autonomous
 */

export interface AutonomousTask {
  id: string;
  name: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'queued' | 'running' | 'completed' | 'failed' | 'paused';
  progress: number;
  createdAt: Date;
  startedAt?: Date;
  completedAt?: Date;
  result?: any;
  error?: string;
  dependencies?: string[];
  retries: number;
  maxRetries: number;
}

export interface TaskExecutorConfig {
  maxConcurrent: number;
  retryDelay: number;
  defaultMaxRetries: number;
}

export class AutonomousTaskExecutor {
  private tasks: Map<string, AutonomousTask> = new Map();
  private runningTasks: Set<string> = new Set();
  private taskQueue: string[] = [];
  private config: TaskExecutorConfig;
  private isRunning = false;

  constructor(config?: Partial<TaskExecutorConfig>) {
    this.config = {
      maxConcurrent: config?.maxConcurrent || 3,
      retryDelay: config?.retryDelay || 5000,
      defaultMaxRetries: config?.defaultMaxRetries || 3,
    };
  }

  createTask(
    name: string,
    description: string,
    executor: () => Promise<any>,
    options?: {
      priority?: AutonomousTask['priority'];
      dependencies?: string[];
      maxRetries?: number;
    }
  ): string {
    const taskId = this.generateTaskId();

    const task: AutonomousTask = {
      id: taskId,
      name,
      description,
      priority: options?.priority || 'medium',
      status: 'queued',
      progress: 0,
      createdAt: new Date(),
      dependencies: options?.dependencies || [],
      retries: 0,
      maxRetries: options?.maxRetries || this.config.defaultMaxRetries,
    };

    this.tasks.set(taskId, task);
    this.queueTask(taskId);

    return taskId;
  }

  private queueTask(taskId: string) {
    const task = this.tasks.get(taskId);
    if (!task) return;

    // Insert based on priority
    const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
    const taskPriority = priorityOrder[task.priority];

    let insertIndex = this.taskQueue.length;
    for (let i = 0; i < this.taskQueue.length; i++) {
      const queuedTask = this.tasks.get(this.taskQueue[i]);
      if (queuedTask && priorityOrder[queuedTask.priority] > taskPriority) {
        insertIndex = i;
        break;
      }
    }

    this.taskQueue.splice(insertIndex, 0, taskId);
  }

  async start() {
    if (this.isRunning) return;

    this.isRunning = true;
    this.processQueue();
  }

  stop() {
    this.isRunning = false;
  }

  private async processQueue() {
    while (this.isRunning) {
      // Check if we can run more tasks
      if (this.runningTasks.size < this.config.maxConcurrent && this.taskQueue.length > 0) {
        const taskId = this.taskQueue.shift();
        if (taskId) {
          this.executeTask(taskId);
        }
      }

      // Wait before next check
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  private async executeTask(taskId: string) {
    const task = this.tasks.get(taskId);
    if (!task) return;

    // Check dependencies
    if (task.dependencies && task.dependencies.length > 0) {
      const allDepsCompleted = task.dependencies.every(depId => {
        const dep = this.tasks.get(depId);
        return dep && dep.status === 'completed';
      });

      if (!allDepsCompleted) {
        // Re-queue if dependencies not met
        this.taskQueue.push(taskId);
        return;
      }
    }

    this.runningTasks.add(taskId);
    task.status = 'running';
    task.startedAt = new Date();

    try {
      // Simulate task execution
      task.progress = 0;

      // Progressive updates
      for (let i = 0; i <= 100; i += 10) {
        task.progress = i;
        await new Promise(resolve => setTimeout(resolve, 200));
      }

      task.status = 'completed';
      task.completedAt = new Date();
      task.progress = 100;
      task.result = { success: true, message: `Task ${task.name} completed successfully` };
    } catch (error: any) {
      task.error = error.message;

      if (task.retries < task.maxRetries) {
        // Retry
        task.retries++;
        task.status = 'queued';
        this.taskQueue.push(taskId);
        await new Promise(resolve => setTimeout(resolve, this.config.retryDelay));
      } else {
        task.status = 'failed';
      }
    } finally {
      this.runningTasks.delete(taskId);
    }
  }

  getTask(taskId: string): AutonomousTask | undefined {
    return this.tasks.get(taskId);
  }

  getAllTasks(): AutonomousTask[] {
    return Array.from(this.tasks.values());
  }

  getTasksByStatus(status: AutonomousTask['status']): AutonomousTask[] {
    return this.getAllTasks().filter(task => task.status === status);
  }

  pauseTask(taskId: string) {
    const task = this.tasks.get(taskId);
    if (task && task.status === 'running') {
      task.status = 'paused';
    }
  }

  resumeTask(taskId: string) {
    const task = this.tasks.get(taskId);
    if (task && task.status === 'paused') {
      task.status = 'queued';
      this.queueTask(taskId);
    }
  }

  cancelTask(taskId: string) {
    const task = this.tasks.get(taskId);
    if (task) {
      task.status = 'failed';
      task.error = 'Cancelled by user';

      // Remove from queue
      const queueIndex = this.taskQueue.indexOf(taskId);
      if (queueIndex > -1) {
        this.taskQueue.splice(queueIndex, 1);
      }
    }
  }

  clearCompleted() {
    const completedTasks = this.getTasksByStatus('completed');
    completedTasks.forEach(task => this.tasks.delete(task.id));
  }

  getStats() {
    return {
      total: this.tasks.size,
      queued: this.getTasksByStatus('queued').length,
      running: this.getTasksByStatus('running').length,
      completed: this.getTasksByStatus('completed').length,
      failed: this.getTasksByStatus('failed').length,
      paused: this.getTasksByStatus('paused').length,
    };
  }

  private generateTaskId(): string {
    return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

export default AutonomousTaskExecutor;
