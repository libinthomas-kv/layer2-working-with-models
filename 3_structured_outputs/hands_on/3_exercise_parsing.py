"""
Hands-on 3 (Structured Outputs): Parsing and validating.

Same approach as the demo: define the schema once, then (1) pass it to the LLM via response_format,
(2) use it in validation. Parse with json.loads, then validate required keys and types.

Run from repo root:  python 3_structured_outputs/hands_on/3_exercise_parsing.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import chat

# Schema: single source of truth (same shape for API and validation). Confidence in [0, 1].
CONFIDENCE_MIN, CONFIDENCE_MAX = 0, 1
ANSWER_SCHEMA = {
    "answer": str,
    "confidence": (int, float),
}

# Same shape as ANSWER_SCHEMA, in the format the API expects for response_format.
RESPONSE_FORMAT_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "qa_answer",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "answer": {"type": "string"},
                "confidence": {"type": "number", "description": f"Confidence score from {CONFIDENCE_MIN} to {CONFIDENCE_MAX}"},
            },
            "required": ["answer", "confidence"],
            "additionalProperties": False,
        },
    },
}

SYSTEM = "You are a helpful QA assistant. Answer the question and give a confidence score from 0 to 1."


def parse_safe(raw: str) -> dict | None:
    """Parse JSON; return None on error."""
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


def validate_response(data: dict) -> tuple[bool, list[str]]:
    """Validate parsed data against ANSWER_SCHEMA; confidence must be in [CONFIDENCE_MIN, CONFIDENCE_MAX]."""
    errors = []
    pass # fill in the implementation here


def exercise_3_ask_with_validation(question: str) -> tuple[dict | None, str, list[str]]:
    """Ask the model (schema passed via response_format), parse, validate. Return (data, raw, errors)."""
    if not RESPONSE_FORMAT_SCHEMA:
        return None, "", ["You must fill in RESPONSE_FORMAT_SCHEMA"]
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    raw = chat(messages, response_format=RESPONSE_FORMAT_SCHEMA)
    data = parse_safe(raw)
    if data is None:
        return None, raw, ["JSON parse failed"]
    ok, errs = validate_response(data)
    if not ok:
        return None, raw, errs
    return data, raw, []


if __name__ == "__main__":
    result, raw, errors = exercise_3_ask_with_validation("What is the capital of France?")
    if result:
        print("Result:", result)
    else:
        print("Invalid or unparseable:")
        print("  Raw:", raw[:300] + ("..." if len(raw) > 300 else ""))
        print("  Errors:", errors)
