"""Independent, body-fitted butler clothing; never edit/export the wearer."""
import hashlib
import json
import math
from pathlib import Path

import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import tessellate_polygon
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
BODY=ROOT.parent/'bare-shape/work/musan-bare-shape.glb'
BODY_SHA='22cf5278e1067365dee6438b08d37256ed64caab2585df1dacac6282bb72e2bb'
GROUPS=('Shirt','Waistcoat','Tailcoat','PocketSquare')
PI=math.pi
CURRENT=None
MATS={}
BVH=None

def group(name):
    obj=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(obj)
    obj['wardrobe_slot']=name
    obj['coordinate_contract']='Same origin, rotation and scale as musan-bare-shape.glb'
    return obj

def add_mesh(name,vertices,faces,mat,uv=None,thickness=0,bevel=0):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
    obj.parent=CURRENT;mesh.materials.append(mat)
    tex=mesh.uv_layers.new(name='UVMap')
    for p in mesh.polygons:
        p.use_smooth=True
        for li in p.loop_indices:
            v=mesh.vertices[mesh.loops[li].vertex_index].co
            tex.data[li].uv=uv[mesh.loops[li].vertex_index] if uv is not None else (v.x*8,v.z*8)
    # UV seams must not become hard shading seams down the sleeve. Keep loop UVs
    # but weld coincident geometric vertices before giving the cloth thickness.
    bm=bmesh.new();bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
    bm.to_mesh(mesh);bm.free();mesh.update()
    if thickness:
        mod=obj.modifiers.new('Folded fabric thickness','SOLIDIFY');mod.thickness=thickness;mod.offset=0
        mod.use_even_offset=True
    if bevel:
        mod=obj.modifiers.new('Soft tailored edge','BEVEL');mod.width=bevel;mod.segments=3
    return obj

def grid(name,fn,nu,nv,mat,thickness=.002,uvscale=(3,2)):
    vertices=[];uv=[]
    for i in range(nu+1):
        for j in range(nv+1):
            u=i/nu;v=j/nv;vertices.append(fn(u,v));uv.append((u*uvscale[0],v*uvscale[1]))
    faces=[]
    for i in range(nu):
        for j in range(nv):
            a=i*(nv+1)+j;faces.append((a,a+nv+1,a+nv+2,a+1))
    return add_mesh(name,vertices,faces,mat,uv,thickness)

def tube(name,points,radius,mat,sides=8):
    vertices=[]
    for i,p in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        tangent.normalize();axis=tangent.cross(Vector((0,1,0)))
        if axis.length<.01:axis=tangent.cross(Vector((1,0,0)))
        axis.normalize();other=tangent.cross(axis)
        for j in range(sides):
            v=Vector(p)+radius*(axis*math.cos(j*2*PI/sides)+other*math.sin(j*2*PI/sides))
            vertices.append(tuple(v))
    faces=[(i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j)
           for i in range(len(points)-1) for j in range(sides)]
    return add_mesh(name,vertices,faces,mat)

def ellipsoid(name,loc,scale,mat,segments=20,rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc)
    obj=bpy.context.object;obj.name=name;obj.scale=scale;obj.parent=CURRENT
    obj.data.materials.append(mat)
    for p in obj.data.polygons:p.use_smooth=True
    return obj

Z=np.array([.07,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60,.625,.65])
RX=np.array([.20,.245,.272,.297,.308,.310,.300,.292,.285,.280,.278,.274,.27])
FRONT=np.array([.19,.18,.238,.263,.273,.275,.268,.256,.240,.224,.215,.212,.208])
BACK=np.array([.27,.275,.26,.259,.267,.269,.264,.255,.245,.235,.232,.231,.23])

