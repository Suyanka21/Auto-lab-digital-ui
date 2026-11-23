import bpy
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[2];bpy.ops.wm.open_mainfile(filepath=str(r/'working_models/B3-doors-r2-review.blend'));s=bpy.context.scene
for name,col in {'MAT_Seat_Secondary':(.38,.16,.065,1),'MAT_Dashboard_Trim':(.025,.027,.030,1),'MAT_Cockpit_Black':(.008,.009,.01,1),'MAT_Console_Carbon':(.035,.03,.025,1),'MAT_Console_Metal':(.25,.27,.3,1)}.items():
 m=bpy.data.materials[name];m.diffuse_color=col
 n=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');socket=n.inputs['Base Color']
 for l in list(socket.links):m.node_tree.links.remove(l)
 socket.default_value=col
s.render.use_compositing=False;s.view_settings.exposure=0
for row,z in [('Front',.16),('Rear',-.99)]:
 for o in s.objects:
  if o.type=='MESH':o.hide_render=not o.name.startswith(row+'_door_1_')
 cam=s.camera;cam.data.type='ORTHO';cam.data.ortho_scale=1.43;cam.location=Vector((-1.6,-(z+.12),.87));cam.rotation_euler=(Vector((.77,-z,.65))-cam.location).to_track_quat('-Z','Y').to_euler()
 s.render.filepath=str(r/'reports/B3-doors-r2'/(row.lower()+'-material-regions.png'));bpy.ops.render.render(write_still=True)
