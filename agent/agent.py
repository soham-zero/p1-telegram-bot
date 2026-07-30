import os
import json
import logging
from typing import Optional

from llm.base import BaseLLMProvider
from agent.memory import ConversationMemory
from agent.logger import log_event
from tools import TOOLS_SCHEMA, AVAILABLE_TOOLS

logger = logging.getLogger(__name__)

class DataAgent:
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider
        self.memory = ConversationMemory()
        
        railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost")
        self.log_url = f"https://{railway_domain}/logs/run.jsonl"
        if "localhost" in self.log_url:
            self.log_url = os.environ.get("WEBHOOK_URL", "").replace("/webhook", "/logs/run.jsonl")
        
        self.system_prompt = (
            "You are a strict data analysis agent. You have access to a Python execution tool. "
            "IMPORTANT: If asked for JSON, you must reply with ONLY the raw JSON object. "
            "Do not include markdown code blocks (e.g. ```json ... ```). "
            f"Your final reply must ALWAYS be in this exact format: {{\"answer\": <your answer>, \"log_url\": \"{self.log_url}\"}} "
            "If you need to analyze data, use the execute_python tool. Keep executing code until you find the final answer."
        )

    def _strip_markdown(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            parts = text.split("\n", 1)
            if len(parts) > 1:
                text = parts[1]
            if text.endswith("```"):
                text = text[:-3]
        return text.strip()

    async def run(self, chat_id: int, message: str) -> str:
        log_event(chat_id, "user_message", {"message": message})
        self.memory.add_message(chat_id, "user", message)
        
        max_iterations = 10
        for iteration in range(max_iterations):
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.memory.get_messages(chat_id))
            
            try:
                ai_msg = await self.provider.generate(messages, tools=TOOLS_SCHEMA)
            except Exception as e:
                err = f"Error: {e}"
                log_event(chat_id, "error", {"error": err})
                return f'{{"answer": "{err}", "log_url": "{self.log_url}"}}'

            if ai_msg.tool_calls:
                self.memory.history[chat_id].append({
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": t.id,
                            "type": t.type,
                            "function": {"name": t.function.name, "arguments": t.function.arguments}
                        } for t in ai_msg.tool_calls
                    ]
                })

                for tool_call in ai_msg.tool_calls:
                    func_name = tool_call.function.name
                    args_str = tool_call.function.arguments
                    
                    log_event(chat_id, "tool_call", {"tool": func_name, "arguments": args_str})
                    
                    try:
                        args = json.loads(args_str)
                        if func_name in AVAILABLE_TOOLS:
                            # Execute the tool
                            result = AVAILABLE_TOOLS[func_name](**args)
                        else:
                            result = f"Error: Unknown tool {func_name}"
                    except Exception as e:
                        result = f"Error executing tool: {e}"
                        
                    log_event(chat_id, "tool_result", {"tool": func_name, "result": result})
                    self.memory.history[chat_id].append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
                
                continue
                
            else:
                response_text = ai_msg.content or ""
                clean_response = self._strip_markdown(response_text)
                
                log_event(chat_id, "final_answer", {"content": clean_response})
                self.memory.add_message(chat_id, "assistant", clean_response)
                return clean_response
                
        err = "Error: Agent exceeded maximum iterations."
        log_event(chat_id, "error", {"error": err})
        return f'{{"answer": "{err}", "log_url": "{self.log_url}"}}'
