# Session 1 (Multimodal): Vision — image + text inputs

- Some models can take **both an image and text** in the same request (e.g. gpt-4o, gpt-4o-mini).
- You send: one (or more) images + a text prompt. The model “sees” the image and answers the prompt.
- Same chat API you already use; the only change is the **shape of the user message** (image + text instead of text only).

- For text-only, the user message is: `{"role": "user", "content": "Your question here"}`.
- For vision, **content is a list of parts**:
  - `{"type": "text", "text": "What is in this image?"}`
  - `{"type": "image_url", "image_url": {"url": "https://..."}}`
- So the model gets both the question and the image in one user turn. Order usually doesn’t matter (e.g. text first, then image).
