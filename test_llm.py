from llm.openrouter_client import call_llm


messages = [
    {
        "role": "system",
        "content": "You are a concise Linux assistant."
    },
    {
        "role": "user",
        "content": "Give one safe command to check disk usage."
    }
]

print(call_llm(messages))