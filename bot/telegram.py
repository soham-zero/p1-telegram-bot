"""
bot/telegram.py — Low-level Telegram Bot API helpers.

Responsibilities:
  - Register the webhook URL with Telegram
  - Send messages back to users
"""

import logging
import httpx

logger = logging.getLogger(__name__)

TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}/{method}"


def _api_url(token: str, method: str) -> str:
    return TELEGRAM_API_BASE.format(token=token, method=method)


async def set_webhook(token: str, webhook_url: str) -> None:
    """Register the webhook endpoint with the Telegram Bot API."""
    url = _api_url(token, "setWebhook")
    payload = {"url": webhook_url}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=10)
        data = response.json()

    if not data.get("ok"):
        raise RuntimeError(f"Failed to set webhook: {data}")

    logger.info("setWebhook response: %s", data)


async def send_message(token: str, chat_id: int, text: str) -> None:
    """Send a plain-text message to a Telegram chat."""
    url = _api_url(token, "sendMessage")
    payload = {"chat_id": chat_id, "text": text}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=10)
        data = response.json()

    if not data.get("ok"):
        logger.error("sendMessage failed: %s", data)
