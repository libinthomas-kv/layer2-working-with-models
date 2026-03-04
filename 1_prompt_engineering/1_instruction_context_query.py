"""
Session 1: Instruction → Context → Query structure.

Structure prompts as:
- Instruction: what the model should do (role, format, rules).
- Context: facts, documents, or data the model should use.
- Query: the actual user question or task.

Keep instruction and context separate so the model knows what is "rules" vs "data".
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import complete


# --- Bad: everything in one blob ---
def prompt_bad(user_question: str, doc: str) -> str:
    return complete(
        "",
        f"Answer the question. Doc: {doc}. Question: {user_question}. Be concise.",
    )


# --- Good: instruction, context, query ---
SYSTEM_INSTRUCTION = (
    "You are a precise assistant. Use only the provided context to answer. "
    "If the context does not contain the answer, say 'Not in context.' "
    "Reply in 1-3 sentences."
)


def prompt_good(user_question: str, context: str) -> str:
    system = SYSTEM_INSTRUCTION
    user = f"## Context\n{context}\n\n## Query\n{user_question}"
    return complete(system, user)


def run_demo():
    context = "Our refund policy: full refund within 30 days. No refunds after 30 days."
    query = "Can I get a refund after 25 days?"
    print("Context:", context)
    print("Query:", query)
    print()
    print("--- Bad prompt (instruction + context + query in one blob) ---")
    print(prompt_bad(query, context))
    print()
    print("--- Good prompt (instruction in system, context + query clearly separated) ---")
    print(prompt_good(query, context))


if __name__ == "__main__":
    run_demo()
