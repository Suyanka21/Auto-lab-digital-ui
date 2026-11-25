"""Disposable Cycles swatches under the seat's actual review rig. Never save scene."""
from pathlib import Path
import sys
import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leather import CENTRE, SURROUND, MARGIN, PATTERN, finish_group, hide


def swatch(x, mat):
    u,v = np.meshgrid(np.linspace(-.050,.050,33), np.linspace(-.073,.073,33))
    z = .013*(1-(u/.05)**2) - .006*(v/.073)**2
    vs = np.stack((u, v, z), axis=-1).reshape(-1,3)
    faces = [(a,a+1,a+34,a+33) for j in range(32) for a in range(j*33,j*33+32)]
    me = bpy.data.meshes.new(mat.name)
    me.from_pydata(vs.tolist(), [], faces)
    me.update()
    ob = bpy.data.objects.new(mat.name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (x, .06, .75)
    me.materials.append(mat)
    uv = me.uv_layers.new(name=PATTERN)
    for loop in me.loops:
        uv.data[loop.index].uv = vs[loop.vertex_index,:2]
    margin = me.attributes.new(MARGIN, "FLOAT", "POINT")
    margin.data.foreach_set("value", np.minimum(.05-abs(u),.073-abs(v)).astype("f").ravel())
    for f in me.polygons:
        f.use_smooth = True
    mod = ob.modifiers.new("Turned edge", "SOLIDIFY")
    mod.thickness = .002
    mod = ob.modifiers.new("Lip", "BEVEL")
    mod.width, mod.segments = .0009, 3


def run(out):
    if out.exists(): raise FileExistsError(out)
    sc = bpy.context.scene
    bpy.data.collections["R5_FRONT_SEAT_MASTER"].hide_render = True
    g = finish_group()
    swatch(.372, hide(g,"Plain bolster sample",SURROUND))
    swatch(.478, hide(g,"Punched centre sample",CENTRE,1.))
    cam = bpy.data.objects["CAM_front"]
    cam.location = (.446,-.25,1.04)
    cam.rotation_euler = (Vector((.425,.06,.75))-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.ortho_scale = .242
    sc.camera = cam
    sc.cycles.samples = 48
    sc.render.resolution_x, sc.render.resolution_y = 900, 600
    sc.render.filepath = str(out)
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    run(Path(sys.argv[sys.argv.index("--")+1]).resolve())
