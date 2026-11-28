"""Refine the approved wide room, without importing or modifying Musan.

Photographic CC0 PBR materials, tailored books, soft-edged joinery and a real
open sink. All detail is static, UV-mapped and embedded in the exported GLB.
"""
import hashlib
import json
import math
import random
import shutil
import sys
from pathlib import Path

import bpy
import bmesh
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'kitchen-study-wide'
WORK=ROOT/'work'
TEX=WORK/'textures'
sys.path.insert(0,str(BASE))
import texture_room as original
import build_room
import lighting

M={}
PI=math.pi
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
DETAILS={}

def image_mat(name,color=(1,1,1),rough=.5,metal=0,base=None,normal=None,roughmap=None,strength=.15):
    m=bpy.data.materials.new(name);m.use_nodes=True
    n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    p.inputs['Specular IOR Level'].default_value=.28
    for path,socket in [(base,'Base Color'),(normal,'Normal'),(roughmap,'Roughness')]:
        if not path:continue
        im=bpy.data.images.load(str(path),check_existing=True)
        if socket!='Base Color':im.colorspace_settings.name='Non-Color'
        im.pack();tex=n.new('ShaderNodeTexImage');tex.image=im;tex.extension='REPEAT'
        if socket=='Normal':
            nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=strength
            l.new(tex.outputs['Color'],nm.inputs['Color']);l.new(nm.outputs['Normal'],p.inputs[socket])
        elif socket=='Roughness':
            separate=n.new('ShaderNodeSeparateColor');l.new(tex.outputs['Color'],separate.inputs['Color'])
            l.new(separate.outputs['Green'],p.inputs[socket])
        else:l.new(tex.outputs['Color'],p.inputs[socket])
    return m

def tint(asset,name,target,contrast=.34,crop=None,size=1024,rough_range=(.45,.60)):
    src=WORK/'sources'/asset;out=[]
    for channel in ('Diffuse','nor_gl','Rough'):
        im=Image.open(src/(channel+'.jpg')).convert('RGB')
        if crop:im=im.crop(crop)
        im=im.resize((size,size),Image.Resampling.LANCZOS)
        a=np.asarray(im).astype(float)/255
        if channel=='Diffuse':
            # Preserve the measured grain, not baked shadows or dirty colour.
            luminance=a@np.array([.2126,.7152,.0722])
            modulation=np.clip(1+(luminance-luminance.mean())*contrast,.70,1.30)
            a=modulation[:,:,None]*np.array(target)[None,None,:]/255
        elif channel=='Rough':
            lo,hi=rough_range;a=lo+a*(hi-lo)
        # Normal/roughness are identical across the colourways. Reuse image
        # datablocks as well as bytes to avoid duplicating mobile GPU memory.
        path=TEX/((name if channel=='Diffuse' else asset)+'-'+channel+'.jpg')
        Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(path,quality=94)
        out.append(path)
    return out

def grain_uv(obj):
    me=obj.data;uv=me.uv_layers.active or me.uv_layers.new(name='UVMap')
    name=obj.name.lower()
    vertical=any(t in name for t in ('wall','leg','post','stile','back','side'))
    dims=obj.dimensions
    grain=2 if vertical else max(range(3),key=lambda i:dims[i])
    off=int(hashlib.sha256(name.encode()).hexdigest()[:4],16)/65536
    for face in me.polygons:
        dominant=max(range(3),key=lambda i:abs(face.normal[i]));axes=[i for i in range(3) if i!=dominant]
        if grain in axes:axes=[grain]+[i for i in axes if i!=grain]
        for li in face.loop_indices:
            co=me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv=(co[axes[0]]*abs(obj.scale[axes[0]])/2.0+off,
                            co[axes[1]]*abs(obj.scale[axes[1]])/.48+off*.71)

