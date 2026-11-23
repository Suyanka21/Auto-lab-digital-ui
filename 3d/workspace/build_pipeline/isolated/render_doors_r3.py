"""Door master look-development, separate from runtime textures. No baked/production parity claim."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[2];out=r/'reports/B3-doors-r3';bpy.ops.wm.open_mainfile(filepath=str(r/'working_models/B3-doors-r3.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True;s.render.resolution_x=1280;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.use_compositing=False;s.view_settings.view_transform='AgX';s.view_settings.exposure=0
# Keep exact runtime region name in per-object metadata; master materials are clearly prefixed.
def lin(h):
 v=[int(h[i:i+2],16)/255 for i in (0,2,4)];return tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v)+(1,)
def material(name,colour,rough=.45,metal=0,grain=0):
 m=bpy.data.materials.new('MASTER_'+name);m.use_nodes=True;m.diffuse_color=lin(colour);nodes=m.node_tree.nodes;links=m.node_tree.links;p=nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=lin(colour);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['IOR'].default_value=1.46
 if grain:
  tex=nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=950;tex.inputs['Detail'].default_value=2
  bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.20;bump.inputs['Distance'].default_value=grain;links.new(tex.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],p.inputs['Normal'])
  ramp=nodes.new('ShaderNodeMapRange');ramp.inputs['To Min'].default_value=rough-.045;ramp.inputs['To Max'].default_value=rough+.045;links.new(tex.outputs['Fac'],ramp.inputs['Value']);links.new(ramp.outputs['Result'],p.inputs['Roughness'])
 return m
leather=material('Upholstery_Tan','A97140',.45,grain=.00018);black=material('Padded_Black_Leather','242426',.49,grain=.00016);plastic=material('Fine_Grain_Plastic','191A1B',.57,grain=.00012);metal=material('Satin_Aluminium','A6ADB3',.28,.85);recess=material('Recess_Shadow','08090A',.62)
wood=material('Illustrative_Walnut_Trim','36271C',.30)
p=wood.node_tree.nodes.get('Principled BSDF');p.inputs['Coat Weight'].default_value=.28;p.inputs['Coat Roughness'].default_value=.22
nt=wood.node_tree.nodes;ln=wood.node_tree.links;tex=nt.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=4;tex.inputs['Detail'].default_value=4;tc=nt.new('ShaderNodeTexCoord');v=nt.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=(3,2,95);ln.new(tc.outputs['Generated'],v.inputs[0]);ln.new(v.outputs[0],tex.inputs['Vector']);ramp=nt.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=lin('231B15');ramp.color_ramp.elements[1].color=lin('55412E');ln.new(tex.outputs['Fac'],ramp.inputs[0]);ln.new(ramp.outputs[0],p.inputs['Base Color'])
grille=material('Speaker_Microperforation','343638',.48,.25);nt=grille.node_tree.nodes;ln=grille.node_tree.links;tc=nt.new('ShaderNodeTexCoord');sep=nt.new('ShaderNodeSeparateXYZ');ln.new(tc.outputs['Generated'],sep.inputs[0]);waves=[]
# Perforations are look-development shading on a thin disc; never claimed as baked runtime data.
for axis in ['Y','Z']:
 mul=nt.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=180;ln.new(sep.outputs[axis],mul.inputs[0]);sine=nt.new('ShaderNodeMath');sine.operation='SINE';ln.new(mul.outputs[0],sine.inputs[0]);waves.append(sine)
prod=nt.new('ShaderNodeMath');prod.operation='MULTIPLY';ln.new(waves[0].outputs[0],prod.inputs[0]);ln.new(waves[1].outputs[0],prod.inputs[1]);ramp=nt.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.20;ramp.color_ramp.elements[0].color=(.006,.007,.008,1);ramp.color_ramp.elements[1].position=.55;ramp.color_ramp.elements[1].color=(.075,.078,.082,1);ln.new(prod.outputs[0],ramp.inputs[0]);ln.new(ramp.outputs[0],nt.get('Principled BSDF').inputs['Base Color']);bump=nt.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.3;bump.inputs['Distance'].default_value=.0003;ln.new(prod.outputs[0],bump.inputs['Height']);ln.new(bump.outputs[0],nt.get('Principled BSDF').inputs['Normal'])
regions={'MAT_Seat_Secondary':leather,'MAT_Dashboard_Trim':black,'MAT_Cockpit_Black':plastic,'MAT_Console_Carbon':wood,'MAT_Console_Metal':metal}
doors=[]
for o in s.objects:
 if o.type!='MESH':continue
 if '_door_' not in o.name:o.hide_render=True;continue
 doors.append(o);slot=o.get('runtime_material',o.data.materials[0].name);o['runtime_material']=slot;o.data.materials.clear();o.data.materials.append(grille if 'perforated_face' in o.name else recess if 'release_bowl' in o.name or 'fascia_recess' in o.name else regions[slot])
# Neutral lighting; no white-showroom geometry, coloured rim lights or dramatic exposure tricks.
s.world=bpy.data.worlds.new('Neutral studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.55,.55,.55,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.45
for name,pos,power,size in [('Key',(-1.2,-.7,2.3),220,2.3),('Fill',(-.8,1.6,1.0),90,2.0),('Top',(.0,.4,2.2),120,1.5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((.78,0,.65))-o.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Door inspection camera',bpy.data.cameras.new('Door inspection camera'));s.collection.objects.link(cam);s.camera=cam
views=[('front-straight','Front',.16,'straight'),('front-three-quarter','Front',.16,'angle'),('rear-straight','Rear',-.99,'straight'),('rear-three-quarter','Rear',-.99,'angle'),('armrest-handle-trim-closeup','Front',.16,'close')]
import sys
for filename,row,z,view in (views[-1:] if '--finish' in sys.argv else views):
 for o in doors:o.hide_render=not o.name.startswith(row+'_door_1_')
 target=Vector((.76,-z,.635));cam.data.type='ORTHO';cam.data.ortho_scale=1.48
 cam.location=target+Vector((-2.4,0,0)) if view=='straight' else target+Vector((-2.1,-.85,.45))
 if view=='close':target=Vector((.74,-z-.01,.67));cam.location=target+Vector((-1.8,-.5,.22));cam.data.ortho_scale=.89
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(out/(filename+'.png'));bpy.ops.render.render(write_still=True)
# Save the real lookdev master before diagnostic material changes.
for o in doors:o.hide_render=not o.name.startswith('Front_door_1_')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(r/'working_models/B3-doors-r3-master.blend'))
# Separate flat-colour diagnostic, explicitly not a material-quality image.
diagnostic={k:material('DIAGNOSTIC_'+k,c,.7) for k,c in {'MAT_Seat_Secondary':'E2A83D','MAT_Dashboard_Trim':'6295CF','MAT_Cockpit_Black':'69716A','MAT_Console_Carbon':'BD5C74','MAT_Console_Metal':'D8DDE0'}.items()}
for o in doors:o.data.materials.clear();o.data.materials.append(diagnostic[o['runtime_material']]);o.hide_render=not o.name.startswith('Front_door_1_')
target=Vector((.76,-.16,.635));cam.location=target+Vector((-2.4,0,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.48;s.render.filepath=str(out/'diagnostic-material-regions.png');bpy.ops.render.render(write_still=True)
(out/'render-settings.json').write_text(json.dumps({'engine':'Cycles','samples':48,'resolution':[1280,900],'view':'AgX','exposure':0,'lights':'neutral area softboxes','materialStatus':'MASTER lookdev procedural leather, walnut and microperforation; runtime GLB retains baseline KTX2/carbon; no parity claim','views':[v[0] for v in views],'diagnostic':'separate flat-colour image'},indent=2))

