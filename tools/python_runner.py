import subprocess
import os
import uuid
from pathlib import Path

TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

def execute_python(code: str) -> str:
    script_id = str(uuid.uuid4())
    script_path = TEMP_DIR / f"script_{script_id}.py"
    
    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n[Errors/Warnings]:\n{result.stderr}"
            
        if not output.strip():
            return "Execution completed successfully, but there was no printed output."
            
        return output
        
    except subprocess.TimeoutExpired:
        return "Error: Python execution timed out after 30 seconds."
    except Exception as e:
        return f"System Error during execution: {e}"
    finally:
        if script_path.exists():
            try:
                os.remove(script_path)
            except:
                pass
