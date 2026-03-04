"""
Sub-topic: Chain-of-thought (CoT) for reasoning tasks.

Ask the model to "think step by step" so it shows its reasoning before the final answer.
Improves accuracy on math, logic, multi-step decisions. Use for: calculations, comparisons, planning.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import complete


SYSTEM_COT = """You are a reasoning assistant. You solve problems step by step.
For each step, write one short line of reasoning,
then give the final answer on the last line in the form "Answer: ..."
"""


def reason(question: str) -> str:
    return complete(SYSTEM_COT, question)


def run_demo():
    sep = "=" * 60
    q = "A shirt costs $40. It is on 25% off. How much do I pay after discount?"
    print("\n" + sep)
    print("  Chain-of-thought — step-by-step reasoning before the answer")
    print(sep)
    print("  Question:")
    print(f"    {q}")
    print()
    print("  Response (steps + Answer: ...):")
    response = reason(q).strip()
    for line in response.split("\n"):
        print(f"    {line}")
    print(sep + "\n")


if __name__ == "__main__":
    run_demo()
