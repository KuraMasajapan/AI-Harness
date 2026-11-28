"""Repair the scanned body's seams, transfer its surface data and reattach fur."""
import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from model import positions


def ease(t):
    t=np.clip(t,0,1);return t*t*(3-2*t)


def polish_torso(points,triangles):
    """Remove fitting rings with a volume-preserving Taubin surface filter."""
    edges=np.unique(np.sort(np.concatenate((triangles[:,[0,1]],triangles[:,[1,2]],triangles[:,[2,0]])),axis=1),axis=0)
    src=np.concatenate((edges[:,0],edges[:,1]));dst=np.concatenate((edges[:,1],edges[:,0]))
    degree=np.maximum(np.bincount(src,minlength=len(points)),1)
    weight=ease((points[:,2]-.08)/.08)*ease((.50-points[:,2])/.18)*ease((.34-abs(points[:,0]))/.07)
    for _ in range(150):
        for step in (.5,-.53):
            mean=np.stack([np.bincount(src,weights=points[dst,axis],minlength=len(points))/degree for axis in range(3)],axis=1)
            points+=(mean-points)*(step*weight[:,None])
    # Fill the broad generated tail scar to the torso's convex envelope.
    # Unlike an arbitrary fitted patch, the envelope meets the old surface at
    # zero displacement and cannot introduce a new inward seam around its edge.
    selected=(abs(points[:,0])<.30)&(points[:,2]>.08)&(points[:,2]<.60)
    hull=bmesh.new()
    for point in points[selected]:hull.verts.new(Vector(point))
    bmesh.ops.convex_hull(hull,input=list(hull.verts),use_existing_faces=False)
    hull.normal_update();tree=BVHTree.FromBMesh(hull);hull.free()
    blend=.995*ease((points[:,1]-.08)/.06)*ease((points[:,2]-.12)/.05)*ease((.52-points[:,2])/.10)*ease((.28-abs(points[:,0]))/.05)
    for index in np.flatnonzero(blend):
        point=points[index];hit,_,_,_=tree.ray_cast(Vector((float(point[0]),2,float(point[2]))),Vector((0,-1,0)))
        if hit is not None:points[index,1]+=max(float(hit.y)-point[1],0)*blend[index]
    # Fair the envelope/contact boundary too; otherwise a convex-hull facet
    # can replace the old scar with another visible shading crease.
    for _ in range(80):
        mean=np.stack([np.bincount(src,weights=points[dst,axis],minlength=len(points))/degree for axis in range(3)],axis=1)
        points+=(mean-points)*(.4*blend[:,None])


def preserve_face_rim(points,triangles,face_material,source_points,source_skin):
    """Constrain the remeshed material edge to the original smooth face outline."""
    vertices=source_points[np.unique(source_skin)]
    order=sorted(range(len(vertices)),key=lambda i:(vertices[i,0],vertices[i,2]))
    def turn(a,b,c):
        u=vertices[b,[0,2]]-vertices[a,[0,2]];v=vertices[c,[0,2]]-vertices[a,[0,2]]
        return u[0]*v[1]-u[1]*v[0]
    chains=[]
    for indices in (order,list(reversed(order))):
        chain=[]
        for index in indices:
            while len(chain)>1 and turn(chain[-2],chain[-1],index)<=0:chain.pop()
            chain.append(index)
        chains.extend(chain[:-1])
    hull=vertices[chains];a=hull;b=np.roll(hull,-1,axis=0);direction=b-a
    edge_rows=np.sort(np.concatenate((triangles[:,[0,1]],triangles[:,[1,2]],triangles[:,[2,0]])),axis=1)
    edges,inverse=np.unique(edge_rows,axis=0,return_inverse=True)
    lo=np.full(len(edges),2);hi=np.full(len(edges),-1)
    np.minimum.at(lo,inverse,np.tile(face_material,3));np.maximum.at(hi,inverse,np.tile(face_material,3))
    border=np.unique(edges[lo!=hi])
    for index in border:
        t=np.clip(np.einsum('ij,ij->i',points[index]-a,direction)/np.einsum('ij,ij->i',direction,direction),0,1)
        closest=a+t[:,None]*direction
        points[index]=closest[np.argmin(np.linalg.norm(closest-points[index],axis=1))]
    return len(border)


