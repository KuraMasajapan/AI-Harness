"""Honest side-by-side reference and GLB review sheets."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent;WORK=ROOT/'work'
FONT=os.environ.get('MUSAN_REVIEW_FONT',str(WORK/'NotoSansJP.ttf'))
BG='#f6f3ed';INK='#292824';MUTED='#716c63'

def font(size):
    f=ImageFont.truetype(FONT,size)
    try:f.set_variation_by_axes([450])
    except (OSError,AttributeError):pass
    return f

def place(canvas,im,box,transparent=False):
    if transparent:
        im=im.convert('RGBA');im=im.crop(im.getchannel('A').getbbox())
    else:im=im.convert('RGB')
    im.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    x=box[0]+(box[2]-box[0]-im.width)//2;y=box[1]+(box[3]-box[1]-im.height)//2
    canvas.paste(im,(x,y),im if transparent else None)

def compare(reference):
    ref=Image.open(reference)
    assert ref.size==(1122,1402),f'Unexpected reference dimensions: {ref.size}'
    crop_worn=[(30,105,326,494),(339,105,542,494),(568,105,807,494)]
    crop_outfit=[(88,578,405,824),(450,575,705,826),(795,575,1075,826)]
    views=('front','side','back');labels=('正面','側面','背面')
    canvas=Image.new('RGB',(1800,2010),BG);d=ImageDraw.Draw(canvas)
    d.text((40,22),'執事服一式・調整版 / 参照とGLBの比較',font=font(38),fill=INK)
    d.text((40,78),'服だけをひとつの着脱パーツに統合・タオルなし・素体は変更なし',font=font(24),fill=MUTED)
    rows=[('参照 / 着用イメージ',130,430,False,crop_worn),
          ('GLB / 最新素体への着用',620,430,True,None),
          ('参照 / 衣装のみ',1110,335,False,crop_outfit),
          ('GLB / 衣装のみ（納品するパーツ）',1505,335,True,None)]
    for title,y,height,actual,crops in rows:
        d.text((40,y),title,font=font(27),fill=INK)
        for i,(view,label) in enumerate(zip(views,labels)):
            box=(i*600+36,y+50,(i+1)*600-36,y+height)
            if actual:
                im=Image.open(WORK/('dressed' if y==620 else 'outfit')/(view+'.png'))
            else:im=ref.crop(crops[i])
            place(canvas,im,box,actual)
            d.text((i*600+265,y+height+6),label,font=font(22),fill=MUTED)
    d.text((40,1906),'黒いウール / サテンの襟と蝶ネクタイ / チャコールの織柄ベスト / 白いシャツとチーフ / 金ボタン',font=font(23),fill=INK)
    d.text((40,1953),'参照にあるタオル・ヘッドセットは衣装に含めていません。静止姿勢でのフィット確認です',font=font(22),fill=MUTED)
    canvas.save(WORK/'reference-comparison.png')
    wearing=Image.new('RGB',(1800,1020),BG);d=ImageDraw.Draw(wearing)
    d.text((40,25),'むーさん / 執事服・フィットと丈の調整版',font=font(38),fill=INK)
    d.text((40,82),'最新の素体をそのまま使用・服一式だけを着脱・タオルなし',font=font(24),fill=MUTED)
    for i,(view,label) in enumerate(zip(views,labels)):
        place(wearing,Image.open(WORK/'dressed'/(view+'.png')),(i*600+25,155,(i+1)*600-25,940),True)
        d.text((i*600+265,958),label,font=font(24),fill=MUTED)
    wearing.save(WORK/'wearing-review.png')
    receipt={'reference_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),
             'reference_filename':reference.name,'worn_reference_crops':crop_worn,'outfit_reference_crops':crop_outfit,
             'render_receipts':{kind:hashlib.sha256((WORK/kind/'render-receipt.json').read_bytes()).hexdigest() for kind in ('dressed','outfit')}}
    (WORK/'comparison-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('reference',type=Path);a=p.parse_args();compare(a.reference)
