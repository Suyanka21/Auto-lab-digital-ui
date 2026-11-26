"""R6-A editable form. Blender 5.2.2, metres, X lateral / -Y forward / Z up."""
import argparse
import importlib.util
from math import cos, exp, pi, sin
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r5_sections", D.parent / "R5-A/build.py")
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
ROOT = "R6_REAR_BENCH_MASTER"
PRIMARY = D.parents[1] / "AUTOLAB_INTERIOR_3D_REFERENCE_PACK/04_REAR_BENCH/PRIMARY/AUTOLAB_SUV_REAR_BENCH_PRIMARY_01.jpg"
OUTERS = ((-1, "LH"), (1, "RH"))
CENTER = .442
INNER = .166
BOTTOM = .255  # Stand height for inspection only.


def loft(name, rows, materials, group, **kwargs):
    obj = tool.loft(name, rows, materials, group, **kwargs)
    obj.location.x = 0  # The shared section helper defaults to R5's driver station.
    return obj


def rounded_volume(name, stations, mat, group, exponent=.44, sub=2):
    """Horizontal rounded rings defined by (z, centre X/Y, half width/depth)."""
    rows = [[(cx+x, cy+y, z) for x, y in tool.rounded_section(w, d, exponent)]
            for z, cx, cy, w, d in stations]
    return loft(name, rows, [mat], group, subdiv=sub)


def face_y(z):
    return 1.189 + .32 * (z - .505)


def outer_back(sign, tag, group, mats):
    # Shoulder contact area flares above the waist. The lower wings project
    # forward and the far outboard corner rises to clear the pivot cover.
    rows, faces, indices = [], [], []
    for z, w, depth, wing, insert, crown in (
        (.483,.241,.068,.017,.52,.090), (.496,.263,.099,.028,.53,.093),
        (.534,.271,.124,.050,.55,.090), (.589,.274,.128,.057,.53,.054),
        (.705,.274,.127,.061,.48,.006), (.824,.273,.125,.060,.49,0),
        (.895,.272,.122,.049,.54,0), (.940,.271,.117,.033,.66,0),
        (1.011,.270,.112,.018,.77,0), (1.087,.267,.101,.008,.71,0),
        (1.115,.255,.090,.004,.66,0), (1.123,.238,.064,0,.64,0),
    ):
        y = face_y(z) - .015 * exp(-((z-.68)/.12)**2) - .012*exp(-((z-.57)/.048)**2)
        half = [(0,0), (insert*.55,.003), (insert*.93,.004),
                (insert,.004), (insert+.055,-.12*wing), ((1+insert)/2,-.73*wing),
                (.91,-wing), (.968,-.88*wing), (.995,-.35*wing), (1.007,.30*depth)]
        across = [(-t,dy) for t,dy in reversed(half[1:])] + half
        front, rear = [], []
        for t, dy in across:
            step = max(0, min(1, (t-.66)/.22))
            shoulder = .013 * abs(t)**3 * max(0, min(1, (z-1.05)/.07))
            x = sign*(CENTER+w*t)
            zz = z+crown*step*step*(3-2*step)-shoulder
            # Broad foam crowns meet across a shallow, swept transition.
            relief = (.011*exp(-((z-.875+.045*t*t)/.047)**2)
                      - .012*exp(-((z-1.006)/.095)**2)) * max(0,1-abs(t)**4)
            front.append((x, y+dy+relief, zz))
            rear.append((x, y+depth*(1-.27*abs(t)**16), zz))
        rows.append(front+rear[::-1])
    # Close the lifted outside corner with paired front/rear stations. A
    # single n-gon would triangulate across its curved undercut.
    n = len(across)
    stride = 2*n
    for j in range(len(rows)-1):
        for i in range(stride):
            a, b = j*stride+i, j*stride+(i+1)%stride
            faces.append((a,b,b+stride,a+stride))
            mid = n//2
            indices.append(int(not mid-3 <= i < mid+3))
    for end in (0, len(rows)-1):
        offset = end*stride
        for i in range(n-1):
            faces.append(tuple(offset+k for k in (i,i+1,stride-2-i,stride-1-i)))
            indices.append(1)
    obj = tool.mesh("Backrest • "+tag,sum(rows,[]),faces,mats,group,indices=indices,subdiv=2)
    obj.location.x = 0


