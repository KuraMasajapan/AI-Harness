"""Compose actual before/after renders, using unchanged cameras and lighting."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent
PREV=ROOT.parent/'kitchen-study-wide'/'work'/'preview-materials'
NEW=ROOT/'work'/'preview-materials'
FONT=Path('/home/ubuntu/repos/AI-Harness/deliveries/musan/bare-shape/work/NotoSansJP.ttf')
if not FONT.exists():
    FONT=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

def compare():
    font=ImageFont.truetype(str(FONT),22);small=ImageFont.truetype(str(FONT),17)
    im=Image.new('RGB',(1800,1560),'#f3f0e8');d=ImageDraw.Draw(im)
    d.text((42,25),'KITCHEN / STUDY — MATERIAL & FORM REFINEMENT',fill='#292c28',font=font)
    d.text((42,72),'BEFORE',fill='#655e53',font=small);d.text((920,72),'REFINED',fill='#655e53',font=small)
    rows=[('study-detail','Bindings / paper / joinery'),('kitchen-detail','Limestone / nickel / porcelain'),('wood-detail','Wood grain / tailored furniture')]
    for row,(name,label) in enumerate(rows):
        y=110+row*470
        for col,folder in enumerate((PREV,NEW)):
            source=folder/(name+'.png')
            if row==0 and col==0:source=ROOT/'work'/'baseline'/'preview-materials'/'study-detail.png'
            image=Image.open(source).convert('RGB');image.thumbnail((840,425),Image.Resampling.LANCZOS)
            im.paste(image,(40+col*880+(840-image.width)//2,y))
        d.text((42,y+433),label,fill='#494c45',font=small)
    d.text((42,1527),'Same cameras and evening lighting. Offline GLB renders; not a Muse / iPhone runtime capture.',fill='#655e53',font=small)
    im.save(NEW/'room-refinement-comparison.jpg',quality=95)

if __name__=='__main__':compare()
