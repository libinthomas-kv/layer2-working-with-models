# System prompt (refined instruction)

Same mechanism as the instruction in Session 1 — it goes in the system message. We refine it: role, tone, constraints, output format. Not shown to the end user.

- System prompt is the advanced version of instruction: we design who the model is and how it should respond.

## Persona (who the model "is")

The identity we give the model: e.g. senior engineer, compliance officer, tutor. Persona affects style, tone, and the kinds of answers the model gives.

- Different persona + same user input = different behaviour. We choose the persona to match the task.

## Designing the system prompt

- **Role:** who the model is (e.g. "You are a senior engineer").
- **Tone:** how it speaks (professional, strict, supportive).
- **Constraints:** what it must or must not do (e.g. "Only state facts in the text", "Say Cannot confirm if unsure").
- **Output format:** how to structure the reply (e.g. "Issue: ... Suggestion: ..." or "Yes/No/Cannot confirm plus one line").

---

When we put a clear persona and rules in the system prompt, we get more precise and consistent behaviour for that task — e.g. a code reviewer vs a compliance checker.
