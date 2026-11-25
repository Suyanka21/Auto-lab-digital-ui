import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];OUT=R/'reports/R4-front-door-master';bpy.ops.wm.open_mainfile(filepath=str(R/'working_models/R4-front-door-master.blend'))
S=bpy.context.scene
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
preview='preview' in args
names=[a for a in args if a not in ['preview','final']]
if not names:names=['front-reference','three-quarter']
S.cycles.samples=12 if preview else 64;S.render.threads_mode='FIXED';S.render.threads=4
for name in names:
 S.view_layers[0].material_override=None
 S.cycles.samples=12 if preview else 96 if 'closeup' in name else 64
 S.render.resolution_x=900 if preview else 1440;S.render.resolution_y=625 if preview else 1000
 if name=='material-lab':
  for o in bpy.data.collections['R4_FRONT_DOOR_MASTER'].objects:o.hide_render=True
  for i,mn in enumerate(['Cognac_Padded_Leather','Black_Padded_Leather','Walnut_Trim','Perforated_Speaker_Metal']):
   bpy.ops.mesh.primitive_cube_add(size=1,location=(-.3+i*.2,-.2,.48));o=bpy.context.object;o.name='LAB_'+mn;o.dimensions=(.175,.025,.22);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(bpy.data.materials['R4_MASTER_'+mn]);b=o.modifiers.new('Sample edges','BEVEL');b.width=.008;b.segments=5
   for p in o.data.polygons:p.use_smooth=True
   uv=o.data.uv_layers.active
   for loop in o.data.loops:v=o.data.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(v.x,v.z)
  camera=bpy.data.objects['CAM_front-reference'];camera.location=(0,-2,.50);camera.rotation_euler=(Vector((0,-.20,.48))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=.9;S.camera=camera;S.render.resolution_y=450
 else:
  S.camera=bpy.data.objects['CAM_'+name]
  if name=='front-reference':
   S.camera.location=((600-620)*.00146,-3.04,(632-335)*.00146);S.camera.rotation_euler=Vector((0,1,0)).to_track_quat('-Z','Y').to_euler();S.camera.data.ortho_scale=1.752;S.render.resolution_y=round(S.render.resolution_x*670/1200)
  if name=='neutral-geometry':
   m=bpy.data.materials.new('Inspection_neutral_clay');m.diffuse_color=(.24,.24,.24,1);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.24,.24,.24,1);p.inputs['Roughness'].default_value=.62;S.view_layers[0].material_override=m
 dest=OUT/(('preview-' if preview else '')+name+'.png');S.render.filepath=str(dest);bpy.ops.render.render(write_still=True)
 print('RENDER_COMPLETE',name,flush=True)
 if name=='material-lab':
  for o in list(bpy.data.objects):
   if o.name.startswith('LAB_'):bpy.data.objects.remove(o,do_unlink=True)
  for o in bpy.data.collections['R4_FRONT_DOOR_MASTER'].objects:o.hide_render=False
(OUT/(('preview-' if preview else '')+'render-manifest.json')).write_text(json.dumps({'views':names,'samples':S.cycles.samples,'engine':S.render.engine,'threads':4,'status':'Actual Blender renders; not runtime GLB evidence','cameraAlignment':'front image uses primary 1200:670 framing; unknown AI perspective remains approximate'},indent=2))

