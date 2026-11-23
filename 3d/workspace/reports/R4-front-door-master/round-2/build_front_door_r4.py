"""R4 front-door editable master. Reference-led component construction; no runtime export.
Pixel landmarks refer to the inspected 1200x670 primary reference, never OEM dimensions.
"""
import bpy,math,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
R=Path(__file__).resolve().parents[2];OUT=R/'reports/R4-front-door-master';OUT.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
S=bpy.context.scene;S.unit_settings.system='METRIC';S.render.engine='CYCLES';S.cycles.samples=48;S.cycles.use_denoising=True;S.render.threads_mode='FIXED';S.render.threads=4
S.render.resolution_x=1440;S.render.resolution_y=1000;S.render.resolution_percentage=100;S.render.image_settings.file_format='PNG';S.view_settings.view_transform='AgX';S.view_settings.exposure=0;S.view_settings.look='AgX - Medium High Contrast'
S.render.film_transparent=False;S.render.use_compositing=False
MM=.00146
components=bpy.data.collections.new('R4_FRONT_DOOR_MASTER');S.collection.children.link(components)
rig=bpy.data.collections.new('REVIEW_CAMERAS_AND_LIGHTS');S.collection.children.link(rig)
parts=[]
def loc(px,py,depth):return Vector(((px-620)*MM,-depth,(632-py)*MM))
def lin(h):
 c=[int(h[i:i+2],16)/255 for i in (0,2,4)];return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c)+(1,)
