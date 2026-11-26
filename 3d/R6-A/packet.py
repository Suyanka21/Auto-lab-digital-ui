"""Package native Cycles RGB pixels and labelled, uncropped review sheets."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont, ImageOps

D = Path(__file__).resolve().parent
PRIMARY = D.parents[1] / "AUTOLAB_INTERIOR_3D_REFERENCE_PACK/04_REAR_BENCH/PRIMARY/AUTOLAB_SUV_REAR_BENCH_PRIMARY_01.jpg"
VIEWS = ("three-quarter", "front", "side", "rear", "cabin")


def encode(image, fmt, **options):
    data = BytesIO()
    image.save(data, fmt, **options)
    return data.getvalue()


def sheet(title, cells):
    height = 90 + 473*((len(cells)+1)//2)
    paper = Image.new("RGB", (1440,height), "#f5f2ec")
    pen = ImageDraw.Draw(paper)
    pen.text((20,20), title, fill="#302824", font=ImageFont.load_default(size=31))
    for i,(caption,image) in enumerate(cells):
        x,y = 20+(i%2)*710, 75+(i//2)*473
        resized = ImageOps.contain(image,(692,424),Image.Resampling.LANCZOS)
        paper.paste(resized,(x+(692-resized.width)//2,y+(424-resized.height)//2))
        pen.text((x,y+432),caption,fill="#4e4540",font=ImageFont.load_default(size=21))
    return encode(paper,"JPEG",quality=93,subsampling=0)


def pack(raw, audit_path, out):
    views, members = {}, {}
    for name in VIEWS:
        with Image.open(raw/(name+".png")) as source:
            assert source.size == (1400,960)
            rgb = source.convert("RGB")
        data = encode(rgb,"WEBP",lossless=True,method=4)
        assert Image.open(BytesIO(data)).convert("RGB").tobytes() == rgb.tobytes()
        members["views/"+name+".webp"] = data
        views[name] = rgb
    with Image.open(PRIMARY) as ref:
        members["sheets/primary.jpg"] = sheet("R6-A   /   Rear-bench form", [
            ("Approved rear-bench primary", ref),
            ("R6-A three-quarter   ·   Form materials", views["three-quarter"])])
    members["sheets/placement.jpg"] = sheet("R6-A   /   Silhouette and cabin positioning", [
        ("Front   ·   Three seating positions", views["front"]),
        ("Side   ·   Cushion depth and backrest rake", views["side"]),
        ("Rear   ·   Split load face and four feet", views["rear"]),
        ("Five-seat placement   ·   Provisional floor", views["cabin"])])
    audit = json.loads(audit_path.read_text())
    assert audit["passed"] and audit["collection"] == "R6_REAR_BENCH_MASTER"
    audit["source"] = Path(audit["source"]).name
    members["audit.json"] = (json.dumps(audit,indent=2)+"\n").encode()
    for name in ("checks.json","INSPECTION.md"):
        members[name] = (D/name).read_bytes()
    members["SHA256SUMS"] = "".join(f"{sha256(b).hexdigest()}  {n}\n"
                                     for n,b in sorted(members.items())).encode()
    with ZipFile(out,"x") as archive:
        for name, data in sorted(members.items()):
            info = ZipInfo(name,(2020,1,1,0,0,0))
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info,data)


if __name__ == "__main__":
    pack(*(Path(arg) for arg in sys.argv[1:]))
