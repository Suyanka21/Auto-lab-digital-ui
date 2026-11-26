"""R6-B. Tailor covers over the approved R6-A section cages, in cabin metres."""
from hashlib import sha256
import importlib.util
from pathlib import Path
import sys

import bpy
import numpy as np
from mathutils.bvhtree import BVHTree

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
STAGES = D.parent
FORM_HASH = "b4706f65ec7bb8437b724552892d8fd97909817e1e0cc1f469178bd0701422b9"
HIDE_HASH = "c2674a427043db534e2408c447a7800dc3718a36aa40d33fff6ed7a3695c00f8"
HIDE_FILE = STAGES / "R5-C-refined/R5-front-seat-refined.blend"
ROOT = "R6_REAR_BENCH_MASTER"
TAILOR = "06 • Rear sewn panels"
DETAIL = "07 • Removable tonal stitching"
GUIDES = "CONSTRUCTION ONLY • approved R6-A cages"
THREAD = "Topstitch • warm tonal thread"


def load(stage, name):
    path = STAGES/stage/"build.py"
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


surface = load("R5-B", "seat_sections")
# R5-B/build loads its own form.py; R5-C/build needs the R5-C one.
sys.modules.pop("form", None)
finish = load("R5-C", "seat_finish")
knots, Envelope = surface.knots, surface.Envelope


def collection(parent, name):
    coll = bpy.data.collections.new(name)
    parent.children.link(coll)
    return coll


def archive(obj):
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    guides.objects.link(obj)


def materials():
    roles = ("Yoke", "Lumbar", "Waterfall", "surrounds", "boxing", "recessed turn", "head restraint")
    with bpy.data.libraries.load(str(HIDE_FILE), link=False) as (src, dest):
        dest.materials = ["Cognac • "+r for r in roles]+[THREAD]
        assert set(dest.materials) <= set(src.materials)
    return dict(zip((*roles, "thread"), dest.materials))


def insert(role, tag):
    mat = hide[role].copy()
    mat.name = f"Rear • {tag} {role}"
    return mat


def face_mesh(name, points, faces, uv, mat, role):
    ob = surface.make_mesh(name, points, faces, mat, uv, panels, role)
    ob.location.x = 0
    return ob


def ramp(dist, span):
    return 1-np.exp(-(np.maximum(dist, 0)/span)**1.5)


def seam_line(p, n, direction, inset):
    if direction in ("toe","crown"):
        p, n = p.transpose(1,0,2), n.transpose(1,0,2)
    if direction in ("right","crown"):
        p, n = p[:,::-1], n[:,::-1]
    arc = finish.length(p, 1)
    points, normals = [], []
    for row, ns, along in zip(p,n,arc):
        points.append([np.interp(inset,along,c) for c in row.T])
        normals.append([np.interp(inset,along,c) for c in ns.T])
    return np.array(points), np.array(normals)


def norm(p):
    return p/np.maximum(np.linalg.norm(p,axis=-1,keepdims=True), 1e-12)


def punch_coordinates(ob, pts):
    across, up = finish.length(pts,1), finish.length(pts,0)
    # Offset the first course by its position on the raked back. A shared
    # row number would squash the punch field inside the arched yoke corners.
    start = pts[0] @ np.array([0,.305,.9524]) if "back •" in ob.name else 0
    uv = np.stack((across-.5*across[:,[-1]], up+start), axis=-1)
    dist = np.minimum(np.minimum(across,across[:,[-1]]-across),np.minimum(up,up[[-1]]-up))
    mesh=ob.data
    idx=np.empty(len(mesh.loops),np.int32)
    mesh.loops.foreach_get("vertex_index",idx)
    mesh.uv_layers.new(name=finish.PATTERN).data.foreach_set("uv",uv.reshape(-1,2)[idx].astype("f").ravel())
    mesh.attributes.new(finish.MARGIN,"FLOAT","POINT").data.foreach_set("value",dist.astype("f").ravel())


