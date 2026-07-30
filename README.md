# TDS AI Data Analyst Telegram Bot

An incrementally developed AI Data Analysis Agent for the IITM Tools in Data Science (TDS) project.

Deployed on **Railway** · Backend: **FastAPI** · Language: **Python 3.12+**

---

## Architecture

```
Telegram User → Telegram Bot API → FastAPI (Railway)
                                        │
                                   Agent Orchestrator  ← (Stage 2+)
                                        │
                              Tools / LLM / Memory     ← (Stage 3+)
```

The system is designed to grow incrementally — every commit leaves the bot in a fully deployable state.

---

## Project Structure

```
p1-telegram-bot/
├── app.py              # FastAPI application & webhook entrypoint
├── requirements.txt
├── railway.json
├── .env.example
├── bot/
│   ├── telegram.py     # Telegram API helpers (webhook, sendMessage)
│   └── handlers.py     # Update routing logic
├── agent/              # Stage 2 — LLM agent (placeholder)
├── tools/              # Stage 3 — callable tools (placeholder)
├── logs/               # Runtime logs (git-ignored)
└── temp/               # Temporary files (git-ignored)
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

| Variable      | Description                                      |
|---------------|--------------------------------------------------|
| `BOT_TOKEN`   | Telegram Bot token from @BotFather               |
| `WEBHOOK_URL` | Public HTTPS URL for the `/webhook` endpoint     |
| `PORT`        | Server port (Railway injects this automatically) |

---

## Local Development

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and fill in BOT_TOKEN and WEBHOOK_URL

# 4. Expose local server with ngrok (for webhook testing)
ngrok http 8000
# Copy the https:// URL and set it as WEBHOOK_URL in .env

# 5. Start the server
python app.py
```

---

## API Endpoints

| Method | Path       | Description                        |
|--------|------------|------------------------------------|
| GET    | `/`        | Health check — returns `{"status": "running"}` |
| POST   | `/webhook` | Receives Telegram updates          |

---

## Deployment (Railway)

1. Push to `main` — Railway auto-deploys via the `railway.json` config.
2. Set `BOT_TOKEN` and `WEBHOOK_URL` in the Railway dashboard under **Variables**.
3. Railway injects `$PORT` automatically — no manual configuration needed.

---

## Development Stages

| Stage | Status      | Description                          |
|-------|-------------|--------------------------------------|
| 1     | ✅ Complete  | FastAPI + Telegram webhook → "Hi"    |
| 2     | 🔜 Next     | LLM agent integration (Gemini)       |
| 3     | 🔜 Planned  | Tool calling (file parser, runner)   |
| 4     | 🔜 Planned  | Memory & conversation context        |
| 5     | 🔜 Planned  | Full data analysis agent             |
