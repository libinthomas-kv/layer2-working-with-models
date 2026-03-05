"""
Hands-on 1 (Multimodal): Vision — image + text.

Given an image URL, ask the model a specific question (e.g. "What is the main subject?" or "List the text you see.").
Run from repo root:  python 2_multimodal_inputs/hands_on/1_exercise_vision.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import complete_vision

# TODO 1.1: Write system prompt: role (e.g. image analyst) + rule (answer only from what you see).
VISION_SYSTEM = "" # <-- fill in

def exercise_1_ask_image(image_url: str, question: str) -> str:
    """Return the model's answer about the image."""

    if VISION_SYSTEM == "":
        return "You must fill in the VISION_SYSTEM variable."
    if question == "":
        return "You must fill in the question variable."
    if image_url == "":
        return "You must fill in the image_url variable."
    
    return complete_vision(VISION_SYSTEM, question, image_url)


if __name__ == "__main__":
    # Use a public image URL or a data:image/...;base64,... string
    url = "https://miro.medium.com/v2/resize:fit:720/format:webp/1*sBFL8hwkg4sewWgDBodq0Q.png"
    print(exercise_1_ask_image(url, "What is in this image in one sentence?"))