def surface(obj,name,mat,zone):
    obj.name=name;obj['layout_zone']=zone;obj['refined_detail']=True
    obj.data.materials.clear();obj.data.materials.append(mat)
    if not obj.data.uv_layers:original.uv_project(obj)
    if mat.get('wood'):grain_uv(obj)
    return obj

def box(name,loc,size,mat,zone='kitchen',r=.008):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if r:
        mod=o.modifiers.new('Machined edge radius','BEVEL');mod.width=min(r,min(size)*.44);mod.segments=4 if r>=.015 else 2
        norm=o.modifiers.new('Continuous face normals','WEIGHTED_NORMAL');norm.keep_sharp=True
    return surface(o,name,mat,zone)

def mesh(name,verts,faces,mat,zone='kitchen',smooth=True,uvs=None):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o)
    for p in me.polygons:p.use_smooth=smooth
    surface(o,name,mat,zone)
    if uvs:
        uv=me.uv_layers.active
        for li,l in enumerate(me.loops):uv.data[li].uv=uvs[l.vertex_index]
    return o

def tube(name,points,r,mat,zone='kitchen'):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2 if r>.007 else 1
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active=o;o.select_set(True)
    bpy.ops.object.convert(target='MESH');o.select_set(False)
    return surface(o,name,mat,zone)

def lathe(name,loc,profile,mat,zone='kitchen',n=64):
    verts=[];uv=[];faces=[]
    for j,(r,z) in enumerate(profile):
        for i in range(n):
            t=i*math.tau/n;verts.append((loc[0]+r*math.cos(t),loc[1]+r*math.sin(t),loc[2]+z));uv.append((i/n,j/max(1,len(profile)-1)))
    for j in range(len(profile)-1):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    return mesh(name,verts,faces,mat,zone,uvs=uv)

def materials(palette):
    for key,target in [('honey-oak',(164,125,85)),('wall-oak',(187,156,120)),
                       ('floor-oak',(171,137,99)),('warm-walnut',(103,78,58))]:
        paths=tint('dark_wood',key,target,contrast=.52,rough_range=(.37,.55))
        M[key]=image_mat('Refined '+key,base=paths[0],normal=paths[1],roughmap=paths[2],strength=.14)
        M[key]['wood']=True
    for key,target in [('ivory-linen',(224,214,193)),('plum-linen',(86,57,61)),('sage-cloth',(103,119,104))]:
        paths=tint('rough_linen',key,target,.85,size=512,rough_range=(.72,.92))
        M[key]=image_mat('Refined woven '+key,base=paths[0],normal=paths[1],roughmap=paths[2],strength=.24)
    paths=tint('marble_01','honed-limestone',(188,181,163),.42,crop=(430,285,690,480),size=512,rough_range=(.33,.48))
    M['stone']=image_mat('Honed limestone slab',base=paths[0],normal=paths[1],roughmap=paths[2],strength=.12)
    paths=tint('fine_grained_wood','chopping-board',(161,126,82),.40,size=512,rough_range=(.48,.65))
    M['boardwood']=image_mat('Fine-grained chopping board',base=paths[0],normal=paths[1],roughmap=paths[2],strength=.12)
    M['boardwood']['wood']=True
    M['brass']=image_mat('Satin champagne brass',(.49,.32,.13),.26,.88)
    M['steel']=image_mat('Brushed nickel',(.44,.47,.49),.22,.94)
    M['black']=image_mat('Graphite cast iron',(.012,.015,.017),.48,.64)
    M['enamel']=image_mat('Warm ivory lacquer',(.70,.67,.58),.30)
    M['glass']=image_mat('Oven dark reflective glass',(.008,.014,.018),.12,.18)
    M['ceramic']=image_mat('Sage porcelain glaze',(.12,.21,.16),.20)
    M['white']=image_mat('Warm white porcelain',(.78,.75,.66),.18)
    M['bottle']=image_mat('Olive glass bottle',(.045,.070,.026),.16,.05)
    M['leather']=image_mat('Cognac leather cushion',(.23,.11,.055),.54)
    # Replace materials by data identity. This also retains UVs on source food.
    remap={palette[k]:v for k,v in M.items() if k in palette}
    remap[palette['limestone']]=M['stone'];remap[palette['paint']]=M['enamel']
    for o in bpy.context.scene.objects:
        if o.type!='MESH':continue
        for slot in o.material_slots:
            if slot.material in remap:slot.material=remap[slot.material]
        if any(m.get('wood') for m in o.data.materials):grain_uv(o)
    M['paper']=palette['paper']
    # Retain a dark, modestly textured seam, not a black cartoon outline.
    seams=[m for m in bpy.data.materials if m.name=='Timber seams']
    for m in seams:
        if m.use_nodes:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.25,.18,.12,1)

