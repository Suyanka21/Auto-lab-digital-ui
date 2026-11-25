"""Fresh-open structural checks against the approved R5-B, not a realism score."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy
import numpy as np

D = Path(__file__).resolve().parent
sys.path.insert(0,str(D))
from form import BASE, PANELS, grid, normals, read_co
from leather import FINISH, MARGIN, PATTERN
from build import DETAIL

ROOT = "R5_FRONT_SEAT_MASTER"
LUMBAR = "Back • drawn lumbar insert"
MODIFIED = {LUMBAR,"Back • outboard bolster","Back • inboard bolster","Cushion • centre waterfall"}


def snapshot():
    dg = bpy.context.evaluated_depsgraph_get()
    geometry, topology, boundaries, extents = {}, {}, {}, []
    tris = 0
    for ob in bpy.data.collections[ROOT].all_objects:
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        try:
            me.calc_loop_triangles()
            xyz = read_co(me.vertices)
            assert np.isfinite(xyz).all()
            transform = np.asarray(ev.matrix_world)
            world = xyz@transform[:3,:3].T+transform[:3,3]
            idx = np.empty(len(me.loop_triangles)*3, np.int32)
            me.loop_triangles.foreach_get("vertices",idx)
            geometry[ob.name] = sha256(world.tobytes()+idx.tobytes()).hexdigest()
            extents.append((world.min(axis=0),world.max(axis=0)))
            tris += len(idx)//3
            if ob.get("editable_region"):
                topology[ob.name] = (len(xyz),sha256(idx.tobytes()).hexdigest())
                # Use the source loops: triangulation diagonals aren't cut edges.
                counts = np.zeros(len(ob.data.edges), dtype=np.int32)
                for loop in ob.data.loops:
                    counts[loop.edge_index] += 1
                edge_ids = np.flatnonzero(counts == 1)
                seam = sorted({v for i in edge_ids for v in ob.data.edges[int(i)].vertices})
                boundaries[ob.name] = sha256(world[seam].tobytes()).hexdigest()
        finally:
            ev.to_mesh_clear()
    ext = np.asarray(extents)
    return geometry,topology,boundaries,(ext[:,0].min(axis=0),ext[:,1].max(axis=0)),tris


def run(base, report):
    if report.exists() or sha256(base.read_bytes()).hexdigest()!=BASE:
        raise ValueError("Require the approved B and an unused report path")
    new,top,cuts,bounds,tris = snapshot()
    covers = bpy.data.collections[PANELS]
    punched, finish_ids = [], set()
    for ob in covers.objects:
        n = ob.data.materials[0].node_tree.nodes[FINISH]
        if n.inputs["Perforation"].default_value:
            assert n.inputs["Perforation"].default_value == 1.
            punched.append(ob["editable_region"])
            finish_ids.add(ob.data.materials[0].name)
            uv = np.array([tuple(v.uv) for v in ob.data.uv_layers[PATTERN].data])
            assert np.isfinite(uv).all() and min(np.ptp(uv,axis=0))>.15
            margins = [s.value for s in ob.data.attributes[MARGIN].data]
            assert min(margins) == 0. and max(margins) > .05
    key = bpy.data.objects[LUMBAR].data.shape_keys.key_blocks["Drawn lumbar channels"]
    assert key.value == 1
    ob = bpy.data.objects[LUMBAR]
    plain,_ = grid(ob)
    draw,_ = grid(ob,shaped=True)
    signed = ((draw-plain)*normals(plain)).sum(axis=-1)
    nrows = len(signed)
    valleys = [int(np.sum((r[1:-1]<r[2:])&(r[1:-1]<r[:-2])&(r[1:-1]<-.003)))
               for r in signed[[nrows//4,nrows//2,3*nrows//4]]]
    key.value = 0
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    assert np.array_equal(read_co(ev.data.vertices),plain.reshape(-1,3))
    key.value = 1
    details = bpy.data.collections[DETAIL]
    stitches = sum(len(o.data.splines) for o in details.objects)
    assert all(o.type=="CURVE" and o.get("fitted_to") for o in details.objects)
    bpy.ops.wm.open_mainfile(filepath=str(base.resolve()))
    old,oldtop,oldcuts,oldbounds,_ = snapshot()
    changed = {n for n in old if old[n] != new.get(n)}
    # Quads can be tessellated along a different diagonal after sculpting;
    # verify actual saved polygon loops, not a renderer's triangle choice.
    source_faces = lambda: {o.name: sha256(np.asarray(
        [l.vertex_index for l in o.data.loops], dtype=np.int32).tobytes()
        +np.asarray([f.loop_total for f in o.data.polygons],dtype=np.int32).tobytes()).hexdigest()
        for o in bpy.data.collections[PANELS].objects}
    faces_b = source_faces()
    original_plain,_ = grid(bpy.data.objects[LUMBAR])
    bpy.ops.wm.open_mainfile(filepath=str(candidate))
    checks = {
        "same14NamedPanelMeshesAndPolygonLoops": len(oldtop)==len(top)==14 and faces_b==source_faces()
            and all(top[k][0]==oldtop[k][0] for k in top),
        "allOriginalCutEdgesExactlyStationary": oldcuts==cuts,
        "onlyFourIntendedSurfacesChanged": changed==MODIFIED,
        "unchangedHeadrestRailsAndOverallHeight": all(bounds[i][2]==oldbounds[i][2] for i in (0,1))
            and not any(n.startswith(("Restraint","Rail","Foot")) for n in changed),
        "fourRecessesWithPositivePaddingAtThreeLevels": valleys==[4,4,4] and all(
            r.max()>.003 for r in signed[[nrows//4,nrows//2,3*nrows//4]]),
        "zeroKeyRestoresApprovedPlainFoundation": np.array_equal(plain,original_plain),
        "independentPerforationOnlyOnThreeInserts": sorted(punched)==["lumbar","pan","upper"] and len(finish_ids)==3,
        "separateRemovableThreadRuns": len(details_names)==5 and stitches>0,
        "fiveThreadObjectsOnlyAdditions":set(new)-set(old)==details_names,
    }
    result = {"passed":all(checks.values()),"checks":{k:bool(v) for k,v in checks.items()},
        "originalMeshesUnchanged":len(old)-len(changed),"shapeKeyValleyCounts":valleys,
        "signedDrawRangeM":[round(float(signed.min()),6),round(float(signed.max()),6)],
        "separateThreadStitches":stitches,"evaluatedTrianglesIncludingThread":tris,
        "evaluatedGeometryDigest":sha256(json.dumps(new,sort_keys=True).encode()).hexdigest(),
        "scope":"Digital structure and stored presentation state only. No leather sample, installed fit, visual acceptance or runtime performance certification."}
    report.write_text(json.dumps(result,indent=2)+"\n")
    print(result)
    if not result["passed"]: raise ValueError("Construction check failed")


if __name__ == "__main__":
    candidate = Path(bpy.data.filepath)
    details_names = {o.name for o in bpy.data.collections[DETAIL].objects}
    run(*(Path(s) for s in sys.argv[sys.argv.index("--")+1:]))
