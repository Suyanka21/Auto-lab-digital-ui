# R5-C · driver-seat leather study

**Owner visual review; not a production asset.** [Editable Blender master](R5-front-seat-leather.blend) · [Cycles review packet](R5-C-review.zip) · [inspection and open issues](INSPECTION.md) · [approval for the input design](APPROVAL-BASE.md).

## What to inspect

Start with `sheets/reference.jpg`, then `sheets/progression.jpg` for a fixed-camera comparison with R5-B. The primary sheet mirrors the presentation **only on that sheet**. Individual images are at native render resolution; the three lossless PNG crops isolate small surface detail without JPEG compression. The diagnostic shows material assignments, not simulated finishes: blue yoke, teal lumbar, amber waterfall, rust bolster faces, violet boxing, olive headrest, charcoal turn-ins and gold thread. Hardware retains its own grey materials.

## Editing the seat

- **Colour and treatment:** select an insert in `01 • Tailored upholstery panels`. In its first material slot, the **Editable region finish** node has **Hide tone**, **Perforation** and **Pitch (m)**. Each centre has a separate material instance. Set **Perforation** to `0` for plain leather; do this on all three for the plain study. Punches are procedural colour/normal impressions, not through-holes, opacity or mesh cuts. The physical pitch, thread size and cognac pigment are study choices, not specifications.
- **Grain and gloss:** opening the shared finish group exposes the cell grain, broader variation, roughness, topcoat and pore graph. Editing the group changes the recipe across regions; editing a group **input on a material** changes only that material's users. Plain leather uses local object-metre grain; the three inserts also have measured-across / centreline-length coordinates for a staggered punch field, with an unpunched seam margin. This is not a production UV layout.
- **Lumbar padding:** `Back • drawn lumbar insert` → Object Data → Shape Keys → **Drawn lumbar channels**. `0` restores the original R5-B plain foundation and `1` restores the R5-C draw and raised lands. This is independent of perforation.
- **Thread:** disable `06 • Removable topstitch` in viewport **and render** to remove it. Each stitch is a tapered curve segment. The paired rows follow surface distance in from the bolster cut edges; the headrest line fits the evaluated pad. They follow this saved shape, not arbitrary future vertex edits: regenerate them after resculpting their supporting surface.
- **Frozen:** the 14 panels have the original polygon loops and world-space cut edges. The corrected hidden R5-B construction cages, headrest position, handed structure and rails remain. R5-C is not a new seat layout or a production material binding.

## Reproduction

From repository root, with the verified Blender 5.2.2 LTS (`d13f752e3b9c`), its bundled NumPy, Git LFS, and Python/Pillow 12.3.0 for packaging:

```bash
set -eu
export PYTHONDONTWRITEBYTECODE=1
B=blender
D=3d/R5-C
BASE=3d/R5-B/R5-front-seat-upholstery.blend
git lfs pull --include='3d/R5-A/*.blend,3d/R5-B/*.blend,3d/R5-C/*.blend' --exclude=''
sha256sum -c 3d/R5-A/SHA256SUMS
sha256sum -c 3d/R5-B/SHA256SUMS
sha256sum -c "$D/SHA256SUMS"
W=$(mktemp -d)
mkdir "$W/raw" "$W/package"
M="$W/R5-front-seat-leather.blend"
"$B" -b "$BASE" -t 2 --python-exit-code 1 -P "$D/lab.py" -- "$W/raw/swatches.png"
"$B" -b "$BASE" -t 2 --python-exit-code 1 -P "$D/build.py" -- "$M"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/check.py" -- "$BASE" "$W/package/checks.json"
"$B" -b "$M" -t 2 --python-exit-code 1 \
  -P .agents/skills/autolab-premium-cabin-modeling/scripts/audit_master.py -- \
  --collection R5_FRONT_SEAT_MASTER --report "$W/package/audit.json"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/render.py" -- "$W/raw" \
  presentation three-quarter bolster channels cushion needlework material-map plain-control
cp "$D/INSPECTION.md" "$W/package/"
python3 "$D/package.py" "$W/raw" "$W/package"
```

The build first applies the four local surface edits to the **exact hashed R5-B source**, then assigns finishes. For geometry-only inspection, run `form.py` instead of `build.py` on the same input, writing a new scratch `.blend`. Neither builder modifies its input. The rendering scripts work in memory and never save a camera or diagnostic material over the master.

For retrieval rather than rebuilding, start with an empty directory and no shared Git LFS cache:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --single-branch --branch devin/r5-a-front-seat-form \
  https://github.com/Suyanka21/Auto-lab-digital-ui.git seat-receipt
cd seat-receipt
git lfs pull --include='3d/R5-A/*.blend,3d/R5-B/*.blend,3d/R5-C/*.blend' --exclude=''
sha256sum -c 3d/R5-C/SHA256SUMS
T=$(mktemp -d)
unzip -q 3d/R5-C/R5-C-review.zip -d "$T"
(cd "$T" && sha256sum -c SHA256SUMS)
blender -b 3d/R5-C/R5-front-seat-leather.blend --python-exit-code 1 \
  -P 3d/R5-C/check.py -- 3d/R5-B/R5-front-seat-upholstery.blend "$T/fresh.json"
cmp "$T/fresh.json" "$T/checks.json"
```

The packet also records the hashes of the full-size source PNGs. Rebuilds may have different Blender file bytes, render noise across platforms and audit paths. Use the construction checker and controlled renders to compare the rebuilt **content**, not separately saved `.blend` hashes. No external textures, fonts, HDRIs, rebakes or runtime exporters are needed.
