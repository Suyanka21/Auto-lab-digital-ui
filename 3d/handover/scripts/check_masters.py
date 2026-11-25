"""Open every distinct archived Blender file; expose external-resource dependencies."""
from pathlib import Path
import bpy,json,sys
repo=Path(__file__).resolve().parents[3];inventory=json.loads((repo/'3d/handover/workspace-inventory.json').read_text());names=sorted({x['repositoryPath'] for x in inventory['files'] if x['essential'] and Path(x['repositoryPath']).suffix in ['.blend','.blend1']});rows=[]
for name in names:
 try:
  bpy.ops.wm.open_mainfile(filepath=str(repo/name));external=[]
  for im in bpy.data.images:
   if im.source=='FILE' and not im.packed_file:external.append({'image':im.name,'path':im.filepath})
  libraries=[lib.filepath for lib in bpy.data.libraries if not lib.packed_file]
  rows.append({'path':name,'opened':True,'objects':len(bpy.data.objects),'meshes':len(bpy.data.meshes),'unpackedImages':external,'unpackedLibraries':libraries})
 except Exception as e:rows.append({'path':name,'opened':False,'error':str(e)})
result={'passed':all(x['opened'] and not x.get('unpackedImages') and not x.get('unpackedLibraries') for x in rows),'blender':bpy.app.version_string,'distinctMasters':len(rows),'masters':rows,'scope':'Open/read and packed-resource audit; no visual or runtime acceptance'}
out=Path(sys.argv[sys.argv.index('--')+1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'distinctMasters':len(rows)},indent=2))
if not result['passed']:raise RuntimeError('Master portability issue; inspect report')
