"""Compose evidence from the reimported GLB renders, never reference images."""
from PIL import Image, ImageDraw, ImageFont
from build_room import WORK


def sheet(output, tiles, width):
    font=ImageFont.truetype("DejaVuSans.ttf",22)
    tile_height=round(width*1100/1800) if len(tiles)==2 else round(width*1100/1400)
    canvas=Image.new("RGB",(width*len(tiles),tile_height+58),(32,29,25))
    draw=ImageDraw.Draw(canvas)
    for i,(path,label) in enumerate(tiles):
        frame=Image.open(path).convert("RGB").resize((width,tile_height),Image.Resampling.LANCZOS)
        canvas.paste(frame,(i*width,58))
        draw.text((i*width+20,16),label,font=font,fill=(244,234,215))
    canvas.save(output)


if __name__=="__main__":
    p=WORK/"preview-materials"
    sheet(p/"materials-comparison.png",[(WORK/"preview/interior.png","BEFORE - same camera and lighting"),
                                         (p/"interior.png","AFTER - embedded PBR materials, original v12")],1000)
    sheet(p/"materials-closeups.png",[(p/"wood-detail.png","OAK / BRASS / PAPER"),
                                       (p/"fabric-detail.png","LINEN / SOFT BEDDING"),
                                       (p/"kitchen-detail.png","STONE / STEEL / ENAMEL")],800)
