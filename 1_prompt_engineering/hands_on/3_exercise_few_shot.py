"""
Hands-on 3 (after Session 3): Few-shot.

Classify support tickets into: BUG, FEATURE_REQUEST, QUESTION. Put 2-3 examples in the prompt.
Run from repo root:  python 1_prompt_engineering/hands_on/3_exercise_few_shot.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import complete

# TODO 3.1: Write the system prompt
SYSTEM_PROMPT = ""

# TODO 3.2: Write 2–3 few-shot examples. Each example: "Ticket: ..." then "Output: ..."
FEW_SHOT_EXAMPLES = ""


def exercise_3_classify_ticket(ticket_text: str) -> str:
    """Classify ticket as BUG, FEATURE_REQUEST, or QUESTION (few-shot)."""
    if not SYSTEM_PROMPT or not FEW_SHOT_EXAMPLES:
        raise ValueError("Complete the TODO's")
    else:
        user = f"{FEW_SHOT_EXAMPLES.strip()}\n\nTicket: {ticket_text}\nOutput:"
        return complete(SYSTEM_PROMPT, user)


if __name__ == "__main__":
    print(exercise_3_classify_ticket("Export to PDF is broken in Safari."))
    print(exercise_3_classify_ticket("How do I change my password?"))
