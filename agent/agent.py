import logging
from typing import Optional

from llm.base import BaseLLMProvider
from agent.memory import ConversationMemory

logger = logging.getLogger(__name__)

class DataAgent:
    """
    The orchestrator that handles memory, constructs prompts, calls the LLM, 
    and enforces JSON formatting for the evaluator.
    """
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider
        self.memory = ConversationMemory()
        
        # System prompt injected before every generation to enforce behavior
        self.system_prompt = (
            "You are a strict data analysis agent. "
            "IMPORTANT: If asked for JSON, you must reply with ONLY the raw JSON object. "
            "Do not include markdown code blocks (e.g. ```json ... ```). "
            "Do not include prose before or after. "
            "Output valid, parsable JSON."
        )

    def _strip_markdown(self, text: str) -> str:
        """
        The grading script literally parses our output with json.loads(reply).
        LLMs love to wrap JSON in markdown blocks. This safely strips them.
        """
        text = text.strip()
        if text.startswith("```"):
            parts = text.split("\n", 1)
            if len(parts) > 1:
                text = parts[1]
            if text.endswith("```"):
                text = text[:-3]
        return text.strip()

    async def run(self, chat_id: int, message: str) -> str:
        # Add user's new message to memory
        self.memory.add_message(chat_id, "user", message)
        
        # Construct the payload (System Prompt + History)
        # Note: Some models expect a 'system' role. Groq/Llama 3 supports 'system'.
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory.get_messages(chat_id))
        
        # Ask the LLM Provider
        response_text = await self.provider.generate(messages)
        
        # Strip markdown to protect against format_errors in the grader
        clean_response = self._strip_markdown(response_text)
        
        # Save our own cleaned response to memory so we remember what we actually said
        self.memory.add_message(chat_id, "assistant", clean_response)
        
        return clean_response