def patch(name, env, s, t, shape, normal_sign, mat, role, dist, sewing=()):
    base, normal = env.frame(s,t)
    normal *= normal_sign
    pts = base + normal*shape[...,None]
    # The draw and the stitch share the padded surface, including the seam roll.
    ns = norm(np.cross(np.gradient(pts,axis=1),np.gradient(pts,axis=0))) * normal_sign
    m,n = s.shape
    faces = [(i,i+1,i+1+n,i+n) for j in range(m-1) for i in range(j*n,(j+1)*n-1)]
    if normal_sign < 0:
        faces = [f[::-1] for f in faces]
    uv = np.stack((s,t),axis=2)
    ob = face_mesh(name,pts.reshape(-1,3),faces,uv.reshape(-1,2),mat,role)
    ob["source_form"] = source_name
    if mat.name.startswith("Rear •"):
        punch_coordinates(ob,pts)
    ob.data.materials.append(hide["recessed turn"])
    turn = (dist[:-1,:-1]+dist[1:,1:]+dist[:-1,1:]+dist[1:,:-1])*.25
    ob.data.polygons.foreach_set("material_index",(turn < .0008).astype("i").ravel())
    if sewing:
        paths = [seam_line(pts,ns,side,inset) for side,inset in sewing]
        finish.running_stitches(ob, paths, detail, hide["thread"])
    return pts


def cap(name, parts, axis, normal):
    # Zip opposite halves of a non-planar perimeter across its long axis.
    # A fan from the centroid can bridge the raised outboard pivot recess.
    ring = np.concatenate([p[:-1] for p in parts])
    n = len(ring)
    lo,hi = ring[:,axis].argmin(),ring[:,axis].argmax()
    def walk(step):
        r = [lo]
        while r[-1] != hi:
            r.append((r[-1]+step)%n)
        return r
    a,b = walk(1),walk(-1)
    i=j=0
    faces=[]
    while i<len(a)-1 or j<len(b)-1:
        if j==len(b)-1 or (i<len(a)-1 and ring[a[i+1],axis] <= ring[b[j+1],axis]):
            tri=(a[i],b[j],a[i+1])
            i+=1
        else:
            tri=(a[i],b[j],b[j+1])
            j+=1
        if len(set(tri))==3:
            faces.append(tri)
    area = sum((np.cross(ring[c]-ring[a],ring[b]-ring[a]) for a,c,b in faces),np.zeros(3))
    if np.dot(area,normal)<0:
        faces=[f[::-1] for f in faces]
    coords = ring[:,[0,1] if axis==0 else [1,2]]
    ob = face_mesh(name,ring,faces,coords,hide["boxing"],"return")
    ob["source_form"] = source_name


