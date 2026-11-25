"""Consolidated cabin, Blender 5.2.2 LTS. No external geometry or texture pixels.
Run scripts/prepare-front-cabin.mjs first; finalization/KTX2 occurs outside Blender.
Exporter RNA checked against installed Blender; https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html
"""
import bpy
import bmesh
import sys
import math
import json
import time
import hashlib
from pathlib import Path
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
import front_cabin_constants as C
from cockpit_surfaces import closed_loft, smooth_outline
from lexus_l2b_cockpit import build_cockpit
from front_cabin_carbon import make_carbon, physical_uvs
sys.path.insert(0, str(C.ROOT/'.agents/skills/realistic-3d-craft/scripts'))
from craft_kit import bevel_and_smooth, rect_path

start = time.perf_counter()
C.OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system='METRIC'
bpy.ops.import_scene.gltf(filepath=str(C.OUT/'source-render.glb'))
parts=[]; delivered=[]; component=''
source_materials={m.name:m for m in bpy.data.materials}

def select(obj):
    bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj

for obj in list(bpy.context.scene.objects):
    if not obj.name.startswith('GEO_Seat_') or 'Passenger' in obj.name:
        bpy.data.objects.remove(obj,do_unlink=True);continue
    select(obj);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    side=-1 if 'Driver' in obj.name or obj.name=='GEO_Seat_Stitching_Front' else 1
    for vertex in obj.data.vertices:
        x,y,z=vertex.co; local=x-side*.38
        # Match shoulder/headrest taper without moving the existing panel seams apart.
        taper=max(0,min(1,(z-1.09)/.21))
        vertex.co.x=side*C.SEAT_CENTRE+local*(1-.065*taper)
        # Subtle cushion crown and lumbar support, applied to thread geometry as well.
        vertex.co.z += .004*math.exp(-(local/.19)**4-((y+.045)/.23)**4-((z-.49)/.065)**4)
        vertex.co.y -= .008*math.exp(-(local/.14)**4-((z-.73)/.15)**4-((y-.30)/.13)**4)
    # Submillimetre thread cylinders dominate the old mesh; reduce them before broad surfaces.
    dec=obj.modifiers.new('Budget-preserving detail reduction','DECIMATE')
    dec.ratio=C.STITCH_DECIMATION if 'Stitching' in obj.name else C.BODY_DECIMATION
    bpy.ops.object.modifier_apply(modifier=dec.name)
    delivered.append(obj)

# The accepted passenger was already mirrored from this driver. Preserve that
# derivation after reduction, avoiding independent decimator/UV seam drift.
for driver in list(delivered):
    passenger=driver.copy();passenger.data=driver.data.copy();bpy.context.collection.objects.link(passenger)
    passenger.name='GEO_Seat_Front_Passenger' if driver.name=='GEO_Seat_Front_Driver' else 'GEO_Seat_Stitching_Front_Passenger'
    passenger.data.name=passenger.name;passenger.scale.x=-1
    select(passenger);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    delivered.append(passenger)

def material(name,color,rough,metal=0):
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return mat

leather=source_materials['MAT_Dashboard_Trim'];steering=source_materials['MAT_Steering_Leather']
accent=source_materials['MAT_Cockpit_Accent'];black=source_materials['MAT_Cockpit_Black']
console_black=material('MAT_Console_Black',(.009,.010,.012),.42)
carbon=make_carbon(C.OUT)
metal=material('MAT_Console_Metal',(.46,.48,.50),.3,.7)

# Seeded owned leather microdetail; carbon maps are baked in front_cabin_carbon.
import numpy as np
rng=np.random.default_rng(22350)

# Smooth leather: owned stochastic micrograin, not the old L2A perforation pixels.
# Existing primary atlas spans .8 x .72m; no changes to Diamond/perforated UVs.
n=1024;fine=rng.normal(0,1,(n,n))
for _ in range(2):fine=(fine+np.roll(fine,1,0)+np.roll(fine,-1,0)+np.roll(fine,1,1)+np.roll(fine,-1,1))/5
height=fine*.000045;dx,dy=np.gradient(height,.72/n,.8/n)
normal=np.dstack((-dy,-dx,np.ones_like(fine)));normal/=np.linalg.norm(normal,axis=2,keepdims=True)
for role in ['base','normal','orm']:
    pixels=np.ones((n,n,4),dtype=np.float32)
    if role=='normal':pixels[:,:,:3]=normal*.5+.5
    elif role=='base':pixels[:,:,:3]=np.clip(.55+fine[:,:,None]*.012,0,1)
    else:pixels[:,:,0]=1;pixels[:,:,1]=np.clip(.80+fine*.07,.65,.95);pixels[:,:,2]=0
    image=bpy.data.images.new('front-cabin-classic-'+role,width=n,height=n,alpha=True)
    if role!='base':image.colorspace_settings.name='Non-Color'
    image.pixels.foreach_set(pixels.ravel());image.filepath_raw=str(C.OUT/('front-cabin-classic-'+role+'.png'));image.file_format='PNG';image.save()

