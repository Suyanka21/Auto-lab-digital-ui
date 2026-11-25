# AutoLab isolated 3D workspace
Created 2026-11-18. This is a selected-file workspace, not an application checkout.

Start with [inventory and dependencies](reports/WORKSPACE_INVENTORY_AND_DEPENDENCIES.md), then [full-cabin assessment and construction sequence](reports/FULL_CABIN_ASSESSMENT.md).

- production_baseline/: unchanged shipped GLBs; never overwrite.
- build_pipeline/: archived source scripts, historical inputs, read-only viewer contracts, baseline inspection utility.
- references/: 35-photo gallery and research, internal use only; unmerged PR6 code is review-only.
- working_models/, textures/, exports/: reserved for independent candidate work; currently empty.
- reports/: remote snapshots, hashes, environment probes, assessment and plan.

Run the lightweight inspection: `python build_pipeline/inspect_baseline.py`.
Do not run archived finalizers as-is: they promote outputs into public/ and require adaptation first.
No app, npm install, server, rendering or texture baking was run. No repositories cloned.
