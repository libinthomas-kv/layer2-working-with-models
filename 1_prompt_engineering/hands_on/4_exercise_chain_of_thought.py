"""
Hands-on 4 (after Session 4): Chain-of-thought.

Compare two options step by step, then end with "Recommendation: A" or "Recommendation: B".
Run from repo root:  python 1_prompt_engineering/hands_on/4_exercise_chain_of_thought.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import complete

# TODO 4.1: Write the system prompt so the model compares two options step by step:
COT_SYSTEM = ""


def exercise_4_recommend(option_a: str, option_b: str, criteria: str = "best value") -> str:
    """Return step-by-step reasoning and then Recommendation: A or B."""
    # TODO 4.2: Build user message with criteria, Option A, Option B, and a short question like "Which is better?"
    user = ""
    if not COT_SYSTEM or not user:
        raise ValueError("Complete the TODO's")
    else:
        return complete(COT_SYSTEM, user)


if __name__ == "__main__":
    print(exercise_4_recommend("$10/month, 5GB", "$15/month, 20GB"))
