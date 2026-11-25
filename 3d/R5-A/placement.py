"""Read the saved master and decoded cabin in memory. Never save the combined scene."""
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def bounds(points):
    return [[round(op(v[k] for v in points),5) for k in range(3)] for op in (min,max)]


def tree(points, faces):
    return BVHTree.FromPolygons(points,faces,all_triangles=True)


def study_colour(name,rgb):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*rgb,1)
    return m


path,out=map(Path,sys.argv[sys.argv.index("--")+1:])
results=[out/f"cabin-{key}.png" for key in ("existing","r5-a")]
report=out/"placement.json"
if any(p.exists() for p in [*results,report]):
    raise ValueError("Use a new output directory")
out.mkdir(exist_ok=True,parents=True)
src=json.loads(path.read_text())
root=bpy.data.collections["R5_FRONT_SEAT_MASTER"]
sc=bpy.context.scene
scene_parts=list(root.all_objects)
dg=bpy.context.evaluated_depsgraph_get()
master_pts,master_trees=[],{}
for o in scene_parts:
    ev=o.evaluated_get(dg)
    me=ev.to_mesh()
    pts=[ev.matrix_world@v.co for v in me.vertices]
    me.calc_loop_triangles()
    master_trees[o.name]=tree(pts,[tuple(t.vertices) for t in me.loop_triangles])
    master_pts.extend(pts)
    ev.to_mesh_clear()

shell=study_colour("Context • cockpit",(.092,.112,.127))
seat=study_colour("Context • production seating",(.247,.290,.310))
driver=study_colour("Context • baseline driver",(.47,.245,.111))
replaced={"GEO_Seat_Front_Driver","GEO_Seat_Stitching_Front"}
old_pts,old_objects,intersections=[],[],{}
for n in src["nodes"]:
    me=bpy.data.meshes.new(n["name"])
    me.from_pydata(n["vertices"],[],n["faces"])
    me.update()
    o=bpy.data.objects.new(n["name"],me)
    sc.collection.objects.link(o)
    me.materials.append(driver if o.name in replaced else seat if "Seat" in o.name else shell)
    for f in me.polygons:
        f.use_smooth=True
    if o.name in replaced:
        old_pts.extend(n["vertices"])
        old_objects.append(o)
    else:
        other=tree(n["vertices"],n["faces"])
        hits=[name for name,bvh in master_trees.items() if bvh.overlap(other)]
        if hits:
            intersections[o.name]=hits
if len(old_objects)!=2 or len(src["nodes"])!=11:
    raise ValueError("Unexpected baseline node set")

# Wide doorway inspection, identical for both renders, not a new app preset.
target=Vector((.035,-.11,.72))
cam=sc.camera
cam.location=(2.45,-1.42,2.28)
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.lens=43
sc.render.resolution_x,sc.render.resolution_y=1100,800
sc.cycles.samples=24
# The stand used for the product study would cut off the older suspended cockpit.
bpy.data.objects["Studio ground"].location.z=-.46
for path,show_new in zip(results,(False,True)):
    for o in scene_parts:
        o.hide_render=not show_new
    for o in old_objects:
        o.hide_render=show_new
    sc.render.filepath=str(path.resolve())
    bpy.ops.render.render(write_still=True)
report.write_text(json.dumps({
    "baselineSHA256":src["hash"],"basis":"Blender world metres; x lateral, -y forward, z up",
    "oldDriverBounds":bounds(old_pts),"masterEvaluatedBounds":bounds(master_pts),
    "translationAppliedToMaster":[0,0,0],"oldDriverHiddenOnlyInSecondView":sorted(replaced),
    "otherNodesTested":len(src["nodes"])-len(old_objects),
    "intersectingSurfacePairsByContextObject":intersections,
    "scope":"Triangle-surface intersection only, not clearance, containment, floor anchorage, travel or human fit.",
    "camera":{"position":list(cam.location),"target":list(target),"lens":cam.data.lens},
    "renderedWith":"Blender "+bpy.app.version_string+" / Cycles CPU, 24 samples; diagnostic materials",
},indent=2)+"\n")
