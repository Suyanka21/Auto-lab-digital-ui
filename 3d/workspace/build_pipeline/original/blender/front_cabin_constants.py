"""Photo-based estimates in metres, NOT manufacturer component specifications.
Sources and document constraints: docs/review/front-cabin-2026-11-05/REFERENCES.md.
Blender X lateral, -Y forward, Z up. Existing seat topology/UV atlas retained.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'blender/out/front-cabin'
SEAT_CENTRE = .425
CONSOLE_HALF_WIDTH = .12
DECK_Z = .568
CUP_X = .055
CUP_Y = (-.18, -.075)
CUP_RADIUS = .041
CUP_DEPTH = .058
ARMREST_CENTRE = (0, .22, .626)
ARMREST_SIZE = (.222, .31, .067)
SELECTOR_CENTRE = (-.057, -.335, .645)
# Official diagonal; photo-estimated widescreen aspect/lean and outer frame.
DISPLAY_DIAGONAL = 12.3 * .0254
DISPLAY_ASPECT = 2.65
DISPLAY_LEAN_DEGREES = 7
STITCH_DECIMATION = .55
BODY_DECIMATION = .86
