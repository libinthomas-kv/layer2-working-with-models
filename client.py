"""LLM client for Structured Outputs & Function Calling session. Uses OpenAI API; set OPENAI_API_KEY in .env."""
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
    messages: list[dict],
    model: str = "gpt-4o-mini",
    max_tokens: int = 1024,
    response_format: dict | None = None,
    tools: list | None = None,
    tool_choice: str | dict | None = None,
):
    """
    Send messages to the LLM.
    If tools is None: returns assistant reply text (str).
    If tools is set: returns the raw choice object (use .message.content / .message.tool_calls).
    response_format: e.g. {"type": "json_object"} for JSON mode.
    """
    client = get_client()
    if client is None:
        return "[Install openai and set OPENAI_API_KEY to call the API]"
    kwargs = dict(model=model, messages=messages, max_tokens=max_tokens)
    if response_format is not None:
        kwargs["response_format"] = response_format
    if tools is not None:
        kwargs["tools"] = tools
        if tool_choice is not None:
            kwargs["tool_choice"] = tool_choice
    r = client.chat.completions.create(**kwargs)
    choice = r.choices[0]
    if tools is not None:
        return choice
    return (choice.message.content or "").strip()


def complete(system: str, user: str, model: str = "gpt-4o-mini") -> str:
    """One system + one user message."""
    return chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        model=model,
    )


def complete_json(system: str, user: str, model: str = "gpt-4o-mini", max_tokens: int = 1024) -> str:
    """Same as complete but request JSON output. Returns raw string (parse with json.loads)."""
    return chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        model=model,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )
