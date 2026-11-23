"""Check portable skill references, payload hashes and protected application trees."""
from pathlib import Path
import argparse,ast,hashlib,json,re,subprocess
from PIL import Image

def main():
 p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parents[3];errors=[]
 skill=root/'.agents/skills/autolab-premium-cabin-modeling';entry=(skill/'SKILL.md').read_text(encoding='utf-8-sig')
 if not entry.startswith('---\n') or 'name: autolab-premium-cabin-modeling' not in entry:errors.append('Invalid skill frontmatter')
 docs=[root/'DEVIN_START_HERE.md',*list((root/'3d/handover').glob('*.md')),*list(skill.rglob('*.md'))];links=0
 for f in docs:
  for dest in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8-sig')):
   if '://' in dest or dest.startswith('#'):continue
   links+=1
   if not (f.parent/dest.split('#')[0]).exists():errors.append('Missing local link '+str(f.relative_to(root))+' -> '+dest)
 scripts=[*skill.joinpath('scripts').glob('*.py'),*root.joinpath('3d/handover/scripts').glob('*.py'),*root.joinpath('3d/handover/tests').glob('*.py')]
 for f in scripts:ast.parse(f.read_text(encoding='utf-8-sig'))
 images=list(root.joinpath('3d/workspace/reports/R4-front-door-refined').glob('*.png'))
 for f in images:
  with Image.open(f) as im:im.verify()
 inv=json.loads((root/'3d/handover/workspace-inventory.json').read_text());tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0'));untracked=sorted({x['repositoryPath'] for x in inv['files'] if x['essential']}-tracked)
 if untracked:errors.append('Essential files not tracked: '+str(untracked))
 protected={}
 for name in ['src','public','scripts','tests','package.json','package-lock.json','AUTOLAB_INTERIOR_3D_REFERENCE_PACK','AUTOLAB_2020_LEXUS_RX350_REFERENCE_LIBRARY']:
  before=subprocess.check_output(['git','rev-parse','cd0760e:'+name],cwd=root).decode().strip();now=subprocess.check_output(['git','rev-parse','HEAD:'+name],cwd=root).decode().strip();protected[name]=before==now
  if before!=now:errors.append('Protected tree changed: '+name)
  if subprocess.check_output(['git','diff','HEAD','--',name],cwd=root).strip():errors.append('Protected working tree changed: '+name)
 result={'passed':not errors,'localLinksChecked':links,'pythonScriptsParsed':len(scripts),'refinedPngsReadable':len(images),'allEssentialFilesTracked':not untracked,'protectedTreesUnchanged':protected,'errors':errors}
 a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
