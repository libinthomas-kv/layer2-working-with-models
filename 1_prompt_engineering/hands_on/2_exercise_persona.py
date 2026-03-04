"""
Hands-on 2 (after Session 2): Persona / System prompt.

Act as a strict grammar checker: output only the corrected sentence(s), no explanations, one per line.
Run from repo root:  python 1_prompt_engineering/hands_on/exercise_2_persona.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import complete

# TODO 2.1: Write the system prompt so the model is a "strict grammar checker":
STRICT_GRAMMAR_SYSTEM = ""


def exercise_2_grammar_check(text: str) -> str:
    """Return grammar-corrected text only (persona: strict grammar checker)."""
    if not STRICT_GRAMMAR_SYSTEM or not text:
        raise ValueError("Complete the TODO's")
    else:
        return complete(STRICT_GRAMMAR_SYSTEM, text)


if __name__ == "__main__":
    print(exercise_2_grammar_check("Me and him went to the store."))
