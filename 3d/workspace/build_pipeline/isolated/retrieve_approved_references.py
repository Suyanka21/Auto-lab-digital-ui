import urllib.request,json,hashlib,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
root=Path(r'C:\Users\user\Documents\AUTOLAB_3D_WORKSPACE')
out=root/'references/approved_ai_design'; commit='0e68d56c8863b5890fdcd580e570a2910edeaf38'; prefix='AUTOLAB_INTERIOR_3D_REFERENCE_PACK/'
req=urllib.request.Request(f'https://api.github.com/repos/Suyanka21/Auto-lab-digital-ui/git/trees/{commit}?recursive=1',headers={'User-Agent':'AutoLab-isolated-reference-retrieval'})
tree=json.load(urllib.request.urlopen(req,timeout=40))
files=[x for x in tree['tree'] if x['type']=='blob' and x['path'].startswith(prefix)]
manifest=(out/'REFERENCE_MANIFEST.md').read_text(encoding='utf-8-sig'); ledger={}
for line in manifest.splitlines():
 if '| JPEG |' in line:
  cells=[c.strip() for c in line.split('|')];ledger[cells[1].strip('`')]=(int(cells[4].replace(',','')),cells[6].strip('`'))
def fetch(item):
 rel=item['path'][len(prefix):]; dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True)
 url=f'https://raw.githubusercontent.com/Suyanka21/Auto-lab-digital-ui/{commit}/'+urllib.parse.quote(item['path'])
 data=urllib.request.urlopen(url,timeout=60).read(); blob=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
 if blob!=item['sha']:raise RuntimeError('Remote blob mismatch '+rel)
 if dest.exists() and dest.read_bytes()!=data:raise RuntimeError('Refusing to replace differing reference '+rel)
 dest.write_bytes(data); sha=hashlib.sha256(data).hexdigest();expected=ledger.get(rel)
 return {'path':rel,'bytes':len(data),'sha256':sha,'gitBlobVerified':True,'manifestBytes':expected[0] if expected else None,'manifestSha256':expected[1] if expected else None,'manifestMatches':(len(data),sha)==expected if expected else None,'source':url}
with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,files))
images=[r for r in records if r['path'].lower().endswith(('.jpg','.jpeg','.png'))]
report={'commit':commit,'files':records,'imageCount':len(images),'manifestMismatchCount':sum(not r['manifestMatches'] for r in images)}
(root/'reports/approved-ai-reference-retrieval.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'fileCount':len(records),'imageCount':len(images),'manifestMismatchCount':report['manifestMismatchCount'],'images':[{'path':r['path'],'bytes':r['bytes'],'manifestMatches':r['manifestMatches']} for r in images]},indent=2))
