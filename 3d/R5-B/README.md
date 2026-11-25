# R5-B · Front-seat upholstery construction

**Owner review only.** Open the [editable Blender master](R5-front-seat-upholstery.blend) or the [review packet](R5-B-review.zip). The packet contains the seven individual views, primary comparison, inspection sheets, discrepancy report, audit and construction checks. [Approval scope and original form hash](APPROVAL-BASE.md) · [remaining visual discrepancies](INSPECTION.md).

## Edit the master

`01 • Tailored upholstery panels` contains separate meshes for the backrest yoke, lumbar insert, both back bolsters, rear boxing, cushion waterfall, thigh bolsters and side boxing, plus four end returns. “Boxing” is the strip of upholstery wrapping around the sides of a pad. These are abutting surface pieces, not independently watertight manufactured parts. Their panel edges register in the saved master. The original seat station and hardware are retained.

Select **Back • drawn lumbar insert → Object Data Properties → Shape Keys → Drawn lumbar channels**. At `1` the insert has the four reference-led draw lines; at `0` it returns to the unchannelled foundation without changing the cut edge. Primary and secondary regions can be selected separately. The recessed turn-in is a study material on the depressed edge faces, not a stitch or texture. The diagnostic render temporarily changes face colours; it does not save them to the master or add application slots. No perforation or quilt pattern is baked in.

The corrected backrest and cushion cages are retained in a disabled **CONSTRUCTION_ONLY** collection, outside the rendered master. The tailored surfaces are generated from those cages, **not live-bound** to them. To refit all adjacent pieces together, edit the parameters and rebuild into a new file; to alter one local seam in Blender, edit both mating boundaries. UVs are panel coordinates, not a production bake atlas. No thread, grain or finished leather response is claimed here.

## Reproduce in a clean workspace

Blender **5.2.2 LTS** (build `d13f752e3b9c`); NumPy supplied with Blender. For the review packet use Python and Pillow 12.3.0. No network calls or downloads by the builders. Start from repository root, with Git LFS installed:

```bash
set -eu
D=3d/R5-B
A=3d/R5-A/R5-front-seat-master.blend
H=.agents/skills/autolab-premium-cabin-modeling/scripts
git lfs pull --include='3d/R5-A/*.blend,3d/R5-B/*.blend' --exclude=''
sha256sum -c "$D/SHA256SUMS"
W=$(mktemp -d)
mkdir "$W/raw" "$W/package"
M="$W/R5-front-seat-upholstery.blend"
blender -b "$A" -t 2 --python-exit-code 1 -P "$D/build.py" -- "$M"
blender -b "$M" -t 2 --python-exit-code 1 -P "$D/check.py" -- "$A" "$W/package/checks.json"
blender -b "$M" -t 2 --python-exit-code 1 -P "$H/audit_master.py" -- \
  --collection R5_FRONT_SEAT_MASTER --report "$W/package/audit.json"
blender -b "$M" -t 2 --python-exit-code 1 -P "$D/render.py" -- "$W/raw" \
  three-quarter channels front side cushion bolster regions --samples 36 --size 1100
cp "$D/INSPECTION.md" "$W/package/"
python3 "$D/package.py" "$W/raw" "$W/package"
```

The check compares all untouched evaluated components and verifies directed edge pairs, not just mesh counts. A separate-process rebuild and a fresh LFS download produced the same geometry digest. Exact *file hashes* are for retrieval, not for separately serialized Blender files or machine-specific audit paths.

## Evidence storage

Original R5-A renders were supplied separately when the original LFS review-image batch was rejected. The same branch now carries [verified compact copies](../R5-A/README.md) in normal Git. R5-B uses LFS for the editable master and an ordinary, single compact ZIP for review images and reports; the full-size lossless PNGs can be regenerated. The package uses fixed archive metadata and lists the SHA-256 of each payload member. Nothing is promoted to production.
