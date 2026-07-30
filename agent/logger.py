import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

LOG_FILE = Path("logs/run.jsonl")

def log_event(chat_id: int, event_type: str, data: dict) -> None:
    LOG_FILE.parent.mkdir(exist_ok=True)
    
    log_entry = {
        "chat_id": chat_id,
        "event": event_type,
        "data": data
    }
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        logger.error("Failed to write to JSONL log: %s", e)
