"""Fresh-open comparisons with the approved R5-A, evaluated without changing either file."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import sys

import bpy
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from form import APPROVED, BACK, PAN


def evaluated():
    dg = bpy.context.evaluated_depsgraph_get()
    by_name = {}
    extents = []
    for obj in sorted(bpy.data.collections["R5_FRONT_SEAT_MASTER"].all_objects,key=lambda o:o.name):
        ev = obj.evaluated_get(dg)
        mesh = ev.to_mesh()
        try:
            mesh.calc_loop_triangles()
            xyz = np.empty(len(mesh.vertices)*3,np.float32)
            mesh.vertices.foreach_get("co",xyz)
            pts = xyz.reshape(-1,3)
            matrix = np.asarray(ev.matrix_world)
            world = pts@matrix[:3,:3].T+matrix[:3,3]
            ix = np.empty(len(mesh.loop_triangles)*3,np.int32)
            mesh.loop_triangles.foreach_get("vertices",ix)
            by_name[obj.name] = sha256(world.tobytes()+ix.tobytes()).hexdigest()
            extents.append([world.min(axis=0),world.max(axis=0)])
        finally:
            ev.to_mesh_clear()
    return by_name,np.asarray(extents)


def border_mates(objects):
    # Weld *only* exposed boundary edges numerically, without welding the master.
    # A sewn skin has exactly one oppositely directed mate, including its caps.
    border=Counter()
    per_panel={}
    for ob in objects:
        if ob.data.shape_keys:
            pos=ob.data.shape_keys.key_blocks["Drawn lumbar channels"].data
        else:
            pos=ob.data.vertices
        edges={}
        for p in ob.data.polygons:
            loop=p.vertices[:]
            for a,b in zip(loop,(*loop[1:],loop[0])):
                k=(min(a,b),max(a,b))
                if k in edges:
                    del edges[k]
                else:
                    edges[k]=(a,b)
        per_panel[ob.name]=len(edges)
        for a,b in edges.values():
            pa,pb=(tuple(round(float(c),6) for c in pos[i].co) for i in (a,b))
            if pa==pb:
                raise ValueError("Collapsed boundary interval: "+ob.name)
            border[pa,pb]+=1
    unmatched=sum(1 for (a,b),n in border.items() if n!=1 or border[b,a]!=1)
    return unmatched, sum(per_panel.values())


def channel_samples(ob):
    keys=ob.data.shape_keys.key_blocks
    delta=np.array([(a.co-b.co).length for a,b in zip(keys[1].data,keys[0].data)])
    cols=ob.data.polygons[0].vertices[3]
    grid=delta.reshape(-1,cols)
    counts=[]
    for row in (grid[len(grid)//4],grid[len(grid)//2],grid[3*len(grid)//4]):
        counts.append(int(np.sum((row[1:-1]>row[:-2])&(row[1:-1]>row[2:])&(row[1:-1]>.003))))
    return counts, float(grid.max()), float(max(grid[[0,-1]].max(),grid[:,[0,-1]].max()))


def main():
    baseline, report = map(Path,sys.argv[sys.argv.index("--")+1:])
    if report.exists() or sha256(baseline.read_bytes()).hexdigest()!=APPROVED:
        raise ValueError("Require a new report and the approved R5-A input")
    new, ext=evaluated()
    covers=bpy.data.collections["01 • Tailored upholstery panels"]
    unmatched, total=border_mates(covers.objects)
    counts, depth, border_move=channel_samples(bpy.data.objects["Back • drawn lumbar insert"])
    guides=bpy.data.collections["CONSTRUCTION_ONLY • corrected section cages"]
    head=new["Restraint • adjustable pad"]
    checks={"bothGuidesHidden":bool(guides.hide_render and guides.hide_viewport and len(guides.objects)==2),
            "all14PanelsSeparate":len(covers.objects)==len({o.data.name for o in covers.objects})==14,
            "allCutEdgesPairedAtMicrometreGrid":unmatched==0,
            "fourIndependentDepressionsAtThreeLevels":counts==[4,4,4],
            "optionalDrawKeyPreservesEdge":border_move<1e-6}
    bpy.ops.wm.open_mainfile(filepath=str(baseline.resolve()))
    old,prior=evaluated()
    unchanged=[n for n in old if n not in (BACK,PAN)]
    checks.update({"allOtherEvaluatedMeshesUnchanged":all(new.get(n)==old[n] for n in unchanged),
                   "headrestUnmoved":old["Restraint • adjustable pad"]==head,
                   "railBottomAndOverallHeightUnchanged":bool(ext[:,0,2].min()==prior[:,0,2].min()
                   and ext[:,1,2].max()==prior[:,1,2].max())})
    result={"passed":all(checks.values()),"checks":checks,"unchangedMeshes":len(unchanged),
            "evaluatedGeometryDigest":sha256(json.dumps(new,sort_keys=True).encode()).hexdigest(),
            "directedPanelBoundaryEdges":total,"unpairedEdges":unmatched,"channelCounts":counts,
            "maxDrawDisplacementM":round(depth,6),"maxDrawBoundaryDisplacementM":round(border_move,8),
            "lowestAndHighestZM":[round(float(ext[:,0,2].min()),6),round(float(ext[:,1,2].max()),6)],
            "scope":"Digital geometry and panel registration only; no floor fit, leather response or visual acceptance."}
    report.write_text(json.dumps(result,indent=2)+"\n")
    print(result)
    if not result["passed"]:
        raise ValueError("R5-B construction checks failed")


if __name__=="__main__":
    main()
