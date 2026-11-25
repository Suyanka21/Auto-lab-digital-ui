"""Local offsets on the hydrated R5-B cover. Panel seams and topology stay fixed."""
from hashlib import sha256
from pathlib import Path
import sys

import bpy
import numpy as np

BASE = "5119f1a97a4c15ed5bf5c7cc66acf66d3700b6e83438b6ac962183014ab7cb74"
PANELS = "01 • Tailored upholstery panels"


def read_co(points):
    a = np.empty(len(points)*3, np.float32)
    points.foreach_get("co", a)
    return a.reshape(-1, 3).astype(float)


def grid(ob, shaped=False):
    me = ob.data
    cols = me.polygons[0].vertices[3]
    points = me.shape_keys.key_blocks[-1].data if shaped and me.shape_keys else me.vertices
    p = read_co(points).reshape(-1, cols, 3)
    uv = np.empty((p.size//3, 2))
    for loop, val in zip(me.loops, me.uv_layers[0].data):
        uv[loop.vertex_index] = val.uv
    return p, uv.reshape(*p.shape[:2], 2)


def normals(p):
    n = np.cross(np.gradient(p, axis=1), np.gradient(p, axis=0))
    return n / np.maximum(np.linalg.norm(n, axis=2, keepdims=True), 1e-12)


def correct():
    if sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() != BASE:
        raise ValueError("Start with the approved R5-B LFS file")
    for ob in bpy.data.collections[PANELS].objects:
        tag = ob["editable_region"]
        if tag not in ("lumbar", "pan") and not (tag == "bolster" and ob.name.startswith("Back")):
            continue
        p, uv = grid(ob)
        u, v = uv.transpose(2, 0, 1)
        n = normals(p)
        z, y = p[..., 2], p[..., 1]
        if tag == "lumbar":
            # Make the padded lands convex, not the holes deeper everywhere.
            # Put both the draw and the loft on the optional key.
            a = abs(2*u-1)
            h = v/.56
            crown = (.007*np.exp(-((a-.588)/.091)**2)
                     + .0048*np.exp(-(a/.33)**2)
                     + .0038*np.exp(-((a-.84)/.09)**2))
            key = ob.data.shape_keys.key_blocks["Drawn lumbar channels"]
            old = read_co(key.data).reshape(p.shape)
            target = old + .22*(old-p) + n*(crown*np.sin(np.pi*np.clip(h,0,1))**.6)[...,None]
            dest = key.data
        elif tag == "pan":
            # Crown above the bend; relax the immediately adjacent apron face.
            x = abs(p[...,0])
            d = (.0085*np.exp(-((y+.248+.012*(x/.17)**2)/.037)**2)
                 -.0048*np.exp(-((z-.479)/.021)**2)*np.exp(-((y+.305)/.025)**2))
            mask = np.clip((z-.44)/.045,0,1)*np.sin(np.pi*u)**1.2
            target, dest = p+n*(mask*d)[...,None], ob.data.vertices
        else:
            s = u if "outboard" in ob.name else 1-u
            line = .881+.050*s-.012*np.sin(np.pi*s)
            d = (-.0105*np.exp(-((z-line)/.018)**2)
                 +.0042*np.exp(-((z-line-.039)/.040)**2)
                 +.0032*np.exp(-((z-line+.051)/.041)**2))
            target, dest = p+n*(d*np.sin(np.pi*s)**.72)[...,None], ob.data.vertices
        target[[0,-1]] = p[[0,-1]]
        target[:,[0,-1]] = p[:,[0,-1]]
        dest.foreach_set("co", np.ascontiguousarray(target, dtype=np.float32).ravel())
        ob.data.update()
    bpy.context.view_layer.update()


if __name__ == "__main__":
    out = Path(sys.argv[sys.argv.index("--")+1]).resolve()
    if out.exists() or out.suffix != ".blend":
        raise ValueError("Use a fresh .blend destination")
    correct()
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)
