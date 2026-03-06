"""
Session 3 (Structured Outputs): Parsing and validating model outputs in production.

Demo Goal:
1. First request contains all fields -> validation SUCCESS
2. Second request missing journey_date -> validation FAILURE

Run:
python 3_structured_outputs/3_parsing_validation.py
"""

import json
import sys
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ValidationError, field_validator

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import chat


class TrainBooking(BaseModel):
    from_station: str
    to_station: str
    journey_date: date

    @field_validator("from_station", "to_station")
    def non_empty_station(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be empty")
        return v

    @field_validator("journey_date")
    def not_in_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("journey_date must be today or in the future")
        return v


# JSON Schema sent to LLM
# journey_date is intentionally NOT required
RESPONSE_FORMAT_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "train_booking",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "from_station": {
                    "type": "string",
                    "description": "Departure station name."
                },
                "to_station": {
                    "type": "string",
                    "description": "Arrival station name."
                },
                "journey_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Journey date in YYYY-MM-DD format."
                },
            },
            "required": ["from_station", "to_station", "journey_date"],
            "additionalProperties": False,
        },
    },
}

SYSTEM = (
    "You are a train booking extraction assistant. "
    "Extract booking details from the user's request."
)


def parse_json_safe(raw: str):
    """Parse JSON safely."""
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


def validate_booking(data: dict):
    """Validate parsed JSON with Pydantic."""
    if not isinstance(data, dict):
        return None, ["Expected a JSON object"]

    try:
        booking = TrainBooking.model_validate(data)
        return booking, []

    except ValidationError as e:
        errors = []
        for err in e.errors():
            loc = ".".join(str(x) for x in err.get("loc", []))
            msg = err.get("msg", "Invalid value")
            errors.append(f"{loc}: {msg}")
        return None, errors


def book_train_with_validation(text: str):
    """LLM → JSON → Validation pipeline."""

    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": (
                "Extract train booking details and return structured JSON."
                f"Request:\n{text}"
            ),
        },
    ]

    raw = chat(messages=messages, response_format=RESPONSE_FORMAT_SCHEMA)

    data = parse_json_safe(raw)

    if data is None:
        return None, raw, ["JSON parsing failed"]

    booking, errors = validate_booking(data)

    if booking is None:
        return None, raw, errors

    return booking, raw, []


def run_demo():

    complete_request = "Book a train from London to Edinburgh on 2026-03-20."
    missing_date_request = "Book a train from Kochi to Kottayam"

    print(f"\n--- SUCCESS CASE --- {complete_request} ---")
    result, raw, errors = book_train_with_validation(complete_request)

    if result:
        print("Valid booking:", result)
    else:
        print("Validation failed")
        print("Raw response:", raw)
        print("Errors:", errors)

    print(f"\n--- FAILURE CASE (Missing journey_date) --- {missing_date_request} ---")
    result, raw, errors = book_train_with_validation(missing_date_request)

    if result:
        print("Valid booking:", result)
    else:
        print("Validation failed")
        print("Raw response:", raw)
        print("Errors:")
        for e in errors:
            print(" -", e)


if __name__ == "__main__":
    run_demo()