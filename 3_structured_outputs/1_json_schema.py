"""
Session 1 (Structured Outputs): JSON mode and schema enforcement.

Two approaches:
1. Shape in prompt: response_format={"type": "json_object"}, describe keys in the prompt.
2. Pydantic + responses.parse(): define a BaseModel, get a typed object back (output_parsed).

Run from repo root:  python 3_structured_outputs/1_json_schema.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import complete_json, get_client
from pydantic import BaseModel

SYSTEM_JSON = (
    "You are a structured data assistant. "
    "Respond only with valid JSON. No markdown, no explanation. "
    "Extract any table or list-like data from the text and return it using the keys requested."
)


def table_from_paragraph(text: str) -> str:
    """
    Case 1: Structure in prompt. We ask for JSON, define exact keys, and give an example.
    """
    user = (
        "Extract table/list data from the paragraph. Return only valid JSON in this shape:\n"
        '{"data": [{"product": "<name>", "units": <int>, "price": <number>}, ...]}\n\n'
        "Paragraph:\n" + text
    )
    return complete_json(SYSTEM_JSON, user)


# Case 2: Pydantic + responses.parse() — SDK turns your model into a schema and parses the reply.
class TableRow(BaseModel):
    product: str
    units: int
    price: float


class TableData(BaseModel):
    data: list[TableRow]


def table_from_paragraph_via_pydantic(text: str) -> TableData | str:
    """
    Case 2: Pydantic + responses.parse(). Define the shape as a BaseModel;
    the SDK sends it as the schema and returns response.output_parsed as a typed object.
    """
    client = get_client()
    if client is None:
        return "[Install openai and set OPENAI_API_KEY to call the API]"
    try:
        response = client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": "Extract table or list data. Each row has product (string), units (integer), price (number).",
                },
                {"role": "user", "content": "Paragraph:\n" + text},
            ],
            text_format=TableData,
        )
        return response.output_parsed
    except Exception as e:
        return f"[Error: {e}]"


def run_demo():
    sample = (
        "Our Q1 sales were as follows. Product A sold 100 units at $5 each, "
        "Product B 200 units at $3, and Product C 150 units at $4."
    )
    print("--- Case 1: shape described in prompt (json_object) ---")
    raw1 = table_from_paragraph(sample)
    print("Raw:", raw1)
    try:
        print("Parsed:", json.dumps(json.loads(raw1), indent=2))
    except json.JSONDecodeError as e:
        print("Parse error:", e)

    print("\n--- Case 2: Pydantic + responses.parse() ---")
    result2 = table_from_paragraph_via_pydantic(sample)
    print("output_parsed:", result2)
    if result2 is not None and hasattr(result2, "model_dump"):
        print("As dict:", result2.model_dump())


if __name__ == "__main__":
    run_demo()