def book_material():
    colors=[(43,58,62),(88,57,55),(75,91,76),(154,132,92),(69,77,94),(170,156,128),(105,85,65),(58,80,77)]
    names=['BOTANICA','THE SEA','ATELIER','FIELD NOTES','ESSAYS','NATURAL HISTORY','FORM & LIGHT','KINSHIP']
    im=Image.new('RGB',(1024,1024));d=ImageDraw.Draw(im)
    font=ImageFont.truetype(FONT,24);small=ImageFont.truetype(FONT,12)
    for c,(col,title) in enumerate(zip(colors,names)):
        left=c*128;d.rectangle((left,0,left+127,1023),fill=col)
        gold=tuple(int(v*.35+g*.65) for v,g in zip(col,(206,181,125)))
        for y in [72,85,840,855,927]:d.line((left+14,y,left+113,y),fill=gold,width=2)
        d.rectangle((left+12,150,left+115,800),outline=tuple(int(v*1.17) for v in col),width=2)
        label=Image.new('RGBA',(600,60));ld=ImageDraw.Draw(label)
        ld.text((10,16),title,font=font,fill=(*gold,255));label=label.rotate(90,expand=True)
        im.paste(label,(left+35,230),label)
        d.text((left+37,883),f'VOL {c+1}',font=small,fill=gold)
        for k in range(4):d.arc((left+40-k*4,120-k*5,left+87+k*4,170+k*5),0,360,fill=gold,width=1)
    a=np.asarray(im).astype(float);rng=np.random.default_rng(12)
    a+=rng.normal(0,.85,a.shape[:2])[:,:,None]
    path=TEX/'book-cloth-atlas.jpg';Image.fromarray(np.uint8(np.clip(a,0,255))).save(path,quality=96)
    M['book']=image_mat('Cloth bindings and foil titles',base=path,rough=.72)
    paper=np.zeros((512,512,3));noise=rng.normal(0,.008,(512,512))
    rows=np.sin(np.arange(512)*2.1)[:,None]*.025
    paper[:]=np.array([.82,.79,.70]);paper+=noise[:,:,None]+rows[:,:,None]
    path=TEX/'individual-page-edges.jpg';Image.fromarray(np.uint8(np.clip(paper,0,1)*255)).save(path,quality=95)
    M['pages']=image_mat('Ivory individual page edges',base=path,rough=.91)

