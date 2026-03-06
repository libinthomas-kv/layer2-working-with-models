"""
Hands-on 3 (Structured Outputs): Parsing and validating with Pydantic.

Goal:
1. Extract restaurant reservation details from a request
2. Parse JSON output from the model
3. Validate using a Pydantic model

Run:
python 3_structured_outputs/hands_on/3_exercise_parsing.py
"""

import json
import sys
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ValidationError, field_validator

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import chat


# TODO: Students must complete the Pydantic model
# should contain restaurant_name, party_size, reservation_date
# field validators
    # restaurant_name should not be empty
    # party_size should be greater than 0
    # reservation_date should be today or in the future
class Reservation(BaseModel):
   pass # fill in the implementation here


RESPONSE_FORMAT_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "restaurant_reservation",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "restaurant_name": {"type": "string"},
                "party_size": {"type": "integer"},
                "reservation_date": {
                    "type": "string",
                    "format": "date"
                },
            },
            "required": ["restaurant_name", "party_size", "reservation_date"],
            "additionalProperties": False,
        },
    },
}

SYSTEM = """You are a restaurant reservation assistant. Extract restaurant reservation details from user requests. 
    Do not make up any information other than the information provided in the request."""

def parse_safe(raw: str):
    """Parse JSON safely."""
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None

def ask_with_validation(text: str):
    """LLM → JSON → Pydantic validation"""

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": text},
    ]

    raw = chat(messages, response_format=RESPONSE_FORMAT_SCHEMA)

    data = parse_safe(raw)

    if data is None:
        return None, raw, ["JSON parsing failed"]

    try:
        reservation = Reservation.model_validate(data)
        return reservation, raw, []

    except ValidationError as e:
        errors = []
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            errors.append(f"{loc}: {err['msg']}")
        return None, raw, errors


if __name__ == "__main__":

    request = "Reserve a table for 4 people for lunch on 2026-04-10"
    # request = "Reserve a table for 4 people for lunch on 2026-04-10 at Olive Garden"
    # request = "Reserve a table for 4 people for lunch at Olive Garden"

    result, raw, errors = ask_with_validation(request)

    if result:
        print("Reservation:", result)
    else:
        print("Invalid output")
        print("Raw:", raw)
        print("Errors:", errors)