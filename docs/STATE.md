# Experimental showroom state
Updated: 2026-11-16
Repository: Auto-lab-digital-ui; branch devin/1794835282-3d-0-reproducibility.
Current: 3D-0 (reproducibility and asset validation) complete for owner review.
Done: provenance chain traced; Linux rebuild with Blender 5.2.2 + KTX 4.4.2 in scratch; asset gate fixed.
Result: rebuild is structurally equal and gate-clean but not byte-identical; shipped GLBs stay the baseline.
Report: docs/3d-roadmap/3D-0_REPRODUCIBILITY_REPORT.md; evidence in docs/evidence/3d-0/.
Validated: typecheck, lint, 6 test files, npm run asset:gate (3 PASS), build.
Unchanged: src/, public/ GLBs (hashes pinned by test), original repository.
Gaps: fa3d62a seat/cockpit inputs lack editable sources; Windows toolchain bytes not reproducible on Linux.
Budgets unchanged: 80,000 triangles, 24 draw calls, 5 MB per model.
Next (needs approval): portable build PR, candidate-vs-baseline render review, then 3D-1.
Default camera unchanged (Driver Hero); Driver Hero vs Cabin Pair screenshots await owner decision.
Dilum retry: X post confirmed as creator claim; YouTube/CodePen not readable; research incomplete.
No merge or deployment.
