---
name: autolab-premium-cabin-modeling
description: Build and review editable premium automotive cabin components in Blender from approved primary references, using AutoLab's R4 modelling discipline. Use for reference-led geometry, upholstery, materials, master review, and planning a separately validated runtime derivative; not for automatic production promotion.
---

# AutoLab premium cabin modelling

Create convincing, editable components whose visible construction follows the owner's approved design. R4 is a quality benchmark and worked example, not a template to stamp onto unrelated parts.

## Establish the contract

Read the current project handover and approval record before editing. Identify the component, approved primary image, permitted output directory, previous checkpoint and whether the task authorises **master work** or a **runtime derivative**. Preserve approved files; use a new checkpoint. A task to model does not authorise changing the application, live GLBs, budgets, reference priorities or camera presets.

For this repository, start at `DEVIN_START_HERE.md` and `3d/handover/APPROVAL.md`. Read [the R4 example](references/r4-worked-example.md) once, then only the references needed below. If installed elsewhere, obtain that project's reference and runtime contract; do not assume AutoLab's door dimensions or slot names apply.

## Detailed master workflow

1. **Read the images before scripting.** The approved primary governs visible silhouette, panel boundaries, controls and material regions. Alternates clarify depth; they do not replace contradictory primary features. Label image-derived scale, unseen construction and camera assumptions as provisional. Never call an AI design a manufacturer measurement. See [reference and geometry discipline](references/reference-and-geometry.md).
2. **Resolve large forms first.** Mark a small set of landmarks and paired boundaries. Establish silhouette, thickness, openings and connection surfaces before grain or stitches. Compare a coarse front and oblique view. Rebuild a wrong profile; subdivision only smooths the existing error.

   For a shared front-seat form, see the [R5-A seat section study](references/seat-form-study.md), approved for overall form and proportions only. For editable adjoining panels and reversible draw lines, see the [R5-B upholstery study](references/seat-panel-study.md), still subject to owner review.
3. **Make upholstered construction readable.** Use section-controlled surfaces for inserts and asymmetrical lofts for grips/armrests. Orient sections along a curved path, not one global plane. Model actual recess backs, sidewalls, floors and openings. Adjacent surfaces need coordinated boundaries and deliberate clearances, not intersecting cover patches.
4. **Keep components editable.** Separate upholstery, trim, structural plastic, metal and detail objects into collections. Preserve useful bevel/subdivision modifiers; measure their evaluated cost. Put scene reset only in explicit new-build entrypoints. Refinement opens the prior master and changes selected parts.
5. **Develop material response and UVs.** Read [materials and UVs](references/materials-and-uvs.md). Use coherent surface coordinates, restrained grain/roughness variation, soft edges and appropriate finishes. Grain is not a replacement for padded shape. Render hero material samples before judging them on a whole component.
6. **Review with consistent evidence.** Read [review and validation](references/review-and-validation.md). Use the same cameras, lights and colour management before/after; include front, oblique, problem-area macros, neutral geometry and material presentation. Inspect actual full-resolution renders. Fix the highest-impact visible discrepancies, preserve each milestone and stop at the requested owner checkpoint. If repeated corrections are not improving the same defect, report the structural limitation rather than looping indefinitely.

## Runtime derivative workflow

Only after the relevant approval and an explicit runtime task, read [runtime delivery](references/runtime-delivery.md). Derive a separate lightweight asset; retain the detailed master. Bake unsupported shaders, simplify by silhouette contribution, preserve configuration contracts, validate the exported compressed asset and test the real browser. A master audit or Cycles render never proves WebGL equivalence.

For AutoLab the **complete cabin**, per treatment GLB, remains limited to **80,000 decoded triangles, 24 primitives as a draw-call proxy, and 5,242,880 bytes**. These limits do not apply to each detailed master. Budget changes and new live slots require approval.

## Included helpers

Run under Blender with `--python-exit-code 1`; use the executable verified in the target workspace.

```sh
blender -b component.blend --python-exit-code 1 --python scripts/audit_master.py -- --collection COMPONENT_MASTER --report /tmp/component-audit.json
blender -b component.blend --python-exit-code 1 --python scripts/render_review.py -- --camera CAM_front --out /tmp/component-front.png --samples 64 --width 1440 --height 1000
python scripts/compose_comparison.py primary.jpg /tmp/component-front.png --out /tmp/comparison.jpg
```

Paths above are relative to this skill's directory. The audit checks data and packed/external image availability, not global collisions, UV distortion, manufacturing fit or visual fidelity. The renderer preserves the saved master and its lights/colour management, uses CPU Cycles, and refuses to overwrite existing evidence. Its low-sample smoke tests prove execution only. Comparison output resizes originals without retouching.

## Handoff standard

Deliver the editable master, source/reproduction path, reference mapping, actual renders, measured counts and validation, known limitations, and the owner's decision separately from technical results. Do not invent dimensions, GPU measurements, commercial approvals or unimplemented configuration capabilities. Preserve provenance and the previous milestone. Do not promote, publish, delete or transfer files unless the current task authorises those actions.
