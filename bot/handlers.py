"""
bot/handlers.py — Telegram update routing.

Responsibilities:
  - Parse incoming Telegram Update objects
  - Route each update type to the correct action
  - Reply "Hi" to every incoming text message (Stage 1)

This module is intentionally kept simple. As the agent is introduced in later
stages, routing logic will be extended here without restructuring the project.
"""

import logging
from bot.telegram import send_message
from agent import DataAgent
from llm.groq_provider import GroqProvider

logger = logging.getLogger(__name__)

# Initialize the global agent instance
# We pass the GroqProvider into the Agent, keeping concerns separated.
data_agent = DataAgent(provider=GroqProvider())

async def handle_update(update: dict, token: str) -> None:
    """
    Entry point for all incoming Telegram updates.
    """
    message = update.get("message")
    if not message:
        return

    chat_id: int | None = message.get("chat", {}).get("id")
    text: str | None = message.get("text")

    if chat_id is None:
        logger.warning("Received message with no chat_id: %s", update)
        return

    if text is not None:
        logger.info("Message from chat_id=%s: %s", chat_id, text)
        
        # Get AI response from the Agent (which handles memory and markdown stripping)
        ai_response = await data_agent.run(chat_id, text)
        
        # Send back to Telegram
        await send_message(token, chat_id, ai_response)
