"""Read-only checks on the saved bench, its approved envelope and front-row context."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy
import numpy as np
from mathutils.bvhtree import BVHTree

sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
sys.path[:0]=[str(D),str(D.parent/"R5-B")]
from check import border_mates
from tailor import DETAIL, FORM_HASH, GUIDES, HIDE_FILE, HIDE_HASH, ROOT, TAILOR, THREAD
from leather import FINISH, MARGIN, PATTERN
sys.path.insert(0,str(D.parent/"R6-A"))
from review import context
from bench import PRIMARY


def snapshot(objects):
    dg=bpy.context.evaluated_depsgraph_get()
    boxes, hashes = {},{}
    for ob in objects:
        ev=ob.evaluated_get(dg)
        mesh=ev.to_mesh()
        try:
            mesh.calc_loop_triangles()
            pts=np.empty(3*len(mesh.vertices),np.float32)
            mesh.vertices.foreach_get("co",pts)
            mat=np.array(ev.matrix_world)
            pts=pts.reshape(-1,3)@mat[:3,:3].T+mat[:3,3]
            idx=np.empty(3*len(mesh.loop_triangles),np.int32)
            mesh.loop_triangles.foreach_get("vertices",idx)
            boxes[ob.name]=np.stack((pts.min(axis=0),pts.max(axis=0)))
            hashes[ob.name]=sha256(pts.tobytes()+idx.tobytes()).hexdigest()
        finally:
            ev.to_mesh_clear()
    return boxes,hashes


def bounds(boxes):
    v=np.concatenate(list(boxes.values()))
    return np.stack((v.min(axis=0),v.max(axis=0)))


def crest_height(tag, obj):
    x={"LH":-.442,"centre":0.,"RH":.442}[tag]
    # Same world-space sample on each front roll; cushion vertices are in cabin space.
    assert obj.matrix_world.is_identity
    tree=BVHTree.FromObject(obj,bpy.context.evaluated_depsgraph_get())
    point=tree.ray_cast((x,.792,2),(0,0,-1))[0]
    assert point is not None
    return point.z


def controls(root):
    allowed={}
    for tag in ("LH","RH"):
        for name,role in [(tag+" back • shoulder yoke","Yoke"),(tag+" pan • squab insert","Waterfall"),
                          *((tag+f" back • lumbar pad {i}","Lumbar") for i in (1,2,3))]:
            allowed[name]=f"Rear • {tag} {role}"
    controls={}
    for name,material in allowed.items():
        mesh=root.all_objects[name].data
        assert mesh.materials[0].name==material and len(mesh.uv_layers[PATTERN].data)==len(mesh.loops)
        margin=np.empty(len(mesh.vertices),np.float32)
        mesh.attributes[MARGIN].data.foreach_get("value",margin)
        assert np.min(margin)==0 and np.max(margin)>.025
        uv=np.empty(2*len(mesh.loops),np.float32)
        mesh.uv_layers[PATTERN].data.foreach_get("uv",uv)
        assert np.isfinite(uv).all() and np.all(np.ptp(uv.reshape(-1,2),axis=0)>.07)
        group=mesh.materials[0].node_tree.nodes[FINISH]
        assert group.node_tree.name=="AUTOLAB • refined cognac hide"
        assert abs(group.inputs["Pitch (m)"].default_value-.004)<1e-8
        controls[material]=group.inputs["Perforation"]
    assert len(controls)==6 and all(v.default_value==1 for v in controls.values())
    for name,socket in controls.items():
        socket.default_value=0
        assert all(s.default_value==float(k!=name) for k,s in controls.items())
        socket.default_value=1
    for ob in root.all_objects:
        for slot in ob.material_slots:
            mat=slot.material
            group=mat.node_tree.nodes.get(FINISH) if mat.node_tree else None
            if group and group.inputs["Perforation"].default_value:
                assert allowed.get(ob.name)==mat.name


def thread_fit(detail):
    dg=bpy.context.evaluated_depsgraph_get()
    max_dist=0
    count=0
    for ob in detail.objects:
        owner=bpy.data.objects[ob["fitted_to"]]
        assert ob.type=="CURVE" and ob.data.materials[0].name==THREAD
        assert ob.data.bevel_depth>0 and len(ob.data.splines)>0
        transform=owner.matrix_world.inverted()@ob.matrix_world
        tree=BVHTree.FromObject(owner,dg)
        # One midpoint per individual stitch, in the owner's local metre frame.
        for seg in ob.data.splines:
            pt=transform@seg.points[len(seg.points)//2].co.to_3d()
            max_dist=max(max_dist,tree.find_nearest(pt)[3])
            count+=1
    assert max_dist<.001, max_dist
    return count,round(max_dist*1000,3)


def run(out):
    base=D.parent/"R6-A/R6-A-rear-bench.blend"
    if out.exists() or sha256(base.read_bytes()).hexdigest()!=FORM_HASH or sha256(HIDE_FILE.read_bytes()).hexdigest()!=HIDE_HASH:
        raise ValueError("Use an unused report and approved sources")
    master=bpy.data.filepath
    bpy.ops.wm.open_mainfile(filepath=str(base))
    old,digests=snapshot(bpy.data.collections[ROOT].all_objects)
    tags=("LH","centre","RH")
    crests={tag:crest_height(tag,bpy.data.objects["Cushion • "+tag]) for tag in tags}
    bpy.ops.wm.open_mainfile(filepath=master)
    root=bpy.data.collections[ROOT]
    panels=bpy.data.collections[TAILOR]
    details=bpy.data.collections[DETAIL]
    guides=bpy.data.collections[GUIDES]
    assert guides.hide_render and guides.hide_viewport and len(guides.objects)==5
    assert bytes(bpy.data.images[PRIMARY.name].packed_file.data)==PRIMARY.read_bytes()
    groups={key:[o for o in panels.objects if o["source_form"]==key] for key in guides.objects.keys()}
    assert sorted(map(len,groups.values()))==[6,6,6,13,13]
    assert len(set(o.data.name for o in panels.objects))==len(panels.objects)
    edges=0
    for name,group in groups.items():
        unmatched,total=border_mates(group)
        assert unmatched==0,(name,unmatched)
        edges+=total
    new,current=snapshot(root.all_objects)
    for tag in tags:
        name="plain saddle" if tag=="centre" else "squab insert"
        height=crest_height(tag,bpy.data.objects[tag+" pan • "+name])
        crests[tag]=round(1000*(crests[tag]-height),2)
        assert 3<crests[tag]<15,(tag,crests[tag])
    unchanged=set(old)-set(groups)-{"Centre • armrest pull","Centre • stowed armrest"}
    assert all(digests[n]==current[n] for n in unchanged)
    delta=(bounds(new)-bounds(old))*1000
    assert np.max(np.abs(delta))<3,delta
    leaf=bpy.data.objects["Centre • stowed armrest"]
    assert bpy.data.objects["Centre • armrest pull"].parent==leaf
    assert bpy.data.objects[leaf.name+" • topstitch"].parent==leaf
    controls(root)
    threads,max_dist=thread_fit(details)

    dg=bpy.context.evaluated_depsgraph_get()
    # All release buttons and the new panel meshes have identity world transforms.
    for i in range(1,4):
        button=bpy.data.objects[f"Release • {i}"]
        tree=BVHTree.FromObject(button,dg)
        for panel in panels.objects:
            assert button.matrix_world==panel.matrix_world
            if np.all(new[button.name][0]<=new[panel.name][1]) and np.all(new[button.name][1]>=new[panel.name][0]):
                assert not tree.overlap(BVHTree.FromObject(panel,dg)),(button.name,panel.name)
    pair,cockpit=context()
    gaps={}
    assert len(pair.children)==2
    for coll in (*pair.children,cockpit):
        gap=bounds(new)[0,1]-bounds(snapshot(coll.all_objects)[0])[1,1]
        assert gap>0
        gaps[coll.name]=round(float(gap)*1000,2)
    report={"passed":True,"formSHA256":FORM_HASH,"leatherSourceSHA256":HIDE_HASH,
            "separateCoverPieces":len(panels.objects),"directedPairedBoundaryEdges":edges,
            "unchangedEvaluatedMeshes":len(unchanged),"perforationControls":6,
            "threadObjects":len(details.objects),"separateStitches":threads,"maxThreadMidpointGapMM":max_dist,
            "envelopeDeltaMinMaxXYZmm":delta.astype(float).round(3).tolist(),"clearBuckleReleaseFaces":3,
            "cushionFrontCentreLoweringAtY792mm":crests,
            "evaluatedGeometrySHA256":sha256(json.dumps(current,sort_keys=True).encode()).hexdigest(),
            "foreAftEnvelopeGapMM":gaps,
            "scope":"Static geometry and material controls, not visual acceptance, working mechanisms or installed fit."}
    out.write_text(json.dumps(report,indent=2)+"\n")
    print(report)


if __name__=="__main__":
    run(Path(sys.argv[sys.argv.index("--")+1]))
