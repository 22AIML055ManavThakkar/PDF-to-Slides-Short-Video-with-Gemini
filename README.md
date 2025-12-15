# PDF-to-Slides-Short-Video-with-Gemini

This project converts a PDF document into:
- A PowerPoint presentation (`slides.pptx`)
- A narrated explainer video (`video.mp4`)

It is implemented as a command-line tool.

---

## Architecture (one sentence)

PDF → Text Extraction → LLM-based Sectioning & Summarization → Slide Generation → Video Rendering

---

## Requirements

- Python 3.9+
- FFmpeg (for video rendering)
- Gemini API key (free tier)

---

## Setup

Install Python dependencies:

```bash
pip install -r requirements.txt
