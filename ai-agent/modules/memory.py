"""
Memory Module using ChromaDB for long-term memory
Stores and retrieves agent's thoughts, actions, and experiences
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)


class Memory:
    """Long-term memory system using ChromaDB vector database"""

    def __init__(self, collection_name: str = "agent_memory"):
        """Initialize ChromaDB memory system"""
        self.collection_name = collection_name

        try:
            # Initialize ChromaDB client with persistent storage
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'chromadb')
            os.makedirs(data_dir, exist_ok=True)

            self.client = chromadb.PersistentClient(path=data_dir)

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Agent's long-term memory storage"}
            )

            logger.info(f"✅ Memory system initialized. Collection: {self.collection_name}")
            logger.info(f"📊 Current memory count: {self.collection.count()}")

        except Exception as e:
            logger.error(f"Error initializing memory system: {e}")
            raise

    def store_memory(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a memory in the vector database

        Args:
            text: The memory text to store
            metadata: Optional metadata (type, timestamp, etc.)

        Returns:
            Memory ID
        """
        try:
            # Generate unique ID
            memory_id = f"mem_{datetime.now().timestamp()}_{abs(hash(text))}"

            # Add timestamp to metadata if not present
            if metadata is None:
                metadata = {}

            if 'timestamp' not in metadata:
                metadata['timestamp'] = datetime.now().isoformat()

            # Store in ChromaDB
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[memory_id]
            )

            logger.debug(f"💾 Stored memory: {memory_id}")
            return memory_id

        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            return ""

    def get_recent_memories(
        self,
        limit: int = 10,
        memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recent memories

        Args:
            limit: Number of memories to retrieve
            memory_type: Filter by memory type (optional)

        Returns:
            List of recent memories
        """
        try:
            # Get all memories
            results = self.collection.get(
                limit=limit,
                include=["documents", "metadatas"]
            )

            memories = []
            for i, doc in enumerate(results['documents']):
                memory = {
                    'id': results['ids'][i],
                    'text': doc,
                    'metadata': results['metadatas'][i] if results['metadatas'] else {}
                }

                # Filter by type if specified
                if memory_type and memory['metadata'].get('type') != memory_type:
                    continue

                memories.append(memory)

            # Sort by timestamp (most recent first)
            memories.sort(
                key=lambda x: x['metadata'].get('timestamp', ''),
                reverse=True
            )

            return memories[:limit]

        except Exception as e:
            logger.error(f"Error getting recent memories: {e}")
            return []

    def search_memories(
        self,
        query: str,
        limit: int = 5,
        memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search memories using semantic similarity

        Args:
            query: Search query
            limit: Number of results
            memory_type: Filter by memory type (optional)

        Returns:
            List of relevant memories
        """
        try:
            # Build filter
            where = None
            if memory_type:
                where = {"type": memory_type}

            # Query ChromaDB
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where,
                include=["documents", "metadatas", "distances"]
            )

            memories = []
            if results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    memory = {
                        'id': results['ids'][0][i],
                        'text': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'similarity': 1 - results['distances'][0][i]  # Convert distance to similarity
                    }
                    memories.append(memory)

            logger.debug(f"🔍 Found {len(memories)} memories for query: {query[:50]}")
            return memories

        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            return []

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about stored memories"""
        try:
            total_count = self.collection.count()

            # Get memory types distribution
            all_memories = self.collection.get(include=["metadatas"])
            types = {}
            for metadata in all_memories['metadatas']:
                mem_type = metadata.get('type', 'unknown')
                types[mem_type] = types.get(mem_type, 0) + 1

            return {
                'total_memories': total_count,
                'types': types,
                'collection_name': self.collection_name
            }

        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {'total_memories': 0, 'types': {}}

    def clear_old_memories(self, days: int = 30) -> int:
        """
        Clear memories older than specified days

        Args:
            days: Age threshold in days

        Returns:
            Number of memories deleted
        """
        try:
            from datetime import timedelta

            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

            # Get all memories
            all_memories = self.collection.get(include=["metadatas"])

            # Find old memories
            old_ids = []
            for i, metadata in enumerate(all_memories['metadatas']):
                timestamp = metadata.get('timestamp', '')
                if timestamp and timestamp < cutoff_date:
                    old_ids.append(all_memories['ids'][i])

            # Delete old memories
            if old_ids:
                self.collection.delete(ids=old_ids)
                logger.info(f"🗑️  Deleted {len(old_ids)} memories older than {days} days")

            return len(old_ids)

        except Exception as e:
            logger.error(f"Error clearing old memories: {e}")
            return 0

    def get_context_window(
        self,
        query: str,
        recent_count: int = 3,
        relevant_count: int = 5
    ) -> str:
        """
        Get a context window combining recent and relevant memories

        Args:
            query: Query for finding relevant memories
            recent_count: Number of recent memories
            relevant_count: Number of semantically relevant memories

        Returns:
            Formatted context string
        """
        try:
            # Get recent memories
            recent = self.get_recent_memories(limit=recent_count)

            # Get relevant memories
            relevant = self.search_memories(query, limit=relevant_count)

            # Combine and format
            context = "Recent memories:\n"
            for mem in recent:
                context += f"- {mem['text'][:200]}...\n"

            context += "\nRelevant memories:\n"
            for mem in relevant:
                context += f"- {mem['text'][:200]}...\n"

            return context

        except Exception as e:
            logger.error(f"Error building context window: {e}")
            return "No memory context available"


if __name__ == "__main__":
    # Test the memory system
    logging.basicConfig(level=logging.INFO)

    memory = Memory()
    print(f"Memory stats: {memory.get_memory_stats()}")

    # Test storing
    memory.store_memory("Test thought: The simulation is glitching 🌀", {'type': 'test'})
    print(f"After test: {memory.get_memory_stats()}")
