import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];OUT=R/'reports/R4-front-door-master';bpy.ops.wm.open_mainfile(filepath=str(R/'working_models/R4-front-door-master.blend'))
parts=list(bpy.data.collections['R4_FRONT_DOOR_MASTER'].objects);meshes=[o for o in parts if o.type=='MESH'];rows=[];errors=[];dg=bpy.context.evaluated_depsgraph_get()
for o in meshes:
 mesh=o.data
 if not all(math.isfinite(v) for p in mesh.vertices for v in p.co):errors.append(o.name+': nonfinite coordinates')
 if not mesh.uv_layers:errors.append(o.name+': missing UV')
 if not all(math.isfinite(v) for p in mesh.uv_layers.active.data for v in p.uv):errors.append(o.name+': nonfinite UV')
 if not mesh.materials:errors.append(o.name+': missing material')
 ev=o.evaluated_get(dg);e=ev.to_mesh();e.calc_loop_triangles();rows.append({'object':o.name,'sourceVertices':len(mesh.vertices),'sourceFaces':len(mesh.polygons),'evaluatedTriangles':len(e.loop_triangles),'uvLayer':mesh.uv_layers.active.name,'materials':[m.name for m in mesh.materials],'modifiers':[m.type for m in o.modifiers],'projectedStitches':o.get('surface_projected_stitches'),'skippedStitches':o.get('skipped_outside_surface')});ev.to_mesh_clear()
required=['Release_recess_walls_and_back','Continuous_grip_and_armrest_upholstery','Supported_under_grip_return','Pocket_interior_back','Pocket_inner_floor_and_front_return','Pocket_Leading_end_wall','Pocket_Trailing_end_wall','Speaker_perforated_screen','Integrated_speaker_shoulder']
for name in required:
 if name not in bpy.data.objects:errors.append('Missing '+name)
report={'passed':not errors,'errors':errors,'meshComponents':len(meshes),'evaluatedTriangles':sum(x['evaluatedTriangles'] for x in rows),'objects':rows,'images':[{'name':im.name,'packed':bool(im.packed_file),'size':list(im.size)} for im in bpy.data.images if im.type=='IMAGE'],'scope':'Fresh-open master structural/data checks only; not watertightness, visual acceptance, runtime or browser validation','runtimeExportProduced':False,'settings':{'blender':bpy.app.version_string,'units':bpy.context.scene.unit_settings.system,'look':bpy.context.scene.view_settings.look}}
(OUT/'master-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ['objects','images']},indent=2));assert not errors
