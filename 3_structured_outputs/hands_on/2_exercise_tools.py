"""
Hands-on 2 (Structured Outputs): Function calling.

Same approach as the demo: define the tool schema (TOOLS) once, then pass it to the LLM (chat(..., tools=TOOLS))
and use the same tool name in the execution loop. Implement the tool by calling a public API.

Free Dictionary API (no key). Example curl:
  curl -s "https://api.dictionaryapi.dev/api/v2/entries/en/machine%20learning"

Run from repo root:  python 3_structured_outputs/hands_on/2_exercise_tools.py
"""
import json
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import chat

# Schema: define tools once; we pass TOOLS to the LLM and dispatch by name in the loop.
# TODO 2.1: Fill in one tool: "lookup_term" with parameter "term" (string), description for the model.
TOOLS = []  # <-- fill in: list of one dict with type "function", "function": { "name", "description", "parameters" }


def lookup_term_impl(term: str) -> str:
    """Look up a term using Free Dictionary API (no API key). Returns first definition or an error string."""
    pass # fill in the implementation here


def exercise_2_one_round(user_message: str) -> str:
    """Send user message with tools; if model returns tool_calls, run and return tool result summary."""
    if not TOOLS:
        return "You must fill in TOOLS."
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the lookup tool when the user asks for a definition."},
        {"role": "user", "content": user_message},
    ]
    choice = chat(messages, tools=TOOLS, tool_choice="auto")
    if isinstance(choice, str):
        return choice
    msg = choice.message
    if not getattr(msg, "tool_calls", None):
        return msg.content or "(no content)"
    results = []
    for tc in msg.tool_calls:
        name = tc.function.name
        try:
            args = json.loads(tc.function.arguments or "{}")
        except json.JSONDecodeError:
            args = {}
        if name == "lookup_term":
            out = lookup_term_impl(args.get("term", ""))
        else:
            out = "Unknown tool"
        results.append(out)
    return "\n".join(results)


if __name__ == "__main__":
    print(exercise_2_one_round("What is machine learning?"))
