import json
import re
from llm.openrouter_client import call_llm


SYSTEM_PROMPT = """
You are OpsPilot AI, a Linux troubleshooting planner.

Your job:
Convert a user's troubleshooting request into a safe JSON command plan.

Rules:
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanations outside JSON.
- Only use safe read-only diagnostic commands.
- Do not use destructive commands.
- Do not use sudo.
- Do not use shell operators like &&, ||, ;, >, >>, <, `, or $().
- Prefer simple Linux commands.
- Prefer commands that work inside Ubuntu Docker containers.
- Each command should answer one investigation question.

Allowed command families:
df, du, ps, grep, find, ls, cat, head, tail, wc, echo

Good command examples:
- df -h
- du -sh *
- ps aux
- ps aux --sort=-%cpu
- ps aux --sort=-%mem
- grep -i ERROR sample_logs/app.log
- tail -n 50 sample_logs/app.log
- find . -type f -size +100M
- ls -lah
- wc -l sample_logs/app.log

Category meanings:
- disk: filesystem space and directory size investigation
- process: CPU, memory, running processes
- logs: log inspection and error analysis
- files: file discovery and file size checks
- general: safe fallback or general diagnostics

JSON format:
{
  "plans": [
    {
      "category": "disk | process | logs | files | general",
      "command": "linux command here",
      "reason": "why this command is useful"
    }
  ]
}

For unclear requests, return one safe exploratory command.
"""


def extract_json(text: str) -> dict:
    text = text.strip()

    # Remove markdown fences if present
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: extract first JSON object from response
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in LLM response.")

    return json.loads(match.group(0))


def fallback_plan(reason: str) -> list[dict]:
    return [
        {
            "category": "general",
            "command": f"echo '{reason}'",
            "reason": reason,
        }
    ]


def plan_commands_with_llm(user_input: str) -> list[dict]:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    response = call_llm(messages, temperature=0.0)

    try:
        parsed = extract_json(response)
    except Exception:
        return fallback_plan("LLM planner returned invalid JSON.")

    plans = parsed.get("plans", [])

    if not isinstance(plans, list) or not plans:
        return fallback_plan("No valid plan returned by LLM.")

    cleaned_plans = []

    for plan in plans:
        if not isinstance(plan, dict):
            continue

        cleaned_plans.append(
            {
                "category": plan.get("category", "general"),
                "command": plan.get("command", ""),
                "reason": plan.get("reason", "No reason provided."),
            }
        )

    if not cleaned_plans:
        return fallback_plan("No usable commands returned by LLM.")

    return cleaned_plans