def mat(name,color,rough=.45,metal=0,grain=False):
 m=bpy.data.materials.new('R4_MASTER_'+name);m.diffuse_color=lin(color);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=lin(color);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['IOR'].default_value=1.46
 if grain:
  n=m.node_tree.nodes;l=m.node_tree.links;uv=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=950;noise.inputs['Detail'].default_value=2.4;noise.inputs['Roughness'].default_value=.65;l.new(uv.outputs['UV'],noise.inputs['Vector'])
  vor=n.new('ShaderNodeTexVoronoi');vor.feature='DISTANCE_TO_EDGE';vor.inputs['Scale'].default_value=800;l.new(uv.outputs['UV'],vor.inputs['Vector'])
  mix=n.new('ShaderNodeMath');mix.operation='MULTIPLY_ADD';mix.inputs[1].default_value=.7;l.new(vor.outputs['Distance'],mix.inputs[0]);l.new(noise.outputs['Fac'],mix.inputs[2])
  bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.24;bump.inputs['Distance'].default_value=.00030;l.new(mix.outputs[0],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
  vary=n.new('ShaderNodeMapRange');vary.inputs['To Min'].default_value=rough-.055;vary.inputs['To Max'].default_value=rough+.045;l.new(noise.outputs['Fac'],vary.inputs['Value']);l.new(vary.outputs['Result'],p.inputs['Roughness']);p.inputs['Sheen Weight'].default_value=.10
 return m
leather=mat('Cognac_Padded_Leather','75431E',.41,grain=True);black=mat('Black_Padded_Leather','0C1014',.46,grain=True);plastic=mat('Textured_Structural_Plastic','111315',.55,grain=True);rubber=mat('Soft_Black_Recess','080A0B',.66);metal=mat('Satin_Aluminium','B5B9BD',.27,.92);thread=mat('Cognac_Thread','59391F',.62);light_thread=mat('Thread_Highlight','B4834D',.57);lens=mat('Courtesy_Diffuser','B6B9BA',.3)
wood=mat('Walnut_Trim','48301E',.3);p=wood.node_tree.nodes.get('Principled BSDF');p.inputs['Coat Weight'].default_value=.38;p.inputs['Coat Roughness'].default_value=.19
n=wood.node_tree.nodes;l=wood.node_tree.links;uv=n.new('ShaderNodeTexCoord');warp=n.new('ShaderNodeTexNoise');warp.inputs['Scale'].default_value=3;warp.inputs['Detail'].default_value=2;l.new(uv.outputs['UV'],warp.inputs['Vector']);v=n.new('ShaderNodeVectorMath');v.operation='SCALE';v.inputs[3].default_value=.024;l.new(warp.outputs['Color'],v.inputs[0]);add=n.new('ShaderNodeVectorMath');add.operation='ADD';l.new(uv.outputs['UV'],add.inputs[0]);l.new(v.outputs[0],add.inputs[1]);scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(6,230,1);l.new(add.outputs[0],scale.inputs[0]);tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=1;tex.inputs['Detail'].default_value=3;tex.inputs['Roughness'].default_value=.7;l.new(scale.outputs[0],tex.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=lin('20150E');ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=lin('61452E');l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
# UV-based fine punched screen. Holes reveal a separate acoustic backing; master shader only.
grille=mat('Perforated_Speaker_Metal','565959',.43,.5);n=grille.node_tree.nodes;l=grille.node_tree.links;p=n.get('Principled BSDF');uv=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(uv.outputs['UV'],sep.inputs[0]);factors=[]
for axis in ['X','Y']:
 a=n.new('ShaderNodeMath');a.operation='MULTIPLY';a.inputs[1].default_value=2500;l.new(sep.outputs[axis],a.inputs[0]);b=n.new('ShaderNodeMath');b.operation='SINE';l.new(a.outputs[0],b.inputs[0]);c=n.new('ShaderNodeMath');c.operation='MULTIPLY';l.new(b.outputs[0],c.inputs[0]);l.new(b.outputs[0],c.inputs[1]);factors.append(c)
add=n.new('ShaderNodeMath');add.operation='ADD';l.new(factors[0].outputs[0],add.inputs[0]);l.new(factors[1].outputs[0],add.inputs[1]);cut=n.new('ShaderNodeMath');cut.operation='GREATER_THAN';cut.inputs[1].default_value=.68;l.new(add.outputs[0],cut.inputs[0]);l.new(cut.outputs[0],p.inputs['Alpha'])

def linkmesh(name,verts,faces,material,uv=None,subd=0,thickness=0):
 mesh=bpy.data.meshes.new(name+'_Topology');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);components.objects.link(o);o.data.materials.append(material);o['design_source']='approved front PRIMARY';o['dimension_status']='Provisional image-derived scale and inferred depth';parts.append(o)
 for p in mesh.polygons:p.use_smooth=True
 layer=mesh.uv_layers.new(name='Surface_Metres')
 for loop in mesh.loops:
  vi=loop.vertex_index;v=mesh.vertices[vi].co;layer.data[loop.index].uv=uv[vi] if uv else (v.x,v.z)
 # Consistent outward orientation for open front surfaces; closed solids use explicit bevel later.
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
 area=sum(p.area for p in mesh.polygons);facing=sum(p.normal.y*p.area for p in mesh.polygons)/max(area,1e-9)
 if facing>.01:
  o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.flip_normals();bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
 if subd:
  mod=o.modifiers.new('Editable curvature subdivision','SUBSURF');mod.levels=subd;mod.render_levels=subd
 if thickness:
  mod=o.modifiers.new('Real component wall thickness','SOLIDIFY');mod.thickness=thickness;mod.offset=-1
 return o

def curvepoints(points,count=64,closed=False):
 vs=[Vector(p) for p in points];result=[];segments=len(vs) if closed else len(vs)-1
 for j in range(count):
  t=j/count*segments if closed else j/(count-1)*segments;i=min(int(t),segments-1);t-=i
  a=vs[(i-1)%len(vs)] if closed else vs[max(0,i-1)];b=vs[i];c=vs[(i+1)%len(vs)];d=vs[(i+2)%len(vs)] if closed else vs[min(len(vs)-1,i+2)]
  result.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
 return result

def slab(name,outline,depth,thick,material,bevel=.003):
 pts=curvepoints(outline,96,True);v=[loc(p.x,p.y,depth) for p in pts]+[loc(p.x,p.y,depth-thick) for p in pts];N=len(pts);faces=[tuple(range(N)),tuple(reversed(range(N,2*N)))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)];o=linkmesh(name,v,faces,material)
 if bevel:
  mod=o.modifiers.new('Manufactured edge radius','BEVEL');mod.width=bevel;mod.segments=3
  mod=o.modifiers.new('Face-weighted normals','WEIGHTED_NORMAL');mod.keep_sharp=True
 return o

