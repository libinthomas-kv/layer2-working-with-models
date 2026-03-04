"""
Zero-shot vs few-shot prompting.

- Zero-shot: only instruction (labels + rules), no examples. Model infers from the task description.
- Few-shot: 1–5 example input→output pairs in the prompt so the model mimics format and behaviour.
Useful for: classification, extraction, structured output, consistent style.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import complete


# Zero-shot: same task, instruction only (no examples). Role + rules (Session 1–2 format).
SYSTEM_ZERO_SHOT = """You are a customer support message classifier. You classify customer messages into one label: REFUND, DELIVERY, SUPPORT, COMPLAINT, OTHER. Reply with only the label, nothing else."""

# Few-shot: same role + instruction + examples in user message
SYSTEM_FEW_SHOT = """You are a customer support message classifier. You classify customer messages into one label: REFUND, DELIVERY, SUPPORT, COMPLAINT, OTHER. Reply with only the label, nothing else."""

EXAMPLES = """
Example 1:
Input: Where is my order #8821?
Output: DELIVERY

Example 2:
Input: I want my money back for the broken item.
Output: REFUND

Example 3:
Input: The app keeps crashing on login.
Output: COMPLAINT

Example 4:
Input: Do you ship to Canada?
Output: OTHER

Example 5:
Input: I want to raise an issue regarding the delivery.
Output: SUPPORT
"""


def classify_zero_shot(message: str) -> str:
    user = f"Classify this message.\nInput: {message}\nOutput:"
    return complete(SYSTEM_ZERO_SHOT, user)


def classify_few_shot(message: str) -> str:
    user = f"{EXAMPLES}\nNow classify:\nInput: {message}\nOutput:"
    return complete(SYSTEM_FEW_SHOT, user)


def run_demo():
    sep = "=" * 60
    # Mix of clear and edge-case messages (edge cases often show zero-shot vs few-shot difference)
    test_messages = [
        "Refund this order please",
        "When will it arrive?",
        "Thanks for the discount!",
        "I have a question about my order.",           # ambiguous -> OTHER; zero-shot may add explanation
        "My item never arrived and I want to raise an issue regarding the delivery.",  # REFUND vs DELIVERY; zero-shot may be verbose
    ]
    print("\n" + sep)
    print("  Zero-shot vs few-shot — same task, same labels")
    print(sep)
    print("  Labels: REFUND | DELIVERY | COMPLAINT | OTHER")
    print()

    print("  --- Zero-shot (instruction only, no examples) ---")
    print()
    for msg in test_messages:
        label = classify_zero_shot(msg).strip()
        print(f"  Input:  {msg!r}")
        print(f"  Output: {label}")
        print()

    print("  --- Few-shot (instruction + 4 examples in the prompt) ---")
    print()
    for msg in test_messages:
        label = classify_few_shot(msg).strip()
        print(f"  Input:  {msg!r}")
        print(f"  Output: {label}")
        print()
    print(sep + "\n")


if __name__ == "__main__":
    run_demo()
