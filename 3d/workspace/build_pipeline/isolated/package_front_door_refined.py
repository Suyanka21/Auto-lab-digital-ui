from pathlib import Path
import json, hashlib, html
from html.parser import HTMLParser
from PIL import Image, ImageOps, ImageDraw, ImageFont
R=Path(__file__).resolve().parents[2]
O=R/'reports/R4-front-door-refined'
OLD=R/'reports/R4-front-door-master'
REF=R/'references/approved_ai_design/01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg'
VIEWS=['front-reference','three-quarter','handle-release-closeup','pocket-speaker-closeup','release-trim-closeup','neutral-geometry','realistic-material','material-lab']
LABELS=['Reference-aligned front','Three-quarter depth','Grab handle and armrest','Pocket and speaker junction','Release housing and walnut trim','Neutral geometry inspection','Material presentation','Supplemental master material samples']
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
def sheet(size,title):
 c=Image.new('RGB',size,'#252729');ImageDraw.Draw(c).text((20,14),title,font=FONT,fill='white');return c
def tile(c,path,box,label):
 x,y,w,h=box
 with Image.open(path) as src: im=ImageOps.contain(src.convert('RGB'),(w-20,h-50))
 c.paste(im,(x+(w-im.width)//2,y+45+(h-50-im.height)//2))
 ImageDraw.Draw(c).text((x+12,y+10),label,font=FONT,fill='#e9e6df')
def write_json(name,data): (O/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# Only package fully completed final renders.
manifest=json.loads((O/'render-manifest.json').read_text())
assert manifest['views'] in [VIEWS, ['material-lab']], 'Unexpected final render batch'
evidence=(O/'final-render.log').read_text() + ((O/'material-lab-resume.log').read_text() if (O/'material-lab-resume.log').exists() else '')
manifest['views']=VIEWS
manifest['completionNote']='Seven required views completed in the original run; supplemental material lab completed in a resumed run on 2026-11-23.'
manifest['evidenceLogs']=['final-render.log','material-lab-resume.log']
assert all('RENDER_COMPLETE '+n in evidence for n in VIEWS)
audit=json.loads((O/'master-validation.json').read_text());assert audit['passed']
for n in VIEWS:
 with Image.open(O/(n+'.png')) as im: im.verify()
for n in ['INSPECTION.md','OWNER-REVIEW.md','REVIEW.md','REPRODUCE.md']: assert (O/n).is_file(),n
assert 'Pending inspection' not in (O/'INSPECTION.md').read_text(encoding='utf-8-sig'), 'Final image inspection incomplete'
c=sheet((2400,790),'AUTOLAB | R4 REFINED | PRIMARY DESIGN COMPARISON | OWNER REVIEW OPEN')
tile(c,REF,(0,52,1200,706),'Approved AI primary - visible design, not dimensions')
tile(c,O/'front-reference.png',(1200,52,1200,706),'Refined Blender master - approximate camera alignment')
c.save(O/'reference-comparison.jpg',quality=95)
c=sheet((2400,790),'AUTOLAB | ORIGINAL R4 / REFINED | SAME CAMERA AND STUDIO LIGHTING')
tile(c,OLD/'front-reference.png',(0,52,1200,706),'Original R4 checkpoint - preserved')
tile(c,O/'front-reference.png',(1200,52,1200,706),'R4-front-door-refined - separate editable checkpoint')
c.save(O/'before-after.jpg',quality=95)
c=sheet((2000,1540),'R4 / REFINED | ACTUAL DETAIL RENDERS | SAME CAMERAS')
for row,(name,label) in enumerate([('handle-release-closeup','Grip / armrest'),('pocket-speaker-closeup','Pocket / speaker')]):
 for col,folder in enumerate([OLD,O]): tile(c,folder/(name+'.png'),(col*1000,55+row*735,1000,730),('Original R4 | ' if col==0 else 'Refined | ')+label)
c.save(O/'detail-before-after.jpg',quality=94)
c=sheet((1800,2670),'R4 REFINED | ACTUAL BLENDER RENDERS | MASTER REVIEW ONLY')
for i,(name,label) in enumerate(zip(VIEWS[:7],LABELS[:7])):tile(c,O/(name+'.png'),((i%2)*900,55+(i//2)*650,900,650),label)
ImageDraw.Draw(c).multiline_text((930,2100),'Owner visual decision remains OPEN.\n\nNeutral view diagnoses geometry.\nMaterial views use procedural master shaders.\nNo runtime export or application changes.',font=SMALL,fill='#e9e6df',spacing=14)
c.save(O/'inspection-contact-sheet.jpg',quality=94)
# Region comparisons use identical crops in the analytical reference frame.
c=sheet((1800,1200),'PRIMARY / REFINED | MATCHED FRONTAL DETAIL CROPS')
a=Image.open(REF).convert('RGB').resize((1200,670),Image.Resampling.LANCZOS)
b=Image.open(O/'front-reference.png').convert('RGB').resize((1200,670),Image.Resampling.LANCZOS)
for row,(rect,title) in enumerate([((330,120,1000,420),'Release / grip / insert'),((220,380,950,635),'Pocket / speaker')]):
 for col,im in enumerate([a,b]):
  crop=ImageOps.contain(im.crop(rect),(880,500));c.paste(crop,(col*900+10,100+row*550));ImageDraw.Draw(c).text((col*900+12,65+row*550),('Primary | ' if col==0 else 'Refined | ')+title,font=FONT,fill='white')
c.save(O/'detail-reference-comparison.jpg',quality=95)
checks=[]
for item in json.loads((O/'preserved-before.json').read_text()):
 p=R/item['path'];actual=digest(p) if p.is_file() else None
 checks.append({**item,'actualSha256':actual,'unchanged':actual==item['sha256']})
write_json('preservation-check.json',{'passed':all(x['unchanged'] for x in checks),'checkedFiles':len(checks),'files':checks})
assert all(x['unchanged'] for x in checks),'Protected checkpoint changed'
manifest.pop('samples',None)
manifest.update({'perView':[{'view':n,'resolution':list(Image.open(O/(n+'.png')).size),'samples':96 if 'closeup' in n else 64,'file':n+'.png'} for n in VIEWS],'device':'Cycles CPU; no GPU/runtime measurements','colourManagement':'AgX / Medium High Contrast / exposure 0','denoising':True})
write_json('render-manifest.json',manifest)
rows='\n'.join(f'| {x["object"]} | {x["sourceVertices"]:,} | {x["evaluatedTriangles"]:,} | {", ".join(x["materials"])} |' for x in audit['objects'])
(O/'COMPONENTS.md').write_text('# R4 refined component inventory\n\nFresh-open detailed master counts; not runtime counts.\n\n| Component | Base vertices | Evaluated triangles | Master material |\n|---|---:|---:|---|\n'+rows+'\n',encoding='utf-8')
links=''.join(f'<figure><a href="{n}.png"><img src="{n}.png" alt="{html.escape(l)}" loading="lazy"></a><figcaption>{html.escape(l)}</figcaption></figure>' for n,l in zip(VIEWS,LABELS))
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AutoLab R4 refined front-door review</title><style>body{margin:0;background:#eeece7;color:#252729;font:17px/1.6 system-ui}main{max-width:1440px;margin:auto;padding:32px}h1{font:42px/1.1 Georgia}h2{font:28px Georgia}a{color:#12606b}img{width:100%;height:auto;display:block}figure{margin:0 0 26px}figcaption{padding:8px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.status{border-left:4px solid #b87238;padding:12px 20px;background:#fff8ee}nav{display:flex;flex-wrap:wrap;gap:18px;margin:24px 0}@media(max-width:700px){.grid{grid-template-columns:1fr}main{padding:18px}}</style><main><p>AUTOLAB / R4 REFINED / OWNER CHECKPOINT</p><h1>Front door.<br>A focused refinement.</h1><p class="status">Separate editable Blender master and actual renders. Data and local construction checks PASS. Final visual acceptance remains OPEN.</p><nav><a href="../../working_models/R4-front-door-refined.blend" download>Blender master</a><a href="reference-comparison.jpg" download>Reference comparison</a><a href="before-after.jpg" download>Before and after</a><a href="inspection-contact-sheet.jpg" download>Contact sheet</a><a href="REVIEW.md">Assessment</a><a href="INSPECTION.md">Visual inspection</a><a href="OWNER-REVIEW.md">Owner checklist</a><a href="master-validation.json">Geometry checks</a><a href="preservation-check.json">Preservation checks</a><a href="REPRODUCE.md">Reproduction</a></nav><h2>Approved design and refined master</h2><img src="reference-comparison.jpg" alt="Approved AI primary left and refined Blender render right"><p>Approximate orthographic alignment and matching aspect ratio. The AI image governs visible design; its camera and manufacturing dimensions are unknown.</p><h2>Original R4 and focused refinement</h2><img src="before-after.jpg" alt="Original R4 left and refined master right"><p>Original R4 remains unchanged. Camera, framing and studio lighting are retained for this comparison.</p><img src="detail-before-after.jpg" alt="Original and refined handle and pocket detail renders"><h2>Reference detail comparison</h2><img src="detail-reference-comparison.jpg" alt="Primary and refined detail crops"><p>The armrest is flatter, the grab opening is visible and the former speaker/pocket fold has been replaced. Remaining differences include upholstery tension, grab proportions, lower-panel shaping, control detail and material uniformity. Read the visual inspection before deciding.</p><h2>Final inspection views</h2><div class="grid">'''+links+'''</div><h2>Owner decision</h2><p>Please judge silhouette, grip integration, pocket and speaker construction, release/trim and material credibility. This review does not record acceptance. No runtime GLB, application change, other cabin component or workflow transfer is included.</p></main></html>'''
(O/'index.html').write_text(page,encoding='utf-8')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.paths=[]
 def handle_starttag(self,tag,attrs):self.paths.extend(v for k,v in attrs if k in ('href','src'))
parser=Links();parser.feed(page)
missing=[p for p in parser.paths if not (O/p).is_file()];assert not missing,missing
for p in O.glob('*.jpg'):
 with Image.open(p) as im:im.verify()
base=sum(x['sourceVertices'] for x in audit['objects'])
state_text=f'''# Isolated 3D state
2026-11-23: R4-front-door-refined delivered for OWNER REVIEW; visual acceptance OPEN.
Exclusive workspace AUTOLAB_3D_WORKSPACE; production app/assets untouched; no remote writes.
Design authority: approved AI pack at 0e68d56c8863b5890fdcd580e570a2910edeaf38; PRIMARY front door governs.
Reference originals retained; prior 14 ledger SHA256 discrepancies remain unresolved.
R2 rollback preserved: 78,028 triangles / 22 primitives.
R3 exports preserved: 79,004 triangles / 22 primitives each; only 996 triangles runtime headroom.
Original R4 preserved: working_models/R4-front-door-master.blend; 925,924 evaluated triangles.
Refined: working_models/R4-front-door-refined.blend; 48 meshes / {base:,} base vertices / 719,424 evaluated triangles.
Review: reports/R4-front-door-refined/index.html; comparisons, seven required PNGs and supplemental material lab.
Fresh-open data checks PASS; grip/pocket local rays and lip/grille overlap probe PASS.
{len(checks)} protected files unchanged by SHA256; final image/local-link checks PASS.
Actual Blender 5.2.2 CPU renders: 64 overview / 96 close-up samples; no GPU/browser/phone evidence.
Remaining: interpreted grab/armrest proportions, simplified lower-panel/control detail, uniform materials, grille sampling.
UV-driven procedural master shaders are not baked runtime equivalents; dimensions and hidden construction provisional.
Runtime limits unchanged: 80,000 triangles / 24 primitives / 5,242,880 bytes per complete-cabin GLB.
Diamond-only thread mask does not justify removing stitching geometry from other treatments.
No GLB export, runtime optimisation, other-door work, application change, new tools or modelling-skill transfer.
HOLD: owner visual review required; no human gate closed.
'''
assert len(state_text.splitlines())<=20
(R/'reports/STATE.md').write_text(state_text,encoding='utf-8')
validation={'passed':True,'scope':'Offline review packaging only','finalImagesVerified':len(VIEWS),'comparisonSheetsVerified':5,'localLinksChecked':len(parser.paths),'missingLinks':missing,'stateLines':len(state_text.splitlines()),'protectedFilesUnchanged':len(checks),'masterStructuralCheck':audit['passed'],'browserTested':False,'runtimeExported':False,'humanVisualApproval':False}
write_json('package-validation.json',validation)
artifacts=[R/'working_models/R4-front-door-refined.blend',R/'reports/STATE.md',*(O/(n+'.png') for n in VIEWS),*sorted(O.glob('*.jpg')),*sorted(O.glob('*.md')),O/'index.html',O/'master-validation.json',O/'master-metrics.json',O/'reference-signals.json',O/'final-render.log',O/'material-lab-resume.log',O/'master-validation.log',O/'render-manifest.json',O/'preservation-check.json',O/'package-validation.json',*(R/'build_pipeline/isolated'/n for n in ['refine_front_door_r4.py','render_front_door_refined.py','audit_front_door_refined.py','package_front_door_refined.py'])]
write_json('artifact-hashes.json',[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':digest(p)} for p in artifacts])
print(json.dumps(validation,indent=2))