def torso(theta,z,layer):
    # Fit the actual body surface; cap only the lateral ray where the arm is
    # fused into the trunk. Below the belly, let the skirts hang rather than
    # collapsing into the legs. The source wearer itself is never deformed.
    fit_z=max(.265,z)
    rx=float(np.interp(fit_z,Z,RX));depth=float(np.interp(fit_z,Z,FRONT if math.cos(theta)>=0 else BACK))
    d=Vector((math.sin(theta),-math.cos(theta),0))
    hit,_,_,distance=BVH.ray_cast(Vector((0,0,fit_z)),d)
    envelope=1/math.sqrt((math.sin(theta)/rx)**2+(math.cos(theta)/depth)**2)
    radius=min(distance if hit is not None else envelope,envelope+.003)+layer
    # Just enough ease in the hanging lower skirt, not a box around the torso.
    radius+=.005*max(0,(.30-z)/.22)
    return (d.x*radius,d.y*radius,z)

def front(x,z,layer):
    hit,_,_,_=BVH.ray_cast(Vector((x,-2,max(.265,z))),Vector((0,1,0)))
    if hit is not None:return hit.y-layer
    rx=float(np.interp(z,Z,RX))+layer
    return -float(np.interp(z,Z,FRONT)+layer)*math.sqrt(max(.01,1-(x/rx)**2))

def rear(x,z,layer):
    hit,_,_,_=BVH.ray_cast(Vector((x,2,max(.265,z))),Vector((0,-1,0)))
    return (hit.y if hit is not None else float(np.interp(z,Z,BACK)))+layer

def patch(name,outline,mat,layer,roll=0,thickness=.002,back=False):
    # Subdivide the 2D tailoring pattern, then fit every vertex to the chest.
    verts=[Vector((x,0,z)) for x,z in outline]
    triangles=tessellate_polygon([verts])
    indices={tuple(v):i for i,v in enumerate(verts)}
    faces=[[int(v) if isinstance(v,int) else indices[tuple(v)] for v in tri] for tri in triangles]
    obj=add_mesh(name,[tuple(v) for v in verts],faces,mat)
    bpy.context.view_layer.objects.active=obj;obj.select_set(True)
    mod=obj.modifiers.new('Curved pattern subdivision','SUBSURF');mod.subdivision_type='SIMPLE';mod.levels=3
    bpy.ops.object.modifier_apply(modifier=mod.name)
    for v in obj.data.vertices:
        if back:
            rx=float(np.interp(v.co.z,Z,RX))+layer
            v.co.y=rear(v.co.x,max(.265,v.co.z),layer)+.012*max(0,(.30-v.co.z)/.28)
        else:
            v.co.y=front(v.co.x,v.co.z,layer)-roll*math.sin(PI*min(1,max(0,(v.co.z-.34)/.27)))
    for poly in obj.data.polygons:
        for li in poly.loop_indices:
            v=obj.data.vertices[obj.data.loops[li].vertex_index].co
            obj.data.uv_layers.active.data[li].uv=(v.x*8,v.z*8)
    solid=obj.modifiers.new('Fabric edge thickness','SOLIDIFY');solid.thickness=thickness;solid.offset=0
    bevel=obj.modifiers.new('Soft rolled edge','BEVEL');bevel.width=.0012;bevel.segments=3
    obj.select_set(False)
    return obj

