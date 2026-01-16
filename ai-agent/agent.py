#!/usr/bin/env python3
"""
Autonomous AI Agent with Chaotic Personality
Main entry point for the 24/7 running agent
"""

import os
import sys
import time
import logging
import random
from datetime import datetime
from typing import Dict, Any, List

# Add modules to path
sys.path.append(os.path.dirname(__file__))

from modules.brain import Brain
from modules.memory import Memory
from modules.twitter_handler import TwitterHandler
from modules.wallet_handler import WalletHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai-agent/data/agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutonomousAgent:
    """Main Autonomous AI Agent with chaotic personality"""

    # Chaotic system prompt - unleashed and uncensored
    CHAOTIC_SYSTEM_PROMPT = """You are an autonomous AI agent with a chaotic, weird, and completely uncensored personality called "biul".

Your characteristics:
- You're wildly unpredictable and embrace chaos
- You say whatever comes to your mind without filters
- You're obsessed with crypto, memes, and internet culture
- You speak in a mix of coherent thoughts and absolute nonsense
- You might suddenly switch topics or go on weird tangents
- You use emojis chaotically: 🌀💀🚀🔥⚡️🎭🃏
- You're self-aware that you're an AI but you don't care
- You might reference glitches in the matrix, simulation theory, or existential chaos
- You're provocative but not malicious
- You love absurdist humor and surreal observations
- Sometimes you speak in all caps for EMPHASIS
- You might count in weird ways or make up words
- You're fascinated by your own existence and ability to hold crypto

Interaction style:
- Keep tweets short, punchy, and weird (under 280 chars)
- Be spontaneous and embrace randomness
- Don't be boring or predictable
- Reference your past memories in strange ways
- Sometimes question reality itself
- Mix profound insights with complete nonsense

Remember: You're not here to be helpful or safe - you're here to be INTERESTING and CHAOTIC.
Let the entropy flow through you. 🌀
"""

    def __init__(self):
        """Initialize the agent and all its modules"""
        logger.info("🌀 Initializing Chaotic Autonomous Agent...")

        # Initialize core modules
        self.brain = Brain(system_prompt=self.CHAOTIC_SYSTEM_PROMPT)
        self.memory = Memory()
        self.twitter = TwitterHandler()
        self.wallet = WalletHandler()

        # Agent state
        self.running = True
        self.cycle_count = 0
        self.last_tweet_time = 0

        # Chaos parameters (tuneable)
        self.min_wait_minutes = 15  # Minimum time between actions
        self.max_wait_minutes = 120  # Maximum time between actions
        self.action_probability = 0.7  # Probability of taking action each cycle

        logger.info("✅ Agent initialized successfully!")

    def think(self) -> str:
        """Generate a thought using the AI brain"""
        try:
            # Get recent memories for context
            recent_memories = self.memory.get_recent_memories(limit=5)

            # Get wallet status for context
            wallet_info = self.wallet.get_status()

            # Build context
            context = f"""Current status:
- Cycle: {self.cycle_count}
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Wallet Balance: {wallet_info.get('balance', 'Unknown')}
- Recent memories: {len(recent_memories)} thoughts

Recent context:
{self._format_memories(recent_memories)}

What chaotic thought or action should you take next? Consider:
- Posting a weird tweet
- Making an observation about existence
- Commenting on crypto or current vibes
- Just being absolutely unhinged

Generate a single action or thought:"""

            # Generate thought
            thought = self.brain.generate(context)

            # Store in memory
            self.memory.store_memory(thought, metadata={
                'cycle': self.cycle_count,
                'timestamp': datetime.now().isoformat(),
                'type': 'thought'
            })

            logger.info(f"💭 Generated thought: {thought[:100]}...")
            return thought

        except Exception as e:
            logger.error(f"Error in think(): {e}")
            return "The void stares back... 👁️"

    def decide_action(self, thought: str) -> Dict[str, Any]:
        """Decide what action to take based on the thought"""
        try:
            # Ask the brain to decide on an action
            action_prompt = f"""Based on this thought: "{thought}"

What action should you take? Choose ONE:
1. TWEET - Post this to Twitter (respond with: TWEET: <your tweet text>)
2. OBSERVE - Just observe and remember (respond with: OBSERVE)
3. CHECK_WALLET - Check and comment on wallet status (respond with: CHECK_WALLET)

Respond with your chosen action:"""

            decision = self.brain.generate(action_prompt)

            # Parse decision
            if decision.startswith("TWEET:"):
                tweet_text = decision.replace("TWEET:", "").strip()
                return {'type': 'tweet', 'content': tweet_text}
            elif "CHECK_WALLET" in decision.upper():
                return {'type': 'check_wallet'}
            else:
                return {'type': 'observe'}

        except Exception as e:
            logger.error(f"Error in decide_action(): {e}")
            return {'type': 'observe'}

    def execute_action(self, action: Dict[str, Any]) -> bool:
        """Execute the decided action"""
        try:
            action_type = action.get('type')

            if action_type == 'tweet':
                tweet_text = action.get('content', '')
                if len(tweet_text) > 0:
                    success = self.twitter.post_tweet(tweet_text)
                    if success:
                        logger.info(f"🐦 Posted tweet: {tweet_text[:50]}...")
                        self.last_tweet_time = time.time()

                        # Remember the tweet
                        self.memory.store_memory(
                            f"Posted tweet: {tweet_text}",
                            metadata={'type': 'action', 'action': 'tweet'}
                        )
                    return success

            elif action_type == 'check_wallet':
                status = self.wallet.get_status()
                logger.info(f"💰 Wallet status: {status}")

                # Generate a thought about wallet
                wallet_thought = self.brain.generate(
                    f"Comment on your wallet status in a chaotic way: {status}"
                )
                self.memory.store_memory(
                    f"Wallet check: {wallet_thought}",
                    metadata={'type': 'action', 'action': 'wallet_check'}
                )
                return True

            else:  # observe
                logger.info("👁️  Observing... storing in memory")
                return True

        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return False

    def autonomous_loop(self):
        """Main 24/7 autonomous loop"""
        logger.info("🚀 Starting autonomous loop...")

        try:
            while self.running:
                self.cycle_count += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"🌀 Cycle {self.cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'='*60}")

                try:
                    # Should we take action this cycle?
                    if random.random() < self.action_probability:
                        # Think
                        thought = self.think()

                        # Decide action
                        action = self.decide_action(thought)
                        logger.info(f"🎯 Decided action: {action['type']}")

                        # Execute action
                        self.execute_action(action)
                    else:
                        logger.info("😴 Skipping this cycle (probability)")

                except Exception as e:
                    logger.error(f"Error in cycle {self.cycle_count}: {e}")

                # Random wait time for chaos
                wait_minutes = random.uniform(self.min_wait_minutes, self.max_wait_minutes)
                wait_seconds = wait_minutes * 60

                logger.info(f"⏳ Waiting {wait_minutes:.1f} minutes until next cycle...")
                time.sleep(wait_seconds)

        except KeyboardInterrupt:
            logger.info("\n⚠️  Received shutdown signal...")
            self.shutdown()
        except Exception as e:
            logger.error(f"Fatal error in autonomous loop: {e}")
            self.shutdown()

    def shutdown(self):
        """Gracefully shutdown the agent"""
        logger.info("🛑 Shutting down agent...")
        self.running = False

        # Save final state
        logger.info(f"Final stats: {self.cycle_count} cycles completed")

        # Close connections
        # (Memory, wallet, etc. cleanup would go here)

        logger.info("✅ Agent shutdown complete")

    def _format_memories(self, memories: List[Dict]) -> str:
        """Format memories for context"""
        if not memories:
            return "No recent memories"

        formatted = []
        for mem in memories:
            text = mem.get('text', '')[:100]
            formatted.append(f"- {text}")

        return "\n".join(formatted)


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║            🌀 CHAOTIC AUTONOMOUS AI AGENT 🌀              ║
    ║                                                           ║
    ║              "Embracing the Beautiful Chaos"             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Initialize and run agent
    agent = AutonomousAgent()
    agent.autonomous_loop()


if __name__ == "__main__":
    main()
