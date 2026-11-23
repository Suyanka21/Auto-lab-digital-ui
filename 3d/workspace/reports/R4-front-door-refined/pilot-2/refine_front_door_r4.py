"""One focused refinement of the saved R4 master. No factory reset or runtime export."""
import bpy,math,json,ast,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];OUT=R/'reports/R4-front-door-refined';MM=.00146
source=R/'working_models/R4-front-door-master.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));S=bpy.context.scene
components=bpy.data.collections['R4_FRONT_DOOR_MASTER'];rig=bpy.data.collections['REVIEW_CAMERAS_AND_LIGHTS'];parts=[]
# Reuse first-party construction helpers without executing the original build/reset/save statements.
tree=ast.parse((R/'build_pipeline/isolated/build_front_door_r4.py').read_text())
helpers=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[])
exec(compile(helpers,'r4_existing_helpers','exec'))
materials={k:bpy.data.materials['R4_MASTER_'+v] for k,v in {'leather':'Cognac_Padded_Leather','black':'Black_Padded_Leather','plastic':'Textured_Structural_Plastic','rubber':'Soft_Black_Recess','metal':'Satin_Aluminium','thread':'Cognac_Thread','wood':'Walnut_Trim','grille':'Perforated_Speaker_Metal'}.items()};globals().update(materials)
original={o.name:{'vertices':[tuple(v.co) for v in o.data.vertices],'material':[m.name for m in o.data.materials]} for o in components.objects if o.type=='MESH'}
replaced=[]
def remove(*names):
 for name in names:
  o=bpy.data.objects.get(name)
  if o:replaced.append(name);bpy.data.objects.remove(o,do_unlink=True)
def record(o,why):o['refinement_reason']=why;return o
# A: replace only the upholstered grip/armrest section and return. Keep the reference opening.
remove('Continuous_grip_and_armrest_upholstery','Supported_under_grip_return','Armrest_rear_support','Armrest_upper_double_stitch_A','Armrest_upper_double_stitch_B','Armrest_front_join')
# Each section is a rounded but asymmetric perimeter: top-back, top-front, front face, bottom-back.
# x, upper back pixel y/depth, upper front y/depth, lower front y/depth, lower back y/depth.
sections=[
 (414,271,.052,273,.073,282,.075,280,.050),
 (420,260,.055,268,.092,294,.094,286,.052),
 (429,263,.058,275,.105,306,.105,294,.055),
 (441,283,.064,296,.126,330,.124,312,.061),
 (467,315,.069,328,.149,361,.145,341,.067),
 (502,337,.076,347,.163,380,.160,361,.074),
 (548,342,.078,360,.169,387,.164,371,.075),
 (625,342,.078,363,.169,388,.163,372,.075),
 (682,337,.077,364,.168,389,.159,375,.074),
 (721,321,.073,364,.165,412,.151,409,.066),
 (800,325,.069,366,.158,414,.147,411,.062),
 (883,330,.061,368,.143,412,.128,408,.052),
 (922,338,.049,366,.109,407,.096,402,.043),
 (933,347,.044,365,.077,397,.073,390,.039)]
# Smooth section interpolation is bounded to these profile landmarks; no subdivision increase.
station=curvepoints(sections,148);verts=[];uv=[];profile_count=24
for p in station:
 x=p[0];yb,db,yf,df,yl,dl,yk,dk=p[1:]
 corners=[Vector((yb,db)),Vector((yf,df)),Vector((yl,dl)),Vector((yk,dk))]
 # Rounded rectangular corners using quadratic local interpolation, 6 samples per corner.
 ring=[]
 for j,c in enumerate(corners):
  before=c.lerp(corners[(j-1)%4],.22);after=c.lerp(corners[(j+1)%4],.22)
  for k in range(6):
   t=k/5;ring.append((1-t)**2*before+2*(1-t)*t*c+t*t*after)
 for j,q in enumerate(ring):
  # Submillimetre upholstery tension localised around the bend and the termination.
  compression=.00055*math.exp(-((x-490)/48)**2)*math.sin((x-455)*.15)*(1 if j<12 else .3)
  verts.append(loc(x,q.x,q.y+compression));uv.append(((x-429)*MM,j/profile_count*.16))
