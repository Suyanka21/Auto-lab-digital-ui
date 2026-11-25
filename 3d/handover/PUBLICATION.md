# Publication and independent retrieval: PASS

Verified 2026-11-24. Repository: [Suyanka21/Auto-lab-digital-ui](https://github.com/Suyanka21/Auto-lab-digital-ui). Branch: `chore/autolab-r4-devin-handover`. [Draft PR #8](https://github.com/Suyanka21/Auto-lab-digital-ui/pull/8) is for review; no merge or deployment was performed.

## Published checkpoints

| Commit | Purpose |
|---|---|
| `90e24eb` | Freeze approved master, earlier history, source inventory and LFS archive |
| `d9d68b6` | Portable modelling skill, tested helpers and Devin handover |
| `27dd28d1eaa910e3492f1b8d02b6a17b05db1bb8` | Tested renderer output-path correction; independently retrieved core |

This report and the final remote/cleanup receipts are a subsequent documentation-only commit on the same branch. The core at `27dd28d` adds **450 files / 232,943,487 hydrated bytes** relative to base `cd0760e`. This includes 407 unique archived source files / 231,999,292 bytes. 67 duplicate source paths resolve through inventory aliases. 37 binary paths use LFS. These are checked-out byte counts, not compressed Git transfer sizes; final verification receipts add small text files.

## Independent verification

A new HTTPS clone from GitHub was created at `C:/Users/user/AppData/Local/Temp/autolab-r4-remote-verify`. It used no local Git reference or shared LFS object cache. Its LFS storage is inside its own `.git/lfs/objects`. After fetching the renderer correction, the checked commit matched the published core above.

- `git lfs pull` and `git lfs fsck`: PASS; all 37 LFS objects retrieved; **Git LFS fsck OK**.
- `workspace_transfer.py`: PASS; all 474 essential original paths match SHA-256 through 461 distinct repository copies. Restoration into a new scratch workspace passed.
- `check_handover.py`: PASS; 12 local Markdown links, 8 Python scripts, 10 refined PNGs, essential files tracked, application/dependency/reference trees unchanged from `cd0760e`.
- `quick_validate.py`: PASS; skill format valid in both publication worktree and independent clone.
- `check_masters.py`: PASS from the independent clone; all 16 distinct Blender masters/checkpoints opened with packed image/library resources.
- `test_master_audit.py`: PASS from the independent clone; valid geometry accepted, missing UV/material and empty/missing collections rejected.
- Original R4 and refinement scripts: PASS in `autolab-r4-remote-rebuild`, restored exclusively from GitHub-retrieved bytes. Original: 925,924 evaluated triangles. Refined: 48 mesh components / 50,916 base vertices / 719,424 evaluated triangles. The new helper audited the rebuilt refined master successfully.
- Portable Cycles CPU renderer/comparison: PASS locally. A relative-path regression was fixed and rerun; actual 320x179 PNG, 2 samples, 14.068 seconds. This smoke render establishes execution only. Existing final 64/96-sample renders remain visual evidence.
- Original workspace: all 1,243 files / 359,515,335 bytes unchanged against capture; no reparse points found. Every essential file has an independently retrieved matching copy.

Machine-readable receipts: `remote-verification.json`, `cleanup-inventory.json`, and JSON/logs under `verification/`. The approved frozen master remains SHA-256 `15bb8cecfdc0fff9d011bb159792a2076d24bfa67318a4f9198f992b64ec85e2`; rebuilding creates scratch files only.

## Limits and open work

No essential handover asset is missing. Verification used Windows, Blender 5.2.2 LTS, Python 3.12.6 and the recorded dependencies. Linux/Devin execution, future Blender versions, full historical runtime finalizers, browser/phone/GPU equivalence and a new optimised R4 GLB were **NOT TESTED**. Application tests/build were not rerun because all application, live assets and dependency trees are unchanged; this is a master/skill handover.

The detailed master remains visually approved only. Minor switch/detail limitations, inferred dimensions/hidden surfaces, final fit, UV distortion and runtime optimisation remain qualified. Fourteen inherited reference-ledger hash mismatches are preserved and explained by `reference-hashes.json`. No new licence for unrelated imagery/code is implied. Historical Windows packaging scripts are not the portable entrypoint.

New authored files pass the whitespace check. Immutable archive files retain original byte-level whitespace, including inherited CRLF warnings; they were not rewritten to silence an archive-wide check.

## Cleanup checkpoint

**No deletion performed.** `cleanup-inventory.json` accounts for the entire isolated workspace, including 769 reproducible dependency/cache/intermediate files omitted from publication. The only proposed deletion root is `C:/Users/user/Documents/AUTOLAB_3D_WORKSPACE`. Final owner confirmation and a fresh unchanged-inventory check are required before deletion. Publication worktree, temporary verification directories, application repositories and global tools are outside that scope.

Final packaging correction (2026-11-25): removed generated Python bytecode from the skill's tracked files and ignored its __pycache__ directory. No master, modelling script, runtime asset or essential inventory entry changed. The original workspace remains intact.