def mesh(name,verts,faces,mat):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    for p in data.polygons:p.use_smooth=True
    parts.append(obj);return obj

def box(name,loc,size,mat,bevel=.006,rotation=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);obj=bpy.context.object;obj.name=name;obj.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    obj.data.materials.append(mat)
    if bevel:
        select(obj);bevel_and_smooth(obj,width=min(bevel,min(size)*.4),segments=3 if min(size)>.015 else 1)
        for mod in list(obj.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
    if rotation:obj.rotation_euler=rotation
    parts.append(obj);return obj

def tube(name,points,radius,mat,sides=6,closed=False):
    verts=[];faces=[];count=len(points)
    for i,p in enumerate(points):
        tangent=Vector(points[(i+1)%count])-Vector(points[(i-1)%count]) if closed else Vector(points[min(i+1,count-1)])-Vector(points[max(0,i-1)])
        tangent.normalize();ref=Vector((0,1,0))
        if abs(tangent.dot(ref))>.95:ref=Vector((1,0,0))
        u=tangent.cross(ref).normalized();v=tangent.cross(u)
        for k in range(sides):verts.append(Vector(p)+radius*(math.cos(k*math.tau/sides)*u+math.sin(k*math.tau/sides)*v))
    for i in range(count if closed else count-1):
        for k in range(sides):faces.append((i*sides+k,i*sides+(k+1)%sides,((i+1)%count)*sides+(k+1)%sides,((i+1)%count)*sides+k))
    if not closed:faces.extend([tuple(reversed(range(sides))),tuple((count-1)*sides+k for k in range(sides))])
    obj=mesh(name,verts,faces,mat)
    if not closed:
        obj.data.polygons[-1].use_smooth=False;obj.data.polygons[-2].use_smooth=False
    return obj

def finish_component(name):
    global parts
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts:obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();obj=bpy.context.object
    obj.name=name;obj.data.name=name;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(obj.data);bm.free()
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.012);bpy.ops.object.mode_set(mode='OBJECT')
    # The exporter cannot calculate tangent frames on the loft's n-gon caps.
    tri=obj.modifiers.new('Explicit tangent-safe triangles','TRIANGULATE');bpy.ops.object.modifier_apply(modifier=tri.name)
    # Cockpit grain remains physical microdetail. Console uses its own fixed finish.
    if name in ['GEO_Dashboard_Lexus','GEO_SteeringWheel_Lexus']:
        for uv in obj.data.uv_layers.active.data:uv.uv*=4
    physical_uvs(obj)
    delivered.append(obj);parts=[];return obj

build_cockpit('wheel',mesh,box,tube,steering,accent,black)
# Actual identifying geometry is removed before joining, not painted over.
for obj in list(parts):
    if obj.name in ['Lexus oval emblem','Raised Lexus L']:
        parts.remove(obj);bpy.data.objects.remove(obj,do_unlink=True)
for obj in parts:obj.location.x-=C.SEAT_CENTRE-.38
finish_component('GEO_SteeringWheel_Lexus')

build_cockpit('dashboard',mesh,box,tube,leather,accent,black)
active_w=C.DISPLAY_DIAGONAL/math.sqrt(1+1/C.DISPLAY_ASPECT**2);active_h=active_w/C.DISPLAY_ASPECT
for obj in parts:
    if obj.name=='Continuous upper dash and rolled fascia':
        # Use the existing bounded fascia faces below the leather brow, including
        # the field behind the passenger vent. No separate floating overlay.
        slot=len(obj.data.materials);obj.data.materials.append(carbon)
        for face in obj.data.polygons:
            centre=sum((obj.data.vertices[i].co for i in face.vertices),Vector())/len(face.vertices)
            if centre.x>.32 and .785<centre.z<.875 and centre.y>-.62:face.material_index=slot
    if obj.name in ['Continuous satin ribbon','Centre satin perimeter','Passenger vent satin outline']:
        obj.data.materials.clear();obj.data.materials.append(carbon)
        if obj.name=='Continuous satin ribbon':
            # Broaden the decorative strip within the existing fascia boundary.
            for i,v in enumerate(obj.data.vertices):v.co.z += -.006 if i%4<2 else .006
    if obj.name in ['Display curved housing','Inactive display glass']:
        # Width/height shrink about housing centre; no arbitrary 5.5in translation.
        sx=(active_w+.035)/.365 if obj.name=='Display curved housing' else active_w/.329
        sz=(active_h+.025)/.143 if obj.name=='Display curved housing' else active_h/.112
        for v in obj.data.vertices:v.co.x=.08+(v.co.x-.08)*sx;v.co.z=1.017+(v.co.z-1.017)*sz
    if any(word in obj.name for word in ['instrument','Instrument','Cowl','cowl']):obj.location.x-=C.SEAT_CENTRE-.38
