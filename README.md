# layer2-working-with-models

Topics and demos for working with LLMs (prompt engineering, failure modes, etc.).

## Topics (Session 1: Prompt engineering)

- **1** — Instruction, context, query (structuring prompts)
- **2** — System prompts and persona
- **3** — Few-shot examples
- **4** — Chain of thought
- **5** — Failure modes (hallucination, prompt injection, ambiguity)

Hands-on exercises are in `1_prompt_engineering/hands_on/` (numbered 1–5).

## Setup

```bash
git clone https://github.com/libinthomas-kv/layer2-working-with-models
cd layer2-working-with-models
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` in the repo root with your OpenAI key:

```
OPENAI_API_KEY=sk-...
```

## Run

From the repo root (so `client.py` is on the path):

```bash
python 1_prompt_engineering/1_instruction_context_query.py
python 1_prompt_engineering/2_system_prompts_persona.py
python 1_prompt_engineering/3_few_shot.py
python 1_prompt_engineering/4_chain_of_thought.py
python 1_prompt_engineering/5_failure_modes.py
```

Exercises:

```bash
python 1_prompt_engineering/hands_on/1_exercise_instruction_context_query.py
# ... same pattern for 2–5
```
