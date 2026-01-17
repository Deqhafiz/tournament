# 🎮 AI Agent Terminal - Demo & Tutorial

## Quick Start Demo

### 1. Setup & Installation

```bash
# Clone the repository
git clone https://github.com/Deqhafiz/tournament.git
cd tournament

# Install dependencies
npm install

# Run development server
npm run dev
```

Open your browser at `http://localhost:3000`

### 2. First Interaction

When you open the terminal, you'll see:

```
🚀 AI Agent Terminal v2.0 - Beyond Truth Terminal
Type /help for commands or just chat with me!
```

### 3. Basic Commands Demo

#### Get Help
```bash
$ /help
```

Response:
```
🤖 AI Agent Terminal Commands:

/help - Show this help
/memory [save|load|clear] - Memory management
/task [create|list|run] - Task management
/plugin [load|list|unload] - Plugin system
/stats - Show AI statistics
/export - Export conversation data

Personalities: genius, hacker, trader, researcher, creative, autonomous
Current: Genius Mode
```

#### View Stats
```bash
$ /stats
```

Response:
```
📊 AI Agent Stats:
- Messages: 5
- Current Personality: Genius Mode
- Tasks: 0
- Plugins: 0
- Memory: 0 entries
```

### 4. Switching AI Personalities

#### Genius Mode (Default)
```bash
$ @genius
$ How can I optimize a binary search algorithm?
```

Response: Detailed algorithm optimization with Big-O analysis

#### Hacker Mode
```bash
$ @hacker
$ Explain SQL injection vulnerabilities
```

Response: In-depth security analysis with prevention techniques

#### Crypto Trader Mode
```bash
$ @trader
$ Analyze current T-Coin market trends
```

Response: Market analysis with trading signals

#### Research Mode
```bash
$ @researcher
$ What are the latest trends in AI?
```

Response: Data-driven research with citations

#### Creative Mode
```bash
$ @creative
$ Write a viral tweet about AI agents
```

Response: Creative content with marketing insights

#### Autonomous Mode
```bash
$ @autonomous
$ Scrape cryptocurrency prices and analyze them
```

Response: Autonomous execution with progress updates

### 5. Task Management Demo

#### Create Tasks
```bash
$ /task create Analyze market data
```

Response:
```
Task created: Analyze market data
```

#### List Tasks
```bash
$ /task list
```

Response:
```
Tasks: 1 total
- Task #1: Analyze market data [pending]
```

### 6. Memory System Demo

#### Save Information
```bash
$ Remember that my favorite crypto is T-Coin
```

AI will remember this in future conversations

#### Save Memory
```bash
$ /memory save
```

Response:
```
Memory saved successfully!
```

#### Check Memory Stats
```bash
$ /memory stats
```

Response:
```
Memory entries: 3
```

### 7. Plugin System Demo

#### Load Web Scraper
```bash
$ /plugin load web-scraper
```

Then use it:
```bash
$ Scrape https://example.com
```

#### Load Code Executor
```bash
$ /plugin load code-executor
```

Then execute code:
```bash
$ Execute JavaScript: console.log("Hello from AI Agent!")
```

### 8. T-Coin Integration Demo

#### Initialize Wallet
```bash
$ Initialize my T-Coin wallet
```

Response:
```
✅ Wallet initialized!
Address: 0xabc123...
Balance: 0 T-Coin
```

#### Start Mining
```bash
$ Start mining T-Coin
```

Response:
```
⛏️ Mining started!
Mining... Block found! +5.3 T-Coin
Current balance: 5.3 T-Coin
```

#### Check Price
```bash
$ What's the current T-Coin price?
```

Response:
```
💰 T-Coin Price: $45.67
24h Change: +12.3%
Volume: $1.2M
```

#### Get Trading Signals
```bash
$ Give me T-Coin trading signals
```

Response:
```
📊 Trading Signals:
✅ BUY: Strong support at $50
⚠️ HOLD: Accumulation phase detected
📈 BULLISH: Volume increasing
```

### 9. Autonomous Task Execution Demo

```bash
$ @autonomous
$ Create a task to monitor T-Coin price every hour and alert me if it goes above $100
```

Response:
```
✅ Autonomous task created!
Task ID: task_1234567890
Status: Running
Progress: 0%

Monitoring T-Coin price...
Current: $45.67 (below threshold)
Next check in 1 hour
```

### 10. Advanced Usage Examples

#### Multi-Step Task
```bash
$ @genius
$ Analyze T-Coin whitepaper, extract key points, and create a summary report
```

