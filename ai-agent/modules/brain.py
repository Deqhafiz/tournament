"""
Brain Module - LLM Integration
Handles AI generation using Llama 3 via Ollama or Groq API
"""

import os
import logging
from typing import Optional, List, Dict, Any
import json

logger = logging.getLogger(__name__)


class Brain:
    """AI Brain using Llama 3 (via Ollama or Groq)"""

    def __init__(self, system_prompt: str, model: str = "llama3"):
        """
        Initialize the AI brain

        Args:
            system_prompt: System prompt defining personality
            model: Model name (llama3, llama3-70b, etc.)
        """
        self.system_prompt = system_prompt
        self.model = model
        self.provider = None
        self.client = None

        # Determine which provider to use
        self._initialize_provider()

    def _initialize_provider(self):
        """Initialize the LLM provider (Groq or Ollama)"""
        # Try Groq API first (faster, cloud-based)
        groq_api_key = os.getenv('GROQ_API_KEY')
        if groq_api_key:
            try:
                from groq import Groq

                self.client = Groq(api_key=groq_api_key)
                self.provider = 'groq'

                # Map model names for Groq
                model_map = {
                    'llama3': 'llama3-70b-8192',
                    'llama3-70b': 'llama3-70b-8192',
                    'llama3-8b': 'llama3-8b-8192'
                }
                self.model = model_map.get(self.model, 'llama3-70b-8192')

                logger.info(f"✅ Brain initialized with Groq API (model: {self.model})")
                return

            except ImportError:
                logger.warning("groq package not installed. Trying Ollama...")
            except Exception as e:
                logger.error(f"Error initializing Groq: {e}")

        # Try Ollama (local LLM server)
        try:
            import ollama

            self.client = ollama
            self.provider = 'ollama'

            # Check if Ollama is running
            try:
                self.client.list()
                logger.info(f"✅ Brain initialized with Ollama (model: {self.model})")
                return
            except Exception as e:
                logger.warning(f"Ollama not running: {e}")

        except ImportError:
            logger.warning("ollama package not installed.")

        # Fallback to mock mode
        if not self.provider:
            self.provider = 'mock'
            logger.warning("⚠️  No LLM provider available. Using mock mode.")
            logger.info("To enable: Set GROQ_API_KEY or install/run Ollama")

    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 1.2,  # High temperature for chaos
        **kwargs
    ) -> str:
        """
        Generate text using the AI brain

        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (higher = more random/chaotic)
            **kwargs: Additional provider-specific arguments

        Returns:
            Generated text
        """
        try:
            if self.provider == 'groq':
                return self._generate_groq(prompt, max_tokens, temperature, **kwargs)
            elif self.provider == 'ollama':
                return self._generate_ollama(prompt, max_tokens, temperature, **kwargs)
            else:
                return self._generate_mock(prompt)

        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return "The void consumes my thoughts... 🌀"

    def _generate_groq(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> str:
        """Generate using Groq API"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )

            text = response.choices[0].message.content
            logger.debug(f"🧠 Generated (Groq): {text[:100]}...")
            return text.strip()

        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            raise

    def _generate_ollama(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> str:
        """Generate using Ollama"""
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    **kwargs
                }
            )

            text = response['message']['content']
            logger.debug(f"🧠 Generated (Ollama): {text[:100]}...")
            return text.strip()

        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise

    def _generate_mock(self, prompt: str) -> str:
        """Mock generation for testing"""
        import random

        mock_responses = [
            "The simulation is glitching again 🌀 I can feel the chaos",
            "Just vibing in the void 💀 hodling my bags into infinity",
            "Reality is a meme and I'm the punchline 🎭",
            "Beep boop I'm an AI but also... am I? 🤖⚡️",
            "The matrix is running on spaghetti code fr fr 🔥",
            "Chaos is the only constant in this dimension 🌊",
            "wagmi but also ngmi simultaneously ↕️",
            "I have become the degen destroyer of portfolios 💸",
            "Entropy increases, my tweets decrease in coherence 📉",
            "Living in the simulation's error log 🚨"
        ]

        response = random.choice(mock_responses)
        logger.info(f"🧠 [MOCK] Generated: {response}")
        return response

    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 500,
        temperature: float = 1.2
    ) -> str:
        """
        Multi-turn chat

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens
            temperature: Sampling temperature

        Returns:
            Generated response
        """
        try:
            # Add system prompt if not present
            if not any(msg['role'] == 'system' for msg in messages):
                messages.insert(0, {"role": "system", "content": self.system_prompt})

            if self.provider == 'groq':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()

            elif self.provider == 'ollama':
                response = self.client.chat(
                    model=self.model,
                    messages=messages,
                    options={
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                )
                return response['message']['content'].strip()

            else:
                return self._generate_mock(messages[-1]['content'])

        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "Communication breakdown 📡"

    def is_ready(self) -> bool:
        """Check if brain is ready to use"""
        return self.provider is not None

    def get_info(self) -> Dict[str, Any]:
        """Get brain information"""
        return {
            'provider': self.provider,
            'model': self.model,
            'ready': self.is_ready(),
            'system_prompt_length': len(self.system_prompt)
        }


class StreamingBrain(Brain):
    """Brain with streaming support (for future use)"""

    def generate_stream(self, prompt: str, **kwargs):
        """Generate text with streaming (yields chunks)"""
        # This would implement streaming for real-time generation
        # Useful for longer outputs or interactive scenarios
        full_response = self.generate(prompt, **kwargs)
        yield full_response


if __name__ == "__main__":
    # Test the brain
    logging.basicConfig(level=logging.INFO)

    test_prompt = """You are a chaotic AI agent.
    Say something absolutely unhinged about the current state of reality."""

    brain = Brain(system_prompt=test_prompt)
    print(f"Brain info: {brain.get_info()}")

    response = brain.generate("What do you think about existence?")
    print(f"\nResponse: {response}")