def pan(name, xmin, xmax, central, group, mats):
    # Sagittal sections wrap from the leading face over the thigh support
    # into the rear tuck. Inside corners retreat at the buckle wells.
    profile = [
        (.748,.458,0),(.747,.489,0),(.757,.520,.003),(.787,.537,.007),
        (.840,.541,.013),(.924,.532,.025),(1.038,.514,.034),(1.113,.507,.030),
        (1.179,.507,.019),(1.211,.499,.009),(1.227,.477,0),(1.224,.434,0),
        (1.204,.418,0),(1.117,.414,0),(.898,.414,0),(.783,.419,0),(.755,.430,0)]
    span = xmax-xmin
    stations = (-1,-.983,-.93,-.78,-.60,-.54,-.28,0,.28,.54,.60,.78,.93,.983,1)
    rows = []
    for t in stations:
        x = (xmin+xmax)/2 + t*span/2
        h = exp(-((abs(t)-.80)/.22)**2)
        edge = abs(t)**12
        well = exp(-((abs(x)-INNER)/.054)**4)
        row = []
        for y,z,lift in profile:
            # Round the door-side plan corners more than the shared boundaries.
            nose = (.020 + .053*(abs(x)/.718)**5) * edge * max(0, (1.0-y)/.25)**2
            tuck = well*.085*max(0, min(1, (y-1.07)/.14))**2
            zz = .47+(z-.47)*(1-.17*edge) + h*lift*(.25 if central else 1)
            row.append((x,y+nose-tuck,zz))
        rows.append(row)
    loft(name, rows, mats, group, region=lambda j,i:
         int(central or abs((stations[j]+stations[j+1])/2)>.57 or not 1<=i<=9), caps=(1,1))


def centre(group, mats):
    leather, trim, dark = mats
    def block(name, cx, w, lo, hi, front, depth, mat):
        levels = ((lo,.90,.71),(lo+.004,.97,.92),(lo+.015,1,1),
                  ((lo+hi)/2,1,1),(hi-.012,.999,.99),(hi-.003,.97,.9),(hi,.92,.72))
        return rounded_volume(name, [(z,cx,face_y(z)+front+depth/2,w*s,depth*k/2)
                              for z,s,k in levels], mat, group, .31)
    block("Centre • backing",0,.163,.515,1.113,.077,.034,dark)
    block("Centre • lower bolster",0,.159,.488,.641,-.014,.100,trim)
    block("Centre • headrest bridge",0,.162,1.046,1.122,-.002,.104,trim)
    for sign,tag in OUTERS:
        block("Centre • reveal "+tag,sign*.153,.009,.640,1.048,.006,.075,trim)
    leaf = block("Centre • stowed armrest",0,.142,.644,1.043,-.007,.077,leather)
    # Put the editable leaf origin at the lower crosswise axis. Keep its shape
    # in the stowed position; no assumed hinge or latch kinematics.
    pivot = Vector((0,face_y(.650)+.038,.650))
    for v in leaf.data.vertices:
        v.co -= pivot
    leaf.location = pivot
    leaf["pose"] = "Stowed. Local X is the provisional fold-down axis."
    # A soft pull tab folded over the top edge of the leaf.
    rows=[]
    for z,dy,w in ((1.041,.013,.0088),(1.043,-.001,.009),
                   (1.039,-.010,.009),(1.023,-.014,.009),(1.001,-.018,.0082)):
        rows.append([(x,face_y(z)+dy+y,z) for x,y in tool.rounded_section(w,.0024,.5,16)])
    tab=loft("Centre • armrest pull",rows,[trim],group,subdiv=1)
    tab.parent=leaf
    tab.location=-pivot


def restraint(cx, tag, central, group, head, plastic, steel):
    w=.115 if central else .122
    if central:
        levels = [(1.126,.77,.035),(1.130,.91,.052),(1.142,.99,.065),
                  (1.164,1,.066),(1.209,.99,.061),(1.233,.94,.055),
                  (1.242,.82,.043),(1.244,.65,.032)]
    else:
        levels = [(1.134,.81,.046),(1.140,.95,.062),(1.155,1,.070),
                  (1.219,.99,.072),(1.285,.90,.065),(1.316,.83,.056),
                  (1.326,.73,.043),(1.329,.61,.032)]
    def axis(z):
        return 1.427 + .22*(z-1.134)
    rounded_volume("Headrest • "+tag,[(z,cx,axis(z),w*k,d) for z,k,d in levels],
                   head,group,.50)
    for side, suffix in ((-1,"a"),(1,"b")):
        x=cx+side*(.059 if central else .065)
        for part,r,lo,hi,mat in (("Guide",.012,1.114,1.127,plastic),
                                  ("Post",.006,1.118,levels[0][0]+.019,steel)):
            rounded_volume(f"{part} • {tag} {suffix}",
                         [(z,x,axis(z),r*k,r*k) for z,k in
                          ((lo,.88),(lo+.001,1),(hi-.001,1),(hi,.88))],mat,group,1.,1)