# Centre audio/climate stack has its own descending fascia, tied to the lower console.
sections=[]
for y,z,w in [(-.515,.758,.203),(-.478,.69,.187),(-.426,.602,.156)]:
    sections.append([(-w,y-.018,z),(w,y-.018,z),(w,y+.018,z),(-w,y+.018,z)])
mesh('Descending centre stack',*closed_loft(sections),black)
for side in [-1,1]:tube('Stack satin edge',[(side*.206,-.49,.766),(side*.19,-.452,.697),(side*.159,-.40,.596)],.003,accent,6)
for row,z in enumerate([.733,.698,.666]):
    y=-.488+( .733-z)*.55
    box('Recessed audio climate strip',(0,y,z),(.326,.012,.022),black,.004)
    for j in range(6):box('Physical stack key',(-.132+j*.052,y+.007,z),(.043,.004,.009),black,.001)
for x in [-.17,.17]:
    tube('Audio dial',[(x,-.476,.730),(x,-.459,.730)],.013,accent,20)
    tube('Dial face',[(x,-.458,.730),(x,-.455,.730)],.010,black,20)
box('Centre-stack lower socket cover',(.055,-.407,.612),(.080,.014,.026),black,.003)
box('Glovebox padded lower fascia',(.47,-.565,.674),(.50,.115,.145),leather,.025)
box('Glovebox release',(.49,-.500,.710),(.064,.008,.012),black,.004)
finish_component('GEO_Dashboard_Lexus')

