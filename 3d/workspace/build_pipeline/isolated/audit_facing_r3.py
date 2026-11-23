import bpy,json
from pathlib import Path
r=Path(__file__).resolve().parents[2];bpy.ops.wm.open_mainfile(filepath=str(r/'working_models/B3-doors-r3.blend'))
rows=[]
for o in bpy.context.scene.objects:
 if o.type=='MESH' and '_door_' in o.name:
  area=sum(p.area for p in o.data.polygons);x=sum(p.normal.x*p.area for p in o.data.polygons)/area if area else 0
  sign=int(o.name.split('_door_')[1].split('_')[0]);ok=x*sign<=.05
  rows.append({'name':o.name,'areaWeightedNormalX':x,'faces':len(o.data.polygons),'inwardOrClosed':ok})
report={'passed':all(v['inwardOrClosed'] for v in rows),'objects':rows,'scope':'Area-weighted orientation of door source surfaces; not a manifold or browser rasterisation test'}
(r/'reports/B3-doors-r3/facing-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps({'passed':report['passed'],'objects':len(rows)}));assert report['passed']
