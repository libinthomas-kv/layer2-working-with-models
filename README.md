# layer2-working-with-models

Topics and demos for working with LLMs (multimodal inputs: vision, audio, document understanding).

## Topics (Multimodal inputs)

1 — Vision (image + text)  
2 — Audio transcription (Whisper)  
3 — Document understanding (PDF, text, image)

Hands-on exercises are in `2_multimodal_inputs/hands_on/` (numbered 1–3).

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

```bash
python 2_multimodal_inputs/1_vision_image_text.py
python 2_multimodal_inputs/2_audio_transcription.py
python 2_multimodal_inputs/3_document_understanding.py
```

Exercises:

```bash
python 2_multimodal_inputs/hands_on/1_exercise_vision.py
python 2_multimodal_inputs/hands_on/2_exercise_audio.py
python 2_multimodal_inputs/hands_on/3_exercise_document.py
```
