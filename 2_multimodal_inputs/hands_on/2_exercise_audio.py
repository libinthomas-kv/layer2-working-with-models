"""
Hands-on 2 (Multimodal): Audio transcription.

Transcribe an audio file, then (optional) summarize it in 2–3 sentences using the LLM.
Run from repo root:  python 2_multimodal_inputs/hands_on/2_exercise_audio.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import transcribe_audio, complete

def exercise_2_transcribe(audio_path: str | Path) -> str:
    """Return raw transcript."""
    return transcribe_audio(audio_path)

# TODO 2.1: Summarize transcript in 2–3 sentences. System: role + "Summarize in 2–3 sentences."
def exercise_2_summarize(transcript: str) -> str:
    """Return short summary."""
    system = ""  # <-- fill in
    if system == "":
        return "You must fill in the system variable."

    return complete(system, transcript)


if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "neural_networks.mp3"
    t = exercise_2_transcribe(path)
    print("Transcript:", t)
    print("Summary:", exercise_2_summarize(t))