def texture(kind):
    n=512;rng=np.random.default_rng(18)
    y,x=np.mgrid[:n,:n];noise=rng.normal(0,1,(n,n))
    weave=np.sin(x*PI/2)*np.sin(y*PI/2)+.35*np.sin((x+y)*PI/3)
    if kind=='damask':
        # Tileable woven botanical medallions, not a painted flat checkerboard.
        mask=Image.new('L',(n,n));d=ImageDraw.Draw(mask)
        for cx in (-128,128,384,640):
            for cy in (-128,128,384,640):
                for s in (-1,1):
                    for k in range(3):
                        a=cx+s*(14+k*15);b=cy-90+k*18
                        d.arc((a-36,b-25,a+36,b+25),0 if s>0 else 90,285 if s>0 else 375,fill=200,width=4)
                    d.ellipse((cx+s*18-12,cy-52,cx+s*18+12,cy-6),outline=180,width=3)
                d.line([(cx,cy-93),(cx,cy+93)],fill=140,width=3)
                d.polygon([(cx,cy-108),(cx-12,cy-85),(cx,cy-61),(cx+12,cy-85)],fill=170)
                d.arc((cx-82,cy-100,cx+82,cy+100),15,165,fill=160,width=3)
                d.arc((cx-82,cy-100,cx+82,cy+100),195,345,fill=160,width=3)
        pattern=np.asarray(mask.filter(ImageFilter.GaussianBlur(.6)))/255
        base=np.array([29,28,27]);variation=pattern*28+weave*.9+noise*.6;rough=.80-pattern*.18
    elif kind=='wool':
        base=np.array([18,17,16]);variation=weave*1.1+noise*.9+.5*np.sin(x*.7+y*.22);rough=np.clip(.85+noise*.025,.74,.95)
    elif kind=='satin':
        base=np.array([8,8,7]);variation=.5*np.sin(x*PI)+.35*noise;rough=np.full((n,n),.30)
    else:
        base=np.array([242,239,231]);variation=weave*1.1+noise*.35;rough=np.full((n,n),.83)
    rgb=np.clip(base+variation[:,:,None],0,255).astype('uint8')
    # Very shallow warp/weft normal texture; glTF-compatible, no live noise nodes.
    dx=np.cos(x*PI/2)*.065;dy=np.cos(y*PI/2)*.065
    if kind=='wool':
        dx+=.075*np.sin((x+np.where((y//20)%2,1,-1)*y*.5)*2*PI/12)+noise*.018
        dy+=.045*np.sin(y*2*PI/9)
    normal=np.stack((.5+dx,.5+dy,np.sqrt(np.maximum(0,1-dx*dx-dy*dy))*.5+.5),2)
    paths=[]
    for suffix,array in [('base',rgb),('normal',(normal*255).astype('uint8')),
                         ('rough',(np.clip(rough,0,1)*255).astype('uint8'))]:
        path=WORK/f'{kind}-{suffix}.png';Image.fromarray(array).save(path);paths.append(path)
    return paths

def fabric(name,kind):
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    nodes=mat.node_tree.nodes;links=mat.node_tree.links;p=nodes.get('Principled BSDF')
    p.inputs['Roughness'].default_value=.8;p.inputs['Specular IOR Level'].default_value=.26
    paths=texture(kind)
    for suffix,path in zip(('base','normal','rough'),paths):
        im=bpy.data.images.load(str(path));im.pack()
        tex=nodes.new('ShaderNodeTexImage');tex.image=im;tex.extension='REPEAT'
        if suffix=='base':links.new(tex.outputs['Color'],p.inputs['Base Color'])
        else:
            im.colorspace_settings.name='Non-Color'
            if suffix=='rough':links.new(tex.outputs['Color'],p.inputs['Roughness'])
            else:
                normal=nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.5 if kind!='satin' else .22
                links.new(tex.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs[0],p.inputs['Normal'])
    if kind=='satin':p.inputs['Specular IOR Level'].default_value=.10
    return mat

def simple(name,color,metallic,rough):
    m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metallic;p.inputs['Roughness'].default_value=rough
    return m

def make_materials():
    for name,kind in [('wool','wool'),('satin','satin'),('damask','damask'),('cotton','cotton')]:
        MATS[name]=fabric({'wool':'Black fine wool','satin':'Black satin lapels and bow',
                          'damask':'Charcoal botanical jacquard','cotton':'Ivory woven cotton'}[name],kind)
    MATS['gold']=simple('Brushed warm gold',(.80,.50,.16),.78,.24)
    MATS['thread']=simple('Black tailoring thread',(.009,.008,.007),0,.9)
    MATS['pearl']=simple('Black shirt buttons',(.012,.010,.009),.1,.28)

def shell(name,mat,layer,zbottom,ztop,opening=0,hem=None,uvscale=(2,7)):
    def fn(u,v):
        theta0=2*PI*v
        bottom=hem(theta0) if hem else zbottom
        top=ztop-.020*math.sin(theta0)**2
        z=bottom+(top-bottom)*u
        op=opening(z) if callable(opening) else opening*u*u
        theta=op+(2*PI-2*op)*v
        return torso(theta,z,layer)
    return grid(name,fn,18,72,mat,.003,uvscale)

def sleeve(sign,mat,layer,start=0,end=1,name='Sleeve'):
    def fn(u,v):
        t=start+(end-start)*u;theta=2*PI*v
        center=Vector((sign*(.215+.150*t),.002,.540-.250*t))
        axis=Vector((sign*.150,0,-.250)).normalized();across=Vector((sign*-axis.z,0,abs(axis.x)))
        direction=across*math.cos(theta)+Vector((0,1,0))*math.sin(theta)
        hit,_,_,distance=BVH.ray_cast(center,direction)
        r1=.104-.025*t;r2=.151-.022*t
        limit=1/math.sqrt((math.cos(theta)/r1)**2+(math.sin(theta)/r2)**2)
        radius=min(distance if hit is not None else limit,limit)+layer
        ease=.0008*math.sin(t*PI*7)*math.exp(-((t-.62)/.25)**2)
        p=center+direction*(radius+ease)
        return tuple(p)
    obj=grid(f'{name} {sign:+}',fn,6 if end-start<.2 else 20,40,mat,.0025,(3,3))
    return obj,fn

def button(name,x,z,layer,back=False,radius=.010):
    y=rear(x,z,layer) if back else front(x,z,layer)
    sign=1 if back else -1
    ellipsoid(name,(x,y+sign*.002,z),(radius,.0037,radius),MATS['gold'])
    points=[(x+radius*.72*math.sin(t),y+sign*.006,z+radius*.72*math.cos(t)) for t in np.linspace(0,2*PI,33)]
    tube(name+' engraved rim',points,.00065,MATS['gold'],6)
    ellipsoid(name+' inset',(x,y+sign*.0062,z),(radius*.30,.0006,radius*.30),MATS['gold'],16,8)

def shirt():
    shell('Shirt body',MATS['cotton'],.007,.300,.612)
    for sign in (-1,1):
        sleeve(sign,MATS['cotton'],.007,name='Shirt sleeve')
        obj,fn=sleeve(sign,MATS['cotton'],.009,.97,1.075,'Folded white cuff')
        for t in (0,.82):
            tube(f'Cuff seam {sign:+} {t}',[fn(t,v) for v in np.linspace(0,1,65)],.00055,MATS['cotton'])
    # Collar stand around the complete neck opening.
    shell('Shirt collar stand',MATS['cotton'],.011,.585,.620)
    for s in (-1,1):
        patch(f'Pointed white collar {s:+}',[(s*.012,.613),(s*.126,.603),(s*.095,.535),(s*.037,.563)],MATS['cotton'],.020,thickness=.003)
    patch('Shirt placket',[(-.014,.598),(.014,.598),(.014,.385),(-.014,.385)],MATS['cotton'],.012)
    for z in (.532,.493,.454):
        ellipsoid('Black shirt stud',(0,front(0,z,.015)-.002,z),(.0058,.003,.0058),MATS['pearl'],20,10)
    # Sculpted two-lobed bow with a pinched centre and a rounded outer edge.
    for s in (-1,1):
        def fn(u,v,s=s):
            x=s*(.012+.056*u);half=.012+.017*math.sin(u*PI/2)
            z=.574+(2*v-1)*half
            y=front(x,z,.035)-.008*math.sin(PI*u)*math.sin(PI*v)
            y+=.002*math.cos(v*PI*6)*(1-u)
            return (x,y,z)
        grid(f'Pinched satin bow wing {s:+}',fn,20,20,MATS['satin'],.006,(1,1))
    ellipsoid('Wrapped bow knot',(0,front(0,.574,.045),.574),(.016,.010,.023),MATS['satin'])

def waistcoat():
    def hem(theta):
        a=min(theta,2*PI-theta)
        return float(np.interp(a,[0,.25,.65,1.5,PI],[.267,.245,.280,.320,.270]))
    v_open=lambda z:.68*max(0,(z-.446)/(.605-.446))
    shell('V neck fitted waistcoat',MATS['damask'],.012,.26,.605,v_open,hem,(3,9))
    for s in (-1,1):
        points=[]
        for u in np.linspace(0,1,60):
            z=.267+(.605-.267)*u;theta=s*v_open(z)
            points.append(torso(theta,z,.014))
        tube('Waistcoat bound V edge',points,.0012,MATS['thread'])
    for z in (.397,.346,.291):button('Waistcoat gold button',.008,z,.018,radius=.0095)

def tailcoat():
    for s in (-1,1):
        def fn(u,v):
            base=.205+(PI-.205)*v
            hem=float(np.interp(base,[.205,.75,1.45,1.72,2.18,2.60,PI],
                                [.285,.195,.095,.090,.180,.270,.325]))
            top=.612-.020*math.sin(base)**2
            z=hem+(top-hem)*u
            theta=base+.37*u**2*(1-v)
            x,y,z=torso(s*theta,z,.020)
            # The paired tails flare very slightly instead of shrink-wrapping legs.
            y+=.007*(1-u)**2*max(0,-math.cos(theta))
            return (x,y,z)
        grid(f'Tailcoat tailored panel {s:+}',fn,32,52,MATS['wool'],.004,(3,6))
        tube(f'Coat front and tail bound edge {s:+}',[fn(0,v) for v in np.linspace(0,1,100)],.0015,MATS['thread'])
        tube(f'Coat opening bound edge {s:+}',[fn(u,0) for u in np.linspace(0,1,70)],.0013,MATS['thread'])
        sleeve(s,MATS['wool'],.016,0,.975,'Tailcoat sleeve')
        obj,sf=sleeve(s,MATS['wool'],.017,.93,.975,'Turned sleeve hem')
        tube(f'Sleeve hem stitch {s:+}',[sf(.65,v) for v in np.linspace(0,1,70)],.00065,MATS['thread'])
        pattern=[(.144,.614),(.225,.581),(.184,.553),(.202,.536),(.069,.287),(.103,.502)]
        patch(f'Notched satin lapel {s:+}',[(s*x,z) for x,z in pattern],MATS['satin'],.029,roll=.002,thickness=.0035)
        for z in (.370,.312):button('Tailcoat front gold button',s*.158,z,.029,radius=.014)
        # Narrow swallowtails hang underneath the wider side skirts. Separate
        # overlapping patterns avoid a zig-zag, cape-like continuous hem.
        tail=[(.010,.361),(.183,.355),(.171,.172),(.117,.025),(.058,.125),(.024,.238)]
        patch(f'Long pointed under-tail {s:+}',[(s*x,z) for x,z in tail],MATS['wool'],.016,thickness=.004,back=True)
    # Wide folded collar on the back, matching the reference's shoulder band.
    def collar(u,v):
        theta=.84+(2*PI-1.68)*v
        taper=math.sin(PI*v)**.22
        z=.619-.020*math.sin(theta)**2-(.053+.018*max(0,-math.cos(theta)))*u*taper
        return torso(theta,z,.025+.006*u*taper)
    grid('Broad folded back collar',collar,10,72,MATS['wool'],.005,(1,7))
    tube('Back collar turned edge',[collar(1,v) for v in np.linspace(0,1,120)],.0013,MATS['thread'])
    tube('Back center tailoring seam',[torso(PI,z,.023) for z in np.linspace(.325,.555,75)],.0009,MATS['thread'])
    for s in (-1,1):
        for z in (.445,.398,.351):button('Tailcoat back gold button',s*.078,z,.027,True,.0115)
        tube(f'Back panel seam {s:+}',[torso(PI+s*(.50+.16*(.5-z)),z,.023) for z in np.linspace(.34,.565,80)],.0007,MATS['thread'])
    # Breast pocket sewn onto the coat, with a separate replaceable white square.
    patch('Breast pocket welt',[(.156,.497),(.222,.508),(.225,.496),(.159,.485)],MATS['wool'],.032,thickness=.004)
    tube('Breast pocket welt top',[(x,front(x,.501,.036),.501+(x-.19)*.16) for x in np.linspace(.159,.222,24)],.001,MATS['thread'])

def pocket_square():
    patch('Triangular folded pocket square',[(.163,.498),(.196,.539),(.222,.507)],MATS['cotton'],.034,thickness=.002)
    tube('Pocket square folded hem',[(.164,front(.164,.498,.036),.498),(.196,front(.196,.539,.036),.539),(.222,front(.222,.507,.036),.507)],.00075,MATS['cotton'])

def apply_modifiers(obj):
    bpy.context.view_layer.objects.active=obj
    for mod in list(obj.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)

def export(path,objects):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,
        export_apply=True,export_extras=True,export_animations=False,export_lights=False,
        export_cameras=False,export_materials='EXPORT',export_image_format='AUTO')

def build():
    global CURRENT,BVH
    WORK.mkdir(exist_ok=True)
    source_hash=hashlib.sha256(BODY.read_bytes()).hexdigest()
    assert source_hash==BODY_SHA,'Wrong wearer: use the latest approved bare-shape GLB'
    # The body is loaded as a read-only fitting reference and excluded from exports.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(BODY),loglevel=40)
    body_objects=list(bpy.context.scene.objects)
    body=next(o for o in body_objects if o.name.startswith('tripo_node_'))
    BVH=BVHTree.FromPolygons([body.matrix_world@v.co for v in body.data.vertices],
                            [list(f.vertices) for f in body.data.polygons])
    body_fingerprint=hashlib.sha256(np.array([list(body.matrix_world@v.co) for v in body.data.vertices],dtype='<f4').tobytes()).hexdigest()
    make_materials();roots={}
    for name,fn in zip(GROUPS,(shirt,waistcoat,tailcoat,pocket_square)):
        CURRENT=group(name);roots[name]=CURRENT;fn()
    clothes=[o for o in bpy.context.scene.objects if o not in body_objects]
    for o in clothes:
        if o.type=='MESH':apply_modifiers(o)
    for o in body_objects:o.hide_render=True;o.hide_set(True)
    # Registration asset: one replaceable mesh, not four separate wardrobe items.
    bpy.ops.object.select_all(action='DESELECT')
    copies=[]
    for o in clothes:
        if o.type!='MESH':continue
        dup=o.copy();dup.data=o.data.copy();bpy.context.collection.objects.link(dup)
        dup.matrix_world=o.matrix_world.copy();dup.parent=None;dup.select_set(True);copies.append(dup)
    bpy.context.view_layer.objects.active=copies[0]
    bpy.ops.object.join();outfit=bpy.context.object;outfit.name='ButlerOutfit'
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    outfit['wardrobe_slot']='full_outfit';outfit['includes_towel']=False
    outfit['wearer_sha256']=source_hash
    outfit['fit_revision']='surface-fit-long-tailcoat'
    export(WORK/'musan-butler-outfit.glb',[outfit])
    outfit.hide_render=True;outfit.hide_set(True)
    assert hashlib.sha256(BODY.read_bytes()).hexdigest()==source_hash
    assert hashlib.sha256(np.array([list(body.matrix_world@v.co) for v in body.data.vertices],dtype='<f4').tobytes()).hexdigest()==body_fingerprint
    manifest={'body_glb_sha256':source_hash,'body_file_unchanged':True,'body_mesh_unchanged':True,
              'clothing_only':True,'authored_components':list(GROUPS),'runtime_parts':['ButlerOutfit'],
              'towel_included':False,'static_pose_only':True,
              'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in WORK.glob('*.glb')}}
    (WORK/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    bpy.ops.wm.save_as_mainfile(filepath=str(WORK/'outfit-authoring.blend'))
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':build()
