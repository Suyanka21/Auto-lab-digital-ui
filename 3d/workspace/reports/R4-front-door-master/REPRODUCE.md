# R4 reproduction

Run from the isolated AUTOLAB_3D_WORKSPACE. No dependency installation is required.

Open working_models/R4-front-door-master.blend for direct editing. The approved image is packed as a camera guide, not a surface texture.

For reproducibility, existing scripts are:

1. build_pipeline/isolated/build_front_door_r4.py — rebuilds the R4 master and master-metrics.json. It replaces only the named R4 master; do not run over subsequent manual edits without a backup.
2. build_pipeline/isolated/render_front_door_r4.py — opens the master without saving it; renders the requested review cameras.
3. build_pipeline/isolated/audit_front_door_r4.py — opens the saved master and writes structural evidence.
4. build_pipeline/isolated/package_front_door_r4.py — creates the comparison sheets, local review page and component inventory from actual outputs; rechecks preserved-file hashes.

Used executable: C:\Program Files\Blender Foundation\Blender 5.2\blender.exe (5.2.2 LTS).

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -t 4 --python-exit-code 1 --python build_pipeline/isolated/render_front_door_r4.py -- final front-reference three-quarter handle-release-closeup pocket-speaker-closeup neutral-geometry realistic-material material-lab
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b -t 2 --python-exit-code 1 --python build_pipeline/isolated/audit_front_door_r4.py
& 'C:\Python312\python.exe' build_pipeline/isolated/package_front_door_r4.py
```

Final-render metadata is in render-manifest.json. master-metrics.json describes saved scene defaults (48 samples); it does not override the actual final render script's 64/96 sample settings.

No GLB export command is part of this checkpoint. The original 80k / 24 primitive / 5 MiB complete-cabin runtime limits remain unchanged.