faces=[(i*profile_count+j,i*profile_count+(j+1)%profile_count,(i+1)*profile_count+(j+1)%profile_count,(i+1)*profile_count+j) for i in range(len(station)-1) for j in range(profile_count)]
faces += [tuple(reversed(range(profile_count))),tuple(range((len(station)-1)*profile_count,len(station)*profile_count))]
record(linkmesh('Continuous_grip_and_armrest_upholstery',verts,faces,leather,uv,1),'Asymmetric flatter face and sloping top deck; reference-led taper instead of inflated tube section')
# Broad upholstered lower return bounded by the visible opening, rather than a thin tubular loop.
record(strip('Supported_under_grip_return',[(492,369),(523,392),(562,403),(646,403),(694,405),(715,412)],[(505,389),(541,412),(575,418),(651,418),(697,418),(716,416)],leather,nu=72,nv=10,subd=1,depth_fn=lambda u,t,q:.100-.016*t+.004*math.sin(math.pi*t),thickness=.005),'Broad return frames a real opening under the grip; inferred concealed depth')
record(strip('Armrest_rear_support',[(720,405),(800,407),(888,404),(924,386)],[(722,415),(800,417),(890,414),(923,397)],leather,nu=58,nv=8,subd=1,depth=.074,crown=.003),'Reduced support fits the thinner front face')
stitchpath=[(433,271,.08),(444,295,.10),(475,333,.14),(514,355,.16),(552,367,.17),(630,370,.17),(720,371,.16),(803,373,.15),(881,374,.14),(921,371,.10)]
stitches('Armrest_upper_double_stitch_A',stitchpath);stitches('Armrest_upper_double_stitch_B',stitchpath,.0026)
sweep('Armrest_front_join',[(548,359,.171),(550,373,.169),(561,386,.164)],thread,.00032,.00032,ns=24,sides=6)
# Subtle local insert tension, preserving the original section topology and boundaries.
insert=bpy.data.objects['Sculpted_upholstery_insert']
for v in insert.data.vertices:
 x=v.co.x/MM+620;y=632-v.co.z/MM
 v.co.y+=.0006*math.exp(-((x-461)/62)**2-((y-287)/34)**2)*math.sin((y-262)*.30)
record(insert,'Submillimetre local compression at grab attachment; no global noisy displacement')
remove('Insert_double_stitch_A','Insert_double_stitch_B')
seam=[(367,357,.057),(411,299,.064),(460,272,.066),(596,250,.067),(785,239,.064),(957,231,.056)]
stitches('Insert_double_stitch_A',seam);stitches('Insert_double_stitch_B',seam,.0026)
# B: remove the intersecting pocket/shoulder surfaces and recreate a shared continuous boundary.
remove('Pocket_interior_back','Pocket_front_moulded_wall','Pocket_open_mouth_lip','Pocket_inner_floor_and_front_return','Pocket_Leading_end_wall','Pocket_Trailing_end_wall','Integrated_speaker_shoulder')
centre=Vector((333,519));a0=-.67;a1=1.0

def shoulder_radius(a):
 sn=math.sin(a);cs=math.cos(a)
 # Smooth elliptical envelope avoids the previous hard min() radius kinks.
 rx=112 if cs>=0 else 97;ry=122 if sn<0 else 83
 return 1/math.sqrt((cs/rx)**2+(sn/ry)**2)
def shoulder_depth(a):return .025+.115*max(math.cos(a),0)**2*(1-.65*max(0,math.sin(a)))
def boundary(a):
 rr=shoulder_radius(a);return centre+Vector((math.cos(a)*rr,math.sin(a)*rr))
left=[boundary(a0+(a1-a0)*j/40) for j in range(41)]
start=left[0];end=left[-1]
ptop=[tuple(start),(447,496),(474,525),(560,527),(735,521),(892,515)]
pbottom=[tuple(end),(460,608),(570,615),(685,622),(790,619),(864,581)]
def pocket_depth(u,t,q):
 edge=shoulder_depth(a0+(a1-a0)*t);main=.143-.075*t+.005*math.sin(math.pi*t)
 return edge*(1-u)**2+main*(1-(1-u)**2)
record(strip('Pocket_front_moulded_wall',ptop,pbottom,plastic,nu=90,nv=28,subd=1,depth_fn=pocket_depth,left_boundary=[tuple(p) for p in left]),'Curved front wall meets new speaker envelope; no overlapping patch')
# Shoulder ring shares the pocket edge profile. No clamped-radius crease.
verts=[];faces=[];N=160
for fraction in [1,.82,.55,.28,.09,0]:
 for j in range(N):
  a=j*math.tau/N;rr=77+(shoulder_radius(a)-77)*fraction;q=centre+Vector((math.cos(a)*rr,math.sin(a)*rr));depth=.074+(shoulder_depth(a)-.074)*fraction**1.4+.008*math.sin(math.pi*fraction)
  verts.append(loc(q.x,q.y,depth))
for k in range(5):
 for j in range(N):a=k*N+j;b=k*N+(j+1)%N;faces.append((a,b,b+N,a+N))
