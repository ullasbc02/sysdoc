from datetime import datetime
from pathlib import Path

from src.config import load_config
from llm.openrouter_client import call_llm


def get_scripts_dir() -> Path:
    config = load_config()
    return Path(config["paths"]["scripts_dir"])


SYSTEM_PROMPT = """
You are OpsPilot AI, a safe Bash automation assistant.

Your job:
Generate safe Bash scripts for Linux automation.

Rules:
- Return ONLY the Bash script.
- Do not include markdown fences.
- Do not include explanations outside the script.
- The script must include comments.
- Prefer dry-run behavior when deletion or modification is involved.
- Do not use sudo.
- Do not use rm -rf.
- Do not use destructive commands without clear dry-run mode.
- Include set -euo pipefail.
- Assume Ubuntu Linux.
"""


def generate_bash_script(user_request: str) -> str:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_request,
        },
    ]

    return call_llm(messages, temperature=0.0).strip()


def explain_bash_script(script: str) -> str:
    messages = [
        {
            "role": "system",
            "content": """
You are OpsPilot AI, a Bash script reviewer.

Explain what a Bash script does in clear, concise language.

Rules:
- Be practical.
- Mention safety concerns if any.
- Do not rewrite the script.
- Do not invent behavior not present in the script.
""",
        },
        {
            "role": "user",
            "content": f"""
Explain this Bash script:

{script}
""",
        },
    ]

    return call_llm(messages, temperature=0.0).strip()


def save_script(script: str) -> str:
    scripts_dir = get_scripts_dir()
    scripts_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = scripts_dir / f"script_{timestamp}.sh"

    path.write_text(script, encoding="utf-8")

    return str(path)
