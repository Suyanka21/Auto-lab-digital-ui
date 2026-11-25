import bpy,json
from pathlib import Path
r=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(r/'working_models/B3-doors.blend'))
o=bpy.data.objects['GEO_Cabin_Expansion'];bpy.context.view_layer.objects.active=o
bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
m=o.data;before_positions=[tuple(v.co) for v in m.vertices];before_pairs={(tuple(m.vertices[l.vertex_index].co),tuple(m.uv_layers.active.data[l.index].uv)) for l in m.loops}
ngons=sum(len(p.vertices)>4 for p in m.polygons)
try:m.calc_tangents(uvmap=m.uv_layers.active.name);failure=None
except Exception as e:failure=str(e)
tri=o.modifiers.new('Tangent regression triangulation','TRIANGULATE')
if hasattr(tri,'keep_custom_normals'):tri.keep_custom_normals=True
bpy.ops.object.modifier_apply(modifier=tri.name);m=o.data;m.calc_tangents(uvmap=m.uv_layers.active.name)
assert before_positions==[tuple(v.co) for v in m.vertices]
assert all((tuple(m.vertices[l.vertex_index].co),tuple(m.uv_layers.active.data[l.index].uv)) in before_pairs for l in m.loops)
assert all(len(p.vertices)==3 for p in m.polygons)
assert all(l.tangent.length>.99 for l in m.loops)
report={'beforeNgons':ngons,'beforeTangentFailure':failure,'afterTangentCalculation':'PASS','positionsUnchanged':True,'cornerUVPairsPreserved':True,'triangles':len(m.polygons),'tangentLoopCount':len(m.loops),'normalNote':'Triangulate modifier requests custom-normal preservation where supported; baseline untouched; no claim of bit-exact new door shading.'}
(r/'reports/reference-r2/tangent-regression.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
