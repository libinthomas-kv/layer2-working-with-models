# Session 2: Tool/function calling

- **Function calling**: you define tools (name, description, parameters as JSON Schema). The model can respond with a **tool_calls** array instead of (or in addition to) text.
- The model **decides when** to call a tool based on the user message and tool descriptions. You execute the function and optionally send the result back for another round.
- Typical flow: user message → API call with `tools` → if `message.tool_calls` present, run each function, append `tool` role messages with results → call API again if you want the model to summarize or continue.
- Design tips: clear tool names and descriptions improve when the model chooses a tool; keep parameter schemas simple and precise.
