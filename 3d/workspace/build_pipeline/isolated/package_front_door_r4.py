from pathlib import Path
import json,hashlib,shutil,html
from PIL import Image,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];O=R/'reports/R4-front-door-master'
ref=R/'references/approved_ai_design/01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg'
views=['front-reference','three-quarter','handle-release-closeup','pocket-speaker-closeup','neutral-geometry','realistic-material','material-lab']
labels=['Reference-aligned front','Three-quarter depth','Grab handle / armrest / release','Pocket / speaker','Neutral geometry inspection','Material presentation','Master material lab']
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
def tile(canvas,path,box,label):
 x,y,w,h=box;im=ImageOps.contain(Image.open(path).convert('RGB'),(w,h-42));canvas.paste(im,(x+(w-im.width)//2,y+42+(h-42-im.height)//2));ImageDraw.Draw(canvas).text((x+10,y+9),label,font=font,fill='#e9e6df')
c=Image.new('RGB',(2400,790),'#252729');d=ImageDraw.Draw(c);d.text((20,12),'R4 FRONT-DOOR MASTER | OWNER REVIEW | No visual acceptance',font=font,fill='white')
tile(c,ref,(0,52,1200,706),'Approved AI design reference - not dimensional evidence')
tile(c,O/'front-reference.png',(1200,52,1200,706),'R4 Blender master - approximate orthographic alignment')
c.save(O/'reference-comparison.jpg',quality=95)
c=Image.new('RGB',(1800,2010),'#252729');ImageDraw.Draw(c).text((20,12),'R4 | ACTUAL BLENDER RENDERS | MASTER ONLY',font=font,fill='white')
for i,name in enumerate(views[:6]):tile(c,O/(name+'.png'),((i%2)*900,55+(i//2)*650,900,650),labels[i])
c.save(O/'inspection-contact-sheet.jpg',quality=94)
# Detail crops derive from originals; source pixels remain unchanged.
c=Image.new('RGB',(1800,1160),'#252729')
a=Image.open(ref).convert('RGB').resize((1200,670),Image.Resampling.LANCZOS);b=Image.open(O/'front-reference.png').convert('RGB').resize((1200,670),Image.Resampling.LANCZOS)
for row,(rect,title) in enumerate([((330,120,1000,420),'Release / grip / insert'),((220,380,950,635),'Pocket / speaker')]):
 for col,im in enumerate([a,b]):
  crop=ImageOps.contain(im.crop(rect),(880,510));c.paste(crop,(col*900+10,row*580+60));ImageDraw.Draw(c).text((col*900+10,row*580+15),('Reference | ' if col==0 else 'Master | ')+title,font=font,fill='white')
c.save(O/'detail-comparison.jpg',quality=95)
audit=json.loads((O/'master-validation.json').read_text());assert audit['passed']
preserved=json.loads((O/'preserved-before.json').read_text());checks=[]
for item in preserved:
 p=R/item['path'];got=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None;checks.append({**item,'actualSha256':got,'unchanged':got==item['sha256']})
assert all(x['unchanged'] for x in checks)
(O/'preservation-check.json').write_text(json.dumps({'passed':True,'checkedFiles':len(checks),'files':checks},indent=2))
m=json.loads((O/'render-manifest.json').read_text());m.pop('samples',None);m['perView']=[{'view':n,'resolution':list(Image.open(O/(n+'.png')).size),'samples':96 if 'closeup' in n else 64,'file':n+'.png'} for n in views];m['device']='Cycles CPU; no GPU/runtime measurements';m['colourManagement']='AgX / Medium High Contrast / exposure 0';m['denoising']=True
(O/'render-manifest.json').write_text(json.dumps(m,indent=2))
rows='\n'.join(f'| {x["object"]} | {x["sourceVertices"]:,} | {x["evaluatedTriangles"]:,} | {", ".join(x["materials"])} |' for x in audit['objects'])
(O/'COMPONENTS.md').write_text('# R4 editable component inventory\n\nFresh-open master counts, not runtime counts.\n\n| Component | Base vertices | Evaluated triangles | Master material |\n|---|---:|---:|---|\n'+rows+'\n',encoding='utf-8')
links=''.join(f'<figure><a href="{n}.png"><img src="{n}.png" alt="{html.escape(l)}" loading="lazy"></a><figcaption>{html.escape(l)}</figcaption></figure>' for n,l in zip(views,labels))
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AutoLab R4 front-door master review</title><style>body{margin:0;background:#eeece7;color:#252729;font:17px/1.6 system-ui}main{max-width:1440px;margin:auto;padding:32px}h1{font:42px/1.1 Georgia}h2{font:28px Georgia}a{color:#12606b}img{width:100%;height:auto;display:block}figure{margin:0 0 26px}figcaption{padding:8px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.status{border-left:4px solid #b87238;padding:12px 20px;background:#fff8ee}nav{display:flex;flex-wrap:wrap;gap:18px;margin:24px 0}@media(max-width:700px){.grid{grid-template-columns:1fr}main{padding:18px}}</style><main><p>AUTOLAB / R4 / OWNER CHECKPOINT</p><h1>One front-door master.<br>Visual approval remains open.</h1><p class="status">Editable Blender candidate and actual renders. Structural checks pass; premium visual fidelity remains unresolved. No runtime GLB, application change or production promotion.</p><nav><a href="../../working_models/R4-front-door-master.blend" download>Download Blender master</a><a href="reference-comparison.jpg" download>Reference comparison</a><a href="inspection-contact-sheet.jpg" download>Contact sheet</a><a href="REVIEW.md">Assessment</a><a href="master-validation.json">Validation</a><a href="OWNER-REVIEW.md">Owner checklist</a><a href="INSPECTION.md">Image inspection record</a></nav><h2>Approved design versus candidate</h2><img src="reference-comparison.jpg" alt="Approved AI reference left, actual R4 front-door master right"><p>Same aspect and approximate framing. Unknown AI camera and inferred depth prevent exact projection or dimensional comparison. References are unchanged.</p><h2>Remaining visible discrepancies</h2><p>Release lever and switches are simplified; armrest profile and support opening differ; the speaker-to-pocket junction is pinched and the lip profile differs; upholstery grain and seams remain weak. Procedural wood reads too uniform. These require owner judgement before any continuation.</p><img src="detail-comparison.jpg" alt="Reference and rendered detail crops"><h2>Inspection views</h2><div class="grid">'''+links+'''</div><h2>Review decision</h2><p>Please review silhouette, trim/release integration, grip support, pocket depth, speaker contour and material quality. Accept or request corrections to this master before runtime optimisation or any other cabin component. This page does not record approval.</p></main></html>'''
(O/'index.html').write_text(page,encoding='utf-8')
print('Review composites, index, component inventory and preservation check written.')

# Local review consistency checks; no browser/runtime claim.
from html.parser import HTMLParser
class Links(HTMLParser):
 def __init__(self):super().__init__();self.paths=[]
 def handle_starttag(self,tag,attrs):
  self.paths.extend(v for k,v in attrs if k in ('href','src'))
parser=Links();parser.feed(page)
missing=[p for p in parser.paths if not (O/p).is_file()];assert not missing,missing
for n in views:
 with Image.open(O/(n+'.png')) as im:im.verify()
state=R/'reports/STATE.md';backup=O/'STATE-before-R4.md'
if not backup.exists():shutil.copy2(state,backup)
state_text='''# Isolated 3D state
2026-11-20: R4 single front-door master delivered for OWNER REVIEW; visual acceptance OPEN.
Exclusive workspace AUTOLAB_3D_WORKSPACE; production app/assets unchanged; no remote writes.
Design authority: approved AI pack at 0e68d56c8863b5890fdcd580e570a2910edeaf38; PRIMARY front door governs.
Reference originals retained; prior 14 ledger SHA256 discrepancies remain documented, not resolved by R4.
R2 rollback preserved: 78,028 triangles / 22 primitives.
R3 exports preserved: exports/B3-doors-r3/{classic,diamond,perforated}.glb; 79,004 triangles / 22 primitives each.
R3 sizes: 4,102,316 / 4,238,780 / 3,961,316 bytes; only 996 triangles runtime headroom.
R4 master: working_models/R4-front-door-master.blend; 48 mesh components / 54,782 base vertices.
R4 evaluated master: 925,924 triangles; not a runtime GLB and not approved for integration.
Review: reports/R4-front-door-master/index.html; seven final PNGs, comparison sheets and REVIEW.md.
Fresh-open structural/data checks PASS; 177 protected-file hashes unchanged; image/link checks PASS.
Actual Blender 5.2.2 CPU renders, 64 overview / 96 close-up samples; no GPU/browser/phone evidence.
Remaining: flat release lever, armrest/support proportions, pointed trim ends, speaker-to-pocket pinch, material response.
UV-driven master shaders and projected stitches; not baked runtime equivalents; dimensions/depth provisional.
Runtime limits unchanged: 80,000 triangles / 24 primitives / 5,242,880 bytes per complete-cabin GLB.
Diamond-only thread mask does not justify removing stitching geometry from other treatments.
No optimisation, other-door replication, new baking pipeline, viewer change or additional cabin construction.
HOLD: owner visual review required before any next milestone; no human gate closed.
'''
assert len(state_text.splitlines())<=20
state.write_text(state_text,encoding='utf-8')
validation={'passed':True,'scope':'Offline review packaging only','imagesVerified':len(views),'localLinksChecked':len(parser.paths),'missingLinks':missing,'stateLines':len(state_text.splitlines()),'protectedFilesUnchanged':len(checks),'masterStructuralCheck':audit['passed'],'browserTested':False,'runtimeExported':False,'humanVisualApproval':False}
(O/'package-validation.json').write_text(json.dumps(validation,indent=2))
artifacts=[R/'working_models/R4-front-door-master.blend',state,*sorted(O.glob('*.png')),*sorted(O.glob('*.jpg')),*sorted(O.glob('*.md')),O/'index.html',O/'master-validation.json',O/'render-manifest.json',O/'package-validation.json',*sorted((R/'build_pipeline/isolated').glob('*front_door_r4.py'))]
(O/'artifact-hashes.json').write_text(json.dumps([{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in artifacts],indent=2))
print(json.dumps(validation,indent=2))
