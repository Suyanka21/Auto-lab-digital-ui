"""Blender master data checks. No visual, runtime, watertightness or fit approval."""
import argparse,json,math,sys
from pathlib import Path
import bpy

def audit(collection):
 errors=[];rows=[];group=bpy.data.collections.get(collection)
 if group is None:return {'passed':False,'errors':['Missing collection: '+collection],'objects':[],'meshComponents':0,'evaluatedTriangles':0}
 dg=bpy.context.evaluated_depsgraph_get()
 for obj in sorted(group.all_objects,key=lambda o:o.name):
  if obj.type!='MESH':continue
  mesh=obj.data
  if not mesh.vertices or not mesh.polygons:errors.append(obj.name+': empty geometry')
  if not all(math.isfinite(c) for v in mesh.vertices for c in v.co):errors.append(obj.name+': nonfinite source coordinates')
  if not mesh.uv_layers:errors.append(obj.name+': missing UV layer')
  elif not all(math.isfinite(c) for v in mesh.uv_layers.active.data for c in v.uv):errors.append(obj.name+': nonfinite UV')
  if not mesh.materials or any(m is None for m in mesh.materials):errors.append(obj.name+': missing material')
  if any(poly.material_index>=len(mesh.materials) for poly in mesh.polygons):errors.append(obj.name+': invalid material index')
  evaluated=obj.evaluated_get(dg);ev=evaluated.to_mesh()
  try:
   ev.calc_loop_triangles()
   if not all(math.isfinite(c) for v in ev.vertices for c in v.co):errors.append(obj.name+': nonfinite evaluated coordinates')
   rows.append({'name':obj.name,'baseVertices':len(mesh.vertices),'evaluatedTriangles':len(ev.loop_triangles),'materials':[m.name if m else None for m in mesh.materials],'uvLayers':[uv.name for uv in mesh.uv_layers],'modifiers':[m.type for m in obj.modifiers]})
  finally:evaluated.to_mesh_clear()
 if not rows:errors.append('No mesh components in selected collection')
 images=[]
 for im in bpy.data.images:
  if im.source!='FILE':continue
  packed=bool(im.packed_file);exists=Path(bpy.path.abspath(im.filepath)).is_file()
  images.append({'name':im.name,'packed':packed,'externalFilePresent':exists})
  if not packed and not exists:errors.append('Unresolved image: '+im.name)
 return {'passed':not errors,'blender':bpy.app.version_string,'source':bpy.data.filepath,'collection':collection,'meshComponents':len(rows),'evaluatedTriangles':sum(x['evaluatedTriangles'] for x in rows),'baseVertices':sum(x['baseVertices'] for x in rows),'objects':rows,'images':images,'errors':errors,'scope':'Data integrity only; no visual acceptance, manifoldness, cabin fit or runtime equivalence'}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--collection',required=True);parser.add_argument('--report',type=Path,required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
 result=audit(args.collection);args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['objects','images']},indent=2))
 if not result['passed']:raise RuntimeError('Master data audit failed')
if __name__=='__main__':main()
