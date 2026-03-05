"""
Session 2 (Multimodal): Audio transcription — Whisper and equivalents.

Pipeline: audio file -> transcribe -> text. Optional: pass transcript to LLM for summarization or extraction.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import transcribe_audio, complete


def transcribe(path: str | Path) -> str:
    """Transcribe audio file to text (Whisper)."""
    return transcribe_audio(path)


def summarize_transcript(transcript: str) -> str:
    """Use LLM to summarize transcript. Role + rule in system."""
    system = (
        "You are a meeting notes assistant. "
        "Summarize the transcript in 3–5 bullet points. Keep it concise."
    )
    return complete(system, transcript)


def run_demo():
    print("Audio: transcribe then optional LLM step")
    print("  transcribe(audio_path) -> raw text")
    print("  summarize_transcript(transcript) -> bullet summary")
    # Path relative to this script so it works from any cwd
    audio_path = Path(__file__).resolve().parent / "story.mp3"
    if not audio_path.exists():
        print("  Provide an audio file (e.g. .mp3, .wav) in 2_multimodal_inputs/ to try transcribe().")
        return
    transcript = transcribe(audio_path)
    print("Transcript:")
    print(transcript)
    print()
    print("Summary:", summarize_transcript(transcript))


if __name__ == "__main__":
    run_demo()
