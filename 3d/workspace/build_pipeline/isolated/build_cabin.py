"""Local candidate construction. Coordinates authored in glTF metres, converted to Blender Z-up.
Dimensions are provisional, anchored to accepted seats and gallery relationships, not OEM CAD.
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
STAGES=['A-frame','B1-floor','B2-rear','B3-doors','B4-pillars','B5-roof','B6-vents','C-cockpit']
stage=sys.argv[sys.argv.index('--')+1]; level=STAGES.index(stage)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'working_models/baseline-render.glb'))
base=list(bpy.context.scene.objects)
materials={m.name:m for m in bpy.data.materials}
new=[]; components=[]
def cv(p): return Vector((p[0],-p[2],p[1]))
def finish(obj,name,mat,ref):
    obj.name=name; obj.data.materials.clear();obj.data.materials.append(materials[mat]);new.append(obj)
    obj['reference']=ref;obj['dimension_status']='provisional'
    components.append({'name':name,'material':mat,'reference':ref,'dimensionStatus':'provisional'})
    return obj
def box(name,c,d,mat,bevel=.008,ref='07/23/29/31; provisional'):
    bpy.ops.mesh.primitive_cube_add(size=1,location=cv(c));o=bpy.context.object;o.dimensions=(d[0],d[2],d[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=o.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=1
        bpy.ops.object.modifier_apply(modifier=mod.name)
        for p in o.data.polygons:p.use_smooth=True
        mod=o.modifiers.new('Surface normals','WEIGHTED_NORMAL');mod.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=mod.name)
    return finish(o,name,mat,ref)
def beam(name,a,b,width,depth,mat,ref):
    mid=(Vector(a)+Vector(b))/2;delta=cv(b)-cv(a)
    o=box(name,mid,(width,delta.length,depth),mat,min(width,depth)*.18,ref)
    o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return o
# Curved padded panels avoid perfectly planar cushion highlights.
def pillow(name,c,d,mat,ref,tilt=0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=cv(c));o=bpy.context.object
    # Superellipsoid gives softened rectangular silhouette instead of an ellipsoid.
    for v in o.data.vertices:
        for axis in range(3): v.co[axis]=math.copysign(abs(v.co[axis])**.42,v.co[axis])
    o.scale=(d[0]/2,d[2]/2,d[1]/2);o.rotation_euler.x=tilt
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for p in o.data.polygons:p.use_smooth=True
    return finish(o,name,mat,ref)
def disc(name,c,r,depth,mat,axis='X',ref='24/31'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=depth,location=cv(c));o=bpy.context.object
    if axis=='X':o.rotation_euler.y=math.pi/2
    elif axis=='Z':o.rotation_euler.x=math.pi/2
    for p in o.data.polygons:p.use_smooth=True
    return finish(o,name,mat,ref)
F='MAT_Dashboard_Trim';K='MAT_Cockpit_Black';P='MAT_Seat_Primary';S='MAT_Seat_Secondary';C='MAT_Console_Carbon';M='MAT_Console_Metal'
box('Floor_connected_shell',(0,.245,-.40),(1.66,.055,2.72),F,.025)
for sign in [-1,1]:box('Sill_'+str(sign),(sign*.795,.30,-.42),(.075,.10,2.70),K,.015)
if level>=1:
    box('Centre_tunnel',(0,.30,-.40),(.30,.10,2.55),K,.035)
    for sign in [-1,1]:
        box('Front_carpet_'+str(sign),(sign*.445,.282,.42),(.56,.025,.68),F,.025)
        box('Rear_carpet_'+str(sign),(sign*.44,.282,-.75),(.57,.025,.58),F,.025)
        for x in [sign*.25,sign*.60]:box('Seat_rail',(x,.303,-.06),(.036,.045,.64),K,.006)
    box('Toe_board',(0,.40,.83),(1.52,.28,.09),F,.035)
if level>=2:
    box('Rear_bench_plinth',(0,.355,-1.225),(1.48,.16,.58),K,.045,'25/26/31/32')
    for i,x in enumerate([-.49,0,.49]):
        width=.45 if i!=1 else .43
        pillow('Rear_cushion_'+str(i),(x,.47,-1.18),(width,.19,.57),S,'26/32')
        pillow('Rear_insert_'+str(i),(x,.555,-1.17),(width*.70,.04,.43),P,'26/32')
        pillow('Rear_backrest_'+str(i),(x,.855,-1.455),(width,.65,.15),S,'26/32',-.12)
        pillow('Rear_back_insert_'+str(i),(x,.86,-1.365),(width*.71,.45,.025),P,'26/32',-.12)
        for dx in [-.065,.065]:beam('Rear_headrest_post',(x+dx,1.13,-1.49),(x+dx,1.27,-1.51),.013,.013,M,'26/32')
        pillow('Rear_headrest_'+str(i),(x,1.27,-1.50),(.29,.25,.14),S,'26/32')
        box('Rear_buckle_'+str(i),(x+.18,.54,-1.29),(.035,.035,.05),K,.008,'26/32; no unverified release markings')
    # Fold seams represented; no folding mechanism is claimed.
if level>=3:
    for sign in [-1,1]:
        for row,z,length in [('Front',.16,1.15),('Rear',-.99,1.10)]:
            ref='24' if row=='Front' else '25/31/32'
            box(row+'_door_shell_'+str(sign),(sign*.825,.65,z),(.075,.68,length),F,.035,ref)
            box(row+'_door_belt_'+str(sign),(sign*.805,.965,z),(.08,.09,length-.02),F,.02,ref)
            box(row+'_door_trim_'+str(sign),(sign*.779,.89,z-.06),(.022,.045,length*.69),C,.009,ref)
            pillow(row+'_door_insert_'+str(sign),(sign*.774,.73,z-.10),(.04,.23,length*.60),S,ref)
            box(row+'_door_armrest_'+str(sign),(sign*.733,.575,z-.04),(.16,.065,length*.70),S,.022,ref)
            box(row+'_door_storage_'+str(sign),(sign*.76,.385,z-.12),(.11,.16,length*.57),K,.025,ref)
            # Diagonal grab-handle sweep follows the gallery door-card hierarchy.
            beam(row+'_door_grab_'+str(sign),(sign*.747,.60,z+.02),(sign*.754,.865,z+.25),.024,.025,M,ref)
            box(row+'_door_handle_recess_'+str(sign),(sign*.765,.84,z+.25),(.035,.07,.19),K,.015,ref)
            box(row+'_door_handle_'+str(sign),(sign*.737,.845,z+.25),(.018,.018,.13),M,.006,ref)
            disc(row+'_speaker_'+str(sign),(sign*.773,.455,z+.35),.09,.013,K,ref=ref)
            for k in range(4 if row=='Front' and sign==1 else 1):box(row+'_window_switch_'+str(sign)+'_'+str(k),(sign*.705,.615,z+.06-k*.045),(.035,.012,.025),K,.003,ref)
if level>=4:
    for sign in [-1,1]:
        beam('A_pillar_'+str(sign),(sign*.78,.96,.84),(sign*.65,1.55,.27),.075,.075,F,'17/23/29')
        beam('B_pillar_'+str(sign),(sign*.82,.32,-.44),(sign*.70,1.57,-.44),.09,.075,F,'23/25/29')
        beam('C_pillar_'+str(sign),(sign*.81,.85,-1.60),(sign*.66,1.53,-1.38),.11,.085,F,'15/25/32')
        beam('Roof_side_rail_'+str(sign),(sign*.67,1.55,.29),(sign*.67,1.55,-1.42),.09,.09,F,'17/25')
        beam('Rear_belt_'+str(sign),(sign*.69,1.30,-1.48),(sign*.65,.57,-1.18),.035,.008,K,'26/32; static visual belt')
if level>=5:
    # Gallery17 supports two glazed openings and a central crossmember; no moving mechanism.
    for sign in [-1,1]:box('Headliner_side_'+str(sign),(sign*.58,1.565,-.55),(.22,.045,1.80),F,.025,'17')
    for z,width in [(.30,.22),(-.49,.12),(-1.43,.20)]:box('Roof_crossmember',(0,1.565,z),(1.30,.055,width),F,.02,'17')
    # Preserve existing material names: dark glossy static roof inserts, not optical glass simulation.
    for z,length in [(-.08,.62),(-.98,.77)]:box('Sunroof_closed_insert',(0,1.59,z),(.96,.018,length),K,.015,'17; reflective opaque approximation')
    box('Overhead_console',(0,1.52,.24),(.23,.05,.19),F,.018,'17')
    for sign in [-1,1]:
        box('Sunvisor_'+str(sign),(sign*.38,1.51,.29),(.35,.035,.20),F,.015,'17; folded, no labels')
        beam('Rear_grab_handle_'+str(sign),(sign*.65,1.49,-.85),(sign*.65,1.49,-1.02),.02,.025,K,'25/32')
if level>=6:
    box('Rear_vent_housing',(0,.46,-.455),(.28,.28,.12),K,.025,'31')
    for sign in [-1,1]:
        box('Rear_vent_recess',(sign*.068,.52,-.524),(.115,.095,.012),K,.008,'31')
        for j in range(4):box('Rear_vent_louvre',(sign*.068,.49+j*.019,-.535),(.103,.007,.012),M,.002,'31')
    box('Rear_lower_connection',(0,.35,-.525),(.20,.06,.018),K,.006,'31; ports not asserted')
if level>=7:
    # Visible decorative faces use the existing shared trim slot; upper deck stays fixed leather.
    box('Passenger_decorative_face',(-.43,.857,.509),(.53,.052,.025),C,.012,'07/33/35; bespoke finish')
    box('Display_hood_top',(0,1.074,.717),(.48,.018,.15),F,.008,'16/18/35')
    for x in [-.235,.235]:box('Display_hood_side',(x,1.035,.723),(.014,.09,.13),F,.006,'16/18/35')
    box('Console_touchpad',(.057,.579,.10),(.085,.015,.115),K,.008,'34')
    box('Touchpad_surround',(.057,.566,.10),(.102,.012,.135),C,.008,'34')
    for j in range(3):box('Console_switch_'+str(j),(.061,.594,.214+j*.021),(.065,.012,.014),K,.003,'19/34; neutral controls')
    # Layered boot folds around the baseline selector base; no shifter mechanics.
    for j in range(4):box('Shifter_boot_fold_'+str(j),(.056,.585+j*.011,.327),(.105-j*.014,.013,.14-j*.017),K,.006,'34')
    disc('Drive_mode_dial',(.063,.599,-.005),.025,.018,M,axis='Y',ref='34')
    for sign in [-1,1]:box('Dash_end_junction_'+str(sign),(sign*.753,.82,.60),(.06,.24,.19),F,.024,'23/29')
# Explicit component geometry census before joining.
component_counts=[]
for o in new:
    o.data.calc_loop_triangles();component_counts.append({'name':o.name,'triangles':len(o.data.loop_triangles)})
triangles=sum(x['triangles'] for x in component_counts)
if triangles+66260>80000:raise RuntimeError('STOP triangle budget before export: '+str(triangles+66260))
# UVs laid out consistently in metric-ish local projection. Baseline geometry/UVs untouched.
for o in new:
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    if not o.data.uv_layers:o.data.uv_layers.new(name='UVMap')
    uv=o.data.uv_layers.active.data
    for poly in o.data.polygons:
        normal=poly.normal; axis=max(range(3),key=lambda a:abs(normal[a]));axes=[a for a in range(3) if a!=axis]
        for li in poly.loop_indices:
            v=o.data.vertices[o.data.loops[li].vertex_index].co
            uv[li].uv=(v[axes[0]]*2,v[axes[1]]*2)
# One static expansion mesh; six existing materials maximum.
bpy.ops.object.select_all(action='DESELECT')
for o in new:o.select_set(True)
bpy.context.view_layer.objects.active=new[0];bpy.ops.object.join();added=bpy.context.object;added.name='GEO_Cabin_Expansion';added['component_names']='|'.join(c['name'] for c in components)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'working_models'/f'{stage}-additions.glb'),export_format='GLB',use_selection=True,export_texcoords=True,export_normals=True,export_tangents=True,export_materials='EXPORT',export_cameras=False,export_lights=False)
# Review-only runtime colour emulation, applied AFTER additions export; GLB factors stay unchanged.
colours={'MAT_Seat_Primary':'191A1E','MAT_Seat_Secondary':'191A1E','MAT_Seat_Stitching':'565860','MAT_Dashboard_Trim':'2A2B2E','MAT_Cockpit_Black':'121316','MAT_Cockpit_Accent':'787D82','MAT_Steering_Leather':'191A1E'}
for name,h in colours.items():
    mat=materials[name]; rgb=[int(h[i:i+2],16)/255 for i in (0,2,4)]; linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    bsdf=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    socket=bsdf.inputs['Base Color']
    # Imported texture multiplied by runtime tint, matching the application's colour semantics.
    if socket.is_linked:
        link=socket.links[0]; source=link.from_socket;mat.node_tree.links.remove(link)
        mix=mat.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*linear,1)
        mat.node_tree.links.new(source,mix.inputs[1]);mat.node_tree.links.new(mix.outputs[0],socket)
    else:socket.default_value=(*linear,1)
# Review scene: baseline PNG materials plus new surfaces; embedded textures packed in source.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.use_denoising=True
scene.render.resolution_x=900;scene.render.resolution_y=650;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Review studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.20,.23,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.45
scene.view_settings.view_transform='AgX'
def light(name,pos,power,size,target):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=cv(pos);o.rotation_euler=(cv(target)-o.location).to_track_quat('-Z','Y').to_euler()
light('Large softbox',(.3,3.5,-.3),1200,4,(0,.7,-.3));light('Front fill',(-2.0,2,1.4),900,3,(0,.8,-.3));light('Rear edge',(2,2,-2),1100,3,(0,.8,-.7))
camdata=bpy.data.cameras.new('Inspection camera');cam=bpy.data.objects.new('Inspection camera',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.lens=42
cam.location=cv((2.75,2.65,-3.1));target=cv((0,.78,-.45));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
# Roof is not hidden in the saved full model. Extra cutaway inspection is generated separately.
reportdir=ROOT/'reports'/stage;reportdir.mkdir(parents=True,exist_ok=True)
(reportdir/'construction.json').write_text(json.dumps({'stage':stage,'newTriangles':triangles,'components':components,'componentTriangleCounts':component_counts,'gaps':['all dimensions provisional','rear-seat upholstery UV layout provisional; fine detailing deferred','closed roof glazing uses existing opaque material; no new slot','hidden mechanics not reconstructed','browser integration and human acceptance not performed']},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'working_models'/f'{stage}.blend'))
scene.render.filepath=str(reportdir/'context.png');bpy.ops.render.render(write_still=True)
print('MILESTONE',stage,'NEW_TRIANGLES',triangles)

