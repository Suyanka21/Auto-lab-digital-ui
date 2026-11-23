from pathlib import Path
import json,struct,hashlib
ROOT=Path(__file__).resolve().parents[1]
records=[]
for p in sorted((ROOT/'production_baseline').glob('*.glb')):
 b=p.read_bytes();magic,version,length=struct.unpack_from('<III',b)
 assert magic==0x46546c67 and version==2 and length==len(b)
 size,kind=struct.unpack_from('<II',b,12);assert kind==0x4e4f534a
 g=json.loads(b[20:20+size]);materials=[m.get('name') for m in g.get('materials',[])]
 nodes=[]
 for n in g.get('nodes',[]):
  if 'mesh' not in n:continue
  ps=g['meshes'][n['mesh']]['primitives']
  nodes.append(dict(name=n.get('name'),slots=[materials[v['material']] for v in ps],triangles=sum(g['accessors'][v['indices']]['count']//3 for v in ps),primitives=len(ps)))
 records.append(dict(file=p.name,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),materials=materials,nodes=nodes,triangles=sum(n['triangles'] for n in nodes),primitives=sum(n['primitives'] for n in nodes),extensions=g.get('extensionsRequired'),inspection='JSON metadata only; compressed geometry not decoded; NOT an asset-gate pass'))
(ROOT/'reports/baseline-inspection.json').write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
