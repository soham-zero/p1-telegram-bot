from abc import ABC, abstractmethod
from typing import List, Dict

class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Ensures that our Agent can swap out Gemini, Groq, or OpenAI seamlessly.
    """
    
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        Takes a list of message dictionaries (e.g., [{"role": "user", "content": "Hi"}])
        and returns the generated text string.
        """
        pass
