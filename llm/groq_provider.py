import os
import logging
from typing import List, Dict
from groq import AsyncGroq
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)

class GroqProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name
        
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY is not set. Provider will fail on generation.")
            self.client = None
        else:
            self.client = AsyncGroq(api_key=api_key)

    async def generate(self, messages: List[Dict[str, str]], tools: List[Dict] = None) -> any:
        if not self.client:
            raise RuntimeError("GROQ_API_KEY is not configured.")
            
        try:
            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 1024,
                "temperature": 0.0
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"
                
            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message
        except Exception as e:
            logger.error("Groq API error: %s", e)
            raise
