# Chain-of-thought (CoT)

We ask the model to show its reasoning step by step before giving the final answer. "Think step by step" or "Show your work" — the model writes intermediate steps, then the answer.

- CoT improves accuracy on math, logic, and multi-step tasks because the model reasons explicitly instead of jumping to a conclusion

## Why use CoT

- **Calculations:** model shows working (e.g. discount, total) so we can check and so it makes fewer mistakes.
- **Comparisons and decisions:** step-by-step makes the logic visible and easier to correct.
- **Planning:** breaking into steps helps the model and the user follow the plan.

## How we prompt it

- **System (or user):** tell the model to solve step by step, one short line per step, and to put the final answer on the last line in a fixed form (e.g. "Answer: ...").
- The model then outputs reasoning lines followed by "Answer: ...".

## When to use

Use CoT when the task needs reasoning (math, logic, multi-step). For simple lookup or classification, plain instruction or few-shot is often enough.

## Hierarchy: CoT and structured reasoning frameworks

ReAct and Plan-and-Execute are built on Chain-of-Thought; they are structured evolutions of CoT, not separate from it.

**Flow:** Prompting → Chain-of-Thought (reason step-by-step) → Structured CoT → Plan-and-Execute → ReAct (Reason + Act with tools) → Autonomous Agents

- **Plan-and-Execute** = CoT + task decomposition + controlled execution. Phase 1: plan (break task into steps). Phase 2: execute (complete each step). Good for long tasks, system design, code generation, structured outputs.
- **ReAct** = CoT + tool use. Model alternates Thought → Action (e.g. search tool) → Observation, then next thought, until final answer. Adds iterative reasoning, feedback loop, and environment interaction.

## Comparison (reasoning frameworks)

| Technique         | Uses reasoning steps? | Uses planning? | Uses tools? |
|-------------------|------------------------|----------------|-------------|
| Basic CoT         | Yes                    | No             | No          |
| Plan-and-Execute  | Yes                    | Yes            | Optional    |
| ReAct             | Yes                    | Sometimes      | Yes         |

## Teaching line

Chain-of-thought is about reasoning. Plan-and-Execute is about structuring reasoning. ReAct is about reasoning + interacting (with tools).

---

When we ask for step-by-step reasoning, we get a clearer and often more correct final answer — and we can see how the model got there.