# Console shell: closed sides and bottom with actual cup recesses in the top deck.
outline=smooth_outline([(-.105,-.57),(.105,-.57),(.12,-.44),(.12,.32),(.095,.38),(-.095,.38),(-.12,.32),(-.12,-.44)],3)
sections=[[(x*s,y,.32 if i==0 else .545) for x,y in outline] for i,s in enumerate([.80,1])]
shell=mesh('Console structural body',*closed_loft(sections),console_black)
box('Forward console to stack transition',(0,-.454,.565),(.25,.16,.080),console_black,.012)
deck=box('Carbon console deck',(0,-.09,C.DECK_Z-.009),(.218,.68,.020),carbon,.009)
for cy in C.CUP_Y:
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=C.CUP_RADIUS+.002,depth=.16,location=(C.CUP_X,cy,C.DECK_Z-.02))
    cutter=bpy.context.object
    select(deck);mod=deck.modifiers.new('Physical cup opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    # Remove the underlying body roof at the same location so wells have real depth.
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=C.CUP_RADIUS+.002,depth=.10,location=(C.CUP_X,cy,.548))
    cutter=bpy.context.object;select(shell);mod=shell.modifiers.new('Cup clearance','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
for side in [-1,1]:
    tube('Padded console side rail',[(side*.115,.33,.582),(side*.12,.17,.582),(side*.12,-.18,.586),(side*.12,-.39,.596),(side*.145,-.48,.670)],.009,console_black,8)
    tube('Console edge satin strip',[(side*.111,.08,.570),(side*.111,-.32,.570),(side*.135,-.43,.596)],.002,metal,6)
# Touchpad and its palm support behind the selector (driver half).
box('Touchpad satin frame',(-.053,-.092,.578),(.096,.126,.009),metal,.009)
box('Remote touch surface',(-.053,-.092,.584),(.086,.115,.009),console_black,.006)
for x in [-.08,-.051,-.022]:box('Map menu back key',(x,-.158,.582),(.025,.016,.006),console_black,.002)
box('Touchpad palm support',(-.052,.025,.593),(.098,.075,.036),console_black,.018)
tube('Drive mode rotary knob',[(.054,.042,.575),(.054,.042,.595)],.024,metal,32)
tube('Drive mode face',[(.054,.042,.596),(.054,.042,.599)],.021,console_black,32)
for x in [.028,.080]:box('Mode adjacent button',(x,.078,.575),(.025,.022,.006),console_black,.003)
finish_component('GEO_Console_Body')

for label,cy in zip(['Front','Rear'],C.CUP_Y):
    rings=[]
    for radius,z in [(C.CUP_RADIUS+.001,C.DECK_Z+.002),(C.CUP_RADIUS-.002,C.DECK_Z-.005),(C.CUP_RADIUS-.005,C.DECK_Z-C.CUP_DEPTH),(.001,C.DECK_Z-C.CUP_DEPTH)]:
        rings.append([(C.CUP_X+radius*math.cos(i*math.tau/48),cy+radius*math.sin(i*math.tau/48),z)for i in range(48)])
    verts,faces=closed_loft(rings)
    # Open top; close the tiny bottom ring. This is a well, not a black disc.
    mesh('Recessed cup well',verts,faces[:-2]+[faces[-1]],console_black)
    tube('Cup rolled satin rim',[(C.CUP_X+C.CUP_RADIUS*math.cos(i*math.tau/48),cy+C.CUP_RADIUS*math.sin(i*math.tau/48),C.DECK_Z+.002)for i in range(48)],.0018,metal,6,True)
    for a in [0,math.tau/3,math.tau*2/3]:
        box('Cup retaining tab',(C.CUP_X+.034*math.cos(a),cy+.034*math.sin(a),C.DECK_Z-.019),(.009,.009,.022),console_black,.003)
    finish_component('GEO_Console_Cupholder_'+label)

sx,sy,sz=C.SELECTOR_CENTRE
box('Selector carbon surround',(sx,sy,.579),(.103,.158,.012),carbon,.012)
box('Selector boot recess',(sx,sy,.586),(.090,.145,.010),console_black,.012)
sections=[]
for z,rx,ry,shift in [(.589,.040,.064,0),(.605,.031,.052,.004),(.640,.017,.026,.009),(.662,.012,.017,.012)]:
    sections.append([(sx+rx*math.cos(i*math.tau/32)*(1+.045*math.sin(i*4)),sy+shift+ry*math.sin(i*math.tau/32),z) for i in range(32)])
mesh('Folded leather selector boot',*closed_loft(sections),console_black)
box('Standard leather selector grip',(sx,sy+.010,.687),(.043,.053,.075),console_black,.018,rotation=(math.radians(-12),0,0))
box('Selector satin front inset',(sx,sy-.014,.690),(.031,.010,.055),metal,.006,rotation=(math.radians(-12),0,0))
box('Selector release',(sx,sy+.037,.695),(.025,.009,.020),console_black,.005)
finish_component('GEO_Console_Selector')

box('Padded front centre armrest',C.ARMREST_CENTRE,C.ARMREST_SIZE,console_black,.030)
box('Armrest lower joint',(0,.22,.590),(.216,.302,.015),console_black,.012)
# Fine fixed tone-on-tone seam following the upholstered cover perimeter.
path=rect_path(.222,.31,.019,corner=.018,n=7)
tube('Armrest inset seam',[(x,y+.22,.6585)for x,y in path],.0006,console_black,4,True)
finish_component('GEO_Console_Armrest')

counts={}
for obj in delivered:
    # Historical -X driver coordinates made a right-hand-drive cabin when viewed
    # from inside. Mirror the complete assembly to match the selected US car.
    select(obj);obj.scale.x=-1;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    obj['measurementStatus']='Controlled photo approximation; not OEM CAD'
    obj['referenceRecord']='docs/review/front-cabin-2026-11-05/REFERENCES.md'
    obj.data.calc_loop_triangles();counts[obj.name]={'triangles':len(obj.data.loop_triangles),'dimensionsMetres':list(obj.dimensions)}
    assert all(math.isfinite(c) for v in obj.data.vertices for c in v.co)
total=sum(n['triangles']for n in counts.values());assert total<=80000,total
bpy.ops.object.select_all(action='DESELECT')
for obj in delivered:obj.select_set(True)
args=dict(filepath=str(C.OUT/'cabin-raw.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
    export_cameras=False,export_lights=False,export_extras=True,export_animations=False,export_skins=False,export_morph=False,
    export_tangents=True,export_texcoords=True,export_materials='EXPORT',export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,
    export_draco_texcoord_quantization=14,export_draco_generic_quantization=12)
assert all(k in bpy.ops.export_scene.gltf.get_rna_type().properties.keys() for k in args)
bpy.ops.export_scene.gltf(**args);bpy.ops.wm.save_as_mainfile(filepath=str(C.OUT/'front-cabin.blend'))
report={'blender':bpy.app.version_string,'seconds':time.perf_counter()-start,'triangles':total,'nodes':counts,
    'sourceHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),C.ROOT/'blender/front_cabin_constants.py',C.ROOT/'blender/front_cabin_carbon.py']},
    'activeDisplayMetres':[active_w,active_h],'seatCentresMetres':{'driver':C.SEAT_CENTRE,'passenger':-C.SEAT_CENTRE},
    'consoleWidthMetres':2*C.CONSOLE_HALF_WIDTH,'badgeGeometryRemoved':True}
(C.OUT/'build.json').write_text(json.dumps(report,indent=2));print('FRONT_CABIN_BUILD '+json.dumps(report),flush=True)
