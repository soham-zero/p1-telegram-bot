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

    async def generate(self, messages: List[Dict[str, str]]) -> str:
        if not self.client:
            return "Error: GROQ_API_KEY is not configured."
            
        try:
            # We enforce JSON mode softly via system prompt in the Agent,
            # but Groq supports standard OpenAI chat completion formatting.
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1024,
                temperature=0.0  # Temperature 0 for deterministic data analysis/JSON
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("Groq API error: %s", e)
            return "Sorry, I encountered an error while thinking."
