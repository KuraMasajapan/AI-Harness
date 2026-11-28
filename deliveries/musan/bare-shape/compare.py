"""Height-normalised shape and sampled rendered-colour comparison."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
VIEWS=('front','side','back')
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
# Fixed interior fur patches on the height-normalised (580 x 670) panels.
# Avoid the face, silhouette edges, hands and contact shadows.
COLOR_PATCHES={'crown':(245,30,335,70),'torso':(240,300,340,470)}
FACE_PATCHES={'forehead':(260,95,320,135),'lower_face':(275,220,305,230),
              'cheek_L':(205,175,235,195),'cheek_R':(345,175,375,195)}

def lab(rgb):
    """sRGB to CIE Lab, D65; used only for rendered-image comparisons."""
    s=np.asarray(rgb,dtype=float)/255
    linear=np.where(s<=.04045,s/12.92,((s+.055)/1.055)**2.4)
    xyz=np.array([[.4124564,.3575761,.1804375],
                  [.2126729,.7151522,.0721750],
                  [.0193339,.1191920,.9503041]])@linear
    t=xyz/np.array([.95047,1,1.08883]);d=6/29
    f=np.where(t>d**3,np.cbrt(t),t/(3*d*d)+4/29)
    return np.array([116*f[1]-16,500*(f[0]-f[1]),200*(f[1]-f[2])])

def colour_samples(reference,fitted,patches=COLOR_PATCHES):
    result={}
    for name,box in patches.items():
        a,b=[np.median(np.asarray(img.crop(box)).reshape(-1,3),axis=0)
             for img in (reference,fitted)]
        delta=lab(b)-lab(a)
        result[name]={'box_xyxy':box,'reference_srgb':a.tolist(),'render_srgb':b.tolist(),
                      'delta_L':float(delta[0]),'delta_b':float(delta[2]),
                      'delta_E76':float(np.linalg.norm(delta))}
    return result

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
    draw.text((30,810),'FITTED GLB / lighter cream beige, unchanged lighting and surface',font=title,fill='#29323b')
    overlay=Image.new('RGB',(1800,790),'white');od=ImageDraw.Draw(overlay)
    od.text((30,20),'SILHOUETTE / green: shared, cyan: reference only, orange: GLB only',font=label,fill='#29323b')
    scores={};colours={};face={}
    for col,view in enumerate(VIEWS):
        rm=silhouette(Image.open(WORK/(view+'-reference-mask.png')))
        ri=reference.crop(target[view]['crop'])
        r,reference_mask,rr=normalise(ri,rm)
        f=Image.open(WORK/'fitted'/(view+'.png')).convert('RGBA')
        fitted,fitted_mask,fr=normalise(f,silhouette(f.getchannel('A')))
        colours[view]=colour_samples(r,fitted)
        if view=='front':face=colour_samples(r,fitted,FACE_PATCHES)
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
    errors=[p['delta_E76'] for v in colours.values() for p in v.values()]
    report={'reference_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),
            'render_receipt_sha256':hashlib.sha256((WORK/'fitted'/'render-receipt.json').read_bytes()).hexdigest(),
            'normalised_panel_size':[580,670],'views':colours,
            'mean_patch_delta_E76':float(np.mean(errors)),
            'front_face':face,
            'mean_face_patch_delta_E76':float(np.mean([p['delta_E76'] for p in face.values()])),
            'note':'Fixed interior fur-patch medians under unchanged studio lighting. '
                   'Not an albedo match or a texture/whole-character similarity score. '
                   'Reference and mesh have different local shading, especially in side view.'}
    (WORK/'color-measurements.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(scores,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('reference_image',type=Path)
    compare(parser.parse_args().reference_image)
