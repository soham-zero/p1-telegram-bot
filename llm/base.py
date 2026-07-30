from abc import ABC, abstractmethod
from typing import List, Dict

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]], tools: List[Dict] = None) -> any:
        pass