def books():
    for o in list(bpy.context.scene.objects):
        if o.name.startswith(('Book spine','Book gold band')):bpy.data.objects.remove(o,do_unlink=True)
    book_material();rng=random.Random(43);count=0
    for row,z0 in enumerate((.132,.622,1.172)):
        for i in range(9):
            y=-.055+i*.128;h=rng.uniform(.30,.425) if row!=1 else rng.uniform(.33,.44)
            thickness=rng.uniform(.066,.095);dep=rng.uniform(.245,.31);x=-3.645-rng.uniform(0,.025)
            c=(i+row*3)%8
            for sign in (-1,1):
                o=box('Cloth-covered hardback cover',(x-dep/2,y+sign*thickness/2,z0+h/2),
                      (dep+.01,.006,h+.012),M['book'],'study',.002)
                uv=o.data.uv_layers.active
                for e in uv.data:e.uv=((c+.5)/8,.97)
            o=box('Layered paper block',(x-dep/2-.008,y,z0+h/2),
                  (dep-.02,thickness-.01,h-.016),M['pages'],'study',.002)
            uv=o.data.uv_layers.active
            for face in o.data.polygons:
                for li in face.loop_indices:
                    co=o.data.vertices[o.data.loops[li].vertex_index].co
                    uv.data[li].uv=(co.x*3,(co.y/(thickness-.01) if abs(face.normal.z)>.5 else co.z/h))
            verts=[];uv=[];faces=[];nu=1;nv=12
            for j in range(nu+1):
                u=j/nu
                for k in range(nv+1):
                    v=k/nv;verts.append((x+.010*math.sin(v*PI),y+(v-.5)*thickness,z0+h*u))
                    uv.append(((c+.03+.94*v)/8,.02+.96*u))
            for j in range(nu):
                for k in range(nv):
                    a=j*(nv+1)+k;faces.append((a,a+1,a+nv+2,a+nv+1))
            mesh('Rounded printed book spine',verts,faces,M['book'],'study',uvs=uv)
            count+=1
    DETAILS['individual_bound_books']=count

def furniture():
    prefixes=('Writing desk top','Writing desk leg','Desk drawer','Drawer pull','Lamp shade')
    for o in list(bpy.context.scene.objects):
        if o.name.startswith(prefixes):bpy.data.objects.remove(o,do_unlink=True)
    box('Rounded solid-oak desktop',(-3.64,-1.12,.80),(.86,1.65,.065),M['honey-oak'],'study',.028)
    for x in (-3.95,-3.33):
        for y in (-1.80,-.44):
            verts=[]
            for z,r,dx in [(.06,.023,.016),(.765,.038,0)]:
                verts.extend([(x+sx*r+math.copysign(dx,x+3.64),y+sy*r,z) for sx,sy in [(-1,-1),(-1,1),(1,1),(1,-1)]])
            o=mesh('Tapered walnut desk leg',verts,[(0,3,2,1),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],M['warm-walnut'],'study',False)
            be=o.modifiers.new('Leg edge chamfer','BEVEL');be.width=.006;be.segments=4
            o.modifiers.new('Leg weighted normals','WEIGHTED_NORMAL')
    box('Drawer carcass shadow',(-3.64,-1.12,.682),(.65,1.49,.15),M['warm-walnut'],'study')
    for y in (-1.62,-1.12,-.62):
        box('Inset walnut drawer front',(-3.299,y,.683),(.027,.485,.129),M['warm-walnut'],'study',.008)
        tube('Champagne drawer pull',[(-3.269,y-.06,.685),(-3.25,y-.06,.685),(-3.25,y+.06,.685),(-3.269,y+.06,.685)],.005,M['brass'],'study')
    # Open, thin linen shade; no opaque caps closing the lampshade.
    shade=M['ivory-linen'].copy();shade.name='Woven translucent-look linen shade'
    shade.node_tree.nodes.get('Principled BSDF').inputs['Emission Color'].default_value=(1,.61,.30,1)
    shade.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=.10
    sh=lathe('Hollow linen lampshade',(-3.76,-.52,0),[(.190,1.225),(.188,1.23),(.108,1.47),(.105,1.475)],shade,'study')
    so=sh.modifiers.new('Thin linen edge','SOLIDIFY');so.thickness=.002
    for r,z in [(.19,1.225),(.105,1.475)]:tube('Lampshade stitched rim',[(-3.76+r*math.cos(t),-.52+r*math.sin(t),z) for t in np.linspace(0,math.tau,65)],.0025,M['ivory-linen'],'study')
    box('Sewn cognac seat cushion',(-2.98,-1.15,.562),(.405,.376,.035),M['leather'],'study',.026)
    # Real cabinet front and restrained brass hardware, inside the old footprint.
    box('Bedside inset drawer',(2.34,.939,.49),(.47,.022,.20),M['warm-walnut'],'bed',.007)
    tube('Bedside brass pull',[(2.28,.916,.49),(2.28,.902,.49),(2.40,.902,.49),(2.40,.916,.49)],.005,M['brass'],'bed')
    for name in ('Ivory pillow - soft cushion','Plum pillow - soft cushion'):
        o=bpy.data.objects.get(name)
        if not o:continue
        bb=[Vector(p) for p in o.bound_box];lo=Vector([min(p[k] for p in bb) for k in range(3)]);hi=Vector([max(p[k] for p in bb) for k in range(3)])
        center=(lo+hi)/2;half=(hi-lo)/2;points=[]
        for t in np.linspace(0,math.tau,100):
            pt=center+Vector((math.copysign(abs(math.cos(t))**.44,math.cos(t))*half.x,
                              math.copysign(abs(math.sin(t))**.44,math.sin(t))*half.y,0))
            points.append(o.matrix_world@pt)
        tube('Pillow tailored piping',points,.002,M['ivory-linen' if name.startswith('Ivory') else 'plum-linen'],'bed')
    DETAILS['joinery']='Radius-edged oak top, tapered legs, three inset drawers, brass pulls, hollow linen shade, sewn cushions'

