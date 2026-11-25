"""Blender 5.2.2: cut an editable cover over the corrected R5-A section cages."""
from math import pi
from pathlib import Path
import sys

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from form import correct


def knots(n, extra=()):
    return np.unique(np.round([*np.linspace(0, 1, n), .005, .014, .032,
                               .968, .986, .995, *extra], 7))


class Envelope:
    """Uniform cubic surface. First index is across; second runs along a panel."""
    def __init__(self, cage, shape, is_back):
        points = np.array([list(v.co) for v in cage.data.vertices]).reshape(*shape, 3)
        self.points = points.transpose(1, 0, 2) if is_back else points
        self.periodic = (is_back, not is_back)

    @staticmethod
    def basis(q):
        t = q-np.floor(q)
        return ((1-t)**3/6, (4-6*t*t+3*t**3)/6,
                (1+3*t+3*t*t-3*t**3)/6, t**3/6)

    def at(self, u, v):
        wx, wy = self.basis(u), self.basis(v)
        ix, iy = np.floor(u).astype(int), np.floor(v).astype(int)
        def index(i, axis):
            n = self.points.shape[axis]
            return i % n if self.periodic[axis] else np.clip(i, 0, n-1)
        return sum((x*y)[..., None]*self.points[index(ix+a-1, 0), index(iy+b-1, 1)]
                   for a,x in enumerate(wx) for b,y in enumerate(wy))

    def frame(self, s, t):
        ds = self.at(s+.002, t)-self.at(s-.002, t)
        dt = self.at(s, t+.002)-self.at(s, t-.002)
        n = np.cross(ds, dt)
        return self.at(s,t), n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-12)


