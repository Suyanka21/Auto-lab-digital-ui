"""R5-B / Blender 5.2.2: local edits to two approved R5-A section cages."""
from hashlib import sha256
from math import exp
from pathlib import Path

import bpy


APPROVED = "12ccc710d47dd9445a2b6f2bc03748ad2a0845a2aba8d70f7e8a9b956305a0c7"
BACK = "Backrest • lumbar to shoulder"
PAN = "Cushion • dished pan and thigh roll"


def correct():
    if sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() != APPROVED:
        raise ValueError("Open the exact, hydrated R5-A master")
    back, pan = (bpy.data.objects[n] for n in (BACK, PAN))
    for v in back.data.vertices:
        row, col = divmod(v.index, 26)
        col = min(col, 26-col)
        # Ease the outer shoulder inward at the waist. Give the lower wing a
        # forward lip and let the upper shoulder roll back into the body.
        x, y, z = v.co
        flank = (0, 0, .04, .25, .65, 1, 1, .92, .72, .30, .08, 0, 0, 0)[col]
        v.co.x = x * (1 + flank * (.028*exp(-((z-.98)/.075)**2)
                                   - .078*exp(-((z-.842)/.068)**2)))
        v.co.y = y + flank * (.017*exp(-((z-.86)/.068)**2)
                              - .023*exp(-((z-.69)/.105)**2))
    for v in pan.data.vertices:
        _, col = divmod(v.index, 17)
        x, y, z = v.co
        # Keep the pan near the hip and its connection to the apron. Reduce
        # front-centre loft; do not drop the outer thigh-support crests with it.
        middle = exp(-(x/.167)**4)
        if col in range(1, 7):
            cut = (.005, .012, .020, .016, .007, .001)[col-1]
            v.co.z -= cut * (.32 + .68*middle)
        if col in (0, 1, 2, 16):
            v.co.y += (.003, .006, .005, .001)[(0, 1, 2, 16).index(col)] * middle
    bpy.context.view_layer.update()
    return back, pan