def strip(name,top,bottom,material,depth=.03,crown=.01,nu=64,nv=12,subd=1,thickness=.003,depth_fn=None,left_boundary=None):
 a=curvepoints(top,nu);b=curvepoints(bottom,nu);verts=[];uv=[]
 left=curvepoints(left_boundary,nv+1) if left_boundary else None
 length=sum((a[i]-a[i-1]).length for i in range(1,nu))*MM
 for j in range(nv+1):
  t=j/nv
  for i in range(nu):
   u=i/(nu-1);q=a[i].lerp(b[i],t)
   if left is not None:q+=(left[j]-a[0].lerp(b[0],t))*(1-u)
   d=depth_fn(u,t,q) if depth_fn else depth+crown*math.sin(math.pi*t)**.8*(.7+.3*math.sin(math.pi*u))
   verts.append(loc(q.x,q.y,d));uv.append((u*length,t*(a[i]-b[i]).length*MM))
 faces=[]
 for j in range(nv):
  for i in range(nu-1):k=j*nu+i;faces.append((k,k+1,k+nu+1,k+nu))
 return linkmesh(name,verts,faces,material,uv,subd,thickness)

def sweep(name,path,material,vertical=.01,deep=.01,ns=120,sides=20,rectangular=False):
 # Path entries image x,y,outward depth,vertical radius,depth radius. Physical section is independently controlled.
 pts=curvepoints(path,ns);verts=[];uv=[];length=0
 for i,p in enumerate(pts):
  prev=pts[max(0,i-1)];nxt=pts[min(ns-1,i+1)];t=Vector((nxt.x-prev.x,-nxt.y+prev.y));t.normalize();perp=Vector((-t.y,t.x));vr=p[3] if len(p)>3 else vertical;dr=p[4] if len(p)>4 else deep
  if i:length+=(loc(p.x,p.y,p.z)-loc(prev.x,prev.y,prev.z)).length
  for j in range(sides):
   th=2*math.pi*j/sides;c=math.cos(th);s=math.sin(th)
   if rectangular:c=math.copysign(abs(c)**.38,c);s=math.copysign(abs(s)**.38,s)
   co=loc(p.x,p.y,p.z);co.x+=perp.x*vr*c;co.z+=perp.y*vr*c;co.y-=dr*s;verts.append(co);uv.append((length,j/sides*2*math.pi*max(vr,dr)))
 faces=[(i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j) for i in range(ns-1) for j in range(sides)]
 faces+=[tuple(reversed(range(sides))),tuple(range((ns-1)*sides,ns*sides))]
 return linkmesh(name,verts,faces,material,uv,1)

def stitches(name,path,offset=0):
 pts=curvepoints(path,180);world=[loc(p.x,p.y,p.z) for p in pts];dist=[0]
 for a,b in zip(world,world[1:]):dist.append(dist[-1]+(b-a).length)
 verts=[];faces=[];cursor=.002;idx=1
 while cursor<dist[-1]-.002:
  while idx<len(dist)-1 and dist[idx]<cursor:idx+=1
  t=(cursor-dist[idx-1])/max(dist[idx]-dist[idx-1],1e-9);p=world[idx-1].lerp(world[idx],t);tan=(world[idx]-world[idx-1]).normalized();side=tan.cross(Vector((0,-1,0))).normalized();p+=side*offset;n=len(verts)
  for end in [-1,1]:
   q=p+tan*(.00105*end)
   for k in range(6):a=k*math.pi/3;verts.append(q+side*(math.cos(a)*.00024)+Vector((0,-math.sin(a)*.00024,0)))
  faces.extend((n+k,n+(k+1)%6,n+(k+1)%6+6,n+k+6) for k in range(6));cursor+=.0036
 return linkmesh(name,verts,faces,light_thread)

