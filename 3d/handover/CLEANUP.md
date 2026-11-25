# Local cleanup — awaiting explicit confirmation

**No deletion has been performed or authorised.** The publication instruction explicitly requires a final owner confirmation after remote verification.

Proposed future scope is strictly `C:\Users\user\Documents\AUTOLAB_3D_WORKSPACE` and its inventoried contents. `workspace-inventory.json` lists all 1,243 files, 359,515,335 bytes, with SHA-256, size, essential status and destination or exclusion reason. It includes 474 essential files and 769 reproducible dependency/cache/derived-intermediate files. Empty directories contain no unique content.

Remote retrieval PASSED on 2026-11-24. `remote-verification.json` and `cleanup-inventory.json` record verified core commit `27dd28d` and per-file copy status. All 474 essential paths have independently retrieved matching bytes, all 1,243 original files are unchanged, and no reparse points were found. A successful push or local hash check alone is insufficient. Any missing essential file or new/changed local file blocks deletion.

Before any later deletion:

1. Obtain the owner's explicit final confirmation for this exact directory.
2. Re-run the remote inventory verifier and `workspace_transfer.py --check-local C:/Users/user/Documents/AUTOLAB_3D_WORKSPACE`; stop for any discrepancy.
3. Resolve the absolute target and confirm it equals the named isolated workspace. Inspect reparse points; do not follow a junction into other directories.
4. Use native PowerShell literal-path operations within that exact root only, and report removed bytes/files and anything retained.

Outside the scope: the experimental application checkout, publication worktree, temporary retrieval/reproduction directories, original production repository, global Blender/KTX installations, shared caches, Downloads, attachments and unrelated projects. They remain untouched. This handover contains no automatic deletion script.
