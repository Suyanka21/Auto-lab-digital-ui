import bpy,json
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[2];bpy.ops.wm.open_mainfile(filepath=str(r/'working_models/B3-doors-r2.blend'))
scene=bpy.context.scene;cam=scene.camera
# Blender-imported vertex-colour nodes read black on new meshes without a colour layer;
# the runtime instead uses white when COLOR_0 is absent. Explicit review-only white aligns them.
for o in scene.objects:
 if o.type=='MESH' and o.get('dimension_status')=='provisional' and not o.data.color_attributes:
  attr=o.data.color_attributes.new(name='ReviewWhite',type='FLOAT_COLOR',domain='CORNER')
  for d in attr.data:d.color=(1,1,1,1)
  o.data.color_attributes.active_color=attr
scene.cycles.samples=24
scene.view_settings.exposure=-.5
# Inspection camera and lighting only, no GLB mutation.
def cv(p):return Vector((p[0],-p[2],p[1]))
for row,z in [('Front',.16),('Rear',-.99)]:
 for o in scene.objects:
  if o.type=='MESH':o.hide_render=not o.name.startswith(row+'_door_1_')
 cam.location=cv((-1.6,.87,z+.12));cam.rotation_euler=(cv((.77,.65,z))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.43
 scene.render.filepath=str(r/'reports/B3-doors-r2'/(row.lower()+'-door-colour.png'));bpy.ops.render.render(write_still=True)
for o in scene.objects:
 if o.type=='MESH':o.hide_render=False
cam.data.type='PERSP';cam.data.lens=42;cam.location=cv((2.75,2.65,-3.1));cam.rotation_euler=(cv((0,.78,-.45))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(r/'working_models/B3-doors-r2-review.blend'))