# Outer molded carrier: traced silhouette, not a rectangular support board.
outline=[(216,123),(241,120),(245,71),(261,52),(507,46),(768,37),(1007,37),(1016,44),(991,146),(971,239),(950,333),(929,427),(909,519),(886,577),(858,606),(810,625),(764,629),(509,616),(317,604),(272,589),(247,560),(230,515),(221,424),(219,307)]
slab('Structural_carrier',outline,.018,.024,plastic,.006)
# Broad leading-side molding: structured curved strip merging toward the speaker shoulder.
strip('Leading_side_sculpted_molding',[(219,130),(250,141),(296,161),(336,220),(323,294),(282,372),(239,424)],[(229,450),(267,414),(318,372),(358,315),(378,244),(343,186),(306,142)],plastic,.030,.016,nu=72,nv=18,subd=1)
upper=strip('Upper_padded_roll',[(250,66),(487,55),(755,46),(1003,45)],[(253,134),(499,143),(763,143),(983,143)],black,.040,.025,nu=96,nv=20,subd=2)
sweep('Window_weatherseal',[(250,53,.04),(505,43,.04),(770,34,.04),(1010,35,.04)],rubber,.004,.006,ns=96,sides=12)
sweep('Upper_roll_lower_welt',[(257,136,.044),(504,145,.044),(762,145,.044),(980,145,.044)],black,.0012,.0012,ns=100,sides=8)
# Fascia structural surround and wood are separate constructed surfaces.
strip('Integrated_fascia_base',[(307,138),(490,142),(740,146),(980,145)],[(382,216),(520,219),(753,218),(953,210)],black,.032,.005,nu=80,nv=14)
strip('Walnut_decorative_insert',[(553,144),(689,146),(845,147),(970,147)],[(602,191),(713,196),(860,195),(944,185)],wood,.046,.006,nu=88,nv=14,subd=2)
sweep('Thin_decorative_reveal',[(552,145,.049),(598,193,.050),(713,200,.050),(867,199,.049),(937,191,.047),(963,161,.043)],metal,.0015,.0012,ns=140,sides=10)
# Release bowl has a rim, actual sloped walls and a back surface behind the lever.
outer=curvepoints([(350,141),(545,143),(561,154),(581,190),(565,202),(402,205),(384,192)],84,True)
inner=curvepoints([(364,151),(535,153),(546,162),(563,185),(552,191),(411,194),(399,184)],84,True)
verts=[loc(p.x,p.y,.050) for p in outer]+[loc(p.x,p.y,.051) for p in inner];faces=[(i,(i+1)%84,(i+1)%84+84,i+84) for i in range(84)]
o=linkmesh('Release_housing_satin_bezel',verts,faces,metal,subd=1,thickness=.002)
back=[p.lerp(Vector((466,173)),.17) for p in inner];verts=[loc(p.x,p.y,.049) for p in inner]+[loc(p.x,p.y,.014) for p in back];faces=[(i,(i+1)%84,(i+1)%84+84,i+84) for i in range(84)]+[tuple(range(84,168))];linkmesh('Release_recess_walls_and_back',verts,faces,rubber,subd=1)
slab('Sculpted_release_lever',[(450,177),(476,176),(486,166),(535,170),(551,181),(543,187),(456,187)],.058,.008,metal,.0025)
# Small separate memory strip in reference; neutral controls, no manufacturer logo.
slab('Memory_control_recess',[(382,154),(410,155),(434,190),(414,191)],.047,.004,rubber,.001)
for i in range(3):
 z=160+i*9;slab('Memory_button_'+str(i+1),[(390+i*5,z),(397+i*5,z),(400+i*5,z+4),(393+i*5,z+4)],.050,.003,plastic,.0008)