record(linkmesh('Integrated_speaker_shoulder',verts,faces,plastic,subd=1),'Smooth elliptical envelope with continuous depth transition into the pocket wall')
lip_path=[]
for i,p in enumerate(curvepoints(ptop,100)):
 u=i/99;lip_path.append((p.x,p.y,pocket_depth(u,0,p)+.001))
sweep('Pocket_open_mouth_lip',lip_path,plastic,.0023,.0032,ns=100,sides=12)
# Reference opening is concentrated at left/centre. The right lower panel slopes down to its mouth.
strip('Pocket_interior_back',[(429,456),(542,450),(670,451),(706,462)],[(472,526),(551,529),(637,528),(687,523)],rubber,depth=.026,crown=.002,nu=60,nv=12,subd=1)
record(strip('Pocket_Trailing_end_wall',[(737,416),(793,417),(857,416),(913,409)],[(686,524),(747,522),(823,519),(892,515)],plastic,nu=66,nv=16,subd=1,depth_fn=lambda u,t,q:.090+.050*t+.012*math.sin(math.pi*t)*math.sin(math.pi*u),thickness=.004),'Visible broad sloping right panel from the approved reference; replaces generic narrow end wall')
left_inside=curvepoints([tuple(start),(432,477),(450,511),(474,525)],36)
verts=[loc(p.x,p.y,d) for d in [.026,.096] for p in left_inside];faces=[(i,i+1,i+37,i+36) for i in range(35)]
linkmesh('Pocket_Leading_end_wall',verts,faces,plastic,subd=1,thickness=.003)
floorpath=curvepoints([(452,513),(477,527),(553,530),(636,528),(688,524)],60)
verts=[loc(p.x,p.y,d) for d in [.026,.141] for p in floorpath];faces=[(i,i+1,i+61,i+60) for i in range(59)]
linkmesh('Pocket_inner_floor_and_front_return',verts,faces,rubber,subd=1,thickness=.003)
# C: constant-width rounded bezel correspondence and a concave bowl with a shaped lever.
remove('Release_housing_satin_bezel','Release_recess_walls_and_back','Sculpted_release_lever')
outer=curvepoints([(351,143),(392,141),(530,143),(547,151),(574,186),(574,194),(561,200),(410,204),(394,195),(366,164)],120,True)
inner=[]
for i,p in enumerate(outer):
 tangent=(outer[(i+1)%120]-outer[(i-1)%120]).normalized();inner.append(p+Vector((-tangent.y,tangent.x))*5.5)
verts=[]
for blend,d in [(0,.045),(.22,.049),(.72,.050),(1,.046)]:
 for i,p in enumerate(outer):q=p.lerp(inner[i],blend);verts.append(loc(q.x,q.y,d))
faces=[(k*120+i,k*120+(i+1)%120,(k+1)*120+(i+1)%120,(k+1)*120+i) for k in range(3) for i in range(120)]
linkmesh('Release_housing_satin_bezel',verts,faces,metal,subd=1,thickness=.0015)
back=[p.lerp(Vector((470,173)),.08) for p in inner];verts=[loc(p.x,p.y,.046) for p in inner]+[loc(p.x,p.y,.009) for p in back];faces=[(i,(i+1)%120,(i+1)%120+120,i+120) for i in range(120)]+[tuple(range(120,240))]
linkmesh('Release_recess_walls_and_back',verts,faces,rubber,subd=1)
record(strip('Sculpted_release_lever',[(458,181),(496,180),(516,177),(524,171),(542,173),(558,186)],[(466,191),(493,193),(520,192),(540,191),(551,190),(560,188)],metal,nu=64,nv=12,subd=1,thickness=.005,depth_fn=lambda u,t,q:.024+.026*t+.008*math.sin(math.pi*t)+.006*u),'Sloping scooped lever face and stepped root, with real thickness; no flat silhouette slab')
# Existing upper roll retained; weatherseal termination shortened and softly tapered.
remove('Window_weatherseal')
sweep('Window_weatherseal',[(250,54,.04,.003,.004),(256,51,.04,.004,.006),(505,43,.04,.004,.006),(770,35,.04,.004,.006),(997,36,.04,.004,.006),(1002,37,.04,.002,.003)],rubber,ns=100,sides=12)
upper=bpy.data.objects['Upper_padded_roll'];bevel=upper.modifiers.new('Refined terminal edge radius','BEVEL');bevel.width=.0016;bevel.segments=3
# D/E: master material refinements only; no runtime slots or texture pipeline changes.
for m in [leather,black]:
 n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Sheen Weight'].default_value=.10
 for node in n:
  if node.bl_idname=='ShaderNodeBump':node.inputs['Strength'].default_value=.30;node.inputs['Distance'].default_value=.00032
  if node.bl_idname=='ShaderNodeMapRange':node.inputs['To Min'].default_value=.46;node.inputs['To Max'].default_value=.57
  if node.bl_idname=='ShaderNodeValToRGB' and m==leather:
   node.color_ramp.elements[0].color=tuple(v*.88 for v in lin('674421')[:3])+(1,);node.color_ramp.elements[1].color=tuple(v*1.04 for v in lin('674421')[:3])+(1,)
