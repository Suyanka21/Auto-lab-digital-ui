"""R5-A construction probes, in Blender. These do not measure a real seat."""
import hashlib
import json
from pathlib import Path
import struct
import sys

import bpy
from mathutils.bvhtree import BVHTree


group=bpy.data.collections["R5_FRONT_SEAT_MASTER"]
dg=bpy.context.evaluated_depsgraph_get()
digest=hashlib.sha256()
trees={}
for o in sorted(group.all_objects,key=lambda obj:obj.name):
    ev=o.evaluated_get(dg)
    me=ev.to_mesh()
    pts=[ev.matrix_world@v.co for v in me.vertices]
    me.calc_loop_triangles()
    tris=[tuple(t.vertices) for t in me.loop_triangles]
    digest.update(o.name.encode()+b"\0")
    for pt in pts:
        digest.update(struct.pack("<3f",*pt))
    for t,ids in zip(me.loop_triangles,tris):
        digest.update(struct.pack("<4I",*ids,t.material_index))
    trees[o.name]=BVHTree.FromPolygons(pts,tris,all_triangles=True)
    ev.to_mesh_clear()


def from_rear(name,x,z):
    hit,_,_,_=trees[name].ray_cast((.425+x,1,z),(0,-1,0))
    if hit is None:
        raise ValueError(f"Inspection ray missed {name} at {x}, {z}")
    return hit.y


foam="Backrest • lumbar to shoulder"
shell="Rear • molded lower carrier"
offsets=[dict(xFromCentre=x,z=z,outerOffsetM=round(from_rear(shell,x,z)-from_rear(foam,x,z),5))
         for x in (-.16,0,.16) for z in (.55,.70,.85)]
checks={"backCoverFollowsFoamAtNineSamples":all(.001 < v["outerOffsetM"] < .022 for v in offsets)}
for side in ("in","out"):
    post=trees["Post • "+side]
    checks[f"post_{side}_enters_headrest"]=bool(post.overlap(trees["Restraint • adjustable pad"]))
    checks[f"post_{side}_enters_backrest"]=bool(post.overlap(trees[foam]))
for name in ("Position paddle","Recline paddle","Lumbar dial"):
    checks[name+"_seatedInOutboardShield"]=bool(trees[name].overlap(trees["Shield • outboard control carrier"]))
for name in (foam,"Cushion • dished pan and thigh roll"):
    checks[name+"_bothUpholsteryZones"]=len({p.material_index for p in bpy.data.objects[name].data.polygons})==2
report={"passed":all(checks.values()),"checks":checks,"rearCoverSamples":offsets,
        "evaluatedGeometryDigest":digest.hexdigest(),
        "digestScope":"Sorted object names, evaluated world coordinates, triangle indices and material indices; same Blender build.",
        "excluded":"Whole-assembly clearance, load paths, travel, installed dimensions and visual acceptance."}
out=Path(sys.argv[sys.argv.index("--")+1])
with out.open("x") as f:
    json.dump(report,f,indent=2)
    f.write("\n")
print(json.dumps(checks))
if not report["passed"]:
    raise RuntimeError("Review failed form probes")
