"""Assemble the six lossless Cycles views, labelled sheets and inspection results."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from PIL import Image, ImageDraw, ImageFont, ImageOps

D = Path(__file__).resolve().parent
VIEWS = ("pair", "front", "rear", "passenger", "diagnostic", "cabin")
PAPER, INK, MUTED = "#f4f1ec", "#2e2824", "#675f57"


def label(draw, xy, words, size, colour=INK):
    draw.text(xy, words, font=ImageFont.load_default(size=size), fill=colour)


def assembly_sheet(images):
    sheet = Image.new("RGB", (1520, 1230), PAPER)
    draw = ImageDraw.Draw(sheet)
    label(draw, (22, 16), "R5-D   /   Front-seat pair", 32)
    label(draw, (23, 61), "Blender Cycles   ·   Production seat stations   ·   X lateral, −Y forward, Z up", 20, MUTED)
    panels = (("pair", "Passenger on left, driver on right"),
              ("cabin", "Dashboard and centre console in slate"),
              ("front", "Front elevation"),
              ("rear", "Rear elevation"))
    for i, (view, caption) in enumerate(panels):
        x, y = 22 + (i % 2) * 748, 102 + (i // 2) * 557
        sheet.paste(ImageOps.contain(images[view], (728, 514), Image.Resampling.LANCZOS), (x, y))
        label(draw, (x, y + 517), caption, 21)
    return sheet


def region_sheet(images):
    sheet = Image.new("RGB", (1460, 1000), PAPER)
    draw = ImageDraw.Draw(sheet)
    label(draw, (24, 16), "R5-D   /   Passenger upholstery and outboard controls", 32)
    sheet.paste(images["diagnostic"].resize((900, 900), Image.Resampling.LANCZOS), (24, 76))
    legend = (
        ("#588cb0", "Upper yoke", "Independent perforation"),
        ("#488f78", "Lumbar insert", "Independent perforation and channel depth"),
        ("#ce9b59", "Cushion waterfall", "Independent perforation"),
        ("#ad7059", "Bolsters", "Plain cognac surrounds"),
        ("#977fa4", "Boxing", "Side wraps and returns"),
        ("#9ba377", "Headrest pad", "Plain cognac leather"),
        ("#54949c", "Outboard shield", "Passenger door side"),
        ("#e4c75a", "Adjustment controls", "Lumbar dial, recline and position paddles"),
    )
    for i, (colour, region, description) in enumerate(legend):
        y = 113 + 96 * i
        draw.rounded_rectangle((956, y + 5, 978, y + 27), 4, fill=colour)
        label(draw, (995, y), region, 24)
        label(draw, (995, y + 37), description, 18, MUTED)
    label(draw, (956, 920), "Diagnostic colours apply to this view only.", 17, MUTED)
    return sheet


def pack(raw, audit_path, checks, inspection, out):
    images = {}
    members = {}
    for view in VIEWS:
        with Image.open(raw / (view + ".png")) as source:
            rgb = source.convert("RGB")
        images[view] = rgb
        buffer = BytesIO()
        rgb.save(buffer, "WEBP", lossless=True, method=4)
        blob = buffer.getvalue()
        assert Image.open(BytesIO(blob)).convert("RGB").tobytes() == rgb.tobytes()
        members["views/" + view + ".webp"] = blob
    for name, sheet in (("assembly", assembly_sheet(images)), ("regions", region_sheet(images))):
        buffer = BytesIO()
        sheet.save(buffer, "JPEG", quality=94, subsampling=0)
        members["sheets/" + name + ".jpg"] = buffer.getvalue()
    members["INSPECTION.md"] = inspection.read_bytes()
    members["checks.json"] = checks.read_bytes()
    assert members["checks.json"] == (D / "checks.json").read_bytes()
    audit = json.loads(audit_path.read_text())
    assert audit["passed"]
    audit["source"] = Path(audit["source"]).name
    members["audit.json"] = (json.dumps(audit, indent=2) + "\n").encode()
    members["SHA256SUMS"] = "".join(f"{sha256(b).hexdigest()}  {n}\n" for n, b in sorted(members.items())).encode()
    with ZipFile(out, "x") as archive:
        for name, data in sorted(members.items()):
            member = ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            member.compress_type = ZIP_DEFLATED
            archive.writestr(member, data)


if __name__ == "__main__":
    pack(*(Path(arg) for arg in sys.argv[1:]))