def kitchen():
    prefixes=('kitchen','door','drawer','Cabinet face','pot','Spoon bowl','Utensil handle','Utensil rail')
    for o in list(bpy.context.scene.objects):
        if o.get('layout_zone')=='kitchen' and o.name.startswith(prefixes):bpy.data.objects.remove(o,do_unlink=True)
    # Three fitted carcasses: hollow so the sink is genuinely recessed.
    for cx in (-3.31,-2.53,-1.75):
        for x in (cx-.357,cx+.357):box('Cabinet side panel',(x,1.70,.43),(.022,.70,.69),M['enamel'])
        box('Cabinet recessed plinth',(cx,1.76,.095),(.69,.53,.11),M['warm-walnut'])
        box('Cabinet back',(cx,2.039,.43),(.70,.022,.69),M['enamel'])
        box('Cabinet floor',(cx,1.70,.13),(.71,.68,.025),M['enamel'])
        if cx!=-2.53:
            for sx in (-1,1):
                x=cx+sx*.179
                box('Recessed door field',(x,1.34,.43),(.337,.018,.615),M['enamel'],r=.004)
                for dx in (-.153,.153):box('Shaker door stile',(x+dx,1.322,.43),(.032,.026,.635),M['enamel'],r=.004)
                for z in (.128,.732):box('Shaker door rail',(x,1.322,z),(.305,.026,.032),M['enamel'],r=.004)
                tube('Cabinet brass pull',[(cx+sx*.045,1.302,.54),(cx+sx*.045,1.278,.54),(cx+sx*.045,1.278,.65),(cx+sx*.045,1.302,.65)],.005,M['brass'])
    # Single-slab counters, with an actual sink aperture cut into four pieces.
    box('Limestone worktop right',(-1.75,1.70,.815),(.78,.77,.06),M['stone'],r=.010)
    cx=-3.31;cy=1.70
    slabverts=[]
    for rx,ry,z in [(.39,.385,.785),(.39,.385,.845),(.256,.199,.785),(.256,.199,.845)]:
        slabverts += [(cx+x*rx,cy+y*ry,z) for x,y in [(-1,-1),(1,-1),(1,1),(-1,1)]]
    slabfaces=[]
    for i in range(4):
        j=(i+1)%4
        slabfaces.extend([(i+4,j+4,j+12,i+12),(j,i,i+8,j+8),(i,j,j+4,i+4),(i+8,i+12,j+12,j+8)])
    slab=mesh('Seamless limestone slab with sink aperture',slabverts,slabfaces,M['stone'],smooth=False)
    be=slab.modifiers.new('Slab eased edges','BEVEL');be.width=.005;be.segments=3
    slab.modifiers.new('Slab weighted normals','WEIGHTED_NORMAL')
    verts=[];faces=[];n=96
    for z,rx,ry in [(.846,.260,.207),(.844,.250,.199),(.822,.243,.192),(.715,.215,.164),(.690,.185,.137),(.688,.01,.01)]:
        for i in range(n):
            t=i*math.tau/n
            verts.append((cx+rx*math.copysign(abs(math.cos(t))**.43,math.cos(t)),cy+ry*math.copysign(abs(math.sin(t))**.43,math.sin(t)),z))
    for j in range(5):
        for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    bowl=mesh('Deep drawn stainless sink',verts,faces,M['steel'])
    so=bowl.modifiers.new('Sink sheet thickness','SOLIDIFY');so.thickness=.002
    lathe('Sink drain',(cx,cy,.689),[(.0,0),(.034,0),(.034,.003),(.015,.005)],M['black'])
    points=[(cx,1.989,.84),(cx,1.989,1.045)]
    points += [(cx,1.89+.099*math.cos(t),1.045+.099*math.sin(t)) for t in np.linspace(0,PI,33)]
    points += [(cx,1.791,1.005)]
    tube('Gooseneck brushed mixer tap',points,.012,M['steel'])
    lathe('Mixer tap foot',(cx,1.989,.838),[(.032,0),(.032,.012),(.017,.018),(.015,.06)],M['steel'])
    tube('Mixer lever',[(cx+.03,1.989,.87),(cx+.06,1.989,.91),(cx+.09,1.989,.91)],.006,M['steel'])
    # Oven and hob: crisp glass, recessed controls, cast-iron grates.
    box('Built-in oven surround',(-2.53,1.326,.435),(.745,.05,.64),M['steel'])
    box('Oven reflective glass',(-2.53,1.294,.405),(.635,.019,.40),M['glass'],r=.018)
    box('Oven viewing pane',(-2.53,1.282,.395),(.49,.005,.27),M['black'],r=.015)
    tube('Oven satin handle',[(-2.79,1.282,.64),(-2.79,1.24,.64),(-2.27,1.24,.64),(-2.27,1.282,.64)],.011,M['steel'])
    for x in np.linspace(-2.79,-2.27,4):
        o=lathe('Oven control knob',(0,0,0),[(.018,0),(.020,.012),(.017,.020)],M['steel'],n=32)
        o.rotation_euler[0]=PI/2;o.location=(x,1.289,.724)
    box('Black ceramic hob',(-2.53,1.70,.827),(.74,.71,.039),M['black'],r=.020)
    for x in (-2.69,-2.37):
        for y in (1.54,1.86):
            lathe('Gas burner',(x,y,.851),[(.0,0),(.083,0),(.085,.009),(.055,.016),(.052,.022)],M['steel'],n=40)
            tube('Cast iron burner ring',[(x+.095*math.cos(t),y+.095*math.sin(t),.885) for t in np.linspace(0,math.tau,49)],.007,M['black'])
            for a in (0,PI/2):
                tube('Burner support',[(x+.13*math.cos(a),y+.13*math.sin(a),.886),(x-.13*math.cos(a),y-.13*math.sin(a),.886)],.008,M['black'])
    lathe('Sage enamel casserole',(-2.37,1.86,.888),[(.0,0),(.116,0),(.138,.018),(.145,.105),(.142,.143),(.135,.148)],M['ceramic'])
    lathe('Casserole rim',(-2.37,1.86,1.033),[(.133,0),(.145,0),(.145,.009),(.133,.010)],M['steel'])
    lathe('Domed casserole lid',(-2.37,1.86,1.044),[(.143,0),(.13,.012),(.08,.028),(.02,.035),(.0,.035)],M['ceramic'])
    lathe('Casserole lid knob',(-2.37,1.86,1.075),[(.015,0),(.018,.012),(.022,.022),(.016,.029),(.0,.030)],M['black'],n=32)
    for s in (-1,1):tube('Casserole loop handle',[(-2.37+s*.14,1.82,1.005),(-2.37+s*.19,1.82,1.005),(-2.37+s*.19,1.90,1.005),(-2.37+s*.14,1.90,1.005)],.011,M['ceramic'])
    # Small-format porcelain splashback, restrained enough for the timber room.
    for row in range(3):
        for col in range(16):
            x=-3.69+col*.145
            box('Ivory porcelain splashback',(x,2.214,.91+row*.105),(.141,.025,.101),M['white'],r=.003)
    box('Solid oak chopping board',(-1.75,1.62,.865),(.39,.29,.028),M['boardwood'],r=.018)
    lathe('Olive glass oil bottle',(-1.50,1.91,.846),[(.0,0),(.038,0),(.041,.025),(.041,.18),(.024,.211),(.017,.218),(.017,.272)],M['bottle'])
    lathe('Oil bottle cap',(-1.50,1.91,1.11),[(.019,0),(.019,.035),(.0,.035)],M['brass'],n=32)
    for x in (-1.87,-1.69):
        lathe('Fine porcelain cup',(x,1.65,.88),[(.0,0),(.033,0),(.044,.078),(.041,.08),(.030,.011),(.0,.011)],M['white'])
        tube('Porcelain cup handle',[(x+.041+.026*math.sin(t),1.65,.921+.032*math.cos(t)) for t in np.linspace(0,PI,25)],.005,M['white'])
    DETAILS['kitchen']='Hollow fitted cabinets, open recessed stainless sink, curved mixer, limestone slabs, porcelain splashback, oven glass, four burners and enamel casserole'

