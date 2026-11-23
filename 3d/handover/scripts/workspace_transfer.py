"""Verify frozen inventory or restore its essential files into a new scratch directory."""
from pathlib import Path
import argparse,hashlib,json,shutil

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def inside(root,name):
 p=(root/name).resolve()
 if not p.is_relative_to(root):raise ValueError('Path escapes root: '+name)
 return p

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument('--restore',type=Path);p.add_argument('--check-local',type=Path);p.add_argument('--report',type=Path);a=p.parse_args();root=a.repo.resolve()
 data=json.loads((root/'3d/handover/workspace-inventory.json').read_text(encoding='utf-8-sig'));errors=[];checked=0;cache={}
 for item in data['files']:
  if not item['essential']:continue
  source=inside(root,item['repositoryPath'])
  if source not in cache:cache[source]=digest(source) if source.is_file() else None
  if cache[source]!=item['sha256']:errors.append({'path':item['repositoryPath'],'issue':'missing or different content; run git lfs pull if pointer'})
  checked+=1
 if a.check_local:
  local=a.check_local.resolve();expected={x['localPath']:x for x in data['files']}
  current={p.relative_to(local).as_posix():p for p in local.rglob('*') if p.is_file()}
  for name in set(current)-set(expected):errors.append({'path':name,'issue':'new local file not inventoried'})
  for name,item in expected.items():
   if name not in current or digest(current[name])!=item['sha256']:errors.append({'path':name,'issue':'local file missing or changed since inventory'})
 if a.restore and not errors:
  out=a.restore.resolve()
  if out==root or out.is_relative_to(root) or root.is_relative_to(out):raise ValueError('Restore outside repository in a separate scratch directory')
  if out.exists() and any(out.iterdir()):raise ValueError('Restore target must be absent or empty')
  out.mkdir(parents=True,exist_ok=True)
  for item in data['files']:
   if not item['essential']:continue
   dest=inside(out,item['localPath']);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(inside(root,item['repositoryPath']),dest)
   if digest(dest)!=item['sha256']:errors.append({'path':item['localPath'],'issue':'restored checksum mismatch'})
 result={'passed':not errors,'essentialFilesChecked':checked,'uniqueRepositoryFilesChecked':len(cache),'excludedReproducibleFiles':sum(not x['essential'] for x in data['files']),'errors':errors,'restored':str(a.restore) if a.restore else None,'localInventoryChecked':bool(a.check_local),'deletionPerformed':False}
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2));return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
