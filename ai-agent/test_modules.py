#!/usr/bin/env python3
"""
Test script to verify all modules are working
Run this before starting the agent to check your setup
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          🧪 AI Agent Module Testing Suite 🧪             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")


def test_brain():
    """Test the Brain module"""
    print("\n1️⃣  Testing Brain Module...")
    try:
        from modules.brain import Brain

        brain = Brain(
            system_prompt="You are a test AI. Respond with exactly: 'Test successful!'"
        )

        info = brain.get_info()
        print(f"   ✅ Brain initialized")
        print(f"      Provider: {info['provider']}")
        print(f"      Model: {info['model']}")
        print(f"      Ready: {info['ready']}")

        # Try generating
        response = brain.generate("Say hi", max_tokens=50)
        print(f"   ✅ Generation test: {response[:50]}...")

        return True

    except Exception as e:
        print(f"   ❌ Brain test failed: {e}")
        return False


def test_memory():
    """Test the Memory module"""
    print("\n2️⃣  Testing Memory Module...")
    try:
        from modules.memory import Memory

        memory = Memory(collection_name="test_collection")
        stats = memory.get_memory_stats()

        print(f"   ✅ Memory initialized")
        print(f"      Total memories: {stats['total_memories']}")

        # Test storing
        mem_id = memory.store_memory("Test memory", {"type": "test"})
        print(f"   ✅ Stored test memory: {mem_id[:20]}...")

        # Test retrieval
        recent = memory.get_recent_memories(limit=1)
        print(f"   ✅ Retrieved {len(recent)} memories")

        # Test search
        results = memory.search_memories("test", limit=1)
        print(f"   ✅ Search found {len(results)} results")

        return True

    except Exception as e:
        print(f"   ❌ Memory test failed: {e}")
        return False


def test_twitter():
    """Test the Twitter module"""
    print("\n3️⃣  Testing Twitter Module...")
    try:
        from modules.twitter_handler import TwitterHandler, MockTwitterHandler

        # Try real handler first
        twitter = TwitterHandler()

        if twitter.enabled:
            stats = twitter.get_stats()
            print(f"   ✅ Twitter initialized (REAL)")
            print(f"      Username: @{stats.get('username', 'unknown')}")
            print(f"      Followers: {stats.get('followers', 0)}")
        else:
            # Fall back to mock
            twitter = MockTwitterHandler()
            print(f"   ✅ Twitter initialized (MOCK)")
            print(f"      Real credentials not found - using mock mode")

        # Test posting
        success = twitter.post_tweet("🧪 Test tweet (not actually posted)")
        print(f"   ✅ Tweet test: {'Success' if success else 'Failed'}")

        return True

    except Exception as e:
        print(f"   ❌ Twitter test failed: {e}")
        return False


def test_wallet():
    """Test the Wallet module"""
    print("\n4️⃣  Testing Wallet Module...")
    try:
        from modules.wallet_handler import WalletHandler, MockWalletHandler

        # Try real handler
        wallet = WalletHandler()

        if wallet.enabled:
            status = wallet.get_status()
            print(f"   ✅ Wallet initialized (REAL)")
            if status['eth']['enabled']:
                print(f"      ETH: {status['eth']['address']} - {status['eth']['balance']} ETH")
            if status['sol']['enabled']:
                print(f"      SOL: {status['sol']['address']} - {status['sol']['balance']} SOL")
        else:
            # Fall back to mock
            wallet = MockWalletHandler()
            status = wallet.get_status()
            print(f"   ✅ Wallet initialized (MOCK)")
            print(f"      Real credentials not found - using mock mode")
            print(f"      ETH: {status['eth']['balance']} (mock)")
            print(f"      SOL: {status['sol']['balance']} (mock)")

        return True

    except Exception as e:
        print(f"   ❌ Wallet test failed: {e}")
        return False


def test_config():
    """Test configuration"""
    print("\n5️⃣  Testing Configuration...")
    try:
        from config.config import Config

        Config.validate()
        print(f"   ✅ Configuration loaded")
        print(f"      Data directory: {Config.DATA_DIR}")
        print(f"      Model: {Config.LLM_MODEL}")

        return True

    except Exception as e:
        print(f"   ❌ Config test failed: {e}")
        return False


def main():
    """Run all tests"""
    results = {
        "Brain": test_brain(),
        "Memory": test_memory(),
        "Twitter": test_twitter(),
        "Wallet": test_wallet(),
        "Config": test_config()
    }

    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)

    passed = sum(results.values())
    total = len(results)

    for module, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {module}")

    print("="*60)
    print(f"Result: {passed}/{total} modules passed")

    if passed == total:
        print("\n🎉 All tests passed! You're ready to run the agent.")
        print("\nRun: python agent.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check your configuration and dependencies.")
        print("\nMake sure you've:")
        print("  1. Installed requirements: pip install -r requirements.txt")
        print("  2. Configured .env file: cp .env.example .env")
        print("  3. Set up your API keys in .env")
        return 1


if __name__ == "__main__":
    sys.exit(main())
