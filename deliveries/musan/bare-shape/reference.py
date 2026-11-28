"""Measure warm-coloured character silhouettes; ignore the grey ground shadow."""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
CROPS={'front':(90,20,680,660),'side':(790,20,1200,660),'back':(1330,20,1945,660)}

def measure(source):
    WORK.mkdir(exist_ok=True)
    im=Image.open(source).convert('RGB')
    result={}
    for view,normalized_box in CROPS.items():
        box=tuple(round(v*im.width/2048) for v in normalized_box)
        rgb=np.asarray(im.crop(box)).astype(float)
        mask=(rgb[:,:,0]-rgb[:,:,2]>12)&(rgb[:,:,0]-rgb[:,:,1]>3)&(rgb[:,:,0]>75)
        ys,xs=np.where(mask)
        top,bottom=int(ys.min()),int(ys.max());height=bottom-top
        center=(xs.min()+xs.max())/2
        profiles=[]
        for y in range(top,bottom+1):
            x=np.where(mask[y])[0]
            profiles.append([round((bottom-y)/height,6),round((x.min()-center)/height,6),round((x.max()-center)/height,6)] if len(x) else [])
        result[view]={'crop':box,'height_px':height,'top_px':top,'bottom_px':bottom,
                      'center_x_px':center,'width_over_height':float((xs.max()-xs.min())/height),
                      'profiles':[p for p in profiles if p]}
        closed=np.asarray(Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)))>128
        core=[]
        for y in range(top,bottom+1):
            row=closed[y];cx=round(center)
            if not row[cx]:continue
            left=cx;right=cx
            while left>0 and row[left-1]:left-=1
            while right+1<len(row) and row[right+1]:right+=1
            core.append([round((bottom-y)/height,6),round((right-left)/height/2,6)])
        result[view]['core_profile']=core
        Image.fromarray((mask*255).astype('uint8')).save(WORK/(view+'-reference-mask.png'))
        print(view,'height',height,'width/height',result[view]['width_over_height'])
    (ROOT/'shape-target.json').write_text(json.dumps(result,indent=2))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('reference_image',type=Path)
    measure(parser.parse_args().reference_image)
