"""Capture immutable workspace history with explicit exclusions and content deduplication."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args();src=a.source.resolve();repo=a.repo.resolve()
assert src!=repo and src not in repo.parents and repo not in src.parents
manifest=repo/'3d/handover/workspace-inventory.json'
assert not manifest.exists(),'Capture once; do not silently replace the frozen inventory'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=repo).decode().split('\0');known={}
for name in tracked:
 if name and (repo/name).is_file():known.setdefault(sha(repo/name),name)
paths=sorted((p for p in src.rglob('*') if p.is_file()),key=lambda p:(0 if p.name in ['R4-front-door-refined.blend','R4-front-door-master.blend'] and p.parent.name=='working_models' else 1,str(p)))
rows=[];new=[]
for f in paths:
 rel=f.relative_to(src).as_posix();h=sha(f);entry={'localPath':rel,'bytes':f.stat().st_size,'sha256':h,'essential':True}
 if 'node_modules' in f.parts or '__pycache__' in f.parts:
  entry.update(essential=False,disposition='excluded-reproducible-cache',reason='Dependency cache or compiled Python cache; lockfile and source are retained.')
 elif f.suffix=='.glb' and (f.name.startswith('pipeline-probe-') or f.name=='baseline-render.glb' or f.name.endswith('-additions.glb')):
  entry.update(essential=False,disposition='excluded-derived-intermediate',reason='Intermediate prepared or additions GLB; source, editable masters, build records and final candidate exports are retained.')
 else:
  binary=f.suffix.lower() in ['.blend','.blend1','.glb','.png','.jpg','.jpeg','.webp','.ktx2','.bin']
  if binary and h in known:
   entry.update(disposition='verified-content-alias',repositoryPath=known[h])
  else:
   target='3d/workspace/'+rel;dest=repo/target;dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists();shutil.copy2(f,dest)
   assert sha(dest)==h
   entry.update(disposition='copied-byte-for-byte',repositoryPath=target);known.setdefault(h,target);new.append(target)
 rows.append(entry)
manifest.write_text(json.dumps({'schema':1,'capturedAt':'2026-11-23','sourceWorkspaceName':src.name,'sourceAbsolutePath':str(src),'repository':'Suyanka21/Auto-lab-digital-ui','baseCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip(),'cleanupAuthorised':False,'files':rows},indent=2)+'\n',encoding='utf-8')
summary={'sourceFiles':len(rows),'sourceBytes':sum(x['bytes'] for x in rows),'essentialFiles':sum(x['essential'] for x in rows),'excludedFiles':sum(not x['essential'] for x in rows),'newFiles':len(new),'newBytes':sum((repo/n).stat().st_size for n in new),'aliases':sum(x['disposition']=='verified-content-alias' for x in rows)}
(repo/'3d/handover/capture-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
