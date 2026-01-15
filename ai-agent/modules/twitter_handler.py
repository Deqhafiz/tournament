"""
Twitter Handler Module
Manages Twitter API integration for posting tweets
"""

import os
import logging
from typing import Optional, Dict, Any
import tweepy
from datetime import datetime

logger = logging.getLogger(__name__)


class TwitterHandler:
    """Handles Twitter API operations using tweepy"""

    def __init__(self):
        """Initialize Twitter API client"""
        self.client = None
        self.api = None
        self.enabled = False

        try:
            # Load credentials from environment variables
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

            # Check if credentials are available
            if not all([api_key, api_secret, access_token, access_token_secret]):
                logger.warning("⚠️  Twitter credentials not found. Twitter posting disabled.")
                logger.info("Set environment variables: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET")
                return

            # Initialize Tweepy Client (v2 API)
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )

            # Also initialize v1.1 API for additional features
            auth = tweepy.OAuth1UserHandler(
                api_key, api_secret, access_token, access_token_secret
            )
            self.api = tweepy.API(auth)

            # Verify credentials
            try:
                user = self.api.verify_credentials()
                self.enabled = True
                logger.info(f"✅ Twitter API initialized. Connected as: @{user.screen_name}")
            except Exception as e:
                logger.error(f"Twitter authentication failed: {e}")
                self.enabled = False

        except Exception as e:
            logger.error(f"Error initializing Twitter handler: {e}")
            self.enabled = False

    def post_tweet(self, text: str) -> bool:
        """
        Post a tweet

        Args:
            text: Tweet text (max 280 characters)

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.warning("🐦 Twitter disabled - Would have tweeted: " + text[:100])
            return False

        try:
            # Truncate if too long
            if len(text) > 280:
                text = text[:277] + "..."

            # Post tweet
            response = self.client.create_tweet(text=text)

            if response.data:
                tweet_id = response.data['id']
                logger.info(f"✅ Tweet posted successfully! ID: {tweet_id}")
                logger.info(f"   Content: {text[:100]}")
                return True
            else:
                logger.error("Tweet posted but no response data received")
                return False

        except tweepy.TweepyException as e:
            logger.error(f"Error posting tweet: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error posting tweet: {e}")
            return False

    def post_reply(self, text: str, reply_to_id: str) -> bool:
        """
        Post a reply to a tweet

        Args:
            text: Reply text
            reply_to_id: Tweet ID to reply to

        Returns:
            True if successful
        """
        if not self.enabled:
            logger.warning("Twitter disabled - Would have replied")
            return False

        try:
            # Truncate if needed
            if len(text) > 280:
                text = text[:277] + "..."

            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=reply_to_id
            )

            if response.data:
                logger.info(f"✅ Reply posted successfully!")
                return True
            return False

        except Exception as e:
            logger.error(f"Error posting reply: {e}")
            return False

    def get_mentions(self, limit: int = 10) -> list:
        """
        Get recent mentions

        Args:
            limit: Number of mentions to retrieve

        Returns:
            List of mention objects
        """
        if not self.enabled:
            return []

        try:
            # Get authenticated user ID
            me = self.api.verify_credentials()

            # Get mentions
            mentions = self.client.get_users_mentions(
                id=me.id,
                max_results=limit,
                tweet_fields=['created_at', 'author_id', 'text']
            )

            if mentions.data:
                logger.info(f"📬 Retrieved {len(mentions.data)} mentions")
                return mentions.data
            return []

        except Exception as e:
            logger.error(f"Error getting mentions: {e}")
            return []

    def get_timeline(self, limit: int = 10) -> list:
        """
        Get home timeline tweets

        Args:
            limit: Number of tweets to retrieve

        Returns:
            List of tweet objects
        """
        if not self.enabled:
            return []

        try:
            tweets = self.api.home_timeline(count=limit)
            logger.info(f"📰 Retrieved {len(tweets)} timeline tweets")
            return tweets

        except Exception as e:
            logger.error(f"Error getting timeline: {e}")
            return []

    def search_tweets(self, query: str, limit: int = 10) -> list:
        """
        Search for tweets

        Args:
            query: Search query
            limit: Number of results

        Returns:
            List of tweet objects
        """
        if not self.enabled:
            return []

        try:
            response = self.client.search_recent_tweets(
                query=query,
                max_results=limit,
                tweet_fields=['created_at', 'author_id', 'text']
            )

            if response.data:
                logger.info(f"🔍 Found {len(response.data)} tweets for query: {query}")
                return response.data
            return []

        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get Twitter account stats"""
        if not self.enabled:
            return {'enabled': False}

        try:
            user = self.api.verify_credentials()
            return {
                'enabled': True,
                'username': user.screen_name,
                'followers': user.followers_count,
                'following': user.friends_count,
                'tweets': user.statuses_count,
                'verified': user.verified
            }

        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'enabled': False, 'error': str(e)}


class MockTwitterHandler(TwitterHandler):
    """Mock Twitter handler for testing without real API"""

    def __init__(self):
        """Initialize mock handler"""
        self.enabled = True
        self.tweets = []
        logger.info("✅ Mock Twitter handler initialized (testing mode)")

    def post_tweet(self, text: str) -> bool:
        """Mock tweet posting"""
        if len(text) > 280:
            text = text[:277] + "..."

        tweet = {
            'id': f"mock_{len(self.tweets)}",
            'text': text,
            'timestamp': datetime.now().isoformat()
        }
        self.tweets.append(tweet)

        logger.info(f"🐦 [MOCK] Posted tweet: {text[:100]}")
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Mock stats"""
        return {
            'enabled': True,
            'username': 'chaotic_agent_test',
            'followers': 0,
            'following': 0,
            'tweets': len(self.tweets),
            'mode': 'MOCK'
        }


if __name__ == "__main__":
    # Test the Twitter handler
    logging.basicConfig(level=logging.INFO)

    # Test with mock
    twitter = MockTwitterHandler()
    twitter.post_tweet("Testing the chaotic agent 🌀")
    print(twitter.get_stats())