def back(tag, sign):
    ob = bpy.data.objects[source_name]
    env = Envelope(ob,(12,38),True)
    archive(ob)
    yoke, lumbar = insert("Yoke",tag), insert("Lumbar",tag)
    # Two interior draw seams, three padded lengths under one arched yoke.
    rib = knots(18)
    rib_ranges = [(r+rib)/3 for r in range(3)]
    full = np.r_[rib_ranges[0],rib_ranges[1][1:],rib_ranges[2][1:]]
    bands = [knots(12),knots(45),knots(34),knots(12)]
    hs = [i+v for i,v in enumerate(bands)]
    whole = np.concatenate([hs[0]]+[h[1:] for h in hs[1:]])
    bottom, top = {},{}
    def make(part, xx, hh, reg, band=None, ribno=None):
        u,h = np.meshgrid(xx,hh)
        g = 2*u-1 if reg=="field" else np.full_like(u, -1 if reg=="in" else 1)
        if reg=="wrap":
            g = np.ones_like(u)
        # Each horizontal cut stays continuous with its neighbour at the welt.
        edge = abs(g)
        depth = u if reg=="out" else 1-u if reg=="in" else 1 if reg=="wrap" else 0
        stations = [-.60+0*u, 2.80+.32*edge**4, 6.54-.92*edge**2+1.03*depth,
                    9.58-.75*edge**6, 11.60+0*u]
        t = stations[0].copy()
        for j in range(4):
            t += (stations[j+1]-stations[j])*np.clip(h-j,0,1)
        width = .505+.260*np.exp(-((t-8.14)/2.03)**2)-.036*np.exp(-((t-2.65)/1.0)**2)
        if reg=="field":
            frac=g*width
        elif reg=="in":
            frac=-1+(1-width)*u
        else:
            frac=width+(1-width)*u
        if reg=="wrap":
            s=18+20*u
        else:
            # Solve in physical width, not cage index. The centre intervals of
            # the approved envelope are much wider than the bolster intervals.
            centre=env.at(9+0*u,t)[...,0]
            limit=env.at(np.where(frac<0,0.,18.),t)[...,0]
            x=centre+abs(frac)*(limit-centre)
            a,b=np.zeros_like(u),np.full_like(u,18.)
            for _ in range(21):
                mid=(a+b)/2
                less=sign*(env.at(mid,t)[...,0]-x)<0
                a,b=np.where(less,mid,a),np.where(less,b,mid)
            s=np.where(frac<=-1,0.,np.where(frac>=1,18.,(a+b)/2))
        local = u if ribno is None else 3*u-ribno
        dx = np.minimum(local,1-local)*({"in":.108,"out":.108,"wrap":.72}.get(reg,.29 if ribno is None else .095))
        dy = np.full_like(u,2.)
        if reg=="field":
            v=h-band
            if band!=0:
                dy=np.minimum(dy,v*(.32 if band==1 else .23 if band==2 else .05))
            if band!=3:
                dy=np.minimum(dy,(1-v)*(.060 if band==0 else .32 if band==1 else .23))
        elif reg in ("in","out"):
            dy=abs(t-stations[2])*.085
        dist=np.maximum(np.minimum(dx,dy),0)
        fade=np.clip(np.minimum(h,4-h)*5,0,1)
        crown = (.0115 if band==2 else .010 if band==1 else .004) if reg=="field" else (.001 if reg=="wrap" else .009)
        if reg=="field" and band==2:
            crown=crown*(.31+.69*np.sin(np.pi*(h-band))**1.4)
        pillow=np.maximum(0,np.sin(np.pi*local))**.8
        loft=fade*(-.0024+ramp(dist,.0053)*(.0028+crown*pillow))
        mat = lumbar if band==1 else yoke if band==2 else hide["boxing" if reg=="wrap" else "surrounds"]
        sewing = ()
        if reg=="field" and band==2:
            sewing=[(d,.0027) for d in ("left","right","toe","crown")]
        if reg=="field" and band==1:
            sewing=[("left",.0025)]+([("right",.0025)] if ribno==2 else [])
        if reg in ("in","out"):
            sewing=[("right" if reg=="in" else "left",.0038)]
            if hh[0]==0:
                sewing.extend([("right" if reg=="out" else "left",k) for k in (.012,.0152)])
            else:
                sewing.append(("toe",.0029))
        p = patch(tag+" back • "+part,env,s,t,loft,sign,mat,part,dist*fade+(1-fade),sewing)
        if hh[0]==0: bottom[reg]=p[0]
        if hh[-1]==4: top[reg]=p[-1]
    make("inner bolster",knots(22),whole[whole<=2],"in")
    make("inner shoulder wing",knots(22),whole[whole>=2],"in")
    make("lower roll",full,hs[0],"field",0)
    for i,us in enumerate(rib_ranges):
        make(f"lumbar pad {i+1}",us,hs[1],"field",1,i)
    make("shoulder yoke",full,hs[2],"field",2)
    make("shoulder crest",full,hs[3],"field",3)
    make("outer bolster",knots(22),whole[whole<=2],"out")
    make("outer shoulder wing",knots(22),whole[whole>=2],"out")
    make("rear boxing",knots(75),whole,"wrap")
    for end,edge,direction in (("bottom",bottom,-1),("top",top,1)):
        cap(tag+" back • "+end+" return",[edge[k] for k in ("in","field","out","wrap")],0,[0,0,direction])


