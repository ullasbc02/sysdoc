import json
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

Allowed command families:
df, du, ps, grep, find, ls, cat, head, tail, wc, echo

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
"""


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
        parsed = json.loads(response)
    except json.JSONDecodeError:
        return [
            {
                "category": "general",
                "command": "echo 'LLM planner returned invalid JSON.'",
                "reason": "Fallback because LLM response could not be parsed.",
            }
        ]

    plans = parsed.get("plans", [])

    if not isinstance(plans, list) or not plans:
        return [
            {
                "category": "general",
                "command": "echo 'No valid plan returned by LLM.'",
                "reason": "Fallback because LLM returned no plans.",
            }
        ]

    cleaned_plans = []

    for plan in plans:
        if not isinstance(plan, dict):
            continue

        category = plan.get("category", "general")
        command = plan.get("command", "")
        reason = plan.get("reason", "No reason provided.")

        cleaned_plans.append(
            {
                "category": category,
                "command": command,
                "reason": reason,
            }
        )

    return cleaned_plans