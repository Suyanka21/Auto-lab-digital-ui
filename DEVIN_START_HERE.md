# Devin: start here

**Repository:** Suyanka21/Auto-lab-digital-ui
**Handover branch:** `chore/autolab-r4-devin-handover`
**Base:** `cd0760e` (includes merged reference-pack PR #7). Do not switch to the original AUTOLAB-DIGITAL-SHOWROOM repository.

The owner approved **R4-front-door-refined as the visual modelling benchmark** on 2026-11-23. It remains a detailed editable master, not a production GLB. Window switches and minor details are accepted limitations for this checkpoint. Read [approval and exact hash](3d/handover/APPROVAL.md) before interpreting the older review reports, which correctly retain their earlier OPEN status.

## Start in your own workspace

```sh
git clone --branch chore/autolab-r4-devin-handover --single-branch https://github.com/Suyanka21/Auto-lab-digital-ui.git autolab
cd autolab
git lfs install --local
git lfs pull
python3 3d/handover/scripts/workspace_transfer.py --report /tmp/autolab-transfer-check.json
```

Git LFS must retrieve actual Blender/GLB bytes, not just pointer files. A GitHub ZIP may not include LFS objects. Install required software only under your environment's approval rules.

1. Read [project handover](3d/handover/HANDOVER.md), [runtime contracts](3d/handover/RUNTIME_CONTRACT.md) and [dependencies/provenance](3d/handover/DEPENDENCIES_AND_PROVENANCE.md).
2. Load `.agents/skills/autolab-premium-cabin-modeling/SKILL.md` (invoke `$autolab-premium-cabin-modeling` where skills are supported). Other agents can read the same Markdown directly.
3. Open `3d/workspace/working_models/R4-front-door-refined.blend` in Blender 5.2.2 LTS. Its primary reference is packed; original reference files remain at `AUTOLAB_INTERIOR_3D_REFERENCE_PACK/`.
4. Inspect `3d/workspace/reports/R4-front-door-refined/reference-comparison.jpg`, `before-after.jpg`, the seven final PNG views, and `INSPECTION.md`. Use [reproduction commands](3d/handover/REPRODUCTION.md) for a complete restored scratch workspace and portable scripts.
5. Continue only the component work authorised by the owner. Preserve the master and production app; use separate checkpoints. Do not replace live GLBs, change contracts, merge or deploy as a consequence of this handover.

[Publication and retrieval evidence](3d/handover/PUBLICATION.md) records what was actually tested. [Cleanup scope](3d/handover/CLEANUP.md) is for the owner: no deletion is authorised by this handover.
