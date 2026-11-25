"""Create labelled review sheets from actual PNGs. No relighting or generated pixels on the model."""
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps


src=Path(sys.argv[1])
primary=Path(__file__).resolve().parents[2]/"AUTOLAB_INTERIOR_3D_REFERENCE_PACK/03_FRONT_SEATS/PRIMARY/AUTOLAB_SUV_FRONT_SEAT_PRIMARY_01.jpg"


def plate(name,title,subtitle,tiles,columns,size):
    target=src/(name+".jpg")
    if target.exists():
        raise FileExistsError(target)
    width,height=size
    margin,top,caption=24,88,38
    rows=(len(tiles)+columns-1)//columns
    sheet=Image.new("RGB",(margin+(width+margin)*columns,top+(height+caption+margin)*rows),(239,237,231))
    draw=ImageDraw.Draw(sheet)
    font=lambda n:ImageFont.load_default(size=n)
    draw.text((margin,14),title,font=font(28),fill="#242521")
    draw.text((margin,54),subtitle,font=font(17),fill="#4c4c48")
    for i,(im,label) in enumerate(tiles):
        x=margin+(i%columns)*(width+margin)
        y=top+(i//columns)*(height+caption+margin)
        sheet.paste(ImageOps.pad(im.convert("RGB"),size,method=Image.Resampling.LANCZOS,
                                 color=(221,221,219)),(x,y))
        draw.text((x,y+height+9),label,font=font(18),fill="#242521")
    sheet.save(target,quality=93)


def render(key):
    return Image.open(src/(key+".png"))


# Crop only empty background from the supplied primary. Flip the *study* for this plate
# only: its +X outboard controls face the opposite way in the unchanged cabin coordinate frame.
plate("primary-comparison","R5-A   /   Front-seat form",
      "Compare shoulders, lumbar return, cushion nose and headrest. The projection and physical scale of the design image are unknown.",
      [(Image.open(primary).crop((625,0,2161,1536)),"01   Approved primary  ·  margin crop"),
       (ImageOps.mirror(render("three-quarter")),"02   Blender study  ·  reflected here for comparison")],2,(690,690))

plate("form-inspection","R5-A   /   Shape inspection",
      "Fixed orthographic views and an oblique neutral-material override. No stitches, flutes or treatment textures.",
      [(render(key),label) for key,label in [
          ("front","01   Front  ·  shoulder width and cushion crown"),
          ("side","02   Outboard side  ·  lumbar depth and base"),
          ("rear","03   Rear  ·  inferred carrier and restraint"),
          ("neutral","04   Neutral  ·  no colour-zone contrast")]],2,(500,500))

plate("placement-comparison","R5-A   /   Driver-station comparison",
      "Same camera, coordinates and cockpit geometry. Diagnostic colours only; not a browser render or an assembly sign-off.",
      [(render("cabin-existing"),"01   Shipped cabin  ·  current driver seat"),
       (render("cabin-r5-a"),"02   R5-A at the same station  ·  original passenger retained")],2,(690,502))