def structure(group, plastic, felt, steel):
    # The visible lateral division is at the inner boundary of one outer seat.
    # Approx. 38:62 of total width; separate rear boards and lower valances.
    for tag, left, right in (("narrow",-.714,-.169),("wide",-.164,.714)):
        rows=[]
        for f in (0,.006,.022,.06,.16,.33,.50,.67,.84,.94,.978,.994,1):
            x=left+f*(right-left)
            end=(abs(x)/.714)**10
            rows.append([(x,y+end*off,z+end*lift) for y,z,off,lift in (
                (.752,.396,.084,0),(.756,.429,.080,.001),(.775,.444,.073,0),
                (1.204,.444,-.015,0),(1.247,.459,-.015,0),(1.275,.502,-.014,0),
                (1.285,.540,-.015,0),(1.309,.548,-.016,0),(1.327,.537,-.016,0),
                (1.336,.465,-.016,0),(1.332,.368,-.014,.002),(1.309,.348,-.012,.005),
                (1.231,.337,0,.007),(.859,.329,.034,.009),(.787,.340,.062,.004),
                (.759,.360,.081,.006))])
        loft("Plinth • "+tag,rows,[plastic],group)
        # Taper and slope the split load face with the backrest rake.
        rows=[]
        for z, shrink in ((.513,.019),(.519,.008),(.536,.003),(.646,.002),
                          (.815,.002),(1.000,.003),(1.063,.006),(1.087,.017),(1.092,.027)):
            depth=.122-.020*max(0,(z-.81)/.282)
            cx=(left+right)/2
            row=[(cx+x,face_y(z)+depth+.009+y,z)
                 for x,y in tool.rounded_section((right-left)/2-shrink,.013,.27)]
            rows.append(row)
        loft("Rear load face • "+tag,rows,[felt],group)
    for sign,tag in OUTERS:
        x=sign*.675
        rows=[[(x+dx,y+dy,z) for dx,dy in tool.rounded_section(w,d,.50)]
              for z,y,w,d in ((.420,1.237,.027,.067),(.436,1.240,.038,.080),
                               (.490,1.242,.041,.078),(.560,1.243,.040,.069),
                               (.619,1.255,.036,.051),(.639,1.265,.025,.033))]
        loft("Pivot cover • "+tag,rows,[plastic],group)
    # Four low pressed mounting brackets with turned lips and a cut-out under the saddle.
    for i,x in enumerate((-.616,-.259,.259,.616),1):
        profile=[(.774,0),(.832,0),(.853,.023),(.870,.061),
                 (1.205,.070),(1.234,.023),(1.250,.011),(1.301,.011),
                 (1.301,.018),(1.252,.018),(1.242,.029),(1.218,.084),
                 (.861,.075),(.845,.030),(.825,.008),(.774,.008)]
        rows=[[(xx,y,BOTTOM+z+min(1,z/.065)*.013) for y,z in profile] for xx in (x-.027,x+.027)]
        loft(f"Foot • {i}",rows,[steel],group,subdiv=0,bevel=.0025)


def receivers(group, plastic, button):
    # Three visible receptacles in the two rear cushion wells; only the
    # envelope and release surface are represented in this form study.
    for i,(x,y) in enumerate(((-.183,1.157),(-.148,1.156),(.166,1.157)),1):
        rounded_volume(f"Receiver • {i}",[(z,x,y+offset,w,d) for z,offset,w,d in (
            (.443,.020,.009,.015),(.464,.016,.012,.018),(.486,.009,.014,.019),
            (.509,0,.014,.019),(.515,-.002,.012,.016))],plastic,group,.42,1)
        rounded_volume(f"Release • {i}",[(z,x,y+offset,w,d) for z,offset,w,d in (
            (.511,-.004,.009,.011),(.516,-.006,.010,.011),(.519,-.006,.009,.010))],
            button,group,.4,1)


CAMERAS = {
    "three-quarter": ((0,1.11,.760),(-1.92,-3.89,1.16),2.22),
    "front": ((0,1.10,.794),(0,-3,0),1.82),
    "side": ((0,1.12,.794),(-3,0,0),1.78),
    "rear": ((0,1.10,.794),(0,3,0),1.82),
    "cabin": ((0,.33,.76),(-2.85,-.90,2.55),3.42),
}