# Darker, less regular walnut response; keep original UV-driven direction and warp architecture.
n=wood.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.38;p.inputs['Coat Weight'].default_value=.18;p.inputs['Coat Roughness'].default_value=.28
for node in n:
 if node.bl_idname=='ShaderNodeValToRGB':node.color_ramp.elements[0].color=lin('0C0B09');node.color_ramp.elements[1].color=lin('30261B')
 if node.bl_idname=='ShaderNodeVectorMath' and node.operation=='SCALE':node.inputs[3].default_value=.040
 if node.bl_idname=='ShaderNodeVectorMath' and node.operation=='MULTIPLY':node.inputs[1].default_value=(8,180,1)
p=metal.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=lin('9EA4A3');p.inputs['Metallic'].default_value=1;p.inputs['Roughness'].default_value=.43
p=thread.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=lin('4B351D')
# Fine staggered round holes with actual alpha reveal to the existing acoustic backing.
n=grille.node_tree.nodes;l=grille.node_tree.links
for node in list(n):n.remove(node)
out=n.new('ShaderNodeOutputMaterial');p=n.new('ShaderNodeBsdfPrincipled');p.inputs['Base Color'].default_value=lin('5A5D5D');p.inputs['Metallic'].default_value=.65;p.inputs['Roughness'].default_value=.49;l.new(p.outputs[0],out.inputs[0])
def mathnode(op,a=None,b=None):
 node=n.new('ShaderNodeMath');node.operation=op
 for idx,value in enumerate([a,b]):
  if value is None:continue
  if isinstance(value,(int,float)):node.inputs[idx].default_value=value
  else:l.new(value,node.inputs[idx])
 return node.outputs[0]
uv=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=1/.00155;l.new(uv.outputs['UV'],scale.inputs[0]);l.new(scale.outputs[0],sep.inputs[0])
y=mathnode('MULTIPLY',sep.outputs['Y'],1.1547);row=mathnode('FLOOR',y);offset=mathnode('MULTIPLY',mathnode('MODULO',row,2),.5)
x=mathnode('SUBTRACT',mathnode('FRACT',mathnode('ADD',sep.outputs['X'],offset)),.5);yy=mathnode('SUBTRACT',mathnode('FRACT',y),.5)
distance=mathnode('SQRT',mathnode('ADD',mathnode('MULTIPLY',x,x),mathnode('MULTIPLY',yy,yy)))
alpha=mathnode('GREATER_THAN',distance,.34);l.new(alpha,p.inputs['Alpha'])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.00012;l.new(distance,bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
# Dedicated trim close-up added to the unchanged reference/overview camera set.
d=bpy.data.cameras.new('CAM_release-trim-closeup');d.type='ORTHO';d.ortho_scale=1.02;o=bpy.data.objects.new('CAM_release-trim-closeup',d);rig.objects.link(o);target=loc(658,176,.04);o.location=target+Vector((-.1,-2,.13));o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
# Save an independent master and trace which base geometry remained intact.
unchanged=[]
for name,data in original.items():
 o=bpy.data.objects.get(name)
 if o and [tuple(v.co) for v in o.data.vertices]==data['vertices']:unchanged.append(name)
for o in parts:o['checkpoint']='R4-front-door-refined';o['runtime_status']='MASTER ONLY; no export or binding change'
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();rows=[]
for o in components.objects:
 if o.type!='MESH':continue
 ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();rows.append({'name':o.name,'sourceVertices':len(o.data.vertices),'evaluatedTriangles':len(me.loop_triangles),'material':o.data.materials[0].name,'modifiers':[m.type for m in o.modifiers]});ev.to_mesh_clear()
manifest={'checkpoint':'R4-front-door-refined','sourceMasterSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'runtimeExport':False,'originalBaseGeometryRetained':unchanged,'replacedComponents':replaced,'objects':rows,'evaluatedTriangles':sum(x['evaluatedTriangles'] for x in rows),'dimensionStatus':'AI design alignment and inferred depth; not manufacturer dimensions','cameraStatus':'Existing front/overview cameras and studio lighting retained; one new trim close-up'}
(OUT/'master-metrics.json').write_text(json.dumps(manifest,indent=2));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'working_models/R4-front-door-refined.blend'));print(json.dumps({k:v for k,v in manifest.items() if k!='objects'},indent=2))
