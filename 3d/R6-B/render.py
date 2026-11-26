"""Render the bench master without changing the saved scene or approved pair."""
from argparse import ArgumentParser
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"R6-A"))
from review import context

VIEWS = ("three-quarter","front","backrest","armrest","cabin","construction")
MACROS = {
    "backrest": ((-.442,1.26,.831),(-.40,-2.25,.31),.714),
    "armrest": ((-.008,1.13,.779),(-.49,-2.1,1.03),.829),
}


def render(out,views,preview):
    out.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    refs=[]
    macro=bpy.data.cameras.new("R6-B macro lens")
    cam=bpy.data.objects.new("R6-B macro position",macro)
    scene.collection.objects.link(cam)
    neutral=bpy.data.materials.new("Review only • clay")
    neutral.diffuse_color=(.36,.37,.38,1)
    for name in views:
        path=out/(name+".png")
        if path.exists(): raise FileExistsError(path)
        if name=="cabin" and not refs: refs=context()
        for c in refs: c.hide_render=(name!="cabin")
        bpy.data.objects["Studio stand"].location.z=-.012 if name=="cabin" else 0.
        scene.view_layers[0].material_override=neutral if name=="construction" else None
        key="three-quarter" if name=="construction" else name
        if key in MACROS:
            target,offset,width=MACROS[key]
            macro.type,macro.ortho_scale="ORTHO",width
            cam.location=Vector(target)+Vector(offset)
            cam.rotation_euler=(-Vector(offset)).to_track_quat("-Z","Y").to_euler()
            scene.camera=cam
            size=(1232,1232)
        else:
            scene.camera=bpy.data.objects["R6 / "+key]
            size=(1680,1152)
        scene.render.resolution_x,scene.render.resolution_y=size
        scene.render.resolution_percentage=40 if preview else 100
        scene.cycles.samples=6 if preview else 40
        scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    p=ArgumentParser()
    p.add_argument("out",type=Path)
    p.add_argument("views",nargs="+",choices=VIEWS)
    p.add_argument("--preview",action="store_true")
    args=p.parse_args(sys.argv[sys.argv.index("--")+1:])
    render(args.out.resolve(),args.views,args.preview)
