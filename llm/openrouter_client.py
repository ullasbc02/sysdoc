import os
from openai import OpenAI
from dotenv import load_dotenv

from config import load_config


load_dotenv()


def get_llm_settings() -> dict:
    config = load_config().get("llm", {})

    return {
        "provider": os.getenv("LLM_PROVIDER", config.get("provider", "openrouter")).strip().lower(),
        "openrouter_model": os.getenv(
            "OPENROUTER_MODEL",
            config.get("openrouter_model", "openrouter/free"),
        ),
        "ollama_model": os.getenv(
            "OLLAMA_MODEL",
            config.get("ollama_model", "llama3.1"),
        ),
        "ollama_base_url": os.getenv(
            "OLLAMA_BASE_URL",
            config.get("ollama_base_url", "http://host.docker.internal:11434/v1"),
        ),
    }


def get_openrouter_client() -> OpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing. Add it to your .env file.")

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def get_ollama_client() -> OpenAI:
    settings = get_llm_settings()

    return OpenAI(
        base_url=settings["ollama_base_url"],
        api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
    )


def get_llm_client() -> tuple[OpenAI, str]:
    settings = get_llm_settings()

    if settings["provider"] == "openrouter":
        return get_openrouter_client(), settings["openrouter_model"]

    if settings["provider"] == "ollama":
        return get_ollama_client(), settings["ollama_model"]

    raise ValueError(
        f"Unsupported LLM_PROVIDER '{settings['provider']}'. Use 'openrouter' or 'ollama'."
    )


def call_llm(messages: list[dict], temperature: float = 0.0) -> str:
    client, model = get_llm_client()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    content = response.choices[0].message.content

    if content is None or not content.strip():
        finish_reason = getattr(response.choices[0], "finish_reason", "unknown")
        raise ValueError(
            f"LLM returned empty assistant content for model '{model}' (finish_reason={finish_reason})."
        )

    return content