def nearest(tree,points,triangles):
    hits=[tree.find_nearest(Vector(point)) for point in points]
    co=np.array([hit[0][:] for hit in hits]);normal=np.array([hit[1][:] for hit in hits])
    index=np.array([hit[2] for hit in hits]);tri=triangles[index]
    a=tri[:,1]-tri[:,0];b=tri[:,2]-tri[:,0];c=co-tri[:,0]
    aa=np.einsum('ij,ij->i',a,a);ab=np.einsum('ij,ij->i',a,b);bb=np.einsum('ij,ij->i',b,b)
    ca=np.einsum('ij,ij->i',c,a);cb=np.einsum('ij,ij->i',c,b);denom=aa*bb-ab*ab
    u=(bb*ca-ab*cb)/denom;v=(aa*cb-ab*ca)/denom
    return co,normal,index,np.stack((1-u-v,u,v),axis=1)


def reattach_fur(fur,source_tree,source_triangles,target_tree,target_triangles,guide_tree,guide_initial,guide_final):
    hp=positions(fur).astype(float)
    faces=np.array([list(face.vertices) for face in fur.data.polygons])
    _,canonical=np.unique(np.round(hp/1e-7).astype(np.int64),axis=0,return_inverse=True)
    edges=canonical[np.concatenate((faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]))]
    labels=np.arange(canonical.max()+1)
    for _ in range(32):
        previous=labels.copy()
        np.minimum.at(labels,edges[:,0],labels[edges[:,1]])
        np.minimum.at(labels,edges[:,1],labels[edges[:,0]])
        labels=labels[labels]
        if np.array_equal(labels,previous):break
    _,component=np.unique(labels[canonical],return_inverse=True)
    count=np.bincount(component);n=len(count)
    assert 1000<n<30000,('Unexpected fibre components',n)
    centers=np.stack([np.bincount(component,weights=hp[:,axis])/count for axis in range(3)],axis=1)
    source_point,source_normal,_,_=nearest(source_tree,centers,source_triangles)
    _,_,guide_face,bary=nearest(guide_tree,source_point,guide_initial)
    transported=np.einsum('ni,nij->nj',bary,guide_final[guide_face])
    target_point,target_normal,_,_=nearest(target_tree,transported,target_triangles)
    v=np.cross(source_normal,target_normal);c=np.einsum('ij,ij->i',source_normal,target_normal)
    k=np.zeros((n,3,3));k[:,0,1]=-v[:,2];k[:,0,2]=v[:,1];k[:,1,0]=v[:,2]
    k[:,1,2]=-v[:,0];k[:,2,0]=-v[:,1];k[:,2,1]=v[:,0]
    rotation=np.eye(3)+k+k@k/np.maximum(1+c,1e-8)[:,None,None]
    opposite=c<-.9999
    if opposite.any():
        axis=np.cross(source_normal[opposite],np.array([1.,0,0]))
        weak=np.linalg.norm(axis,axis=1)<.01
        axis[weak]=np.cross(source_normal[opposite][weak],np.array([0.,1,0]))
        axis/=np.linalg.norm(axis,axis=1)[:,None]
        rotation[opposite]=2*np.einsum('ni,nj->nij',axis,axis)-np.eye(3)
    q=target_point[component]+np.einsum('nij,nj->ni',rotation[component],hp-source_point[component])
    loop_vertices=np.array([loop.vertex_index for loop in fur.data.loops])
    normals=np.array([normal.vector[:] for normal in fur.data.corner_normals])
    normals=np.einsum('nij,nj->ni',rotation[component[loop_vertices]],normals)
    fur.data.vertices.foreach_set('co',q.astype(np.float32).ravel());fur.data.update()
    fur.data.normals_split_custom_set(normals.tolist())
    return n


