"""
Session 1 (Multimodal): Vision — image + text inputs.

Use a vision-capable model (e.g. gpt-4o-mini) with user content = image URL + text prompt.
Same instruction/context/query pattern: role in system, image + question in user.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import complete_vision


SYSTEM_VISION = (
    "You are an image description assistant. "
    "Describe what you see clearly and concisely. "
    "If the user asks a specific question about the image, answer using only what is visible."
)


def describe_image(image_url: str, question: str = "What is in this image?") -> str:
    """Send image + text to vision model. image_url: URL or data:image/...;base64,..."""
    return complete_vision(SYSTEM_VISION, question, image_url)


def run_demo():
    # Demo requires a real image URL or base64. Without it we show the pattern.
    print("Vision: image + text input")
    print("  Use complete_vision(system, user_text, image_url)")
    print("  image_url can be: https://... or data:image/jpeg;base64,...")
    print("  Example: describe_image('https://example.com/photo.jpg', 'What is in this image?')")
    print()
    print(describe_image("https://miro.medium.com/v2/resize:fit:700/1*bPaSl_g6mNjq_-RUZkK8gg.png", "What is in this image?"))


if __name__ == "__main__":
    run_demo()
