from collections import defaultdict
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ConversationMemory:
    def __init__(self, max_history: int = 20):
        self.history: Dict[int, List[Dict[str, str]]] = defaultdict(list)
        self.max_history = max_history

    def get_messages(self, chat_id: int) -> List[Dict[str, str]]:
        return self.history[chat_id]

    def add_message(self, chat_id: int, role: str, content: str) -> None:
        self.history[chat_id].append({"role": role, "content": content})
        if len(self.history[chat_id]) > self.max_history:
            self.history[chat_id] = self.history[chat_id][-self.max_history:]

    def clear(self, chat_id: int) -> None:
        if chat_id in self.history:
            del self.history[chat_id]
