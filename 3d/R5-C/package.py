"""Preserve native Cycles evidence compactly, with lossless 1:1 detail samples."""
import argparse
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from PIL import Image, ImageDraw, ImageFont, ImageOps

D = Path(__file__).resolve().parent
REF = D.parents[1]/"AUTOLAB_INTERIOR_3D_REFERENCE_PACK/03_FRONT_SEATS/PRIMARY/AUTOLAB_SUV_FRONT_SEAT_PRIMARY_01.jpg"
VIEWS = ("presentation","three-quarter","bolster","channels","cushion","needlework",
         "material-map","plain-control","swatches")
SHEETS = ("reference","progression","construction","finishes")


def encode(im, fmt="JPEG", quality=94):
    buf = BytesIO()
    opts = dict(quality=quality,subsampling=0,optimize=True) if fmt=="JPEG" else {}
    im.convert("RGB").save(buf,fmt,**opts)
    return buf.getvalue()


def plate(title, subtitle, entries, cols, wh):
    w,h = wh
    gap, head, cap = 20,100,58
    rows = (len(entries)+cols-1)//cols
    im = Image.new("RGB",(gap+cols*(w+gap),head+rows*(h+cap+gap)), "#f4f1eb")
    draw = ImageDraw.Draw(im)
    def text(x,y,txt,size,c):
        draw.text((x,y), txt, fill=c, font=ImageFont.load_default(size=size))
    text(gap,10,"AUTOLAB     /     FRONT SEAT                                            MASTER STUDIES     /     R5-C",15,"#765235")
    text(gap,37,title,29,"#282521")
    text(gap,75,subtitle,16,"#5e5751")
    for i,(src,label,note) in enumerate(entries):
        x,y = gap+(i%cols)*(w+gap), head+(i//cols)*(h+cap+gap)
        im.paste(ImageOps.pad(src.convert("RGB"),(w,h),Image.Resampling.LANCZOS,color="#dfdbd5"),(x,y))
        text(x,y+h+6,label,19,"#282521")
        text(x,y+h+33,note,14,"#5e5751")
    return im


def sheet(name, raw):
    def v(n):
        return Image.open(raw/(n+".png"))
    if name=="reference":
        return plate("Design reference  /  material presentation",
            "The presentation uses a more frontal review camera. Reference scale, lens, lighting and physical hide are unknown.",[
            (Image.open(REF).crop((625,0,2161,1536)),"01   Approved AI seat primary","Centres are perforated; surrounding leather is plain."),
            (ImageOps.mirror(v("presentation")),"02   R5-C   /   Cycles","Mirrored here only to compare the same visible side.")],2,(700,700))
    if name=="progression":
        with ZipFile(D.parent/"R5-B/R5-B-review.zip") as z:
            before = Image.open(BytesIO(z.read("views/three-quarter.jpg")))
        return plate("From upholstery construction to finished hide",
            "Same native three-quarter camera, studio lights and AgX exposure. R5-B is the approved construction, not a failed material treatment.",[
            (before,"01   R5-B   /   working design","Original 14-panel construction and study materials."),
            (v("three-quarter"),"02   R5-C   /   material study","Local padding edits, grain, tonal thread and switchable centres.")],2,(660,660))
    if name=="construction":
        return plate("Construction details  /  Cycles", "Three fixed macro cameras. Inspect the individual files at native size for grain and stitch scale.",[
            (v("bolster"),"01   Shoulder","Curvature break at the upper bolster."),
            (v("channels"),"02   Lumbar","Raised padding between four adjustable draw lines."),
            (v("cushion"),"03   Waterfall","Rounded crest turning into the apron.")],3,(460,460))
    return plate("Finish controls  /  material regions",
        "The plain control uses the lumbar camera and lighting unchanged. Only the three perforation inputs are zeroed for that render.",[
        (v("material-map"),"01   Material assignments","Blue yoke / teal lumbar / amber cushion / red bolsters."),
        (v("plain-control"),"02   Plain control","No perforation; recessed channels and padding remain."),
        (v("needlework"),"03   Topstitch and hide","Separate thread curves beside the recessed bolster seam."),
        (v("swatches"),"04   Material lab","Curved swatches: plain surround and punched insert.")],2,(550,495))


def pack(raw,out):
    p = out/"R5-C-review.zip"
    data = {f"views/{n}.jpg":encode(Image.open(raw/(n+".png")),quality=96) for n in VIEWS}
    for n in SHEETS:
        b = encode(sheet(n,raw))
        data[f"sheets/{n}.jpg"] = b
        (out/(n+".jpg")).write_bytes(b)
    for n in ("needlework","channels","cushion"):
        im = Image.open(raw/(n+".png"))
        x,y = im.width//2, im.height//2
        data[f"lossless/{n}-1to1.png"] = encode(im.crop((x-192,y-192,x+192,y+192)),"PNG")
    for n in ("audit.json","checks.json","INSPECTION.md"):
        data[n] = (out/n).read_bytes()
    data["ORIGINAL-PNG-HASHES.txt"] = "".join(
        f"{sha256((raw/(n+'.png')).read_bytes()).hexdigest()}  {n}.png\n" for n in VIEWS).encode()
    data["SHA256SUMS"] = "".join(f"{sha256(b).hexdigest()}  {n}\n" for n,b in sorted(data.items())).encode()
    with ZipFile(p,"x") as z:
        for n,b in sorted(data.items()):
            info = ZipInfo(n,(2020,1,1,0,0,0)); info.compress_type = ZIP_DEFLATED
            z.writestr(info,b)
    with ZipFile(p) as z:
        assert z.testzip() is None and all(z.read(n)==b for n,b in data.items())
    print(len(data),"members;",p.stat().st_size,"bytes")


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("raw",type=Path)
    parser.add_argument("out",type=Path)
    parser.add_argument("--sheet",choices=SHEETS)
    a=parser.parse_args()
    if a.sheet:
        (a.out/(a.sheet+".jpg")).write_bytes(encode(sheet(a.sheet,a.raw)))
    else:
        pack(a.raw,a.out)
