"""Simple LLM client for prompt-engineering sessions. Uses OpenAI API; set OPENAI_API_KEY in .env."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

from openai import OpenAI

def get_client() -> OpenAI:
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


def complete_vision(
    system: str,
    user_text: str,
    image_url: str,
    model: str = "gpt-4o-mini",
    max_tokens: int = 1024,
) -> str:
    """Vision: system + user message with image + text. image_url can be URL or data:image/...;base64,..."""
    client = get_client()
    if client is None:
        return "[Install openai and set OPENAI_API_KEY to call the API]"
    user_content: list = [
        {"type": "text", "text": user_text},
        {"type": "image_url", "image_url": {"url": image_url}},
    ]
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ],
        max_tokens=max_tokens,
    )
    return (r.choices[0].message.content or "").strip()


def transcribe_audio(file_path: str | Path, model: str = "whisper-1") -> str:
    """Transcribe audio file to text. Returns raw transcript."""
    client = get_client()
    if client is None:
        return "[Install openai and set OPENAI_API_KEY to call the API]"
    path = Path(file_path)
    if not path.exists():
        return f"[File not found: {path}]"
    with open(path, "rb") as f:
        r = client.audio.transcriptions.create(model=model, file=f)
    return (r.text or "").strip()