# Insert cross sections follow the dipped front edge and the armrest support line.
insert_top=[(364,349),(403,291),(449,260),(590,236),(784,225),(964,216)]
insert_bottom=[(359,366),(414,363),(511,350),(662,354),(807,354),(938,357)]
insert=strip('Sculpted_upholstery_insert',insert_top,insert_bottom,leather,.049,.020,nu=112,nv=24,subd=2,depth_fn=lambda u,t,q:.043+.020*math.sin(math.pi*t)**.7+.008*math.sin(math.pi*u))
sweep('Insert_top_rolled_seam',[(365,354,.055),(408,294,.060),(456,266,.064),(594,243,.064),(785,232,.060),(958,224,.052)],leather,.0013,.0013,ns=180,sides=10)
seam=[(367,357,.057),(411,299,.064),(460,272,.066),(596,250,.067),(785,239,.064),(957,231,.056)]
stitches('Insert_double_stitch_A',seam);stitches('Insert_double_stitch_B',seam,.003)
# One broad, asymmetric, rounded-rectangular upholstered grip and palmrest.
# Depth and vertical section widen independently; no circular tube laid on a box.
path=[(432,270,.064,.018,.018),(440,293,.087,.021,.024),(477,334,.125,.024,.033),(533,361,.148,.028,.048),(610,368,.143,.030,.066),(735,366,.130,.060,.082),(861,367,.114,.058,.083),(914,361,.085,.050,.060),(931,350,.055,.023,.026)]
sweep('Continuous_grip_and_armrest_upholstery',path,leather,ns=180,sides=32,rectangular=True)
# Lower return physically attaches beneath the pull, surrounding an open under-grip space.
sweep('Supported_under_grip_return',[(494,356,.091,.014,.022),(522,385,.088,.013,.022),(568,408,.078,.010,.020),(641,411,.073,.009,.019),(693,393,.080,.013,.021),(722,382,.091,.017,.028)],leather,ns=112,sides=24,rectangular=True)
# Deep rear support under the broad palmrest, separated by a natural upholstery seam.
strip('Armrest_rear_support',[(691,381),(782,387),(907,378),(925,365)],[(699,416),(784,414),(898,413),(918,391)],leather,.078,.013,nu=72,nv=18,subd=2,depth_fn=lambda u,t,q:.104-.030*t+.009*math.sin(math.pi*t))
stitchpath=[(432,269,.084),(443,292,.112),(480,331,.160),(535,352,.197),(613,353,.210),(735,351,.213),(863,351,.198),(914,348,.141)]
stitches('Armrest_upper_double_stitch_A',stitchpath);stitches('Armrest_upper_double_stitch_B',stitchpath,.003)
sweep('Armrest_front_join',[(529,364,.198),(544,381,.186),(561,389,.167)],thread,.0005,.0005,ns=32,sides=6)
# Switch tray is supported by a small upper deck behind the pull; four driver toggles.
strip('Switch_deck',[(470,321),(541,318),(624,319)],[(482,341),(550,346),(635,342)],leather,.083,.006,nu=48,nv=10)
slab('Driver_switch_tray',[(492,322),(623,322),(631,337),(506,342)],.103,.008,rubber,.004)
for i in range(4):
 x=512+i*23;slab('Window_switch_'+str(i+1),[(x,325),(x+15,325),(x+16,333),(x+1,334)],.109,.006,plastic,.001)
 sweep('Window_switch_mark_'+str(i+1),[(x+5,328,.110),(x+11,328,.110)],metal,.0003,.0002,ns=4,sides=4)
# Pocket recess: separate back, bottom, curved front wall and end returns; no top cap.
strip('Pocket_interior_back',[(419,424),(547,439),(712,430),(907,424)],[(445,548),(595,550),(754,540),(888,534)],rubber,.033,.003,nu=72,nv=14)
ptop=[(385,458),(416,501),(452,524),(559,530),(734,523),(892,515)]
pbottom=[(388,585),(421,598),(528,606),(647,615),(782,620),(864,581)]
strip('Pocket_front_moulded_wall',ptop,pbottom,plastic,.11,.005,nu=100,nv=26,subd=2,depth_fn=lambda u,t,q:.143-.075*t+.008*math.sin(math.pi*t),left_boundary=[(386,458),(410,484),(420,519),(411,558),(388,585)])
sweep('Pocket_open_mouth_lip',[(386,459,.143),(419,503,.145),(455,526,.145),(559,532,.144),(734,525,.141),(891,517,.140)],plastic,.0035,.0045,ns=130,sides=16)
# Internal floor and return walls are generated as continuous quad bands at true depth.
inner=curvepoints([(409,475),(452,537),(607,550),(790,546),(882,532)],76);verts=[]
for d in [.034,.14]:
 for p in inner:verts.append(loc(p.x,p.y,d))
