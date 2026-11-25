import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];OUT=R/'reports/R4-front-door-refined';bpy.ops.wm.open_mainfile(filepath=str(R/'working_models/R4-front-door-refined.blend'))
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

# Targeted construction probes on the saved refined master, not manufacturing validation.
from mathutils import Vector
from mathutils.bvhtree import BVHTree
checks={}
for label,pixel in [('gripOpening',(610,397)),('pocketOpening',(570,485))]:
 origin=Vector(((pixel[0]-620)*.00146,-2,(632-pixel[1])*.00146));direction=Vector((0,1,0));hits=[]
 for ob in meshes:
  tree=BVHTree.FromObject(ob,dg);hit,normal,face,distance=tree.ray_cast(origin,direction,3)
  if hit is not None:hits.append({'object':ob.name,'depthMetres':round(-hit.y,6),'distance':distance})
 checks[label]={'analyticalPixel':pixel,'firstHits':sorted(hits,key=lambda x:x['distance'])[:4]}
a=BVHTree.FromObject(bpy.data.objects['Pocket_open_mouth_lip'],dg);b=BVHTree.FromObject(bpy.data.objects['Speaker_perforated_screen'],dg)
checks['lipToGrilleTriangleOverlapPairs']=len(a.overlap(b))
checks['note']='Local geometry probes at chosen image-space landmarks; no global watertightness, hidden construction or visual-acceptance claim.'
report['targetedConstructionProbes']=checks
if checks['lipToGrilleTriangleOverlapPairs']!=0:report['errors'].append('Pocket lip intersects speaker face')
if not checks['gripOpening']['firstHits'] or checks['gripOpening']['firstHits'][0]['object'] in ['Continuous_grip_and_armrest_upholstery','Supported_under_grip_return']:report['errors'].append('Selected grip opening ray is blocked or lacks backing')
report['passed']=not report['errors']
(OUT/'master-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(checks,indent=2));assert report['passed'],report['errors']
