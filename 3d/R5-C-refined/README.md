# R5-C-refined · driver-seat finish

The owner accepted R5-C's overall geometry, 14-panel construction and modelling direction and requested one finish correction. The [editable master](R5-front-seat-refined.blend) and [Cycles review packet](R5-C-refined-review.zip) are pending owner visual review. The [inspection](INSPECTION.md) compares this pass with the frozen R5-C and the approved AI front-seat primary.

## Review and editing

Open `sheets/comparison.jpg` for the fixed-camera before/after and `sheets/primary.jpg` for the design comparison. Open `views/refined.webp` at native size for the full seat, then `views/plain.webp` for the same image with all three punch controls off. Each native view retains every RGB pixel from its Cycles PNG. Only the primary comparison mirrors the seat.

- On each of **Cognac • Yoke**, **Cognac • Lumbar** and **Cognac • Waterfall**, the **Editable region finish** node exposes colour, pitch and the independent **Perforation** switch. The staggered pattern uses R5-C's existing metre-based UVs and seam margins. The pitch stays at 4 mm. The blind impression has a 1.24 mm dark core feathered to a 1.68 mm outer lip. These are modelling values. The surrounding panels and headrest use plain finishes.
- The shared shader controls the satin highlight, local roughness variation and shallow irregular grain. The darker diffuse inside the impression reduces the softbox reflection from the punch floor.
- In **Back • drawn lumbar insert**, dial **Drawn lumbar channels** from 1 to 0 to restore the original plain foundation. Its four tonal thread runs follow that key in position and thickness. The two rows along the yoke joint stay fitted to the fixed seam. All thread objects are in **06 • Removable topstitch**.
- The headrest pad and its existing thread taper locally towards the crown. The cushion adjustment changes its centre crest and underside falloff. The seat station, overall height, guides and rails retain their R5-C placement. Floor mounting remains open with the same approximately 66 mm difference.

## Rebuild and render

Run from repository root with Blender 5.2.2 LTS (`d13f752e3b9c`), Git LFS and Python with Pillow 12.3.0 including WebP. The builder checks the input hash and requires a new output path.

```bash
set -eu
B=blender
D=3d/R5-C-refined
C=3d/R5-C/R5-front-seat-leather.blend
git lfs pull --include='3d/R5-C/*.blend,3d/R5-C-refined/*.blend' --exclude=''
sha256sum -c 3d/R5-C/SHA256SUMS
sha256sum -c "$D/SHA256SUMS"
W=$(mktemp -d)
mkdir "$W/raw" "$W/package"
M="$W/R5-front-seat-refined.blend"
"$B" -b "$C" -t 2 --python-exit-code 1 -P "$D/refine.py" -- "$M"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/verify.py" -- "$C" "$W/package/checks.json"
"$B" -b "$M" -t 2 --python-exit-code 1 \
  -P .agents/skills/autolab-premium-cabin-modeling/scripts/audit_master.py -- \
  --collection R5_FRONT_SEAT_MASTER --report "$W/package/audit.json"
"$B" -b "$C" -t 2 --python-exit-code 1 -P "$D/render.py" -- "$W/raw" before
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/render.py" -- "$W/raw" refined lumbar cushion plain leather
python3 "$D/packet.py" "$W/raw" "$W/package"
```

The three whole-seat views share R5-C's 80 mm perspective camera, three softboxes, environment, exposure and AgX Medium High Contrast look. They use 1536 × 1536 pixels, 44 maximum samples, seed 11, a 1.25-pixel reconstruction filter and albedo/normal-guided denoising. The three close-ups use 880 × 880 pixels and 36 maximum samples. The leather macro reuses R5-C's 125 mm-wide needlework view to resolve the grain beside the perforated insert. The plain control changes only the three material inputs in memory.

## Independent receipt

In a new directory, retrieve from the same dedicated branch and run the fresh-open comparison.

```bash
set -eu
GIT_LFS_SKIP_SMUDGE=1 git clone --single-branch --branch devin/r5-a-front-seat-form \
  https://github.com/Suyanka21/Auto-lab-digital-ui.git receipt
cd receipt
git lfs pull --include='3d/R5-A/*.blend,3d/R5-B/*.blend,3d/R5-C/*.blend,3d/R5-C-refined/*.blend' --exclude=''
D=3d/R5-C-refined
sha256sum -c 3d/R5-A/SHA256SUMS 3d/R5-B/SHA256SUMS 3d/R5-C/SHA256SUMS "$D/SHA256SUMS"
T=$(mktemp -d)
unzip -q "$D/R5-C-refined-review.zip" -d "$T"
(cd "$T" && sha256sum -c SHA256SUMS)
blender -b "$D/R5-front-seat-refined.blend" --python-exit-code 1 -P "$D/verify.py" -- \
  3d/R5-C/R5-front-seat-leather.blend "$T/retrieved.json"
cmp "$T/checks.json" "$T/retrieved.json"
```
