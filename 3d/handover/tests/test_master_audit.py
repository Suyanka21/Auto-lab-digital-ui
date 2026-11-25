"""Blender behavior tests for portable audit, using disposable synthetic meshes only."""
import bpy,sys,json,importlib.util
from pathlib import Path
repo=Path(__file__).resolve().parents[3];path=repo/'.agents/skills/autolab-premium-cabin-modeling/scripts/audit_master.py'
spec=importlib.util.spec_from_file_location('audit_master',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
bpy.ops.wm.read_factory_settings(use_empty=True)
c=bpy.data.collections.new('TEST_COMPONENT');bpy.context.scene.collection.children.link(c)
bpy.ops.mesh.primitive_cube_add();obj=bpy.context.object
for col in list(obj.users_collection):col.objects.unlink(obj)
c.objects.link(obj);obj.data.materials.append(bpy.data.materials.new('TEST_MATERIAL'))
results=[]
def check(name,expected):
 result=module.audit('TEST_COMPONENT');assert result['passed']==expected,(name,result);results.append({'case':name,'expectedPass':expected,'actualPass':result['passed'],'errors':result['errors']})
check('valid cube with UV and material',True)
obj.data.uv_layers.remove(obj.data.uv_layers.active);check('missing UV fails',False)
obj.data.uv_layers.new(name='UVMap');obj.data.materials.clear();check('missing material fails',False)
bpy.data.objects.remove(obj,do_unlink=True);check('empty collection fails',False)
assert not module.audit('NO_SUCH_COLLECTION')['passed'];results.append({'case':'unknown collection fails','expectedPass':False,'actualPass':False})
out=Path(sys.argv[sys.argv.index('--')+1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'passed':True,'cases':results},indent=2)+'\n');print(json.dumps(results,indent=2))
