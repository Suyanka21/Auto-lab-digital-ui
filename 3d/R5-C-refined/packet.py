"""Create compact, lossless native-distance evidence and the review sheets."""
from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from PIL import Image, ImageOps

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D.parent / "R5-C"))
from package import REF, plate, encode

VIEWS = ("before", "refined", "plain", "lumbar", "cushion")
SHEETS = ("comparison", "primary", "details")


def sheet(kind, raw):
    def view(n):
        return Image.open(raw / (n + ".png"))

    if kind == "comparison":
        return plate("Cognac leather under the same studio lights",
            "Same 80 mm camera, AgX look, exposure, sampling and reconstruction filter. Native views are in the packet.", [
            (view("before"), "R5-C", "Preserved master"),
            (view("refined"), "R5-C-refined", "Cognac finish, centre perforations and fitted seams"),
        ], 2, (950, 950))
    if kind == "primary":
        return plate("Approved primary and refined driver seat",
            "The Cycles image is mirrored on this sheet to align the visible sides. The reference lens and lighting are unknown.", [
            (Image.open(REF).crop((625, 0, 2161, 1536)), "Approved AI primary", "Front-seat design reference"),
            (ImageOps.mirror(view("refined")), "R5-C-refined", "Fixed three-quarter camera"),
        ], 2, (850, 850))
    return plate("Leather, channel seams and cushion crest",
        "A tonal row follows each draw line. The yoke joint has two stitch rows. The centre cushion carries the same punch treatment.", [
        (view("lumbar"), "Lumbar and yoke", "Recess, padded land and thread"),
        (view("cushion"), "Centre cushion", "Rolled nose and plain thigh bolsters"),
    ], 2, (830, 830))


def pack(raw, out):
    data = {}
    for name in VIEWS:
        with Image.open(raw / (name + ".png")) as src:
            rgb = src.convert("RGB")
            buf = BytesIO()
            rgb.save(buf, "WEBP", lossless=True, method=4)
            blob = buf.getvalue()
            assert Image.open(BytesIO(blob)).convert("RGB").tobytes() == rgb.tobytes()
            data["views/" + name + ".webp"] = blob
    for kind in SHEETS:
        data["sheets/" + kind + ".jpg"] = encode(sheet(kind, raw), quality=95)
    data["INSPECTION.md"] = (D / "INSPECTION.md").read_bytes()
    for name in ("checks.json", "audit.json"):
        data[name] = (out / name).read_bytes()
    data["SHA256SUMS"] = "".join(f"{sha256(b).hexdigest()}  {n}\n" for n,b in sorted(data.items())).encode()
    with ZipFile(out / "R5-C-refined-review.zip", "x") as z:
        for name, blob in sorted(data.items()):
            info = ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            z.writestr(info, blob)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("raw", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--sheet", choices=SHEETS)
    args = p.parse_args()
    if args.sheet:
        (args.out / (args.sheet + ".jpg")).write_bytes(encode(sheet(args.sheet, args.raw), quality=95))
    else:
        pack(args.raw, args.out)
