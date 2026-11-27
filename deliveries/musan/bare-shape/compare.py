"""Height-normalised reference/render comparison, not a texture comparison."""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
VIEWS=('front','side','back')
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def silhouette(mask):
    mask=mask.convert('L').point(lambda p:255 if p>128 else 0)
    mask=mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    padded=ImageOps.expand(mask,border=1,fill=0)
    ImageDraw.floodfill(padded,(0,0),128)
    return Image.fromarray(np.where(np.asarray(padded)[1:-1,1:-1]==128,0,255).astype('uint8'))

def normalise(image,mask,height=650,width=580):
    bbox=mask.getbbox();x0,y0,x1,y1=bbox
    w=round((x1-x0)/(y1-y0)*height)
    result=Image.new('RGBA',(width,height+20),'white')
    crop=image.crop(bbox).convert('RGBA').resize((w,height),Image.Resampling.LANCZOS)
    result.alpha_composite(crop,((width-w)//2,10))
    small=mask.crop(bbox).resize((w,height),Image.Resampling.NEAREST)
    target=Image.new('L',result.size);target.paste(small,((width-w)//2,10))
    return result.convert('RGB'),np.asarray(target)>128,(x1-x0)/(y1-y0)

def compare(source):
    target=json.loads((ROOT/'shape-target.json').read_text())
    reference=Image.open(source).convert('RGB')
    canvas=Image.new('RGB',(1800,1590),'white');draw=ImageDraw.Draw(canvas)
    title=ImageFont.truetype(FONT,30);label=ImageFont.truetype(FONT,22)
    draw.text((30,20),'REFERENCE / supplied front, side, back',font=title,fill='#29323b')
    draw.text((30,810),'FITTED GLB / original v12 materials, neutral studio light',font=title,fill='#29323b')
    overlay=Image.new('RGB',(1800,790),'white');od=ImageDraw.Draw(overlay)
    od.text((30,20),'SILHOUETTE / green: shared, cyan: reference only, orange: GLB only',font=label,fill='#29323b')
    scores={}
    for col,view in enumerate(VIEWS):
        rm=silhouette(Image.open(WORK/(view+'-reference-mask.png')))
        ri=reference.crop(target[view]['crop'])
        r,reference_mask,rr=normalise(ri,rm)
        f=Image.open(WORK/'fitted'/(view+'.png')).convert('RGBA')
        fitted,fitted_mask,fr=normalise(f,silhouette(f.getchannel('A')))
        baseline=Image.open(WORK/'baseline'/(view+'.png')).convert('RGBA')
        _,baseline_mask,br=normalise(baseline,silhouette(baseline.getchannel('A')))
        iou=lambda m:float(np.logical_and(reference_mask,m).sum()/np.logical_or(reference_mask,m).sum())
        scores[view]={'reference_width_over_height':rr,'baseline_width_over_height':br,
                      'fitted_width_over_height':fr,'baseline_silhouette_iou':iou(baseline_mask),
                      'fitted_silhouette_iou':iou(fitted_mask)}
        x=10+col*600
        canvas.paste(r,(x,100));canvas.paste(fitted,(x,880))
        for y in (65,850):draw.text((x+240,y),view.upper(),font=label,fill='#596775')
        pixels=np.full((*reference_mask.shape,3),255,dtype=np.uint8)
        pixels[reference_mask&fitted_mask]=(110,162,127)
        pixels[reference_mask&~fitted_mask]=(24,164,189)
        pixels[fitted_mask&~reference_mask]=(224,134,66)
        overlay.paste(Image.fromarray(pixels),(x,85))
        od.text((x+140,55),view.upper()+f' / IoU {iou(fitted_mask):.3f}',font=label,fill='#596775')
    canvas.save(WORK/'reference-comparison.png');overlay.save(WORK/'silhouette-comparison.png')
    (WORK/'silhouette-measurements.json').write_text(json.dumps(scores,indent=2)+'\n')
    print(json.dumps(scores,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('reference_image',type=Path)
    compare(parser.parse_args().reference_image)
