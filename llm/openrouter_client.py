import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


def get_openrouter_client() -> OpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing. Add it to your .env file.")

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def call_llm(messages: list[dict], temperature: float = 0.0) -> str:
    client = get_openrouter_client()

    model = os.getenv("OPENROUTER_MODEL", "openrouter/free")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    return response.choices[0].message.content