def repair_body(base,fur):
    old=base.data;p=positions(base).astype(float)
    triangles=np.array([list(face.vertices) for face in old.polygons])
    source_triangles=p[triangles]
    source_tree=BVHTree.FromPolygons([Vector(co) for co in p],triangles,all_triangles=True)
    uv=np.array([loop.uv[:] for loop in old.uv_layers.active.data]).reshape(-1,3,2)
    color=np.array([entry.color[:] for entry in old.color_attributes['Color'].data]).reshape(-1,3,4)
    material=np.array([face.material_index for face in old.polygons]);materials=list(old.materials)
    original_vertices=len(p);original_faces=len(triangles)
    bpy.context.view_layer.objects.active=base
    bpy.ops.object.select_all(action='DESELECT');base.select_set(True)
    base.data.remesh_voxel_size=.007
    bpy.ops.object.voxel_remesh()
    bm=bmesh.new();bm.from_mesh(base.data);bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bm.to_mesh(base.data);bm.free()
    mesh=base.data;q=positions(base).astype(float)
    tri=np.array([list(face.vertices) for face in mesh.polygons])
    guide_initial=q[tri].copy()
    guide_tree=BVHTree.FromPolygons([Vector(co) for co in q],tri,all_triangles=True)
    edges=np.unique(np.sort(np.concatenate((tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]])),axis=1),axis=0)
    src=np.concatenate((edges[:,0],edges[:,1]));dst=np.concatenate((edges[:,1],edges[:,0]))
    degree=np.maximum(np.bincount(src,minlength=len(q)),1)
    weight=ease((q[:,1]-.11)/.08)*ease((.44-q[:,2])/.14)*ease((.31-abs(q[:,0]))/.10)
    front=.35*ease((-q[:,1]-.11)/.08)*ease((.34-q[:,2])/.12)*ease((q[:,2]-.10)/.10)*ease((.31-abs(q[:,0]))/.10)
    weight=np.maximum(weight,front)
    for _ in range(500):
        average=np.stack([np.bincount(src,weights=q[dst,axis],minlength=len(q))/degree for axis in range(3)],axis=1)
        q+=(average-q)*(.55*weight[:,None])
    q[:,2]=(q[:,2]-q[:,2].min())/np.ptp(q[:,2])
    guide_final=q[tri].copy()
    mesh.vertices.foreach_set('co',q.astype(np.float32).ravel());mesh.update()
    modifier=base.modifiers.new('Keep original mobile triangle budget','DECIMATE')
    modifier.ratio=.48
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    mesh=base.data;q=positions(base).astype(float)
    tri=np.array([list(face.vertices) for face in mesh.polygons])
    _,_,source_face,_=nearest(source_tree,q[tri].mean(axis=1),source_triangles)
    face_material=material[source_face]
    assert len(face_material)==len(mesh.polygons)
    assert np.all(q[tri[face_material==0],2]>.58),'Face material must remain on the face'
    rim_vertices=preserve_face_rim(q,tri,face_material,p,triangles[material==0])
    mesh.vertices.foreach_set('co',q.astype(np.float32).ravel());mesh.update()
    # A source-face projection keeps the existing paint, UVs and material slots.
    _,_,source_face,bary=nearest(source_tree,q,source_triangles)
    new_uv=np.einsum('ni,nij->nj',bary,uv[source_face])
    new_color=np.einsum('ni,nij->nj',bary,color[source_face])
    while mesh.uv_layers:mesh.uv_layers.remove(mesh.uv_layers[0])
    while mesh.color_attributes:mesh.color_attributes.remove(mesh.color_attributes[0])
    mesh.uv_layers.new(name='UVMap')
    mesh.color_attributes.new(name='Color',type='BYTE_COLOR',domain='CORNER')
    # Adding CustomData layers can invalidate earlier RNA layer handles.
    uv_layer=mesh.uv_layers['UVMap'];color_layer=mesh.color_attributes['Color']
    loops=np.array([loop.vertex_index for loop in mesh.loops])
    uv_layer.data.foreach_set('uv',new_uv[loops].astype(np.float32).ravel())
    color_layer.data.foreach_set('color',new_color[loops].astype(np.float32).ravel())
    mesh.color_attributes.active_color_name='Color'
    mesh.color_attributes.active_color_index=0
    mesh.color_attributes.render_color_index=0
    mesh.materials.clear()
    for value in materials:mesh.materials.append(value)
    for face,index in zip(mesh.polygons,face_material):face.material_index=int(index);face.use_smooth=True
    target_tree=BVHTree.FromPolygons([Vector(co) for co in q],tri,all_triangles=True)
    strands=reattach_fur(fur,source_tree,source_triangles,target_tree,q[tri],guide_tree,guide_initial,guide_final)
    return {'source_vertices':original_vertices,'source_faces':original_faces,
            'repaired_vertices':len(q),'repaired_faces':len(tri),'voxel_size':.007,
            'fairing_iterations':500,'rigidly_reattached_fibres':strands,'face_rim_vertices':rim_vertices,
            'continuous_fibre_transport':True,'existing_materials_reused':True,'source_uv_and_color_transferred':True}
