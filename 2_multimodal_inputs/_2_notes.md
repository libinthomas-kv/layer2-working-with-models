# Session 2: Audio transcription — Whisper and equivalents

- Pipeline: **audio file → transcribe → text**. OpenAI Whisper (`audio.transcriptions.create`) is the reference.
- Output: raw transcript. Optional next step: send transcript to an LLM for summarization, action items, or extraction.
- Role + rules still apply when you pass transcript to the LLM (e.g. "You are a meeting notes assistant. Summarize in bullet points.").
- Alternatives: local Whisper, other cloud APIs; same pattern (transcribe → text → optional LLM).
