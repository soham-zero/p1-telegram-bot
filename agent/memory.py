from collections import defaultdict
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ConversationMemory:
    """
    Lightweight in-memory storage for conversation histories, keyed by chat_id.
    Keeps the last N messages to prevent context windows from overflowing
    and to save on tokens during multi-turn exchanges.
    """
    def __init__(self, max_history: int = 20):
        # Maps chat_id -> List of message dicts ({"role": "user/assistant", "content": "..."})
        self.history: Dict[int, List[Dict[str, str]]] = defaultdict(list)
        self.max_history = max_history

    def get_messages(self, chat_id: int) -> List[Dict[str, str]]:
        """Retrieve the current conversation history for a chat."""
        return self.history[chat_id]

    def add_message(self, chat_id: int, role: str, content: str) -> None:
        """Append a new message and prune if history exceeds max_history."""
        self.history[chat_id].append({"role": role, "content": content})
        
        if len(self.history[chat_id]) > self.max_history:
            # Keep the system prompt (if it's the first message) and the recent history
            # But for now, we just keep the last N messages simply.
            self.history[chat_id] = self.history[chat_id][-self.max_history:]

    def clear(self, chat_id: int) -> None:
        """Clear memory for a specific chat."""
        if chat_id in self.history:
            del self.history[chat_id]
