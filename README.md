# layer2-working-with-models

Topics and demos for working with LLMs: structured outputs, function calling.

## Topics

**Structured outputs & function calling** (`3_structured_outputs/`)  
1. JSON mode and schema enforcement  
2. Tool/function calling  
3. Parsing and validating model outputs  

Demos: `3_structured_outputs/1_json_schema.py`, `2_function_calling.py`, `3_parsing_validation.py`  
Hands-on: `3_structured_outputs/hands_on/` (1_exercise_json.py, 2_exercise_tools.py, 3_exercise_parsing.py)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in repo root with `OPENAI_API_KEY=sk-...`

## Run (Structured outputs)

```bash
python 3_structured_outputs/1_json_schema.py
python 3_structured_outputs/2_function_calling.py
python 3_structured_outputs/3_parsing_validation.py
```

Exercises:

```bash
python 3_structured_outputs/hands_on/1_exercise_json.py
python 3_structured_outputs/hands_on/2_exercise_tools.py
python 3_structured_outputs/hands_on/3_exercise_parsing.py
```