def cushion(tag):
    ob=bpy.data.objects[source_name]
    env=Envelope(ob,(15,17),False)
    archive(ob)
    centre=tag=="centre"
    mat=hide["surrounds"] if centre else insert("Waterfall",tag)
    # Reduce only the upper/front roll height; leave the lower skirt, buckle
    # recess and outer-cushion envelope as the approved placement references.
    for j,cut in enumerate((0,.002,.008,.011,.010,.006,.002)):
        env.points[:,j,2]-=cut*(.55+.45*np.sin(np.linspace(0,np.pi,15)))
    sections=[knots(21),knots(45),knots(21)]
    uv=[i+v for i,v in enumerate(sections)]
    all_u=np.concatenate([uv[0],uv[1][1:],uv[2][1:]])
    sides=[[],[]]
    def make(name,us,vs,is_top,region):
        u,v=np.meshgrid(us,vs)
        t=.96+(8.74-.96)*v if is_top else 8.74+(17+.96-8.74)*v
        f=(.35 if centre else .06)+.29*np.cos(2*np.pi*(t-1)/17)
        cuts=[-.60+0*u,4.50-f,9.50+f,14.60+0*u]
        s=cuts[0].copy()
        for j in range(3):
            s+=(cuts[j+1]-cuts[j])*np.clip(u-j,0,1)
        dx=np.full_like(u,2.)
        if is_top:
            if region>0: dx=np.minimum(dx,(u-region)*(.32 if region==1 else .10))
            if region<2: dx=np.minimum(dx,(region+1-u)*(.32 if region==1 else .10))
        dy=np.minimum(v,1-v)*(.45 if is_top else .57)
        dist=np.minimum(dx,dy)
        fade=np.clip(np.minimum(u,3-u)*12,0,1)
        crown=(.003 if region==1 else .008) if is_top else 0
        loft=fade*(-.0027+ramp(dist,.005)*(.0027+crown*np.maximum(0,np.sin(np.pi*u)**2)))
        if is_top and region==1 and not centre:
            # Two short draw lines die into the unbroken waterfall at the nose.
            loft-=.0033*np.exp(-((abs(u-1.5)-.15)/.021)**2)*np.sin(np.pi*v)**2
        sewing=()
        if is_top:
            sewing=[("toe",.0028)]
            if region!=1:
                sewing.append(("right" if region==0 else "left",.003))
        p=patch(tag+" pan • "+name,env,s,t,loft,1,
                (mat if region==1 else hide["surrounds"]) if is_top else hide["boxing"],
                "pan" if region==1 and not centre else name,dist*fade+(1-fade),sewing)
        if us[0]==0: sides[0].append(p[:,0])
        if us[-1]==3: sides[1].append(p[:,-1])
    for j,name in enumerate(("left cheek","squab insert" if not centre else "plain saddle","right cheek")):
        make(name,uv[j],knots(67),True,j)
    make("wrap apron",all_u,knots(78),False,None)
    for j,name in enumerate(("left","right")):
        cap(tag+" pan • "+name+" return",sides[j],1,[2*j-1,0,0])


def facing(ob, width, low, high, taper, inset):
    # Closed topstitch on the evaluated face, following the pad's taper.
    tree=BVHTree.FromObject(ob,bpy.context.evaluated_depsgraph_get())
    pts=[]
    ns=[]
    for a in np.linspace(-np.pi,np.pi,301):
        x,z = np.sign(np.cos(a))*abs(np.cos(a))**.38,np.sign(np.sin(a))*abs(np.sin(a))**.38
        z=low+(high-low)*(z+1)/2
        x*= (width-inset)*(1-taper*(z-low)/(high-low))
        loc,n,_,_=tree.ray_cast((x,-3,z),(0,1,0))
        if loc is None:
            raise ValueError(f"Missed {ob.name} at {x}, {z}")
        pts.append(tuple(loc));ns.append(tuple(n))
    return np.array(pts),np.array(ns)


