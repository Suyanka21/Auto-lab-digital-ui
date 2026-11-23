# Refined-master reproduction

Work in AUTOLAB_3D_WORKSPACE using the existing Blender 5.2.2 LTS and Python/Pillow installations.

The refinement script opens working_models/R4-front-door-master.blend and saves a separate working_models/R4-front-door-refined.blend. It imports only function definitions from the original first-party R4 builder; it does not execute that builder's scene reset or save steps. Re-running replaces the refined checkpoint, so preserve later manual edits first.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -t 4 --python-exit-code 1 --python build_pipeline/isolated/refine_front_door_r4.py
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -t 4 --python-exit-code 1 --python build_pipeline/isolated/render_front_door_refined.py -- final front-reference three-quarter handle-release-closeup pocket-speaker-closeup release-trim-closeup neutral-geometry realistic-material material-lab
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -t 2 --python-exit-code 1 --python build_pipeline/isolated/audit_front_door_refined.py
& 'C:\Python312\python.exe' build_pipeline/isolated/package_front_door_refined.py
```

Final overviews and material lab use 64 samples; close-ups use 96. Cycles CPU, four render threads, AgX Medium High Contrast, exposure 0 and denoising are retained from R4. No studio lighting change. Existing overview/detail cameras are retained; one dedicated release/wood close-up is added.

The initial interrupted preview run ended after the handle image. Completed final renders and final-render.log are the delivery evidence; pilots and previews are separately labelled.

The advisory image comparison uses the already available numpy/Pillow helper:

```powershell
& 'C:\Python312\python.exe' build_pipeline/original/.agents/skills/realistic-3d-craft/scripts/compare_to_reference.py reports/R4-front-door-refined/front-reference.png references/approved_ai_design/01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg --out reports/R4-front-door-refined/reference-signals.json
```

Its numerical signals are not visual acceptance criteria; see REVIEW.md for interpretation limits. INSPECTION.md contains the actual final-image assessment. The two pilot folders and their notes preserve the intermediate corrections.

Completion note (2026-11-23): the original final run saved all seven requested inspection views, then stopped before the supplemental material lab and batch manifest. Only `-- final material-lab` was resumed. Its command output is retained in material-lab-resume.log; the packaged render manifest reconciles both completed batches without claiming an uninterrupted eight-view run.
