"""
Hands-on 1 (Structured Outputs): Pydantic + responses.parse().

Same approach as the demo: define the response schema once (Pydantic models), then pass it to the LLM
via text_format=YourModel so the API enforces that shape. We give a paragraph with different data (events).

Run from repo root:  python 3_structured_outputs/hands_on/1_exercise_json.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import get_client
from pydantic import BaseModel

# Paragraph with different data from the demo (events, not product/units/price).
SAMPLE_PARAGRAPH = (
    "This week we had three meetings. Standup on Monday at 9am with 5 attendees. "
    "Planning on Wednesday at 2pm with 8 attendees. Retro on Friday at 4pm with 6 attendees."
)

# TODO 1.1: Create a Pydantic model (or models) for the data in SAMPLE_PARAGRAPH.
# Paragraph describes events: each has name, day, time, attendees (int). Define Event and a wrapper (e.g. EventList with events: list[Event]).
class Event(BaseModel):
    pass

class EventList(BaseModel):
    pass


def exercise_1_parse_events(text: str):
    """
    Call OpenAI with responses.parse(), using your Pydantic model as text_format.
    Return response.output_parsed (typed object). See demo: table_from_paragraph_via_pydantic.
    """
    # TODO 1.2: get client, then client.responses.parse(model=..., input=[system, user], text_format=EventList)
    # System: brief instruction to extract the event/list data. User: "Paragraph:\n" + text
    # Return the parsed object (or an error string if you prefer).
    client = get_client()
    if client is None:
        return "[Install openai and set OPENAI_API_KEY to call the API]"
    # <-- fill in: response = client.responses.parse(...); return response.output_parsed
    return None


if __name__ == "__main__":
    result = exercise_1_parse_events(SAMPLE_PARAGRAPH)
    print("Result:", result)
    if result is not None and hasattr(result, "model_dump"):
        print("As dict:", result.model_dump())
