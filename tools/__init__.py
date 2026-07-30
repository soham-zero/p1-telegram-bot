from .python_runner import execute_python

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": (
                "Write and execute a Python script to perform data analysis. "
                "You can use pandas, numpy, httpx, etc. to download and process data. "
                "Always print() your final answer so you can see it in the output."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The full, runnable Python code. Must include imports."
                    }
                },
                "required": ["code"]
            }
        }
    }
]

AVAILABLE_TOOLS = {
    "execute_python": execute_python
}
