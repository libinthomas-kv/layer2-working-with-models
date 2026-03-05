import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import complete

PRODUCT_CONTEXT = """
Product: Wireless Mouse X1. Price: $29.99. Warranty: 2 years. Compatible: Windows, Mac. Battery: 2x AA, lasts 6 months.
"""


def exercise_1_answer_question(question: str) -> str:
    """Answer the question using only PRODUCT_CONTEXT. Else say 'Not in context'."""
    # TODO 1.1: Set the instruction
    instruction = ""

    # TODO 1.2: Build user message
    user = ""  # <-- fill in (use PRODUCT_CONTEXT and question)

    if not instruction or not user:
        raise ValueError("Complete the TODO's")
    else:
        return complete(instruction, user)


if __name__ == "__main__":
    print("What is the warranty?", exercise_1_answer_question("What is the warranty?"))
    print("Does it work on Linux?", exercise_1_answer_question("Does it work on Linux?"))
