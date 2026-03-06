"""
Session 2 (Structured Outputs): Tool/function calling.

Define tools (name, description, parameters); the model may return tool_calls.
We run one round: send user message, get response; if tool_calls, run them and show result.
Country info from REST Countries (no API key). Calculator evaluates the expression locally.

Run from repo root:  python 3_structured_outputs/2_function_calling.py
"""
import json
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import get_client, chat

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_country_info",
            "description": "Get basic information about a country (capital, population, region).",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {"type": "string", "description": "Country name, e.g. India, France"},
                },
                "required": ["country"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_calculator",
            "description": "Evaluate a math expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression, e.g. 2 + 3 * 4"},
                },
                "required": ["expression"],
            },
        },
    },
]


def run_calculator_impl(expression: str) -> str:
    """Evaluate math expression: safe eval of numbers and basic ops."""
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "Error: only numbers and + - * / ( ) allowed"
        return str(eval(expression))
    except Exception as e:
        return str(e)


def get_country_info_impl(country: str) -> str:
    """Fetch country info from REST Countries API (no API key)."""
    try:
        url = f"https://restcountries.com/v3.1/name/{quote(country.strip())}?fields=name,capital,population,region,subregion"
        with urlopen(Request(url, headers={"User-Agent": "Layer2Demo/1.0"})) as r:
            data = json.loads(r.read().decode())
        if not data:
            return f"No country found for '{country}'"
        c = data[0]
        name = c.get("name", {}).get("common", country)
        capital = c.get("capital", ["N/A"])[0] if c.get("capital") else "N/A"
        pop = c.get("population", 0)
        region = c.get("region", "N/A")
        sub = c.get("subregion", "")
        sub = f", {sub}" if sub else ""
        return f"{name}: capital {capital}, population {pop:,}, region {region}{sub}"
    except Exception as e:
        return f"Country API error: {e}"


def chat_with_tools_one_round(user_message: str) -> str:
    """One round: user -> model; if tool_calls, execute and return summary. Logs whether tools were used."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools when needed."},
        {"role": "user", "content": user_message},
    ]
    choice = chat(messages, tools=TOOLS, tool_choice="auto")
    if isinstance(choice, str):
        return choice  # error message
    msg = choice.message
    if not getattr(msg, "tool_calls", None):
        content = msg.content or "(no content)"
        print("  [No tool] Assistant replied with text.")
        return content
    results = []
    print(f"  [Tool calls]: {msg.tool_calls}")
    for tc in msg.tool_calls:
        name = tc.function.name
        try:
            args = json.loads(tc.function.arguments or "{}")
        except json.JSONDecodeError:
            args = {}
        print(f"  [Tool call] {name}({args})")
        if name == "get_country_info":
            out = get_country_info_impl(args.get("country", ""))
        elif name == "run_calculator":
            out = run_calculator_impl(args.get("expression", ""))
        else:
            out = "Unknown tool"
        results.append(f"{name}({args}) -> {out}")
    return "\n".join(results)


def run_demo():
    print("Demo 1 — question that triggers calculator (tool):")
    print(chat_with_tools_one_round("What is (15 + 7) * 2?"))
    print()
    print("Demo 2 — question that triggers country info (tool):")
    print(chat_with_tools_one_round("Tell me about India."))
    print()
    print("Demo 3 — question that needs no tool (normal reply):")
    print(chat_with_tools_one_round("What color is the sky? One short sentence."))


if __name__ == "__main__":
    run_demo()