faces=[(i,i+1,i+77,i+76) for i in range(75)];linkmesh('Pocket_inner_floor_and_front_return',verts,faces,rubber,subd=1,thickness=.002)
for name,path in [('Leading',[(388,458),(407,487),(422,508),(440,536)]),('Trailing',[(905,425),(903,464),(894,507),(882,533)])]:
 pts=curvepoints(path,32);v=[loc(p.x,p.y,d) for d in [.034,.14] for p in pts];f=[(i,i+1,i+33,i+32) for i in range(31)];linkmesh('Pocket_'+name+'_end_wall',v,f,plastic,subd=1,thickness=.003)
# Integrated molded speaker shoulder, swept from the grille opening into the carrier.
centre=Vector((333,519));verts=[];faces=[];N=128
for fraction,depth in [(1,.025),(.72,.038),(.32,.069),(.06,.075),(0,.072)]:
 for j in range(N):
  a=j*2*math.pi/N;sn=math.sin(a);cs=math.cos(a);outer=min(116,82/sn if sn>.001 else 116,98/-cs if cs<-.001 else 116);rad=77+(outer-77)*fraction;p=centre+Vector((cs*rad,sn*rad));verts.append(loc(p.x,p.y,depth))
for k in range(4):
 for j in range(N):a=k*N+j;b=k*N+(j+1)%N;faces.append((a,b,b+N,a+N))
linkmesh('Integrated_speaker_shoulder',verts,faces,plastic,subd=2)
for name,rad,d,rr,material in [('Speaker_satin_ring',78,.076,.0018,metal),('Speaker_seal',75.8,.075,.0012,rubber)]:
 path=[(333+rad*math.cos(a*2*math.pi/128),519+rad*math.sin(a*2*math.pi/128),d) for a in range(129)];sweep(name,path,material,rr,rr,ns=256,sides=12)
# Dome grid gives gentle curvature and UVs continuous across the face.
for name,depth,material in [('Acoustic_backing',.067,rubber),('Speaker_perforated_screen',.078,grille)]:
 v=[loc(333,519,depth+.003)];N=128;rings=12
 for k in range(1,rings+1):
  rad=75*k/rings
  for j in range(N):a=j*math.tau/N;v.append(loc(333+rad*math.cos(a),519+rad*math.sin(a),depth+.003*(1-(k/rings)**2)))
 f=[(0,1+j,1+(j+1)%N) for j in range(N)]
 for k in range(rings-1):
  for j in range(N):a=1+k*N+j;b=1+k*N+(j+1)%N;f.append((a,b,b+N,a+N))
 linkmesh(name,v,f,material)
slab('Courtesy_lamp_recess',[(692,602),(747,602),(754,617),(689,617)],.090,.008,rubber,.002)
slab('Courtesy_lamp_lens',[(697,605),(742,605),(747,613),(695,613)],.095,.005,lens,.0015)
# Visual landmarks are durable empties, not inferred manufacturing dimensions.
landmarks={'Top_front':(258,58,.04),'Top_rear':(1002,43,.04),'Speaker_centre':(333,519,.078),'Release_centre':(487,175,.05),'Grip_upper_attachment':(432,270,.065),'Grip_to_armrest':(537,361,.15),'Pocket_lip_low':(559,532,.145),'Lower_rear_corner':(799,623,.04)}
for name,p in landmarks.items():
 o=bpy.data.objects.new('REF_'+name,None);components.objects.link(o);o.location=loc(*p);o.empty_display_size=.008;o.hide_render=True;o['reference_pixel']=list(p[:2]);o['depth_status']='inferred'
