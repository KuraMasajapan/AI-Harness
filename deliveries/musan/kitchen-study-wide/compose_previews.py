"""Compose review panels from actual GLB renders; no reference-image collage."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PREVIEW = ROOT / "work/avatar-preview"


def panel(filename, views, labels, title):
    font = ImageFont.truetype("DejaVuSans.ttf",26)
    heading = ImageFont.truetype("DejaVuSans.ttf",30)
    width,height = 574,700
    image = Image.new("RGB",(width*len(views),height+125),(235,232,226))
    draw = ImageDraw.Draw(image)
    draw.text((28,19),title,font=heading,fill=(40,43,45))
    for i,(view,label) in enumerate(zip(views,labels)):
        source = Image.open(PREVIEW/view).convert("RGB")
        source = source.resize((width,height),Image.Resampling.LANCZOS)
        image.paste(source,(i*width,72))
        draw.text((i*width+24,height+84),label,font=font,fill=(40,43,45))
    image.save(PREVIEW/filename)


if __name__ == "__main__":
    panel("v13-three-views.png",["v13-front.png","v13-side.png","v13-back.png"],
          ["Front","Side / single-ear headset","Back / split coat tails"],"Musan v13 | exported GLB review")
    panel("v12-v13-comparison.png",["v12-front.png","v13-front.png"],
          ["Before | v12","Refined | v13"],"Same camera and lighting | offline renders")
