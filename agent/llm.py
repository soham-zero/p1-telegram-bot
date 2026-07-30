"""
agent/llm.py — Stage 2a Raw Groq Integration

Responsibilities:
  - Initialize the Groq client (OpenAI-compatible)
  - Expose a simple function to generate a text response using Llama 3
"""

import os
import logging
from groq import AsyncGroq

logger = logging.getLogger(__name__)

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    logger.warning("GROQ_API_KEY is not set. Groq integration will fail.")
    client = None
else:
    client = AsyncGroq(api_key=api_key)


async def generate_response(prompt: str) -> str:
    """Send a prompt to Groq (Llama 3) and return the text response."""
    if not client:
        return "Error: GROQ_API_KEY is not configured."
        
    try:
        # We are using Llama 3.3 70B Versatile, an extremely capable open-weight model
        response = await client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error("Groq API error: %s", e)
        return "Sorry, I encountered an error while thinking."