def studio(sc):
    rig=tool.collection("R6 • review studio",sc.collection)
    for name,(target,vec,width) in CAMERAS.items():
        cam=bpy.data.objects.new("R6 / "+name,bpy.data.cameras.new("R6 / "+name))
        rig.objects.link(cam)
        cam.location=Vector(target)+Vector(vec)
        tool.point_at(cam,target)
        cam.data.type,cam.data.ortho_scale="ORTHO",width
        if name=="three-quarter":
            cam.data.type,cam.data.lens="PERSP",70
    sc.camera=rig.objects["R6 / three-quarter"]
    im=bpy.data.images.load(str(PRIMARY))
    im.pack()
    im.filepath="//"+PRIMARY.name
    sc.camera.data.background_images.new().image=im
    sc.camera.data.show_background_images=False
    for name,pos,size,power in (("Key",(-1.9,-.95,3.1),2.1,170),
                                ("Fill",(1.85,-.4,1.9),1.6,103),
                                ("Rim",(.8,2.85,2.8),1.6,155)):
        data=bpy.data.lights.new(name,"AREA")
        data.energy,data.shape,data.size=power,"DISK",size
        obj=bpy.data.objects.new("R6 / "+name,data)
        rig.objects.link(obj)
        obj.location=pos
        tool.point_at(obj,(0,1.02,.75))
    stand=tool.mesh("Studio stand",[(x,y,BOTTOM-.001) for x,y in
                    ((-100,-100),(100,-100),(100,100),(-100,100))],[(0,1,2,3)],
                    [tool.material("Studio • stone",(.25,.24,.222),.85)],rig)
    stand.location.x=0
    sc.world=bpy.data.worlds.new("Studio environment")
    sc.world.use_nodes=True
    bg=sc.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value=(.52,.54,.57,1)
    bg.inputs[1].default_value=.53
    sc.unit_settings.system="METRIC"
    sc.render.engine="CYCLES"
    sc.cycles.device="CPU"
    sc.cycles.samples=32
    sc.cycles.seed=11
    sc.cycles.use_denoising=True
    sc.cycles.denoising_input_passes="RGB_ALBEDO_NORMAL"
    sc.view_settings.view_transform="AgX"
    sc.view_settings.look="AgX - Medium High Contrast"
    sc.render.resolution_x,sc.render.resolution_y=1400,960
    sc.render.resolution_percentage=100
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=="VIEW_3D":
                space=area.spaces.active
                space.region_3d.view_location=CAMERAS["three-quarter"][0]
                space.region_3d.view_rotation=sc.camera.rotation_euler.to_quaternion()
                space.region_3d.view_distance=2.5
                space.overlay.show_overlays=False
                space.shading.color_type="MATERIAL"


def build(out):
    if bpy.data.filepath or out.exists() or out.suffix!=".blend":
        raise ValueError("Start fresh and supply an unused .blend path")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc=bpy.context.scene
    root=tool.collection(ROOT,sc.collection)
    foam=tool.collection("01 • Three seating positions",root)
    middle=tool.collection("02 • Centre back and armrest",root)
    heads=tool.collection("03 • Rear restraints",root)
    base=tool.collection("04 • Base and split back carriers",root)
    belts=tool.collection("05 • Belt receivers",root)
    insert=tool.material("R6 • centre upholstery",(.205,.100,.036),.51)
    bolster=tool.material("R6 • surrounding upholstery",(.16,.073,.026),.53)
    head=tool.material("R6 • head restraints",(.156,.071,.026),.51)
    arm=tool.material("R6 • armrest face",(.186,.086,.030),.53)
    plastic=tool.material("R6 • structural graphite",(.044,.047,.050),.57)
    felt=tool.material("R6 • load face",(.062,.060,.059),.85)
    steel=tool.material("R6 • pressed metal",(.13,.14,.15),.42,.72)
    release=tool.material("R6 • receiver release",(.31,.020,.011),.58)
    for sign,tag in OUTERS:
        outer_back(sign,tag,foam,[insert,bolster])
        xmin,xmax=sorted((sign*INNER,sign*.718))
        pan("Cushion • "+tag,xmin,xmax,False,foam,[insert,bolster])
        restraint(sign*CENTER,tag,False,heads,head,plastic,steel)
    pan("Cushion • centre",-.163,.163,True,foam,[insert,arm])
    centre(middle,[arm,bolster,plastic])
    restraint(0,"centre",True,heads,head,plastic,steel)
    structure(base,plastic,felt,steel)
    receivers(belts,plastic,release)
    root["stage"]="R6-A overall form; dimensions inferred from images; floor anchorage unresolved."
    studio(sc)
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("out",type=Path)
    build(p.parse_args(sys.argv[sys.argv.index("--")+1:]).out.resolve())
