"""Build a separate detailed master from the exact published R5-C."""
from hashlib import sha256
from pathlib import Path
import sys

import bpy
import numpy as np

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
sys.path[:0] = [str(D), str(D.parent / "R5-C")]
from build import DETAIL, length, running_stitches
from form import grid, normals, read_co
from finish import apply_finish

BASE_HASH = "f1c58d65b9ecfdd5b52467ff199659ed1d4f71125039175ea861cab868e0d9e4"
LUMBAR = "Back • drawn lumbar insert"
DRAW = "Drawn lumbar channels"
PAN = "Cushion • centre waterfall"
HEAD = "Restraint • adjustable pad"
DRAW_THREAD = "Lumbar • channel topstitch"


def move_interior(points, base, delta):
    dest = base.copy()
    dest[1:-1, 1:-1] += delta[1:-1, 1:-1]
    points.foreach_set("co", dest.astype("f").ravel())
    return dest


def interpolate_line(distances, points, targets):
    return np.stack([np.interp(targets, distances, axis) for axis in points.T], axis=-1)


def bind_draw(property_owner, property_name, expression, key_data):
    driver = property_owner.driver_add(property_name).driver
    driver.type = "SCRIPTED"
    var = driver.variables.new()
    var.name = "draw"
    target = var.targets[0]
    target.id_type, target.id = "KEY", key_data
    target.data_path = f'key_blocks["{DRAW}"].value'
    driver.expression = expression


def channel_thread(ob, plain, drawn, uv, coll, thread):
    # Sample the same surface parcels at both ends of the draw key. The
    # thread follows continuously as the owner dials the channel depth.
    curve = bpy.data.curves.new(DRAW_THREAD, "CURVE")
    curve.dimensions, curve.bevel_resolution = "3D", 1
    obj = bpy.data.objects.new(DRAW_THREAD, curve)
    coll.objects.link(obj)
    obj.matrix_world = ob.matrix_world.copy()
    obj["fitted_to"] = ob.name
    curve.materials.append(thread)
    phase = np.array([0, .18, .5, .82, 1])
    lift = (-.00005 + .00038 * np.sin(np.pi * phase))[:, None]
    keep = (uv[:, 0, 1] > .007) & (uv[:, 0, 1] < .552)
    u = 2 * uv[0, :, 0] - 1
    # A fine row on the lip of each compressed channel.
    base_norm, draw_norm = normals(plain), normals(drawn)
    drawn_positions = []
    for line in (-.71, -.47, .47, .71):
        col = np.argmin(abs(u - (line + np.sign(line) * .015)))
        base_path, draw_path = plain[keep, col], drawn[keep, col]
        arc = length(draw_path)
        for start in np.arange(.0012, arc[-1] - .0032, .0037):
            at = start + phase * .00288
            base_xyz = interpolate_line(arc, base_path, at)
            base_xyz += lift * interpolate_line(arc, base_norm[keep, col], at)
            draw_xyz = interpolate_line(arc, draw_path, at)
            draw_xyz += lift * interpolate_line(arc, draw_norm[keep, col], at)
            s = curve.splines.new("POLY")
            s.points.add(len(phase) - 1)
            s.points.foreach_set("co", np.column_stack((base_xyz, np.ones(len(phase)))).ravel())
            s.points.foreach_set("radius", [.12, .76, 1, .76, .12])
            drawn_positions.append(draw_xyz)
    obj.shape_key_add(name="Relaxed")
    fitted = obj.shape_key_add(name="Fitted to draw")
    fitted.data.foreach_set("co", np.concatenate(drawn_positions).astype("f").ravel())
    bind_draw(fitted, "value", "draw", ob.data.shape_keys)
    bind_draw(curve, "bevel_depth", "0.00042 * draw", ob.data.shape_keys)


def tailor_back(coll, thread):
    ob = bpy.data.objects[LUMBAR]
    plain, uv = grid(ob)
    old, _ = grid(ob, shaped=True)
    u, v = uv.transpose(2, 0, 1)
    a = abs(2*u - 1)
    fade = np.sin(np.pi*np.clip(v/.56, 0, 1))**.65
    depth = (-.0018*np.exp(-((a-.47)/.046)**2) - .0017*np.exp(-((a-.71)/.045)**2)
             + .0014*np.exp(-((a-.59)/.084)**2))
    key = ob.data.shape_keys.key_blocks[DRAW]
    drawn = move_interior(key.data, old, normals(plain)*(fade*depth)[..., None])
    channel_thread(ob, plain, drawn, uv, coll, thread)
    yoke = bpy.data.objects["Back • upper centre yoke"]
    p, _ = grid(yoke)
    n = normals(p)
    paths = []
    # Measure the inset along each surface column, away from the curved joint.
    for offset in (.0026, .0059):
        line, ns = [], []
        for col in range(1, p.shape[1] - 1):
            arc = length(p[:, col])
            line.append(interpolate_line(arc, p[:, col], offset))
            ns.append(interpolate_line(arc, n[:, col], offset))
        paths.append((np.array(line), np.array(ns)))
    running_stitches(yoke, paths, coll, thread)


def taper(x, z):
    h = np.clip((z - 1.12)/.18, 0, 1)
    return x*(1 - .059*h*h*(3 - 2*h))


def local_form():
    pad = bpy.data.objects[HEAD]
    co = read_co(pad.data.vertices)
    co[:, 0] = taper(co[:, 0], co[:, 2])
    pad.data.vertices.foreach_set("co", co.astype("f").ravel())
    pad.data.update()
    thread = bpy.data.objects[HEAD + " • topstitch"]
    for spline in thread.data.splines:
        for pt in spline.points:
            pt.co.x = taper(pt.co.x, pt.co.z)
    pan = bpy.data.objects[PAN]
    p, uv = grid(pan)
    x, y, z = p.transpose(2, 0, 1)
    cross = np.sin(np.pi*uv[..., 0])**1.4
    # Shape the visible crest into a shallow arc, then release its underside.
    d = (.0038*np.exp(-((y+.245+.020*(x/.16)**2)/.030)**2)
         - .0023*np.exp(-((z-.47)/.026)**2 - ((y+.304)/.028)**2))
    move_interior(pan.data.vertices, p, normals(p)*(cross*np.clip((z-.43)/.04, 0, 1)*d)[..., None])
    pan.data.update()


def build(out):
    if out.exists() or out.suffix != ".blend":
        raise ValueError("Choose a new .blend destination")
    if sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() != BASE_HASH:
        raise ValueError("Open the published R5-C master")
    apply_finish()
    thread = bpy.data.materials["Topstitch • warm tonal thread"]
    thread.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (.17,.079,.030,1)
    tailor_back(bpy.data.collections[DETAIL], thread)
    local_form()
    bpy.context.view_layer.update()
    bpy.data.collections["R5_FRONT_SEAT_MASTER"]["phase"] = "R5-C-refined • owner visual review pending"
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)


if __name__ == "__main__":
    build(Path(sys.argv[sys.argv.index("--") + 1]).resolve())