def window_views():
    # Develop the CC0 photographic panorama and extract two rectilinear views.
    # This is a lightweight background plate, not an extra HDR environment or
    # an additional runtime light. The kitchen view does not repeat the sun.
    image=bpy.data.images.load(str(WORK/'sources'/'qwantani_sunset'/'sunset-2k.hdr'),check_existing=True)
    width,height=image.size
    pixels=np.asarray(image.pixels[:]).reshape(height,width,4)[::-1,:,:3]
    luminance=pixels@np.array([.2126,.7152,.0722])
    sy,sx=np.unravel_index(luminance.argmax(),luminance.shape)
    sun_yaw=(sx/width-.5)*math.tau
    n=512;v,u=np.mgrid[0:n,0:n]
    xx=((u+.5)/n*2-1)*math.tan(math.radians(37))
    yy=(1-(v+.5)/n*2)*math.tan(math.radians(37))
    atlas=Image.new('RGB',(1024,512))
    for index,yaw in enumerate((sun_yaw-.10,sun_yaw-.83)):
        lon=np.arctan2(xx,np.ones_like(xx))+yaw
        lat=np.arctan2(yy,np.sqrt(1+xx*xx))+.05
        px=(lon/math.tau+.5)*width;py=(.5-lat/PI)*height
        x0=np.floor(px).astype(int)%width;x1=(x0+1)%width
        y0=np.clip(np.floor(py).astype(int),0,height-1);y1=np.minimum(y0+1,height-1)
        wx=(px-np.floor(px))[:,:,None];wy=(py-np.floor(py))[:,:,None]
        a=(pixels[y0,x0]*(1-wx)+pixels[y0,x1]*wx)*(1-wy)+(pixels[y1,x0]*(1-wx)+pixels[y1,x1]*wx)*wy
        a*=.8
        a=np.clip((a*(2.51*a+.03))/(a*(2.43*a+.59)+.14),0,1)
        a=np.where(a<=.0031308,a*12.92,1.055*a**(1/2.4)-.055)
        atlas.paste(Image.fromarray(np.uint8(np.clip(a,0,1)*255)),(index*512,0))
    path=TEX/'photographic-sunset-windows.jpg';atlas.save(path,quality=97)
    photo=image_mat('Photographic sunset beyond both windows',base=path,rough=1)
    p=photo.node_tree.nodes.get('Principled BSDF');tex=next(n for n in photo.node_tree.nodes if n.type=='TEX_IMAGE')
    for link in list(p.inputs['Base Color'].links):photo.node_tree.links.remove(link)
    p.inputs['Base Color'].default_value=(0,0,0,1)
    photo.node_tree.links.new(tex.outputs['Color'],p.inputs['Emission Color'])
    p.inputs['Emission Strength'].default_value=.90;p.inputs['Specular IOR Level'].default_value=0
    disk=bpy.data.objects['Round dusk window'];disk.data.materials.clear();disk.data.materials.append(photo)
    for e in disk.data.uv_layers.active.data:e.uv.x=.003+e.uv.x*.494;e.uv.y=.006+e.uv.y*.988
    old=bpy.data.objects.get('Window pane')
    if old:bpy.data.objects.remove(old,do_unlink=True)
    verts=[(-3.19,2.216,1.07),(-2.11,2.216,1.07),(-2.11,2.216,2.03),(-3.19,2.216,2.03)]
    mesh('Kitchen photographic sunset view',verts,[(0,1,2,3)],photo,smooth=False,
         uvs=[(.503,.006),(.997,.006),(.997,.994),(.503,.994)])
    glaze=bpy.data.objects['Round window clear glazing'].data.materials[0]
    gp=glaze.node_tree.nodes.get('Principled BSDF')
    gp.inputs['Alpha'].default_value=.045
    gp.inputs['Roughness'].default_value=.085
    mesh('Kitchen clear reflective glazing',[(x,2.209,z) for x,y,z in verts],[(0,1,2,3)],glaze,smooth=False)
    DETAILS['window_background']='Two rectilinear views from CC0 Qwantani Sunset, shared 1024x512 photographic atlas; static plates, not exterior 3D geometry'

