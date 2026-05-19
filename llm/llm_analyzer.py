from llm.openrouter_client import call_llm


SYSTEM_PROMPT = """
You are OpsPilot AI, a Linux operations assistant.

Your job:
Analyze Linux command outputs and explain what they mean.

Rules:
- Be concise.
- Do not invent facts.
- Only use the command outputs provided.
- If output is empty, say that.
- Give practical next steps.
- Avoid destructive recommendations.
"""


def analyze_results_with_llm(user_input: str, results: list[dict]) -> str:
    formatted_results = []

    for result in results:
        formatted_results.append(
            f"""
Command: {result["command"]}
Category: {result.get("category", "unknown")}
Success: {result["success"]}
STDOUT:
{result["stdout"]}

STDERR:
{result["stderr"]}
"""
        )

    joined_results = "\n".join(formatted_results)
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
User request:
{user_input}

Command results:
{joined_results}

Provide:
1. Diagnosis
2. Important findings
3. Recommended next steps
""",
        },
    ]

    return call_llm(messages, temperature=0.0)