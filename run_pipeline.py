import argparse, os
from src.pdf_reader import extract_text
from src.llm_summarizer import summarize_with_gemini
from src.slide_builder import build_slides
from src.video_builder import build_video

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--outdir", required=True)
args = parser.parse_args()

os.makedirs(args.outdir, exist_ok=True)

text = extract_text(args.input)

sections = summarize_with_gemini(text)

slides_data = [
    (s["title"], s["bullets"], s["narration"])
    for s in sections
]

slides_data = slides_data[:12]  # upper bound
if len(slides_data) < 6:
    raise ValueError("Not enough content to generate required slides")

build_slides(slides_data, "assets/placeholder.png",
             os.path.join(args.outdir, "slides.pptx"))

build_video(slides_data,
            os.path.join(args.outdir, "video.mp4"))

print("DONE")
