"""Make the compact inspection packet from actual Blender PNGs. No generated imagery."""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import argparse

from PIL import Image, ImageDraw, ImageFont, ImageOps


D = Path(__file__).resolve().parent
REF = D.parents[1]/"AUTOLAB_INTERIOR_3D_REFERENCE_PACK/03_FRONT_SEATS/PRIMARY/AUTOLAB_SUV_FRONT_SEAT_PRIMARY_01.jpg"
VIEWS = ("three-quarter","front","side","bolster","channels","cushion","regions")


def jpeg(im, quality=92):
    sink=BytesIO()
    im.convert("RGB").save(sink,"JPEG",quality=quality,subsampling=0,optimize=True)
    return sink.getvalue()


def plate(title, subtitle, items, cols, tile):
    w,h=tile
    gap,top,foot=18,91,56
    rows=(len(items)+cols-1)//cols
    im=Image.new("RGB",(gap+(w+gap)*cols,top+(h+foot+gap)*rows),(241,239,234))
    pen=ImageDraw.Draw(im)
    def text(x,y,s,size,col):
        pen.text((x,y),s,font=ImageFont.load_default(size=size),fill=col)
    text(gap,9,"AUTOLAB   /   MASTER STUDIES                                  R5-B     •     UPHOLSTERY",14,"#536253")
    text(gap,31,title,28,"#202622"); text(gap,64,subtitle,17,"#454943")
    for i,(image,label,note) in enumerate(items):
        x=gap+(i%cols)*(w+gap); y=top+(i//cols)*(h+foot+gap)
        im.paste(ImageOps.pad(image.convert("RGB"),tile,Image.Resampling.LANCZOS,
                              color="#dfdfda"),(x,y))
        text(x,y+h+5,label,19,"#202622"); text(x,y+h+31,note,14,"#474c47")
    return im


def main(raw,out):
    package=out/"R5-B-review.zip"
    if package.exists():
        raise FileExistsError(package)
    views={n:Image.open(raw/(n+".png")).convert("RGB") for n in VIEWS}
    sheets={
        "checkpoint-comparison":plate("From form to upholstery","Same native three-quarter camera. Compare the waist below the shoulder and the height of the cushion nose.",[
            (Image.open(D.parent/"R5-A/review/three-quarter.webp"),"01   R5-A   /   approved form","Archived Blender render, before either form correction."),
            (views["three-quarter"],"02   R5-B   /   upholstery study","Corrected support cages and separate fitted cover pieces.")
        ],2,(640,640)),
        "primary-comparison":plate("Design comparison","Silhouette, shoulder return, arched yoke and lower draw lines. Camera and scale of the primary are unknown.",[
            (Image.open(REF).crop((625,0,2161,1536)),"01   Approved seat primary","Margin crop only; authoritative visible design."),
            (ImageOps.mirror(views["three-quarter"]),"02   R5-B   /   reflected for comparison","Only this image is reflected. All other views are native driver side.")
        ],2,(640,640)),
        "fixed-views":plate("Form and panel map","Same driver station, inspection rig and study lighting as R5-A. Diagnostic colours identify editable pieces, not finishes.",[
            (views["front"],"01   Front   /   orthographic","Trace the arch and both pairs of draw lines."),
            (views["side"],"02   Outboard   /   orthographic","Shoulder waist, cushion lip and unchanged rails."),
            (views["three-quarter"],"03   Native three-quarter","Foam transitions into the shield, not a projected image."),
            (views["regions"],"04   Region diagnostic","Blue yoke · teal lumbar · ochre cushion · rust bolsters · violet boxing.")
        ],2,(500,500)),
        "construction-details":plate("Upholstery details","Independent camera renders. The channels and recessed seam profiles are geometry; no treatment texture or perforation is applied.",[
            (views["bolster"],"01   Shoulder to side bolster","The face rolls into a separate wraparound side piece."),
            (views["channels"],"02   Lumbar insert","Two paired draw lines terminate below the curved yoke."),
            (views["cushion"],"03   Cushion waterfall","The centre continues over the nose between separately cut wings.")
        ],3,(438,438)),
    }
    files={f"views/{n}.jpg":jpeg(im,94) for n,im in views.items()}
    files.update({f"sheets/{n}.jpg":jpeg(im) for n,im in sheets.items()})
    for n in ("INSPECTION.md","audit.json","checks.json"):
        files[n]=(out/n).read_bytes()
    files["SHA256SUMS"]=("".join(f"{sha256(b).hexdigest()}  {n}\n"
                                   for n,b in sorted(files.items()))).encode()
    with ZipFile(package,"x") as z:
        for n,b in sorted(files.items()):
            info=ZipInfo(n,(2020,1,1,0,0,0)); info.compress_type=ZIP_DEFLATED
            z.writestr(info,b)
    with ZipFile(package) as z:
        assert z.testzip() is None
        for n,b in files.items():
            assert z.read(n)==b
    for n in sheets:
        (out/(n+".jpg")).write_bytes(files["sheets/"+n+".jpg"])
    print(f"{len(files)} members; {package.stat().st_size} bytes")


if __name__=="__main__":
    arg=argparse.ArgumentParser()
    arg.add_argument("raw",type=Path)
    arg.add_argument("out",type=Path,help="Directory containing INSPECTION.md, audit.json and checks.json")
    args=arg.parse_args()
    main(args.raw,args.out)
