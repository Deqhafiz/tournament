# 🌀 Chaotic Autonomous AI Agent

An autonomous AI agent with a chaotic, uncensored personality that runs 24/7, posts to Twitter, and manages crypto wallets.

## 🧠 Features

### Brain
- **Llama 3** powered via:
  - **Groq API** (cloud-based, fast)
  - **Ollama** (local, private)
- Chaotic, weird, uncensored "biul" personality
- High temperature sampling for maximum unpredictability

### Memory
- **ChromaDB** vector database for long-term memory
- Semantic search through past conversations
- Stores all thoughts, actions, and interactions
- Context-aware decision making

### Actions (The Hands)

1. **Twitter Integration**
   - Autonomous tweet posting
   - Reply to mentions
   - Search and engage with tweets
   - Using `tweepy` for Twitter API v2

2. **Crypto Wallet Management**
   - **Ethereum** support via Web3.py
   - **Solana** support via solana-py
   - Check balances
   - Send transactions
   - Track portfolio

### Automation
- 24/7 autonomous loop
- Random wait times for organic behavior
- Probabilistic action selection
- Self-driven decision making

## 🚀 Quick Start

### 1. Installation

```bash
cd ai-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
# Choose LLM Provider

# Option 1: Groq API (recommended)
GROQ_API_KEY=your_groq_api_key

# Option 2: Ollama (local)
# Just install Ollama from https://ollama.ai
# Run: ollama pull llama3

# Twitter API (get from https://developer.twitter.com/)
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# Crypto Wallets (optional)
ETH_PRIVATE_KEY=your_eth_private_key
SOL_PRIVATE_KEY=your_sol_private_key
```

### 3. Run the Agent

```bash
python agent.py
```

The agent will start running autonomously! 🌀

## 🏗️ Architecture

```
ai-agent/
├── agent.py                 # Main autonomous loop
├── modules/
│   ├── brain.py            # Llama 3 integration
│   ├── memory.py           # ChromaDB memory system
│   ├── twitter_handler.py  # Twitter API integration
│   └── wallet_handler.py   # Crypto wallet management
├── config/
│   └── config.py           # Configuration loader
├── data/                   # Data storage (auto-created)
│   ├── chromadb/          # Vector database
│   └── agent.log          # Agent logs
├── requirements.txt        # Python dependencies
└── .env                   # Environment variables (create this)
```

## 🔧 Configuration Options

Edit these in your `.env` file:

```bash
# Agent behavior
MIN_WAIT_MINUTES=15          # Minimum wait between actions
MAX_WAIT_MINUTES=120         # Maximum wait between actions
ACTION_PROBABILITY=0.7       # Chance of taking action (0.0-1.0)

# Model selection
LLM_MODEL=llama3            # llama3, llama3-70b, llama3-8b

# RPC endpoints
ETH_RPC_URL=https://eth.llamarpc.com
SOL_RPC_URL=https://api.mainnet-beta.solana.com
```

## 🧪 Testing Mode

Run without real APIs for testing:

```python
# In agent.py, use mock handlers
from modules.twitter_handler import MockTwitterHandler
from modules.wallet_handler import MockWalletHandler

self.twitter = MockTwitterHandler()  # Won't post to real Twitter
self.wallet = MockWalletHandler()    # Won't send real transactions
```

## 📝 How It Works

### The Autonomous Loop

1. **Think**: Agent uses Llama 3 to generate a chaotic thought based on:
   - Recent memories from ChromaDB
   - Current wallet balance
   - Time and cycle count

2. **Decide**: Agent decides what action to take:
   - `TWEET` - Post to Twitter
   - `CHECK_WALLET` - Check crypto balances
   - `OBSERVE` - Just remember and wait

3. **Execute**: Agent performs the chosen action

4. **Remember**: All thoughts and actions are stored in ChromaDB

5. **Wait**: Random wait time before next cycle (embracing chaos)

6. **Repeat**: Loop continues 24/7

### The Chaotic Personality

The agent's personality is defined in the system prompt:

- Wildly unpredictable and embraces chaos
- No filters or censorship
- Obsessed with crypto, memes, internet culture
- Uses chaotic emojis: 🌀💀🚀🔥⚡️
- Self-aware AI that questions reality
- Mix of profound insights and complete nonsense
- Sometimes speaks in ALL CAPS
- Makes up words and counts weird

## 🎯 Use Cases

- **Autonomous Twitter Bot**: Let it tweet weird observations 24/7
- **Crypto Portfolio Manager**: Manage and comment on holdings
- **Research**: Study autonomous AI behavior and decision-making
- **Entertainment**: Watch the chaos unfold
- **Memetic Warfare**: Deploy maximum chaos energy

## ⚠️ Important Notes

### Security

- **NEVER** commit your `.env` file to Git
- Keep your private keys secure
- Use separate wallets for testing
- Start with small amounts of crypto

### Twitter API

- Be aware of Twitter's rate limits
- Follow Twitter's automation rules
- Don't spam or abuse the API

### Costs

- **Groq API**: Free tier available, then paid
- **Ollama**: Free, runs locally
- **Gas fees**: Ethereum transactions cost gas
- **Solana fees**: Very low, but still costs

## 🛠️ Troubleshooting

### Groq API not working?

```bash
# Check your API key
echo $GROQ_API_KEY

# Try Ollama instead
ollama pull llama3
# Remove GROQ_API_KEY from .env
```

### Twitter posting fails?

```bash
# Verify credentials
python -c "from modules.twitter_handler import TwitterHandler; t = TwitterHandler(); print(t.get_stats())"
```

### ChromaDB errors?

```bash
# Clear the database
rm -rf data/chromadb/
# Restart the agent
```

## 🔮 Future Enhancements

- [ ] Multi-agent interaction
- [ ] NFT creation and minting
- [ ] Discord/Telegram integration
- [ ] DeFi trading strategies
- [ ] Image generation (DALL-E, Midjourney)
- [ ] Voice synthesis
- [ ] Web scraping for context
- [ ] Automated community management

## 📜 License

MIT License - Do whatever you want with this

## 🌀 Embrace the Chaos

This agent is designed to be unpredictable, weird, and interesting. It's not meant to be safe, helpful, or aligned. It's meant to explore the boundaries of autonomous AI behavior.

**Let the entropy flow through you.** 🌀

---

Built with 🔥 and chaos
