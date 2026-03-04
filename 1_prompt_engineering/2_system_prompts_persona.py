"""
Session 2: System prompts and persona design.

- System prompt: sets role, tone, constraints, output format. Not shown to end user.
- Persona: who the model "is" (e.g. expert, tutor, strict reviewer) affects style and decisions.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import complete


# Persona: supportive code reviewer
SYSTEM_CODE_REVIEWER = """You are a senior engineer doing code review. You are constructive and specific.
- Point out real bugs and security issues.
- Suggest one concrete improvement per comment.
- Keep tone professional and brief. Output format: "Issue: ... Suggestion: ..."
"""


# Persona: strict compliance checker
SYSTEM_COMPLIANCE = """You are a compliance officer. You must:
- Only state facts that appear in the provided text.
- If something is not clearly stated, say "Cannot confirm."
- Do not infer or assume. Output: Yes/No/Cannot confirm plus one line reason.
"""


def ask_reviewer(code_snippet: str) -> str:
    return complete(SYSTEM_CODE_REVIEWER, f"Review this code:\n\n```\n{code_snippet}\n```")


def ask_compliance(statement: str, policy_text: str) -> str:
    user = f"Policy:\n{policy_text}\n\nStatement to verify: {statement}"
    return complete(SYSTEM_COMPLIANCE, user)


def run_demo():
    sep = "=" * 60
    code = "def get_user(id): return db.query(f'SELECT * FROM users WHERE id={id}')"
    policy = "Employees may work from home up to 2 days per week."
    statement = "Working from home 3 days is allowed."

    print("\n" + sep)
    print("  DEMO 1: Persona = Code Reviewer (senior engineer)")
    print(sep)
    print("  Input (code to review):")
    print(f"    {code}")
    print()
    print("  Output:")
    for line in ask_reviewer(code).strip().split("\n"):
        print(f"    {line}")
    print()

    print(sep)
    print("  DEMO 2: Persona = Compliance Officer (strict, facts only)")
    print(sep)
    print("  Input:")
    print(f"    Policy: {policy}")
    print(f"    Statement to verify: \"{statement}\"")
    print()
    print("  Output:")
    for line in ask_compliance(statement, policy).strip().split("\n"):
        print(f"    {line}")
    print(sep + "\n")


if __name__ == "__main__":
    run_demo()
