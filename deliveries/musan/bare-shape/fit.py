"""Continuous, UV-preserving cage deformation; no primitive replacement mesh."""
import json
import hashlib
import numpy as np
import bpy
from model import ROOT,WORK,load_original,positions,export,render

def smooth(values,window=21):
    return np.convolve(np.pad(values,(window//2,window//2),mode='edge'),np.ones(window)/window,'valid')

def interp(x,xp,fp):
    """C1 monotone Hermite interpolation, avoiding profile overshoot."""
    x=np.clip(x,xp[0],xp[-1]);i=np.clip(np.searchsorted(xp,x)-1,0,len(xp)-2)
    spans=np.diff(xp);d=np.diff(fp)/spans;m=np.zeros(len(fp))
    m[0]=d[0];m[-1]=d[-1];same=d[:-1]*d[1:]>0
    w1=2*spans[1:]+spans[:-1];w2=spans[1:]+2*spans[:-1]
    m[1:-1][same]=(w1[same]+w2[same])/(w1[same]/d[:-1][same]+w2[same]/d[1:][same])
    h=xp[i+1]-xp[i];t=(x-xp[i])/h
    return (2*t**3-3*t*t+1)*fp[i]+(-2*t**3+3*t*t)*fp[i+1]+h*((t**3-2*t*t+t)*m[i]+(t**3-t*t)*m[i+1])

def sample(profile,z,column):
    a=np.asarray(profile);a=a[np.argsort(a[:,0])]
    return np.interp(z,a[:,0],a[:,column])

def ease(t):
    t=np.clip(t,0,1);return t*t*(3-2*t)

def pre_shape(p):
    p=np.array(p,dtype=float,copy=True)
    # Lift the generated under-belly overhang without moving the short feet.
    # Its rear lump otherwise reads as a third foot in the side view.
    p[:,2]+=.04*ease((-p[:,1]-.115)/.07)*(1-ease((p[:,2]-.11)/.12))
    # The face in the sheet is slightly shorter and squarer, not a new head.
    w=ease((-p[:,1]-.07)/.08)*ease((p[:,2]-.54)/.10)*ease((1-p[:,2])/.075)
    p[:,2]+=w*(.769+(p[:,2]-.7665)*.94-p[:,2])
    return p

def setup(base):
    target=json.loads((ROOT/'shape-target.json').read_text())
    p=pre_shape(positions(base));z=np.linspace(0,1,201)
    low=[];high=[]
    for height in z:
        q=p[np.abs(p[:,2]-height)<.006]
        if len(q)<8:q=p[np.argsort(abs(p[:,2]-height))[:12]]
        low.append(q.min(axis=0));high.append(q.max(axis=0))
    low=np.asarray(low);high=np.asarray(high)
    # Front/back sheets differ by around 2%; fit their symmetric consensus.
    widths=[(sample(target[v]['profiles'],z,2)-sample(target[v]['profiles'],z,1))/2 for v in ['front','back']]
    tx=(widths[0]+widths[1])/2
    sx=(high[:,0]-low[:,0])/2;cx=(high[:,0]+low[:,0])/2
    side=target['side']['profiles'];ty0=-sample(side,z,2);ty1=-sample(side,z,1)
    sy=high[:,1]-low[:,1]
    fields={'z':z,'x_scale':smooth(np.clip(tx/np.maximum(sx,.015),.82,1.12)),
            'x_center':smooth(cx),'y_scale':smooth(np.clip((ty1-ty0)/np.maximum(sy,.015),.30,1.35),9),
            'y_source_center':smooth((low[:,1]+high[:,1])/2,9),
            'y_target_center':smooth((ty0+ty1)/2,9),'source_outer':smooth(sx)}
    # Measure the torso run between the arms separately, avoiding a balloon-like belly.
    from PIL import Image,ImageFilter
    mask=np.asarray(Image.open(WORK/'baseline/front.png').getchannel('A').filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)))>128
    yy,xx=np.where(mask);top,bottom=yy.min(),yy.max();height=bottom-top;center=round((xx.min()+xx.max())/2)
    core=[]
    for y in range(top,bottom+1):
        row=mask[y]
        if not row[center]:continue
        left=right=center
        while left>0 and row[left-1]:left-=1
        while right+1<len(row) and row[right+1]:right+=1
        core.append([(bottom-y)/height,(right-left)/height/2])
    sc=sample(core,z,1)
    tc=(sample(target['front']['core_profile'],z,1)+sample(target['back']['core_profile'],z,1))/2
    weight=ease((z-.13)/.035)*ease((.54-z)/.055)
    fields['source_core']=smooth(sc)
    fields['core_delta']=smooth(np.clip(tc-sc*fields['x_scale'],-.035,.035)*weight)
    # Sparse cage controls prevent row-level tracing noise becoming sculpted rings.
    controls=np.unique(np.r_[np.linspace(0,1,21),.025,.075,.125,.175,.225,.925,.975])
    for key in list(fields):
        if key!='z':fields[key]=np.interp(controls,z,fields[key])
    fields['z']=controls
    fields['core_delta']*=.25
    return fields

def warp(p,f):
    p=pre_shape(p);z=p[:,2]
    val=lambda key:interp(z,f['z'],f[key])
    x=p[:,0]-val('x_center');ax=abs(x);core=np.maximum(val('source_core'),.025)
    outer=np.maximum(val('source_outer'),core+.02)
    inner_weight=np.sin(np.minimum(ax/core,1)*np.pi/2)
    outer_weight=np.cos(np.clip((ax-core)/(outer-core),0,1)*np.pi/2)
    weight=np.where(ax<=core,inner_weight,outer_weight)
    p[:,0]=x*val('x_scale')+np.sign(x)*weight*val('core_delta')
    p[:,1]=(p[:,1]-val('y_source_center'))*val('y_scale')+val('y_target_center')
    return p

def fingerprint(obj):
    m=obj.data;result={}
    for layer in m.uv_layers:
        a=np.empty(len(layer.data)*2,dtype=np.float32);layer.data.foreach_get('uv',a)
        result['uv:'+layer.name]=hashlib.sha256(a.tobytes()).hexdigest()
    for layer in m.color_attributes:
        a=np.empty(len(layer.data)*4,dtype=np.float32);layer.data.foreach_get('color',a)
        result['color:'+layer.name]=hashlib.sha256(a.tobytes()).hexdigest()
    result['polygons']=len(m.polygons);result['vertices']=len(m.vertices)
    return result

def fit():
    objs=load_original();base=next(o for o in objs if o.name.startswith('tripo_node_'))
    original={o.name:fingerprint(o) for o in objs}
    from retopo import repair_body
    sculpt=repair_body(base,next(o for o in objs if o.name=='Short plush silhouette fibres'))
    assert all(fingerprint(o)==original[o.name] for o in objs if o!=base)
    (WORK/'sculpt-preservation.json').write_text(json.dumps(sculpt,indent=2))
    fields=setup(base);checks={}
    objs.sort(key=lambda obj:0 if obj==base else 1)
    for obj in objs:
        before=fingerprint(obj);p=positions(obj).astype(float)
        q=warp(p,fields)
        if obj.name.startswith('Black button eye') or obj.name=='Small smile':
            old=p.mean(axis=0);center=warp(old[None,:],fields)[0]
            if obj.name.startswith('Black button eye'):
                center[0]=np.sign(old[0])*.0987;center[2]=.7669
                scale=np.array([.887,.9,.88])
            else:
                center[0]=0;center[2]=.7243;scale=np.array([.98,1,1.15])
            q=(p-old)*scale+center
            # Seat unchanged glossy eyes/smile on the deformed face surface.
            inverse=base.matrix_world.inverted()
            from mathutils import Vector
            ok,point,_,_=base.ray_cast(inverse@Vector((float(center[0]),-1,float(center[2]))),Vector((0,1,0)))
            if ok:
                front=(base.matrix_world@point).y
                q[:,1]+=front+(.007 if obj.name.startswith('Black button eye') else -.001)-center[1]
        # Preserve custom shading normals under the deformation's local Jacobian.
        normals=np.array([n.vector[:] for n in obj.data.corner_normals],dtype=float)
        loop_indices=np.array([loop.vertex_index for loop in obj.data.loops])
        if obj==base or obj.name=='Short plush silhouette fibres':
            lp=p[loop_indices];jac=np.empty((len(lp),3,3));eps=.0002
            for axis in range(3):
                offset=np.zeros(3);offset[axis]=eps
                jac[:,:,axis]=(warp(lp+offset,fields)-warp(lp-offset,fields))/(2*eps)
            det=np.linalg.det(jac)
            assert np.all(det>0),f'Folded cage on {obj.name}: {det.min()}'
            normals=np.einsum('nij,nj->ni',np.linalg.inv(jac).transpose(0,2,1),normals)
            normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
        obj.data.vertices.foreach_set('co',q.astype(np.float32).ravel())
        obj.data.update()
        obj.data.normals_split_custom_set(normals.tolist())
        if obj==base:bpy.context.view_layer.update()
        assert fingerprint(obj)==before
        checks[obj.name]={'preserved_uv_colors_topology':True,**before}
    # Finish the torso after profile fitting, so fitting cannot reintroduce rings.
    from retopo import polish_torso,reattach_fur,BVHTree,Vector
    before=positions(base).astype(float);after=before.copy()
    triangles=np.array([list(face.vertices) for face in base.data.polygons])
    polish_torso(after,triangles)
    source_tree=BVHTree.FromPolygons([Vector(co) for co in before],triangles,all_triangles=True)
    target_tree=BVHTree.FromPolygons([Vector(co) for co in after],triangles,all_triangles=True)
    reattach_fur(next(o for o in objs if o.name=='Short plush silhouette fibres'),
                 source_tree,before[triangles],target_tree,after[triangles],source_tree,before[triangles],after[triangles])
    base.data.vertices.foreach_set('co',after.astype(np.float32).ravel());base.data.update()
    base.data.normals_split_custom_set([(0,0,0)]*len(base.data.loops))
    assert all(fingerprint(o)=={k:v for k,v in checks[o.name].items() if k!='preserved_uv_colors_topology'} for o in objs)
    sculpt['post_fit_taubin_iterations']=150
    sculpt['rear_crease_patch']=True
    sculpt['rear_contact_fairing_iterations']=80
    (WORK/'sculpt-preservation.json').write_text(json.dumps(sculpt,indent=2))
    export(WORK/'musan-bare-shape.glb')
    (WORK/'shape-preservation.json').write_text(json.dumps(checks,indent=2))
    (WORK/'deformation-fields.json').write_text(json.dumps({k:v.tolist() for k,v in fields.items()},indent=2))
    names=['musan-bare-shape.glb','shape-preservation.json','sculpt-preservation.json','deformation-fields.json']
    (WORK/'build-manifest.json').write_text(json.dumps({name:hashlib.sha256((WORK/name).read_bytes()).hexdigest() for name in names},indent=2))

if __name__=='__main__':
    fit();render(WORK/'musan-bare-shape.glb','fitted')