def small_parts():
    for ob in bpy.data.collections[ROOT].all_objects:
        for slot in ob.material_slots:
            if slot.material.name in ("R6 • surrounding upholstery","R6 • armrest face","R6 • head restraints"):
                slot.material=hide["head restraint" if ob.name.startswith("Headrest") else "surrounds"]
    arm=bpy.data.objects["Centre • stowed armrest"]
    pivot=arm.location.copy()
    for vert in arm.data.vertices:
        p=vert.co+pivot
        v=np.clip((p.z-.644)/.399,0,1)
        front=np.clip((1.189+.32*(p.z-.505)+.047-p.y)/.052,0,1)
        vert.co.y-=front*(.004+.011*np.sin(np.pi*v))*max(0,1-(abs(p.x)/.142)**2)
        vert.co.x*=.966+.034*np.sin(v*np.pi*.7)
    tab=bpy.data.objects["Centre • armrest pull"]
    for v in tab.data.vertices:
        v.co.y-=.0058
        v.co.x*=.86
    bpy.context.view_layer.update()
    path=facing(arm,.128,.655-pivot.z,1.031-pivot.z,0,0)
    finish.running_stitches(arm,[path],detail,hide["thread"])
    seam=bpy.data.objects[arm.name+" • topstitch"]
    seam.parent=arm
    seam.matrix_parent_inverse=arm.matrix_world.inverted()
    # Headrest mesh coordinates in R6-A already include their station X.
    for tag in ("LH","RH","centre"):
        ob=bpy.data.objects["Headrest • "+tag]
        cx=0 if tag=="centre" else .442*(-1 if tag=="LH" else 1)
        tree=BVHTree.FromObject(ob,bpy.context.evaluated_depsgraph_get())
        paths=[]
        for inset in (0,.0031):
            pts,ns=[],[]
            for a in np.linspace(-np.pi,np.pi,241):
                x,z=np.cos(a),np.sin(a)
                q=.5+.5*np.sign(z)*abs(z)**.40
                lo,hi=(1.137,1.232) if tag=="centre" else (1.146,1.313)
                z=lo+inset+(hi-lo-2*inset)*q
                w=(.101 if tag=="centre" else .110)*(1-(.06 if tag=="centre" else .17)*q)-inset
                x=cx+w*np.sign(x)*abs(x)**.40
                loc,n,_,_=tree.ray_cast((x,0,z),(0,1,0))
                if loc is None: raise ValueError((tag,x,z))
                pts.append(tuple(loc));ns.append(tuple(n))
            paths.append((np.array(pts),np.array(ns)))
        finish.running_stitches(ob,paths,detail,hide["thread"])


def build(out):
    global panels, detail, guides, hide, source_name
    if out.exists() or out.suffix!=".blend":
        raise ValueError("Use a fresh .blend destination")
    if sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()!=FORM_HASH or sha256(HIDE_FILE.read_bytes()).hexdigest()!=HIDE_HASH:
        raise ValueError("Retrieve and open the approved masters")
    root=bpy.data.collections[ROOT]
    panels,detail=collection(root,TAILOR),collection(root,DETAIL)
    guides=collection(bpy.context.scene.collection,GUIDES)
    guides.hide_render=guides.hide_viewport=True
    hide=materials()
    for tag,sign in (("LH",-1),("RH",1)):
        source_name="Backrest • "+tag
        back(tag,sign)
    for tag in ("LH","centre","RH"):
        source_name="Cushion • "+tag
        cushion(tag)
    small_parts()
    root["stage"]="R6-B rear upholstery; stowed pose. Floor anchorage unresolved."
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)


if __name__=="__main__":
    build(Path(sys.argv[sys.argv.index("--")+1]).resolve())
