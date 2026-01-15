"""
Configuration module for AI Agent
Loads settings from environment variables
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration settings for the AI agent"""

    # LLM Settings
    GROQ_API_KEY: Optional[str] = os.getenv('GROQ_API_KEY')
    LLM_MODEL: str = os.getenv('LLM_MODEL', 'llama3')

    # Twitter Settings
    TWITTER_API_KEY: Optional[str] = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET: Optional[str] = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN: Optional[str] = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_BEARER_TOKEN: Optional[str] = os.getenv('TWITTER_BEARER_TOKEN')

    # Ethereum Wallet Settings
    ETH_PRIVATE_KEY: Optional[str] = os.getenv('ETH_PRIVATE_KEY')
    ETH_RPC_URL: str = os.getenv('ETH_RPC_URL', 'https://eth.llamarpc.com')

    # Solana Wallet Settings
    SOL_PRIVATE_KEY: Optional[str] = os.getenv('SOL_PRIVATE_KEY')
    SOL_RPC_URL: str = os.getenv('SOL_RPC_URL', 'https://api.mainnet-beta.solana.com')

    # Agent Behavior Settings
    MIN_WAIT_MINUTES: int = int(os.getenv('MIN_WAIT_MINUTES', '15'))
    MAX_WAIT_MINUTES: int = int(os.getenv('MAX_WAIT_MINUTES', '120'))
    ACTION_PROBABILITY: float = float(os.getenv('ACTION_PROBABILITY', '0.7'))

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / 'data'
    LOG_FILE: Path = DATA_DIR / 'agent.log'

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        warnings = []

        # Check LLM
        if not cls.GROQ_API_KEY:
            warnings.append("GROQ_API_KEY not set - will use Ollama or mock mode")

        # Check Twitter
        twitter_keys = [
            cls.TWITTER_API_KEY,
            cls.TWITTER_API_SECRET,
            cls.TWITTER_ACCESS_TOKEN,
            cls.TWITTER_ACCESS_TOKEN_SECRET
        ]
        if not all(twitter_keys):
            warnings.append("Twitter credentials incomplete - Twitter posting disabled")

        # Check Wallets
        if not cls.ETH_PRIVATE_KEY and not cls.SOL_PRIVATE_KEY:
            warnings.append("No wallet keys set - Wallet functionality disabled")

        if warnings:
            print("\n⚠️  Configuration Warnings:")
            for warning in warnings:
                print(f"   - {warning}")
            print()

        return True

    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        (cls.DATA_DIR / 'chromadb').mkdir(exist_ok=True)


# Ensure directories exist on import
Config.ensure_directories()
