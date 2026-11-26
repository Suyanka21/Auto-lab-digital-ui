"""Preserve native Cycles pixels; sheets are resized, not retouched."""
import argparse
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
spec = spec_from_file_location("r6a_packet", D.parent/"R6-A/packet.py")
base = module_from_spec(spec)
spec.loader.exec_module(base)
VIEWS = ("three-quarter", "front", "backrest", "armrest", "cabin", "construction")


def rgb(path):
    with Image.open(path) as img:
        return img.convert("RGB")


def primary(view):
    return base.sheet("R6-B   /   Rear-bench upholstery", [
        ("Approved rear-bench primary", rgb(base.PRIMARY)),
        ("R6-B   ·   Cognac leather in Cycles", view)])


def pack(raw, audit_path, out):
    views, files = {}, {}
    for key in VIEWS:
        img = rgb(raw/(key+".png"))
        assert img.size == ((1232,1232) if key in ("backrest","armrest") else (1680,1152))
        views[key] = img
        files["views/"+key+".webp"] = base.encode(img,"WEBP",lossless=True,method=4)
    files["sheets/primary.jpg"] = primary(views["three-quarter"])
    files["sheets/construction.jpg"] = base.sheet("R6-B   /   Panel construction and placement", [
        ("Upper yoke, three lumbar pads and side bolsters", views["backrest"]),
        ("Stowed centre armrest, pull and cushion returns", views["armrest"]),
        ("Straight-on elevation   ·   Independent cushions", views["front"]),
        ("Five-seat study   ·   Approved front pair", views["cabin"])])
    audit = json.loads(audit_path.read_text())
    assert audit["passed"] and audit["collection"]=="R6_REAR_BENCH_MASTER"
    audit["source"] = Path(audit["source"]).name
    files["audit.json"] = (json.dumps(audit,indent=2)+"\n").encode()
    for name in ("INSPECTION.md","checks.json"):
        files[name] = (D/name).read_bytes()
    files["SHA256SUMS"] = "".join(f"{sha256(v).hexdigest()}  {k}\n" for k,v in sorted(files.items())).encode()
    with ZipFile(out,"x") as z:
        for key,data in sorted(files.items()):
            info = ZipInfo(key,(2020,1,1,0,0,0))
            z.writestr(info,data,compress_type=ZIP_DEFLATED)
    verify(out,raw)


def verify(archive, raw=None):
    with ZipFile(archive) as z:
        assert z.testzip() is None
        want = {f"views/{v}.webp" for v in VIEWS}|{"sheets/primary.jpg","sheets/construction.jpg",
                                                     "audit.json","checks.json","INSPECTION.md"}
        entries = [line.split("  ",1) for line in z.read("SHA256SUMS").decode().splitlines()]
        assert set(z.namelist())==want|{"SHA256SUMS"} and {name for _,name in entries}==want
        for digest,key in entries:
            assert sha256(z.read(key)).hexdigest()==digest,key
        for key in ("checks.json","INSPECTION.md"):
            assert z.read(key)==(D/key).read_bytes(),key
        if raw:
            for key in VIEWS:
                recovered = rgb(BytesIO(z.read("views/"+key+".webp")))
                src = rgb(raw/(key+".png"))
                assert recovered.size==src.size and recovered.tobytes()==src.tobytes(),key
    print("Manifest and docs verified."+(" All six native RGB arrays matched." if raw else ""))


if __name__=="__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd",required=True)
    build = sub.add_parser("build")
    for arg in ("raw","audit","out"):
        build.add_argument(arg,type=Path)
    read = sub.add_parser("verify")
    read.add_argument("archive",type=Path)
    read.add_argument("--raw",type=Path)
    args=p.parse_args()
    if args.cmd=="build":
        pack(args.raw,args.audit,args.out)
    else:
        verify(args.archive,args.raw)
