# Session 3: Parsing and validating model outputs in production

- Even with JSON mode, output can be malformed (truncation, extra text). **Always parse defensively**: `try/except` around `json.loads()`, handle `None` or invalid structure.
- **Validation**: after parsing, check required keys, value types (string, list, number), and ranges. Return a clear error or fallback instead of assuming shape.
- In production: consider retries with a simpler prompt, or a fallback (e.g. return raw text or a default structure) when validation fails.
- For strict contracts, prefer provider-supported structured output (JSON schema) when available; then validation is mostly redundant but still recommended.
