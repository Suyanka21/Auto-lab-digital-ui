import json,hashlib,csv
from pathlib import Path
from collections import defaultdict
from PIL import Image,ImageOps,ImageDraw,ImageFont
r=Path(__file__).resolve().parents[2];out=r/'reports/B3-doors-r3'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
cur=load(out/'classic.json');src=load(out/'construction.json');before=load(out/'allocation-before.json')
materials=defaultdict(int);nodes=[]
for n in cur['nodes']:
 nodes.append({'node':n['name'],'triangles':sum(p['triangles'] for p in n['primitives'])})
 for p in n['primitives']:materials[p['material']]+=p['triangles']
comp={c['name']:c for c in src['components']};groups=defaultdict(int);rows=[]
for c in src['componentTriangleCounts']:
 name=c['name'];group='Doors' if '_door_' in name else 'Rear seating' if name.startswith('Rear_') and not name.startswith('Rear_carpet') else 'Floor/supports'
 groups[group]+=c['triangles'];rows.append({**c,'material':comp.get(name,{}).get('material'),'group':group})
(out/'allocation-after.json').write_text(json.dumps({'decodedTotal':cur['triangles'],'decodedNodes':nodes,'decodedMaterials':dict(materials),'authoredGroupsBeforeEncoding':dict(groups),'authoredComponentsBeforeEncoding':rows},indent=2))
with (out/'component-material-triangles.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['name','triangles','material','group']);w.writeheader();w.writerows(rows)
checks=[]
for item in load(out/'rollback-hashes.json'):
 actual=hashlib.sha256((r/item['path']).read_bytes()).hexdigest();checks.append({'path':item['path'],'sha256':actual,'unchanged':actual==item['sha256']})
assert all(x['unchanged'] for x in checks)
(out/'rollback-verification.json').write_text(json.dumps({'passed':True,'files':checks},indent=2))
validation=[]
for kind in ['classic','diamond','perforated']:
 d=load(out/(kind+'.json'));actual=hashlib.sha256((r/'exports/B3-doors-r3'/f'{kind}.glb').read_bytes()).hexdigest();assert actual==d['sha256'];assert d['passed'] and d['contract']['passed'] and d['texturePayloadsUnchanged'] and d['preEncodeNonConsoleBaselineExact']
 validation.append({'kind':kind,'triangles':d['triangles'],'primitives':d['primitives'],'materials':len(d['materials']),'bytes':d['bytes'],'khronosErrors':d['khronos']['issues']['numErrors'],'khronosWarnings':d['khronos']['issues']['numWarnings'],'sha256':actual})
(out/'delivery-verification.json').write_text(json.dumps(validation,indent=2))
assert load(out/'regression-tests.json')['passed'];assert load(out/'facing-audit.json')['passed']
# Report is explicit about source/master shading versus runtime-derived materials.
(out/'VISUAL_DISCREPANCIES.md').write_text('''# Door visual discrepancy review
2026-11-20. R3 is a review candidate, not visual acceptance.

## Evidence and comparison method
Approved front/rear PRIMARY AI images from reference pack commit 0e68d56c8863b5890fdcd580e570a2910edeaf38 are the design authority. These are design images, not measured manufacturing drawings. Original files remain unchanged. The comparison sheet mirrors each reference horizontally to align the installed driver-side handing; it does not change the model or claim a camera/perspective match.

Inspected R2 source, existing R2 renders, and R3 front/rear straight and three-quarter renders. The previous R2 images use different lighting/material preview settings: the R2-versus-R3 sheet documents shape evolution, not a controlled material A/B test. All five new R3 inspection views share the same neutral lighting, exposure and material setup.

| Feature | R2 discrepancy / cause | R3 correction | Remaining mismatch |
|---|---|---|---|
| Silhouette | Extruded polygon shell, abrupt corners and nearly planar face | Rebuilt rounded outline and controlled depth rings; distinct tapered rear shell | Outer perimeter and rear wheel-arch curvature still more generic and blunt than the primary design |
| Upper padding | Thin rail reads as a separate bar | Broad convex upholstered roll, softened face transitions | End caps and highlight falloff still pinch; not a continuous production-quality upholstered edge |
| Release and trim | Flat bright plate with small isolated lever | Recessed fascia/bowl, thin perimeter reveal, separated decorative insert and lever | Bowl is shallow and surround angular; missing small lock/seat-memory markings |
| Leather insert | Flat pentagonal slab with sharp seam boundary | Curved perimeter, bulged face and a low-poly seam path | Still reads too planar in the centre; perimeter seam is a fine welt, not detailed sewn stitches |
| Pull attachment | Detached curved rod laid over a flat armrest | Variable-section swept pull continues into the palmrest, with a shaped support | Upper attachment still appears appended; the reference's clear under-grip opening and stitched joint are not yet matched |
| Armrest | Rectangular shelf with uniform thickness | Wider palm support and curved lower saddle with variable section | Too soft/sausage-like at the end; support volume and abrupt insert edge need further review |
| Storage pocket | Flat applied box/plate | Curved bin face, lip and lowered inner floor; no solid top cap | Opening reads as a narrow slit, particularly straight-on; depth and end returns remain less convincing than the reference |
| Speaker | Vertical bevelled bars and thick cylindrical rim | Thin circular disc/rim; procedural fine grille in the master | Disc still looks applied; master microperforation is not baked into runtime GLB |

## Material assessment
R3 master uses tan grain leather, dark padded leather/plastic, satin aluminium, illustrative walnut and a procedural speaker grille under neutral area lights. These are physically based shader settings, not a claim that appearance matches the primary image. Tan looks too pale under the current lighting, grain and stitching are too weak, and the wood reads too uniform at this distance.

The exported GLBs deliberately reuse the existing ten runtime material names and original KTX2 payloads. They do NOT contain the master's procedural walnut/grille textures. Runtime decorative trim remains existing carbon; door leather follows MAT_Seat_Secondary. Independent door colour is not implemented. Do not substitute these master renders for browser evidence or runtime material acceptance.

## Review verdict
Meaningful shape improvement over R2, but visual discrepancy remains. Door milestone stays OPEN. No pillars, roof, cockpit expansion, production replacement or performance-limit change is authorized by this report.
''',encoding='utf-8')
lines=['# R3 measured allocation and optimisation strategy','','## Delivered candidate','R3: 79,004 decoded triangles, 22 primitives, 10 materials. R2: 78,028 triangles. Net increase: 976. Only 996 triangles remain below 80,000; the complete cabin still does not fit without further reductions.','','| Component | Decoded triangles |','|---|---:|']+[f"| {n['node']} | {n['triangles']:,} |" for n in nodes]
lines+=['','| Material | Decoded triangles |','|---|---:|']+[f'| {m} | {v:,} |' for m,v in materials.items()]
lines+=['','## Source allocation before compression','Full per-object/material rows: component-material-triangles.csv and allocation-after.json. These counts precede export filtering and are not delivery totals.','| Group | R2 | R3 |','|---|---:|---:|']+[f"| {g} | {before['authoredGroupsBeforeEncoding'][g]:,} | {v:,} |" for g,v in groups.items()]
lines+=['','## Optimisation performed','- Removed modelled speaker bars; thin face and rim retain the outline. Grille microdetail is procedural in the master only.','- Removed a redundant interior surface ring and reduced tiny seam/reveal tube sections after an initial 82,844-triangle build exceeded the cap. That attempt stopped before final export.','- Spent remaining triangles on contour and variable-section transitions. No decimation of front seats, dashboard, steering or console was performed.','','## Proposed next optimisation (requires subsequent scoped work)','1. Keep this door candidate on hold for visual review. Do not consume the 996-triangle reserve with another construction milestone.','2. Treat front stitch meshes (13,436 triangles) as the first savings investigation. Bake fine/subpixel thread into normal and recolour masks while retaining silhouette-critical perimeter thread. Verify the existing live thread shader before promotion.','3. Reduce invisible front-seat backs/undersides and tiny console bevels while protecting UV borders, upholstery pattern scale and hero-view silhouettes.','4. Bake grille, fine seams, small labels and plastic grain into an explicitly planned atlas. Preserve original runtime slots and prove the added texture payload stays under the existing byte limit.','5. Use fixed-camera master/runtime comparison plus runtime measurements before claiming visual or performance equivalence.','','## Complete-cabin proposal','The unchanged 80,000-triangle allocation proposed BEFORE modelling is in GEOMETRY_ALLOCATION.md: front seats 32k; front stitching 4k; dashboard/steering 9k; console 4k; rear seats 7k; doors 8k; enclosure/pillars/roof 6k; floor/tunnel 3k; secondary vents/details 2k; reserve 5k. These targets are not demonstrated results.','','## Separate master and runtime','Recommend maintaining the editable, component-separated Blender source and a distinct look-development master, then deriving an optimized triangulated GLB. R3 provides both source and render master; it is not a finished high-resolution production master. Procedural shader fidelity is currently ahead of the runtime derivative for grille/wood; parity is explicitly unproven. Keep the 80,000 / 24 primitive proxy / 5,242,880-byte limits unchanged.']
(out/'OPTIMISATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
v=['# Validation evidence','2026-11-20. Offline candidate checks only.','','| Candidate | Triangles | Primitives | Materials | Bytes | Khronos errors / warnings |','|---|---:|---:|---:|---:|---|']+[f"| {d['kind']} | {d['triangles']:,} | {d['primitives']} | {d['materials']} | {d['bytes']:,} | {d['khronosErrors']} / {d['khronosWarnings']} |" for d in validation]
v+=['','- Export hashes rechecked against the actual GLB files: PASS (delivery-verification.json).','- Contract checks: expected nodes/material names, finite mesh data, UV/tangent requirements, bounds and budget: PASS.','- Regression: candidate accepted; missing tangents, renamed material, missing expansion node and excessive primitive count rejected; unsafe output paths rejected. Old four-group tangent failure reproduced.','- Source orientation: 91 door mesh objects checked across both handings; reversed open surfaces corrected. This is an area-weighted orientation check, not proof of watertightness or every rendered pixel.','- R2 three GLBs, Blender source, two builders and review report SHA256: unchanged (rollback-verification.json).','- Three baseline assets: hash guard PASS. Non-console baseline arrays preserved before re-encoding; console concatenation/rebased indices exact before Draco; original KTX2 texture payloads unchanged. Draco re-encoding is lossy: no post-compression bit-exact geometry claim.','- Khronos warnings: 18 per asset relate to KTX2 MIME/image recognition in this validator. It reports Draco/BasisU extensions unsupported for full validation. Separate actual decoder/contract checks run; zero Khronos errors does not alone establish browser compatibility.','- Browser, GPU, phone performance, UI switching and master-to-WebGL visual parity: NOT TESTED in this isolated offline revision. No application was launched or modified.','- Blender 5.2.2 LTS; strict Python exit status. Material.use_nodes deprecation warnings are recorded in the render logs.','','## Actual commands','Run from the isolated workspace.','```powershell',"& 'C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe' -b -t 6 --python-exit-code 1 --python build_pipeline/isolated/build_cabin_r3.py -- B3-doors-r3",'node build_pipeline/isolated/finalize_r3.mjs B3-doors-r3','node build_pipeline/isolated/test_r3.mjs',"& 'C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe' -b -t 2 --python-exit-code 1 --python build_pipeline/isolated/audit_facing_r3.py", "& 'C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe' -b -t 6 --python-exit-code 1 --python build_pipeline/isolated/render_doors_r3.py",'```','The first render run saved the four whole-panel views before interruption. Resume uses `-- --finish` for the close-up and diagnostic, under the same settings. See reports/B3-doors-r3-render.log and B3-doors-r3-render-finish.log.']
(out/'VALIDATION.md').write_text('\n'.join(v)+'\n',encoding='utf-8')
print(json.dumps({'rollbackPassed':True,'groups':dict(groups),'candidates':validation},indent=2))