def make_mesh(name, verts, faces, mat, uv, group, tag):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts.tolist(), [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    group.objects.link(obj)
    obj.location.x = .425
    data.materials.append(mat)
    lay = data.uv_layers.new(name="Panel pattern (provisional)")
    li = np.empty(len(data.loops), dtype=np.int32)
    data.loops.foreach_get("vertex_index", li)
    lay.data.foreach_set("uv", np.asarray(uv[li], dtype=np.float32).ravel())
    data.polygons.foreach_set("use_smooth", np.ones(len(faces), dtype=bool))
    obj["editable_region"] = tag
    return obj


def tailored_patch(name, uvals, vvals, mapper, mat, tag, cap_edges=None):
    u, v = np.meshgrid(uvals, vvals)
    env,s,t,loft,flutes = mapper(u,v)
    co, normal = env.frame(s,t)
    coords = co + normal*loft[...,None]
    rows, cols = u.shape
    faces = [(i,i+1,i+cols+1,i+cols) for j in range(rows-1)
             for i in range(j*cols,(j+1)*cols-1)]
    obj = make_mesh(name, coords.reshape(-1,3), faces, mat,
                    np.stack((u,v),axis=-1).reshape(-1,2), panels, tag)
    if flutes is not None:
        obj.shape_key_add(name="Plain foundation")
        key = obj.shape_key_add(name="Drawn lumbar channels")
        key.data.foreach_set("co", np.asarray(coords + normal*flutes[...,None],
                                               dtype=np.float32).ravel())
        key.value = 1
    if cap_edges:
        cap_edges(coords)
    return obj


def centre_width(h):
    return 2.95-.50*np.exp(-((h-.54)/.18)**2) + .24*np.sin(pi*h)


def boxing_line(h):
    # Outside the lower bolster crest; turns over the shoulder higher up.
    return 6.85-.98*np.exp(-((h-.68)/.105)**2)+.21*np.sin(2*pi*h)


def back_map(region, u, h):
    inner, outer = centre_width(h), boxing_line(h)
    if region in ("upper","lower"):
        a = 2*u-1
        # Keep samples attached to the curving draw lines rather than cutting
        # diagonal grooves across a coarse rectangular grid.
        bend = .105*np.sin(h*pi/.56)*np.sin(pi*a)
        s = (a+bend)*inner
        split = 6.60-.78*(s/inner)**2
    elif region == "out":
        s = inner+(outer-inner)*u
        split = 5.82
    elif region == "boxing":
        s = outer+(26-2*outer)*u
        split = 5.82
    else:
        s = 26-outer+(outer-inner)*u
        split = 5.82
    t = np.where(h<=.56, -.60+(split+.60)*h/.56,
                 split+(12.6-split)*(h-.56)/.44)
    edge = np.minimum(u,1-u)
    width = {"upper":.30,"lower":.30,"out":.097,"in":.097,"boxing":.66}[region]
    ex = 1-np.exp(-(edge*width/.009)**1.28)
    ey = 1-np.exp(-(abs(h-.56)*.69/.008)**1.3) if region in ("lower","upper") else 1
    cap_fade = np.minimum(1, np.minimum(h,1-h)*28)
    crown = {"upper":.0105,"lower":.009,"out":.013,"in":.013,"boxing":.001}[region]
    loft = cap_fade*(-.0028 + ex*ey*(.003 + crown*np.sin(pi*u)**.70))
    flute = None
    if region == "lower":
        a = np.abs(2*u-1)
        valleys = np.exp(-((a-.47)/.026)**2)+.93*np.exp(-((a-.71)/.026)**2)
        flute = -.0046*valleys*ey*cap_fade*ex
    return back_env, s,t,loft,flute


def cap(name, boundary, reverse, mat):
    border = np.concatenate(boundary)
    if reverse:
        border = border[::-1]
    n = len(border)
    verts = np.concatenate((border,border.mean(axis=0,keepdims=True)))
    uv = verts[:,[0,1 if "Back" in name else 2]]
    make_mesh(name, verts, [(i,(i+1)%n,n) for i in range(n)], mat,
              (uv-uv.min(axis=0))/np.maximum(np.ptp(uv,axis=0),1e-6),
              panels,"return")


def back_cover():
    lower, upper = [], []
    a = knots(43, [.5+i*(x+d)/2 for i in (-1,1) for x in (.47,.71)
                   for d in (-.065,-.033,-.015,0,.015,.033,.065)])
    lo, hi = knots(42)*.56, .56+knots(32)*.44
    hs = np.r_[lo,hi[1:]]
    for reg,name,us,vs,mat,tag in [
        ("lower","Back • drawn lumbar insert",a,lo,primary,"lumbar"),
        ("upper","Back • upper centre yoke",a,hi,primary,"upper"),
        ("out","Back • outboard bolster",knots(27),hs,secondary,"bolster"),
        ("boxing","Back • wraparound boxing",knots(98),hs,secondary,"boxing"),
        ("in","Back • inboard bolster",knots(27),hs,secondary,"bolster")]:
        def ends(xyz):
            if reg != "upper": lower.append(xyz[0,:-1])
            if reg != "lower": upper.append(xyz[-1,:-1])
        tailored_patch(name,us,vs,lambda u,h:back_map(reg,u,h),mat,tag,ends)
    cap("Back • lower return",lower,True,secondary)
    cap("Back • crown return",upper,False,secondary)


def pan_map(region,u,v):
    t = -1.4+17*v
    # Widen the centre towards the nose, then pinch it beside the hip.
    inner = 2.86+.33*np.exp(-((t-2)/2.4)**2)-.40*np.exp(-((t-7)/1.95)**2)
    outer = 6.24-.37*np.exp(-((t-5)/2.8)**2)
    ends = (-.60, 9-outer,9-inner,9+inner,9+outer,18.60)
    s = ends[region]+u*(ends[region+1]-ends[region])
    edge = np.minimum(u,1-u)
    width = (.043,.084,.32,.084,.043)[region]
    ex = 1-np.exp(-(edge*width/.007)**1.4)
    # Seam take-up and padding fade on the underside, beneath the cradle.
    top = np.clip(np.minimum((t+1.4)/1.6,(12-t)/1.6),0,1)
    crown = (.001,.014,.0045,.014,.001)[region]
    loft = top*(-.0025+ex*(.0028+crown*np.sin(pi*u)**.83))
    if region in (0,4):
        loft *= np.clip((u if region==0 else 1-u)*6,0,1)
    return pan_env,s,t,loft,None


def pan_cover():
    v = knots(102)
    for i,(name,tag) in enumerate([
        ("inboard side boxing","boxing"),("inboard thigh bolster","bolster"),
        ("centre waterfall","pan"),("outboard thigh bolster","bolster"),
        ("outboard side boxing","boxing")]):
        def ends(xyz):
            if i in (0,4):
                edge = xyz[:-1,0 if i==0 else -1]
                cap("Cushion • "+name+" return",[edge],i==4,secondary)
        tailored_patch("Cushion • "+name, knots(35),v,
                       lambda u,v:pan_map(i,u,v),primary if i==2 else secondary,tag,ends)


if __name__ == "__main__":
    out = Path(sys.argv[sys.argv.index("--")+1]).resolve()
    if out.exists() or out.suffix != ".blend":
        raise ValueError("Choose an unused .blend path")
    back, pan = correct()
    back_env = Envelope(back,(13,26),True)
    pan_env = Envelope(pan,(19,17),False)
    primary, secondary = back.data.materials[:]
    panels = back.users_collection[0]
    panels.name = "01 • Tailored upholstery panels"
    guides = bpy.data.collections.new("CONSTRUCTION_ONLY • corrected section cages")
    bpy.context.scene.collection.children.link(guides)
    for obj in (back,pan):
        panels.objects.unlink(obj)
        guides.objects.link(obj)
    guides.hide_viewport = guides.hide_render = True
    back_cover()
    pan_cover()
    bpy.data.collections["R5_FRONT_SEAT_MASTER"]["phase"] = "R5-B: editable upholstery study"
    bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
