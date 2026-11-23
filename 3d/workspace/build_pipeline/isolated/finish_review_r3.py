from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,hashlib,html
r=Path(__file__).resolve().parents[2];o=r/'reports/B3-doors-r3'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17);title=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',30)
views=[('front-straight','Front door / straight'),('front-three-quarter','Front door / three-quarter'),('rear-straight','Rear door / straight'),('rear-three-quarter','Rear door / three-quarter'),('armrest-handle-trim-closeup','Armrest, pull and trim / close-up'),('diagnostic-material-regions','DIAGNOSTIC regions / not material quality')]
for stem,_ in views:
 with Image.open(o/(stem+'.png')) as im:assert im.size==(1280,900);im.verify()
assert (r/'working_models/B3-doors-r3-master.blend').is_file()
def paste_fit(canvas,path,box,mirror=False):
 im=Image.open(path).convert('RGB')
 if mirror:im=ImageOps.mirror(im)
 im=ImageOps.contain(im,(box[2],box[3]));canvas.paste(im,(box[0]+(box[2]-im.width)//2,box[1]+(box[3]-im.height)//2))
sheet=Image.new('RGB',(1600,1940),'#ebe8e2');d=ImageDraw.Draw(sheet);d.text((30,20),'AUTOLAB / R3 DOOR INSPECTION',font=title,fill='#20252a');d.text((30,66),'Blender look-development master. Runtime KTX2 appearance differs. Visual acceptance OPEN.',font=small,fill='#333333')
for i,(stem,label) in enumerate(views):
 x=20+(i%2)*790;y=110+(i//2)*600;d.text((x,y),label,font=font,fill='#222222');paste_fit(sheet,o/(stem+'.png'),(x,y+36,770,545))
d.text((30,1920),'Neutral studio lighting / Cycles 48 samples / AgX exposure 0 / R2 rollback preserved',font=small,fill='#333333');sheet.save(o/'inspection-contact-sheet.jpg',quality=94)
comp=Image.new('RGB',(1600,1270),'#ebe8e2');d=ImageDraw.Draw(comp);d.text((24,18),'PRIMARY DESIGN vs R3 CANDIDATE',font=title,fill='#20252a');d.text((24,64),'AI references mirrored to match handing; perspective differs. Original reference files unchanged.',font=small,fill='#333333')
for i,row in enumerate(['front','rear']):
 y=110+i*565;d.text((24,y),row.title()+' / approved AI primary (mirrored)',font=font,fill='#222222');d.text((820,y),row.title()+' / R3 Blender master',font=font,fill='#222222')
 paste_fit(comp,r/f'reports/reference-r2/AUTOLAB_SUV_{row.upper()}_DOOR_PANEL_PRIMARY_01.jpg',(20,y+40,770,505),True);paste_fit(comp,o/(row+'-straight.png'),(810,y+40,770,505))
d.text((24,1240),'Reference is design evidence, not OEM dimensions. Master walnut/grille are not baked runtime materials.',font=small,fill='#333333');comp.save(o/'reference-comparison.jpg',quality=94)
comp=Image.new('RGB',(1600,1270),'#ebe8e2');d=ImageDraw.Draw(comp);d.text((24,18),'R2 ROLLBACK vs R3 GEOMETRY REVISION',font=title,fill='#20252a');d.text((24,64),'Different legacy R2 lighting/materials: shape comparison only, not a controlled material A/B test.',font=small,fill='#333333')
for i,row in enumerate(['front','rear']):
 y=110+i*565;d.text((24,y),row.title()+' / R2 preserved',font=font,fill='#222222');d.text((820,y),row.title()+' / R3 master',font=font,fill='#222222')
 paste_fit(comp,r/f'reports/B3-doors-r2/{row}-door.png',(20,y+40,770,505));paste_fit(comp,o/(row+'-straight.png'),(810,y+40,770,505))
comp.save(o/'r2-r3-comparison.jpg',quality=94)
review='''# R3 door-panel owner review
2026-11-20. Technical PASS; visual acceptance OPEN. Stop at doors.

## Start here
- [Reference comparison](reference-comparison.jpg)
- [All inspection renders](inspection-contact-sheet.jpg)
- [Preserved R2 versus R3](r2-r3-comparison.jpg) (different legacy lighting; shape comparison only)
- [Interactive local review index](index.html)
- [Specific visual discrepancies](VISUAL_DISCREPANCIES.md)
- [Allocation before modelling](GEOMETRY_ALLOCATION.md)
- [Measured revised allocation and strategy](OPTIMISATION.md)
- [Per-component and material CSV](component-material-triangles.csv)
- [Validation results and commands](VALIDATION.md)

## What changed
Four door panels rebuilt with rounded shells, padded upper surfaces, recessed release/trim regions, sculpted leather inserts, swept pull/palmrest construction, curved bin faces and thin speaker discs. Reversed open faces were corrected. No production assets, viewer code, original baseline meshes or material contracts were edited.

Classic, Diamond and Perforated each pass offline checks at **79,004 triangles / 22 primitives / 10 materials**. Bytes: **4,102,316 / 4,238,780 / 3,961,316** respectively. Only **996 triangles remain**; the remaining cabin cannot be completed in this headroom. Proposed full-cabin redistribution retains 80,000 triangles and is not yet achieved.

## Material evidence boundary
These are actual Blender geometry renders under neutral studio lighting. The source and separate MASTER look-development file are supplied. Procedural tan leather, illustrative walnut and grille detail in the master do not establish equivalent appearance in the GLBs. Runtime candidates keep original KTX2 textures/carbon trim and material names. Speaker microperforation and wood have not been baked into them. Diagnostic colours are shown separately and prove only region separation.

## Remaining visible issues
The pocket opening is still too shallow visually; the armrest is soft and its under-grip opening/support is less resolved than the primary design. Upper-roll ends, rear silhouette, inset seams, release recess and fine material character need review. R3 improves R2 but does not fully match the primary reference. See the feature-by-feature discrepancy table.

## Owner review checkpoint
- [ ] Judge front and rear silhouette against the primary design.
- [ ] Review pull attachments, under-grip clearance, armrest support and pocket depth.
- [ ] Review upper padding, trim recesses and insert seam boundaries.
- [ ] Review the proposed master/runtime optimisation workflow and full-cabin allocation.
- [ ] Decide whether these door forms need another revision before any next milestone.

No box is pre-approved. Pillars/roof are on hold. Runtime material parity, browser/phone performance and complete-cabin acceptance remain unverified.

## Files and rollback
- Editable component source: `../../working_models/B3-doors-r3.blend`
- Separate shaded master: `../../working_models/B3-doors-r3-master.blend`
- Runtime candidates: `../../exports/B3-doors-r3/{classic,diamond,perforated}.glb`
- Reproducible scripts: `../../build_pipeline/isolated/*r3*`
- R2 rollback: `../../exports/B3-doors-r2/` and `../../working_models/B3-doors-r2.blend`.

SHA256 verification confirms all seven protected R2 files unchanged. Baseline hash guard passes. No push, deployment, production replacement or human-gate closure occurred.
'''
(o/'REVIEW.md').write_text(review,encoding='utf-8')
figures=''.join(f'<figure><a href="{stem}.png"><img src="{stem}.png" alt="{html.escape(label)}"></a><figcaption>{html.escape(label)} <a href="{stem}.png" download>Save PNG</a></figcaption></figure>' for stem,label in views)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>AutoLab R3 door review</title><style>body{margin:0;background:#ebe8e2;color:#25282b;font:17px/1.6 system-ui}main{max-width:1350px;margin:auto;padding:36px}h1{font:44px Georgia}a{color:#125d69}img{max-width:100%;height:auto}figure{margin:0 0 24px}figcaption{padding:10px}nav{display:flex;gap:20px;flex-wrap:wrap}.notice{border-left:4px solid #86632b;padding:14px 22px;background:#f7f3ea}.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}@media(max-width:760px){.grid{grid-template-columns:1fr}main{padding:20px}}</style><main><p>AUTOLAB / DOOR REVIEW / R3</p><h1>Geometry revised. Visual acceptance open.</h1><div class="notice"><strong>Offline technical PASS: 79,004 triangles, 22 primitives, 10 materials.</strong><br>Only 996 triangles remain. No next cabin milestone. These are Blender master renders; procedural wood and grille details are not baked into the runtime GLBs.</div><nav><a href="REVIEW.md">Review report</a><a href="VISUAL_DISCREPANCIES.md">Remaining discrepancies</a><a href="OPTIMISATION.md">Budget and optimisation</a><a href="VALIDATION.md">Validation</a><a href="component-material-triangles.csv" download>Component CSV</a><a href="inspection-contact-sheet.jpg" download>Save contact sheet</a></nav><h2>Primary references and candidate</h2><p>Approved AI design images mirrored only to align handing. Perspective differs.</p><a href="reference-comparison.jpg"><img src="reference-comparison.jpg" alt="Front and rear primary AI reference comparison"></a><h2>Inspection views</h2><p>Neutral area lighting, Cycles 48 samples, AgX exposure 0. Click images for full resolution.</p><div class="grid">'''+figures+'''</div><h2>Diagnostic legend</h2><p>Ochre: secondary upholstery. Blue: upper padded dashboard-trim binding. Grey-green: structural plastic. Rose: decorative carbon binding (wood only in master). Silver: metal. This image does not prove material quality.</p><h2>R2 preserved</h2><p>Different legacy lighting and materials; use this comparison for shape changes only.</p><img src="r2-r3-comparison.jpg" alt="R2 versus R3 shape comparison"><p>Review remains open. Pocket depth, armrest support, seam definition and master/runtime material parity are unresolved.</p></main></html>'''
(o/'index.html').write_text(page,encoding='utf-8')
state=r/'reports/STATE.md';backup=o/'STATE-before-r3.md'
if not backup.exists():backup.write_bytes(state.read_bytes())
state.write_text('''# Isolated 3D state
2026-11-20: R3 door correction delivered for OWNER REVIEW; visual acceptance OPEN.
Exclusive workspace AUTOLAB_3D_WORKSPACE; production assets/app unchanged; no remote writes.
Design authority: approved AI pack at 0e68d56c8863b5890fdcd580e570a2910edeaf38.
Reference originals retained; 16 Git blobs verified; 14 ledger SHA256 mismatches remain documented.
R2 rollback preserved: 78,028 triangles, 22 primitives; seven protected file hashes unchanged.
R3 exports: exports/B3-doors-r3/{classic,diamond,perforated}.glb.
Each R3: 79,004 triangles / 22 primitives / 10 materials; only 996 triangles headroom.
Bytes: Classic 4,102,316; Diamond 4,238,780; Perforated 3,961,316.
Blender source and separate lookdev master: working_models/B3-doors-r3*.blend.
Review index, comparisons, five inspection renders and separate diagnostic: reports/B3-doors-r3/.
Offline contract, decoder, mutation regression, 91-object facing and baseline guards PASS.
Khronos: 0 errors / 18 KTX2 warnings per candidate; browser/GPU/phone NOT TESTED.
Master procedural leather/walnut/grille are NOT runtime baked equivalents; GLBs retain KTX2/carbon.
Door leather follows secondary-seat binding; independent door/headliner/stars not implemented.
Remaining visual issues: pocket depth, armrest support/opening, silhouette, seams and trim recesses.
Complete-cabin 80k allocation proposed, not achieved; front stitch detail is main savings target.
No performance-limit or architecture changes. No seat geometry edits or PR6 promotion.
HOLD: owner door review required before pillars/roof or any next construction milestone.
''',encoding='utf-8')
assert len(state.read_text().splitlines())<=20
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in o.iterdir() if p.suffix in ['.png','.jpg','.md','.csv','.html']}
(o/'review-artifact-hashes.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'imagesVerified':6,'masterExists':True,'stateLines':len(state.read_text().splitlines()),'review':str(o/'index.html')}))