def refine(palette):
    materials(palette);books();furniture();kitchen();window_views()
    # Fix faceted source chair spindles and turned legs without smoothing flat
    # cabinet panels. No subdivision of the whole mobile scene.
    for o in bpy.context.scene.objects:
        if o.type!='MESH':continue
        if o.name.startswith('Natural oak floorboard'):
            for mod in o.modifiers:
                if mod.type=='BEVEL':mod.segments=1
        if any(s in o.name.lower() for s in ('spindle','slender chair leg','stem','window frame','lamp base')):
            bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bm.to_mesh(o.data);bm.free()
            for p in o.data.polygons:p.use_smooth=True
        if o.get('refined_detail'):DETAILS['authored_meshes']=DETAILS.get('authored_meshes',0)+1
    bpy.ops.wm.save_as_mainfile(filepath=str(WORK/'refinement-authoring.blend'))

def build():
    WORK.mkdir(exist_ok=True);TEX.mkdir(exist_ok=True)
    for name in ('kitchen-study.glb','musan-butler-detail-v12.glb'):
        shutil.copy2(BASE/'work'/name,WORK/name)
    original.WORK=WORK;original.TEXTURES=TEX
    lighting.WORK=WORK
    original.build(scene_hook=refine)
    body=WORK/'musan-butler-detail-v12.glb'
    assert hashlib.sha256(body.read_bytes()).hexdigest()==build_room.AVATAR_SHA256
    (WORK/'refinement.json').write_text(json.dumps({'character_modified':False,'character_in_room_glb':False,
        'layout_unchanged':True,'evening_lights_unchanged':True,'details':DETAILS},indent=2)+'\n')
    print('REFINED_ROOM_BUILT',json.dumps(DETAILS))

if __name__=='__main__':build()
