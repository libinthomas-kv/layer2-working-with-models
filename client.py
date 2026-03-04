"""Simple LLM client for prompt-engineering sessions. Uses OpenAI API; set OPENAI_API_KEY in .env."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def get_client() -> "OpenAI | None":
    if OpenAI is None:
        return None
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    return OpenAI(api_key=key)


def chat(
    messages: list[dict[str, str]],
    model: str = "gpt-4o-mini",
    max_tokens: int = 1024,
) -> str:
    """Send messages to the LLM and return the assistant reply text."""
    client = get_client()
    if client is None:
        return "[Install openai and set OPENAI_API_KEY to call the API]"
    r = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )
    return (r.choices[0].message.content or "").strip()


def complete(system: str, user: str, model: str = "gpt-4o-mini") -> str:
    """One system + one user message."""
    return chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        model=model,
    )
