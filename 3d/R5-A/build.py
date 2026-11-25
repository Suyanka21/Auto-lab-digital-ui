"""Blender 5.2.2. Build a NEW R5-A file; never run inside an existing master."""
import argparse
from math import cos, pi, sin
from pathlib import Path
import sys

import bmesh
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


ROOT = Path(__file__).resolve().parents[2]
PRIMARY = ROOT / "AUTOLAB_INTERIOR_3D_REFERENCE_PACK/03_FRONT_SEATS/PRIMARY/AUTOLAB_SUV_FRONT_SEAT_PRIMARY_01.jpg"
MASTER = "R5_FRONT_SEAT_MASTER"
# Blender axes: -Y faces the wheel, +X is outboard at the production driver's station.
CENTER_X = .425
FLOOR = .244


def collection(name, parent):
    c = bpy.data.collections.new(name)
    parent.children.link(c)
    return c


def material(name, rgb, roughness=.55, metal=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    for key, value in (("Base Color", (*rgb, 1)), ("Roughness", roughness), ("Metallic", metal)):
        p.inputs[key].default_value = value
    return m


def mesh(name, vertices, faces, mats, group, *, indices=None, subdiv=0, bevel=0):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    group.objects.link(obj)
    obj.location.x = CENTER_X
    for m in mats:
        data.materials.append(m)
    for poly in data.polygons:
        poly.use_smooth = bool(subdiv)
        if indices:
            poly.material_index = indices[poly.index]
    bm = bmesh.new()
    bm.from_mesh(data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(data)
    bm.free()
    # Local per-face coordinates, only for draft inspection; no bake atlas yet.
    uv = data.uv_layers.new(name="Draft_face_metres")
    for p in data.polygons:
        n = p.normal
        u = n.cross(Vector((0, 0, 1)) if abs(n.z) < .9 else Vector((0, 1, 0))).normalized()
        v = n.cross(u)
        for i in p.loop_indices:
            co = data.vertices[data.loops[i].vertex_index].co
            uv.data[i].uv = (co.dot(u), co.dot(v))
    if subdiv:
        sub = obj.modifiers.new("Form smoothing — editable sections", 'SUBSURF')
        sub.levels = sub.render_levels = subdiv
    if bevel:
        mod = obj.modifiers.new("Edge radius", 'BEVEL')
        mod.width, mod.segments = bevel, 3
        obj.modifiers.new("Face normals", 'WEIGHTED_NORMAL')
    return obj


def loft(name, rows, mats, group, *, region=lambda j, i: 0, caps=(0,0), subdiv=2, bevel=0):
    n = len(rows[0])
    assert all(len(r) == n for r in rows)
    faces, indices = [], []
    for j in range(len(rows) - 1):
        for i in range(n):
            a, b = j*n+i, j*n+(i+1) % n
            faces.append((a, b, b+n, a+n))
            indices.append(region(j, i))
    last = (len(rows)-1)*n
    faces.extend((tuple(reversed(range(n))), tuple(range(last, last+n))))
    return mesh(name, sum(rows, []), faces, mats, group, indices=indices+list(caps),
                subdiv=subdiv, bevel=bevel)


def symmetric(half):
    """Walk from front centre around right wall to rear centre, then back via left."""
    return half + [(-x, y, z) for x, y, z in half[-2:0:-1]]


def backrest():
    # Elevation, half-width, centre contact Y, rearward depth, forward wing reach.
    stations = [
        (.448,.180,.161,.093,.026), (.459,.208,.158,.115,.042),
        (.491,.234,.153,.125,.065), (.558,.247,.151,.136,.093),
        (.648,.255,.165,.144,.111), (.726,.254,.193,.147,.110),
        (.823,.244,.243,.136,.085), (.914,.249,.283,.127,.071),
        (.991,.254,.312,.122,.061), (1.039,.246,.334,.113,.045),
        (1.067,.228,.351,.104,.030), (1.083,.199,.367,.077,.012),
        (1.089,.166,.384,.047,.005),
    ]
    rows = []
    for z,w,y,d,wing in stations:
        # x/w, y displacement: quiet central lumbar crown, asymmetric rolled flanks.
        section = [(0,0),(.35,.002),(.55,.002),(.60,-.10*wing),
                   (.71,-.66*wing),(.82,-wing),(.90,-.97*wing),
                   (.97,-.70*wing),(1,-.18*wing),(1,.35*d),
                   (.96,.72*d),(.84,.92*d),(.55,d),(0,1.02*d)]
        rows.append(symmetric([(x*w,y+dy,z) for x,dy in section]))
    return loft("Backrest • lumbar to shoulder",rows,[primary,secondary],foam,
                region=lambda j,i: int(min(i,25-i) >= 2))


def rear_carrier(back):
    # Take the contact surface from the evaluated foam, including at the dropped corners.
    dg=bpy.context.evaluated_depsgraph_get()
    surface=BVHTree.FromObject(back,dg)
    outer,inner,faces=[],[],[]
    cols=33
    levels=(0,.012,.04,.09,.17,.26,.36,.46,.56,.66,.75,.84,.91,.96,.985,1)
    for j,f in enumerate(levels):
        w=.210+.021*sin(pi*f)-.012*(1-f)**12-.004*f**36
        for i in range(cols):
            t=2*i/(cols-1)-1
            x,zz=w*t,.468+f*(.467-.052*t*t)+.016*(1-f)*t*t
            hit,_,_,_=surface.ray_cast((x,1,zz),(0,-1,0))
            if hit is None:
                raise ValueError(f"Rear profile missed at {x}, {zz}")
            outer.append((x,hit.y+.008+.004*(1-t*t),zz))
            inner.append((x,hit.y-.009,zz))
            k=len(outer)-1
            if i and j:
                faces.append((k,k-1,k-1-cols,k-cols))
    n=len(outer)
    faces += [tuple(i+n for i in reversed(face)) for face in faces]
    border=[*range(cols),*range(2*cols-1,n,cols),*range(n-2,n-cols-1,-1),
            *range(n-2*cols,0,-cols)]
    for i,a in enumerate(border):
        b=border[(i+1)%len(border)]
        faces.append((a,b,b+n,a+n))
    mesh("Rear • molded lower carrier",outer+inner,faces,[plastic],structure,subdiv=2)


def cushion():
    # Sagittal loops carry the top over the nose to the underside without an end cap.
    # (Y, Z, extra height at bolster crest); the roll dies out towards the front lip.
    profile=[(-.316,.454,0),(-.314,.489,.001),(-.293,.518,.005),
             (-.245,.534,.012),(-.168,.531,.026),(-.067,.510,.048),
             (.048,.484,.065),(.141,.478,.057),(.208,.484,.035),
             (.236,.472,.018),(.243,.448,.010),(.220,.419,0),
             (.140,.408,0),(-.044,.395,0),(-.224,.396,0),(-.290,.402,0),
             (-.313,.417,0)]
    # lateral distance, lift at crest, contraction and vertical roll of the outside edge
    half=[(0,0,1,1),(.090,0,1,1),(.148,.02,1,1),(.167,.13,.998,1),
          (.195,.66,.985,1),(.222,1,.96,1),(.245,.96,.918,.98),
          (.259,.72,.87,.94),(.267,.43,.81,.82),(.269,.22,.74,.65)]
    stations=[(-x,h,l,v) for x,h,l,v in half[:0:-1]]+half
    rows=[]
    for x,h,length,vertical in stations:
        rows.append([(x,y*length,.445+(z-.445)*vertical+h*crest)
                     for y,z,crest in profile])
    loft("Cushion • dished pan and thigh roll",rows,[primary,secondary],foam,
         region=lambda j,i: int(abs((stations[j][0]+stations[j+1][0])/2)>.148),caps=(1,1))


def base():
    profile=[(-.314,.413,0),(-.309,.424,0),(-.276,.427,0),(-.212,.428,0),
             (-.112,.430,.007),(.005,.433,.017),(.095,.441,.027),
             (.145,.444,.062),(.190,.443,.099),(.233,.443,.102),
             (.273,.435,.089),(.286,.417,.056),(.283,.374,.016),
             (.252,.338,0),(.19,.313,0),(.045,.296,0),(-.137,.296,0),
             (-.246,.307,0),(-.290,.325,0),(-.310,.360,0)]
    def section(x,h,length):
        return [(x,y*length,z+crest*h) for y,z,crest in profile]
    # Mating end sections share the same section construction with a narrow parting line.
    inner=[(0,0,1),(.13,0,.998),(.179,.10,.990),(.183,.19,.985),(.185,.20,.984)]
    core=[(-x,h,l) for x,h,l in inner[:0:-1]]+inner
    loft("Apron • under-cushion cradle",[section(*s) for s in core],[plastic],structure)
    for sign,label in ((1,"outboard control carrier"),(-1,"inboard plain")):
        seq=[(.1858,.20,.984),(.188,.21,.983),(.197,.32,.978),(.227,.75,.958),
             (.250,1,.921),(.264,1,.877),(.270,.98,.845),(.271,.92,.828)]
        loft("Shield • "+label,[section(sign*x,h,l) for x,h,l in seq],[plastic],handed)


def rounded_section(w, d, exp, count=32):
    def power(a):
        return (1 if a>=0 else -1)*abs(a)**exp
    return [(w*power(cos(2*pi*i/count)),d*power(sin(2*pi*i/count))) for i in range(count)]


def headrest():
    rows=[]
    for z,w,y,d in [
        (1.092,.111,.394,.058),(1.096,.131,.395,.076),(1.106,.140,.395,.081),
        (1.143,.142,.402,.083),(1.222,.132,.422,.075),(1.268,.123,.435,.067),
        (1.287,.115,.442,.060),(1.302,.095,.445,.045),(1.305,.073,.446,.032),
    ]:
        rows.append([(x,y+dy,z) for x,dy in rounded_section(w,d,.53)])
    loft("Restraint • adjustable pad",rows,[head],restraint)
    for x,tag in ((-.071,"in"),(.071,"out")):
        for name,r,bottom,top,mat in (
            ("Guide",.0135,1.080,1.091,plastic),("Post",.007,1.077,1.105,steel)):
            rows=[[(x+dx,.407+dy,z) for dx,dy in rounded_section(r*k,r*k,1)]
                  for z,k in ((bottom,.90),(bottom+.001,1),(top-.001,1),(top,.90))]
            loft(name+" • "+tag,rows,[mat],restraint,subdiv=1)


def prism(name, profile, transform, start, end, mat, group, radius):
    return loft(name,[[transform(a,b,v) for a,b in profile] for v in (start,end)],
                [mat],group,subdiv=0,bevel=radius)


def mechanisms():
    for sign,label in ((1,"outboard"),(-1,"inboard")):
        x=sign*.184
        # Open C-channel with returns and a short nested slider.
        channel=[(-.022,0),(.022,0),(.022,.022),(.011,.022),(.011,.017),
                 (.017,.017),(.017,.005),(-.017,.005),(-.017,.017),
                 (-.011,.017),(-.011,.022),(-.022,.022)]
        axis=lambda a,b,y:(x+a,y,FLOOR+.013+b)
        prism("Runner • "+label,channel,axis,-.293,.258,steel,rails,.0014)
        slide=[(-.014,.007),(.014,.007),(.014,.015),(.008,.015),(.008,.028),
               (.016,.028),(.016,.034),(-.016,.034),(-.016,.028),
               (-.008,.028),(-.008,.015),(-.014,.015)]
        prism("Slider • "+label,slide,axis,-.248,.226,dark_metal,rails,.0013)
        for end,at,sgn in (("front",-.243,-1),("rear",.211,1)):
            foot=[(-.021,.012),(.030,.012),(.045,0),(.078,0),(.078,.005),
                  (.047,.005),(.032,.017),(-.021,.017)]
            prism(f"Foot • {label} {end}",foot,lambda a,b,px:(px,at+sgn*a,FLOOR+b),
                  x-.023,x+.023,steel,rails,.0013)
            riser=[(-.025,.031),(.025,.031),(.031,.064),(.022,.082),
                   (-.018,.086),(-.028,.066)]
            prism(f"Riser • {label} {end}",riser,lambda a,b,px:(px,at+a,FLOOR+b),
                  x-.014,x+.014,dark_metal,rails,.003)
    # Separate, unlabelled proxies on the outboard face, not upholstery embossing.
    for name,y,z,w,h,angle in [
        ("Lumbar dial",.099,.407,.025,.025,0),("Recline paddle",.031,.381,.014,.030,.24),
        ("Position paddle",-.051,.365,.041,.013,.065)]:
        rows=[]
        for x,k in ((.259,.84),(.267,.98),(.273,1),(.280,.96),(.282,.84)):
            pts=rounded_section(w*k,h*k,1 if name=="Lumbar dial" else .58)
            rows.append([(x,y+a*cos(angle)-b*sin(angle),z+a*sin(angle)+b*cos(angle))
                         for a,b in pts])
        loft(name,rows,[switch],handed,subdiv=1)


def point_at(obj, target):
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()


def scene_setup(scene, rig):
    target=(CENTER_X,.060,.753)
    for name,vec,ortho in [
        ("three-quarter",(2.18,-2.28,.77),False),("front",(0,-3.2,0),True),
        ("side",(3.2,0,0),True),("rear",(0,3.2,0),True)]:
        data=bpy.data.cameras.new(name)
        cam=bpy.data.objects.new("CAM_"+name,data)
        rig.objects.link(cam)
        cam.location=Vector(target)+Vector(vec)
        point_at(cam,target)
        if ortho:
            data.type='ORTHO'
            data.ortho_scale=1.30
        else:
            data.lens=80
            scene.camera=cam
    # The guide is available in the camera properties, disabled by default and never rendered.
    image=bpy.data.images.load(str(PRIMARY))
    image.pack()
    image.filepath="//"+PRIMARY.name
    bg=scene.camera.data.background_images.new()
    bg.image=image
    bg.use_flip_x=True
    scene.camera.data.show_background_images=False
    for name,loc,size,energy in [
        ("Softbox key",(1.3,-1.6,2.65),1.65,115),
        ("Front fill",(-1.4,-.9,1.55),1.4,68),
        ("Rear edge",(-.6,1.4,2.2),1.05,135),
    ]:
        light=bpy.data.lights.new(name,'AREA')
        light.energy,light.shape,light.size=energy,'DISK',size
        o=bpy.data.objects.new(name,light)
        rig.objects.link(o)
        o.location=loc
        point_at(o,target)
    mesh("Studio ground", [(-100,-100,FLOOR-.001),(100,-100,FLOOR-.001),
         (100,100,FLOOR-.001),(-100,100,FLOOR-.001)],[(0,1,2,3)],
         [material("Studio • stone",(.25,.24,.222),.85)],rig)
    world=bpy.data.worlds.new("Studio fill")
    scene.world=world
    world.use_nodes=True
    world.node_tree.nodes["Background"].inputs[0].default_value=(.51,.54,.58,1)
    world.node_tree.nodes["Background"].inputs[1].default_value=.58
    scene.unit_settings.system='METRIC'
    scene.render.engine='CYCLES'
    scene.cycles.device='CPU'
    scene.cycles.samples=32
    scene.cycles.use_denoising=True
    scene.view_settings.view_transform="AgX"
    scene.view_settings.look="AgX - Medium High Contrast"
    scene.render.resolution_x,scene.render.resolution_y=1040,1040
    scene.render.resolution_percentage=100
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=="VIEW_3D":
                space=area.spaces.active
                space.region_3d.view_distance=1.7
                space.region_3d.view_location=target
                space.region_3d.view_rotation=scene.camera.rotation_euler.to_quaternion()
                space.shading.color_type='MATERIAL'
                space.overlay.show_overlays=False


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    out=p.parse_args(sys.argv[sys.argv.index("--")+1:]).out.resolve()
    if bpy.data.filepath or out.exists() or out.suffix!=".blend":
        raise ValueError("Start in a fresh Blender process and choose a NEW .blend path")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc=bpy.context.scene
    root=collection(MASTER,sc.collection)
    foam=collection("01 • Main upholstered forms",root)
    restraint=collection("02 • Head restraint",root)
    structure=collection("03 • Carriers",root)
    handed=collection("04 • Handed shields and controls",root)
    rails=collection("05 • Mounting envelope",root)
    rig=collection("REVIEW_ONLY",sc.collection)
    primary=material("Study • centre → Primary",(.48,.25,.118))
    secondary=material("Study • surrounds → Secondary",(.447,.222,.099))
    head=material("Study • headrest → Secondary",(.453,.230,.105))
    plastic=material("Study • structural graphite",(.044,.047,.050),.56)
    switch=material("Study • controls",(.024,.026,.029),.46)
    steel=material("Study • runner metal",(.18,.19,.20),.36,.78)
    dark_metal=material("Study • dark steel",(.064,.072,.080),.42,.64)
    back=backrest()
    cushion()
    rear_carrier(back)
    base()
    headrest()
    mechanisms()
    scene_setup(sc,rig)
    root["phase"]="R5-A: form only. Provisional dimensions. No production mapping applied."
    root["placement"]="Production datum X=.425; -Y forward, +X door side, metres."
    bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