AI will:
1. Fetch the whitepaper
2. Parse and analyze content
3. Extract key points
4. Generate summary
5. Export as markdown

#### Code Execution
```bash
$ @hacker
$ Write and execute a script to check if port 80 is open
```

AI will:
1. Write the scanning script
2. Execute safely in sandbox
3. Return results

#### Data Analysis
```bash
$ @researcher
$ Scrape top 10 crypto prices and create a comparison chart
```

AI will:
1. Scrape data from multiple sources
2. Process and clean data
3. Generate analysis
4. Create visualization data

### 11. Export & Import Sessions

#### Export Current Session
```bash
$ /export
```

Downloads: `ai-session-1234567890.json`

#### Import Session (Future Feature)
```bash
$ /import session.json
```

### 12. Keyboard Shortcuts

- `Ctrl + L` - Clear screen (keeps history)
- `Up/Down Arrow` - Navigate command history
- `Tab` - Auto-complete commands
- `Ctrl + C` - Cancel current operation

### 13. Personality Comparison

| Personality | Use Case | Temperature | Best For |
|------------|----------|-------------|----------|
| Genius | Problem solving | 0.7 | Complex tasks, algorithms |
| Hacker | Security | 0.5 | Security audit, penetration testing |
| Trader | Crypto trading | 0.6 | Market analysis, trading |
| Researcher | Research | 0.4 | Data analysis, fact-finding |
| Creative | Content | 0.9 | Writing, marketing, ideas |
| Autonomous | Automation | 0.7 | Background tasks, monitoring |

### 14. Tips & Tricks

1. **Chain Commands**: Use `;` to chain multiple commands
   ```bash
   $ @trader; /stats; Check T-Coin price
   ```

2. **Persistent Memory**: AI remembers context across sessions
   ```bash
   $ Remember my trading strategy is conservative
   $ /memory save
   ```

3. **Priority Tasks**: Use `!` prefix for high priority
   ```bash
   $ /task create !URGENT: Check security vulnerability
   ```

4. **Batch Operations**: Process multiple items
   ```bash
   $ Analyze these coins: BTC, ETH, T-Coin, SOL
   ```

5. **Context Awareness**: AI remembers your conversation
   ```bash
   $ What's the price of T-Coin?
   $ And what about yesterday? (AI knows you mean T-Coin)
   ```

### 15. Troubleshooting

#### Terminal Not Responding
```bash
$ /stats  # Check if system is working
$ /clear  # Clear and restart
```

#### Memory Full
```bash
$ /memory clear  # Clear old memory
$ /export  # Export before clearing
```

#### Task Stuck
```bash
$ /task list  # Check task status
$ /task cancel <task-id>  # Cancel stuck task
```

### 16. Production Integration

#### API Usage
```javascript
// Chat API
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Hello AI!',
    personality: 'genius'
  })
});

const data = await response.json();
console.log(data.message);
```

#### T-Coin API
```javascript
// Get market data
const market = await fetch('/api/tcoin').then(r => r.json());
console.log(`Price: $${market.price}`);

// Send transaction
const tx = await fetch('/api/tcoin', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    action: 'send',
    to: '0x123...',
    amount: 10
  })
});
```

### 17. Custom Plugin Development

```typescript
// Create custom plugin
class MyCustomPlugin {
  name = 'my-plugin';
  version = '1.0.0';

  async execute(params: any) {
    // Your logic here
    return { success: true, data: 'Result' };
  }
}

// Load in terminal
engine.loadPlugin('my-plugin', new MyCustomPlugin());
```

### 18. Environment Variables

Create `.env.local`:
```bash
# AI API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...

# App Config
NEXT_PUBLIC_APP_URL=http://localhost:3000

# T-Coin Config
NEXT_PUBLIC_TCOIN_NETWORK=mainnet
NEXT_PUBLIC_TCOIN_RPC_URL=https://rpc.tcoin.network
```

### 19. Deployment

#### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production
vercel --prod
```

#### Docker
```bash
# Build
docker build -t ai-terminal .

# Run
docker run -p 3000:3000 ai-terminal
```

### 20. Next Steps

1. ✅ Complete this demo
2. 🎯 Try all personalities
3. 💰 Initialize T-Coin wallet
4. 🤖 Create autonomous tasks
5. 🔌 Build custom plugins
6. 🚀 Deploy to production

---

**AI Agent Terminal v2.0** - The Most Advanced AI Terminal 🚀

Need help? Type `/help` in the terminal or check the [documentation](README.md)
