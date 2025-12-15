from google import genai
import os
import json
import re

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

PROMPT = f"""
You are given text extracted from a PDF.

Task:
- Split the text into logical sections.
- Each section must have:
  - title
  - bullets (2 concise bullet points)
  - narration (1 short sentence)

Rules:
- Works for resumes, chapters, notes, articles
- No markdown
- No explanations
- Return ONLY a valid JSON array

Example format:
[
  {{
    "title": "Summary",
    "bullets": ["Point 1", "Point 2"],
    "narration": "One sentence narration."
  }}
]

Text:
{{content}}
"""

def extract_json(text):
    """Extract JSON array from model output safely"""
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in Gemini response")
    return json.loads(match.group())

def summarize_with_gemini(text):
    prompt = PROMPT.replace("{content}", text)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()
    if not raw:
        raise ValueError("Gemini returned empty response")

    return extract_json(raw)

