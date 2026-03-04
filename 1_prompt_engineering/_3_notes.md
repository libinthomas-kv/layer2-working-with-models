# Zero-shot and few-shot prompting

## Zero-shot prompting

We give the model only the **instruction**: the task, the labels (or output format), and rules. No example input→output pairs. The model infers what to do from the task description.

- **Zero-shot** = no examples ("shots"), only instructions. The model relies on its pre-training to follow the task.
- Works well when the task is simple or the model already "knows" the pattern (e.g. common classifications).
- Risk: format or label choice can be less consistent than with examples.

## Few-shot prompting

We put **1–5 example input→output pairs** in the prompt. The model mimics the format and behaviour. Same idea as "show don't tell": examples make the task and output shape clear.

- **Few-shot** = a few examples in the prompt. The model copies the pattern and format from those examples.
- Use for: classification (model sees how inputs map to labels), extraction (what to pull out and in what format), consistent style.

## Why use few-shot over zero-shot

- **Classification:** model sees how similar inputs map to labels (e.g. REFUND, DELIVERY, OTHER).
- **Extraction:** examples show what to pull out and in what format.
- **Consistent style:** model copies tone and structure from the examples.
- When we need a **fixed set of labels** or a **strict output shape**, few-shot usually gives more consistent results than zero-shot.

## Structure in the code

- **Zero-shot:** system = task + labels + "Reply with only the label". User = "Classify this message. Input: ... Output:" (no examples).
- **Few-shot:** same system; user = examples (Input/Output pairs) + "Now classify: Input: ... Output:" so the model completes the pattern.

## How many examples (few-shot)

Often 1–5. More examples can help for tricky or many-class tasks; too many uses tokens and can confuse. Start small, add if needed.

## Teaching: when both outputs look the same

If zero-shot and few-shot return the same labels for easy inputs (e.g. "Refund this order" → REFUND), say this:

- **"The *mechanism* is different.** Zero-shot has no examples; few-shot has 4 example pairs in the prompt. For simple, clear messages the model often gets it right either way."
- **"Where few-shot helps:** (1) **Strict format** — zero-shot may sometimes add extra text ('The label is REFUND'); few-shot is trained by the examples to reply with only the label. (2) **Edge cases** — for ambiguous or tricky messages (e.g. 'I have a question about my order', 'My item never arrived and I want a refund'), few-shot tends to stick to the pattern and pick one label; zero-shot may explain more or vary. (3) **Custom labels** — if your labels are domain-specific or non-obvious, few-shot makes the mapping clear."
- **"So we use zero-shot when the task is simple and we want less prompt. We use few-shot when we care about consistent format, edge cases, or custom labelling."**

In the demo, zero-shot is deliberately prompted to "Give the label and optionally a very brief reason" so it often outputs extra text (e.g. "REFUND - customer requested refund"). Few-shot is kept strict ("Reply with only the label") so it outputs just "REFUND". That makes the format difference visible side by side.

---

When we add a few clear examples (few-shot), the model follows the same format and labelling logic for new inputs. Zero-shot is simpler and works when the task is clear; use few-shot when we need more consistent format or labelling.
