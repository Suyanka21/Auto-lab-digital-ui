# Validation evidence
2026-11-20. Offline candidate checks only.

| Candidate | Triangles | Primitives | Materials | Bytes | Khronos errors / warnings |
|---|---:|---:|---:|---:|---|
| classic | 79,004 | 22 | 10 | 4,102,316 | 0 / 18 |
| diamond | 79,004 | 22 | 10 | 4,238,780 | 0 / 18 |
| perforated | 79,004 | 22 | 10 | 3,961,316 | 0 / 18 |

- Export hashes rechecked against the actual GLB files: PASS (delivery-verification.json).
- Contract checks: expected nodes/material names, finite mesh data, UV/tangent requirements, bounds and budget: PASS.
- Regression: candidate accepted; missing tangents, renamed material, missing expansion node and excessive primitive count rejected; unsafe output paths rejected. Old four-group tangent failure reproduced.
- Source orientation: 91 door mesh objects checked across both handings; reversed open surfaces corrected. This is an area-weighted orientation check, not proof of watertightness or every rendered pixel.
- R2 three GLBs, Blender source, two builders and review report SHA256: unchanged (rollback-verification.json).
- Three baseline assets: hash guard PASS. Non-console baseline arrays preserved before re-encoding; console concatenation/rebased indices exact before Draco; original KTX2 texture payloads unchanged. Draco re-encoding is lossy: no post-compression bit-exact geometry claim.
- Khronos warnings: 18 per asset relate to KTX2 MIME/image recognition in this validator. It reports Draco/BasisU extensions unsupported for full validation. Separate actual decoder/contract checks run; zero Khronos errors does not alone establish browser compatibility.
- Browser, GPU, phone performance, UI switching and master-to-WebGL visual parity: NOT TESTED in this isolated offline revision. No application was launched or modified.
- Blender 5.2.2 LTS; strict Python exit status. Material.use_nodes deprecation warnings are recorded in the render logs.

## Actual commands
Run from the isolated workspace.
```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -t 6 --python-exit-code 1 --python build_pipeline/isolated/build_cabin_r3.py -- B3-doors-r3
node build_pipeline/isolated/finalize_r3.mjs B3-doors-r3
node build_pipeline/isolated/test_r3.mjs
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -t 2 --python-exit-code 1 --python build_pipeline/isolated/audit_facing_r3.py
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -t 6 --python-exit-code 1 --python build_pipeline/isolated/render_doors_r3.py
```
The first render run saved the four whole-panel views before interruption. Resume uses `-- --finish` for the close-up and diagnostic, under the same settings. See reports/B3-doors-r3-render.log and B3-doors-r3-render-finish.log.
