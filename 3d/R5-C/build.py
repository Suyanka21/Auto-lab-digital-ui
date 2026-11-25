"""Start on the exact R5-B file; write a separate, self-contained master."""
from pathlib import Path
import sys

import bpy
import numpy as np
from mathutils.bvhtree import BVHTree
from mathutils import Vector
from mathutils.geometry import interpolate_bezier

sys.path.insert(0, str(Path(__file__).resolve().parent))
from form import PANELS, correct, grid, normals
from leather import CENTRE, SURROUND, MARGIN, PATTERN, finish_group, hide

DETAIL = "06 • Removable topstitch"
INSERTS = {"upper":"Yoke","lumbar":"Lumbar","pan":"Waterfall"}


def length(p, axis=0):
    step = np.linalg.norm(np.diff(p, axis=axis), axis=-1)
    zero = np.take(step, [0], axis=axis)*0
    return np.concatenate((zero, np.cumsum(step, axis=axis)), axis=axis)


def pattern(ob, p):
    # Use measured surface lengths, not the nonuniform knot indices of the cage.
    across = length(p, 1)
    along = length(p[:,p.shape[1]//2])
    xy = np.stack((across-across[:,[-1]]/2, np.broadcast_to(along[:,None], across.shape)), axis=2)
    dist = np.minimum(np.minimum(across,across[:,[-1]]-across),
                      np.minimum(along,along[-1]-along)[:,None])
    if ob["editable_region"] == "pan":
        dist = np.minimum(dist, np.maximum(0,p[:,:,2]-.438))
    me = ob.data
    old = me.uv_layers.active_index
    uv = me.uv_layers.new(name=PATTERN)
    li = np.empty(len(me.loops),np.int32)
    me.loops.foreach_get("vertex_index",li)
    uv.data.foreach_set("uv", xy.reshape(-1,2)[li].astype("f").ravel())
    me.uv_layers.active_index = old
    attr = me.attributes.new(MARGIN, "FLOAT", "POINT")
    attr.data.foreach_set("value", dist.astype("f").ravel())


def thread_stock():
    mat = bpy.data.materials.new("Topstitch • warm tonal thread")
    mat.use_nodes = True
    bs = mat.node_tree.nodes["Principled BSDF"]
    for k,v in {"Base Color":(.190,.082,.033,1.), "Roughness":.51, "Sheen Weight":.34}.items():
        bs.inputs[k].default_value = v
    return mat


def running_stitches(owner, paths, coll, mat):
    curve = bpy.data.curves.new(owner.name+" • topstitch", "CURVE")
    curve.dimensions, curve.resolution_u = "3D", 1
    curve.bevel_depth, curve.bevel_resolution = .00039, 1
    for points, ns in paths:
        arc = length(points)
        pitch = .0037
        for start in np.arange(.0012, arc[-1]-.0033, pitch):
            t = np.array([0,.18,.5,.82,1.])
            d = start+t*.00288
            xyz = np.array([np.interp(d, arc, axis) for axis in points.T]).T
            norm = np.array([np.interp(d, arc, axis) for axis in ns.T]).T
            xyz += norm * (-.000085+.00037*np.sin(np.pi*t))[:,None]
            seg = curve.splines.new("POLY")
            seg.points.add(len(t)-1)
            seg.points.foreach_set("co", np.column_stack((xyz,np.ones(len(t)))).astype("f").ravel())
            seg.points.foreach_set("radius", np.array([.12,.76,1.,.76,.12],"f"))
    obj = bpy.data.objects.new(curve.name,curve)
    coll.objects.link(obj)
    obj.matrix_world = owner.matrix_world.copy()
    obj["fitted_to"] = owner.name
    curve.materials.append(mat)


def panel_paths(ob):
    p,uv = grid(ob)
    n = normals(p)
    # 'u' runs in opposite directions on mating left and right pieces.
    back = ob.name.startswith("Back")
    reverse = "outboard" in ob.name
    if reverse:
        p, n = p[:,::-1], n[:,::-1]
    distance = length(p, 1)
    v = uv[:,0,1]
    keep = (v>.015)&(v<.984) if back else (v>.065)&(v<.626)
    for inset in (.0031, .0066):
        loc, norm = [], []
        for row, nr, arc in zip(p[keep], n[keep], distance[keep]):
            loc.append([np.interp(inset,arc,c) for c in row.T])
            norm.append([np.interp(inset,arc,c) for c in nr.T])
        yield np.array(loc), np.array(norm)


def head_path(ob):
    # U-shaped facing, fitted onto the evaluated pad rather than a floating outline.
    bvh = BVHTree.FromObject(ob,bpy.context.evaluated_depsgraph_get())
    spans = [
        ((-.122,1.104),(-.126,1.134),(-.114,1.225),(-.106,1.254)),
        ((-.106,1.254),(-.097,1.283),(-.085,1.287),(0,1.2875)),
        ((0,1.2875),(.085,1.287),(.097,1.283),(.106,1.254)),
        ((.106,1.254),(.114,1.225),(.126,1.134),(.122,1.104))]
    points, normals_ = [], []
    for i,s in enumerate(spans):
        for q in interpolate_bezier(*(Vector((x,0,z)) for x,z in s), 61)[int(i>0):]:
            pos, n, _, _ = bvh.ray_cast(q, (0,1,0))
            if pos is None: raise ValueError("Head restraint facing missed its surface")
            points.append(tuple(pos)); normals_.append(tuple(n))
    return np.array(points), np.array(normals_)


def build(out):
    if out.suffix != ".blend" or out.exists(): raise ValueError("Use a fresh .blend destination")
    correct()
    group = finish_group()
    finishes = {k:hide(group, "Cognac • "+v, CENTRE, 1.) for k,v in INSERTS.items()}
    side = hide(group, "Cognac • surrounds", SURROUND)
    fold = hide(group, "Cognac • recessed turn", (.157,.065,.029,1))
    boxing = hide(group, "Cognac • boxing", (.210,.090,.040,1))
    root = bpy.data.collections["R5_FRONT_SEAT_MASTER"]
    coll = bpy.data.collections.new(DETAIL)
    root.children.link(coll)
    thread = thread_stock()
    for ob in bpy.data.collections[PANELS].objects:
        tag = ob["editable_region"]
        ob.data.materials[0] = finishes.get(tag, side if tag=="bolster" else boxing)
        if len(ob.data.materials)>1:
            ob.data.materials[1] = fold
        if tag in INSERTS:
            pattern(ob, grid(ob, shaped=True)[0])
        elif tag=="bolster":
            running_stitches(ob, panel_paths(ob), coll, thread)
    head = bpy.data.objects["Restraint • adjustable pad"]
    head.data.materials[0] = hide(group,"Cognac • head restraint",SURROUND)
    running_stitches(head, [head_path(head)], coll, thread)
    root["phase"] = "R5-C: leather material study; owner visual review pending"
    bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)


if __name__ == "__main__":
    build(Path(sys.argv[sys.argv.index("--")+1]).resolve())
