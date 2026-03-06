"""
Session 3 (Structured Outputs): Parsing and validating model outputs in production.

1. Schema: we pass the response schema to the LLM via response_format (so the model must conform).
2. Parse: API returns a string; parse with json.loads (parse_json_safe).
3. Validate: still validate in code (required keys, types) for robustness and fallbacks.

Run from repo root:  python 3_structured_outputs/3_parsing_validation.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import chat

SCORE_MIN, SCORE_MAX = 0, 100

# Schema we pass to the LLM (response_format). Model output must match this.
RESPONSE_FORMAT_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "extraction",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "entities": {"type": "array", "items": {"type": "string"}},
                "score": {"type": "number", "description": f"Relevance score from {SCORE_MIN} to {SCORE_MAX}"},
            },
            "required": ["summary", "entities", "score"],
            "additionalProperties": False,
        },
    },
}

# Same shape for validation in code (we check types and score range).
EXTRACTION_SCHEMA = {
    "summary": str,
    "entities": list,
    "score": (int, float),
}

SYSTEM = (
    "You are a structured data assistant. "
    f"Summarize in one sentence, list main entities (names/orgs), and give a relevance score from {SCORE_MIN} to {SCORE_MAX}."
)


def parse_json_safe(raw: str) -> dict | None:
    """Parse JSON; return None on failure."""
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


def validate_extraction(data: dict) -> tuple[bool, list[str]]:
    """Validate parsed JSON against EXTRACTION_SCHEMA. Return (ok, list of errors)."""
    errors = []
    if not isinstance(data, dict):
        return False, ["Expected a JSON object"]
    if "summary" not in data or not isinstance(data.get("summary"), EXTRACTION_SCHEMA["summary"]):
        errors.append("Missing or invalid 'summary' (string)")
    if "entities" not in data or not isinstance(data.get("entities"), EXTRACTION_SCHEMA["entities"]):
        errors.append("Missing or invalid 'entities' (list)")
    if "score" not in data:
        errors.append("Missing 'score'")
    else:
        s = data["score"]
        if not isinstance(s, EXTRACTION_SCHEMA["score"]) or not (SCORE_MIN <= s <= SCORE_MAX):
            errors.append(f"'score' must be a number between {SCORE_MIN} and {SCORE_MAX}")
    return len(errors) == 0, errors


def extract_with_validation(text: str, max_tokens: int | None = None) -> tuple[dict | None, str, list[str]]:
    """
    Get JSON from model (schema always passed), parse, validate.
    Optional max_tokens: if set very low, response can be truncated → invalid JSON (for demo failure case).
    Returns (data, raw_response, validation_errors).
    """
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Summarize in one sentence, list main entities (names/orgs), and give a relevance score 0-100.\n\nText:\n{text}"},
    ]
    kwargs = dict(messages=messages, response_format=RESPONSE_FORMAT_SCHEMA)
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    raw = chat(**kwargs)
    data = parse_json_safe(raw)
    if data is None:
        return None, raw, ["JSON parse failed"]
    ok, errs = validate_extraction(data)
    if not ok:
        return None, raw, errs
    return data, raw, []


def run_demo():
    sample = "Apple Inc. and Microsoft Corp announced a partnership on AI in 2024."

    print("--- Success case (schema passed to LLM, enough tokens) ---")
    result, raw, errors = extract_with_validation(sample)
    if result:
        print("Valid result:", result)
    else:
        print("Invalid or unparseable result:")
        print("  Raw response:", raw[:500] + ("..." if len(raw) > 500 else ""))
        print("  Errors:", errors)

    print("\n--- Failure case (schema still passed, but max_tokens very low → response truncated → invalid JSON) ---")
    result, raw, errors = extract_with_validation(sample, max_tokens=25)
    if result:
        print("Valid result:", result)
    else:
        print("Invalid or unparseable result:")
        print("  Raw response:", raw[:500] + ("..." if len(raw) > 500 else ""))
        print("  Errors:", errors)


if __name__ == "__main__":
    run_demo()