# Neutral studio setup, common to all material views.
S.world=bpy.data.worlds.new('R4_neutral_world');S.world.use_nodes=True;S.world.node_tree.nodes['Background'].inputs[0].default_value=(.43,.43,.43,1);S.world.node_tree.nodes['Background'].inputs[1].default_value=.32
for name,pos,energy,size in [('Key',(-1.3,-1.4,1.8),160,1.6),('Fill',(1.4,-.8,1.1),65,1.4),('Top',(0,.1,1.9),95,1.0)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);rig.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,-.04,.48))-o.location).to_track_quat('-Z','Y').to_euler()
# floor, behind the photographed component, separate from the authored component collection.
floor=mat('Studio_Background','A4A4A4',.8);bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.018));ground=bpy.context.object;ground.name='REVIEW_GROUND';ground.data.materials.append(floor)
target=loc(620,336,.04)
views={
 'front-reference':(loc(600,335,.04)+Vector((0,-3,0)),loc(600,335,.04),1.752),
 'three-quarter':(target+Vector((-1.35,-2.6,.55)),target,1.73),
 'handle-release-closeup':(loc(640,285,.12)+Vector((-.28,-2,.23)),loc(640,285,.12),1.02),
 'pocket-speaker-closeup':(loc(552,480,.08)+Vector((-.35,-2,.30)),loc(552,480,.08),1.05),
 'neutral-geometry':(target+Vector((-.8,-3,.35)),target,1.73),
 'realistic-material':(target+Vector((.85,-3,.28)),target,1.73)}
for name,(position,aim,scale) in views.items():
 d=bpy.data.cameras.new('CAM_'+name);d.type='ORTHO';d.ortho_scale=scale;o=bpy.data.objects.new('CAM_'+name,d);rig.objects.link(o);o.location=position;o.rotation_euler=(aim-position).to_track_quat('-Z','Y').to_euler()
# Primary image is a viewport camera guide only; never used as a material texture.
ref=R/'references/approved_ai_design/01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg'
cam=bpy.data.objects['CAM_front-reference'];cam.data.show_background_images=True;bg=cam.data.background_images.new();bg.image=bpy.data.images.load(str(ref));bg.alpha=.35
S.camera=cam
# Editable collections and per-material runtime role notes; no new runtime slot definitions.
roles={leather.name:'MAT_Seat_Secondary',black.name:'MAT_Dashboard_Trim',plastic.name:'MAT_Cockpit_Black',wood.name:'MAT_Console_Carbon',metal.name:'MAT_Console_Metal'}
for o in parts:o['runtime_role_candidate']=roles.get(o.data.materials[0].name,'MASTER_DETAIL_ONLY; mapping requires later approval')
metrics=[];dg=bpy.context.evaluated_depsgraph_get()
for o in parts:
 ev=o.evaluated_get(dg);mesh=ev.to_mesh();mesh.calc_loop_triangles();metrics.append({'name':o.name,'sourceVertices':len(o.data.vertices),'evaluatedTriangles':len(mesh.loop_triangles),'material':o.data.materials[0].name,'uv':'Surface_Metres','modifiers':[m.type for m in o.modifiers]});ev.to_mesh_clear()
manifest={'stage':'R4 front-door MASTER ONLY','runtimeExport':False,'dimensionsStatus':'provisional; not OEM','referenceFrame':[1200,670],'metresPerReferencePixel':MM,'landmarks':{k:list(v) for k,v in landmarks.items()},'objects':metrics,'evaluatedTriangles':sum(m['evaluatedTriangles'] for m in metrics),'views':{k:{'position':list(v[0]),'target':list(v[1]),'orthoScale':v[2]} for k,v in views.items()},'render':{'engine':'Cycles','samples':48,'resolution':[1440,1000],'viewTransform':'AgX','exposure':0,'look':'AgX - Medium High Contrast','threads':4}}
(OUT/'master-metrics.json').write_text(json.dumps(manifest,indent=2))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'working_models/R4-front-door-master.blend'))
print('MASTER_SAVED',len(parts),'components',manifest['evaluatedTriangles'],'evaluated triangles; no runtime asset produced')
