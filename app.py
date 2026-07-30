"""
app.py — FastAPI entry point for the TDS AI Data Analyst Telegram Bot.

Responsibilities:
  - Start the FastAPI application
  - Register the Telegram webhook on startup
  - Expose health-check and webhook endpoints
"""

import os
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv

from bot.telegram import set_webhook
from bot.handlers import handle_update

load_dotenv(".env.local")
load_dotenv()  # Fallback to .env if .env.local doesn't exist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
WEBHOOK_URL: str | None = os.getenv("WEBHOOK_URL")
PORT: int = int(os.getenv("PORT", "8000"))


# ---------------------------------------------------------------------------
# Lifespan: register webhook when the server starts
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    if WEBHOOK_URL:
        logger.info("Registering Telegram webhook …")
        await set_webhook(BOT_TOKEN, WEBHOOK_URL)
        logger.info("Webhook registered: %s", WEBHOOK_URL)
    else:
        logger.warning("No WEBHOOK_URL provided. Skipping webhook registration. (Normal for local dev without ngrok)")
    yield
    # Nothing to tear down at this stage


app = FastAPI(title="TDS Bot", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
async def health_check() -> dict:
    """Simple liveness probe used by Railway and external monitors."""
    return {"status": "running"}


@app.post("/webhook")
async def webhook(request: Request) -> Response:
    """
    Receive Telegram Update payloads and dispatch them to the handler.
    Always returns HTTP 200 so Telegram does not retry the request.
    """
    update = await request.json()
    await handle_update(update, BOT_TOKEN)
    return Response(status_code=200)


# ---------------------------------------------------------------------------
# Local development entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
