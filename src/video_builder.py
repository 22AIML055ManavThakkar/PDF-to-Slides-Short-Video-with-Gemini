from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W, H = 1280, 720

def tts(text, out):
    gTTS(text=text, lang="en").save(out)

def draw_slide(title, bullets, path):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        bullet_font = ImageFont.truetype("DejaVuSans.ttf", 30)
    except:
        title_font = bullet_font = ImageFont.load_default()

    # Title
    d.text((60, 40), title, fill="black", font=title_font)

    # Bullets (wrapped)
    y = 160
    for b in bullets:
        lines = textwrap.wrap(b, 40)
        for line in lines:
            d.text((80, y), "• " + line, fill="black", font=bullet_font)
            y += 40
        y += 10

    # Visual placeholder
    d.rectangle([(820, 180), (1180, 500)], fill=(200, 200, 200))

    img.save(path)

def build_video(slides_data, out_path):
    clips = []
    temp = []

    for i, (t, b, n) in enumerate(slides_data):
        img = f"vslide_{i}.png"
        aud = f"vaudio_{i}.mp3"

        draw_slide(t, b, img)
        tts(n, aud)

        audio = AudioFileClip(aud)
        clip = ImageClip(img).set_duration(audio.duration).set_audio(audio)

        clips.append(clip)
        temp += [img, aud]

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(out_path, fps=24)

    for f in temp:
        os.remove(f)
