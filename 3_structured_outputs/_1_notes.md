# Session 1: JSON mode and schema enforcement

- Many APIs support **JSON mode**: the model is constrained to output valid JSON (e.g. `response_format={"type": "json_object"}` in OpenAI).
- The model does not automatically follow a schema; you **describe the desired shape** in the system or user prompt (e.g. "Respond with JSON with keys: name, date, items list").
- Stronger enforcement: some providers support **structured outputs** with a strict JSON schema (e.g. `response_format={"type": "json_schema", "json_schema": {...}}`); the model must conform.
- Always **parse and validate** in code: `json.loads()` then check required keys and types before using in production.
