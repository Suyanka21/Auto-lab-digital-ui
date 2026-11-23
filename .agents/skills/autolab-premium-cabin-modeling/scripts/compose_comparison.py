"""Create a labelled reference/render comparison; no retouching or geometric edits."""
from pathlib import Path
import argparse
from PIL import Image,ImageOps,ImageDraw,ImageFont

def main():
 p=argparse.ArgumentParser();p.add_argument('reference',type=Path);p.add_argument('render',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists():raise ValueError('Preserve previous evidence; select a new output filename')
 canvas=Image.new('RGB',(2400,850),'#252729');draw=ImageDraw.Draw(canvas);font=ImageFont.load_default(size=24)
 draw.text((20,12),'Reference / actual Blender render | visual judgement required',font=font,fill='white')
 for i,(path,label) in enumerate([(a.reference,'Approved reference - inspect its evidence limitations'),(a.render,'Actual render - unchanged pixels, resized for comparison')]):
  with Image.open(path) as im:tile=ImageOps.contain(im.convert('RGB'),(1180,740))
  canvas.paste(tile,(i*1200+(1200-tile.width)//2,95+(740-tile.height)//2));draw.text((i*1200+12,57),label,font=font,fill='white')
 a.out.parent.mkdir(parents=True,exist_ok=True);canvas.save(a.out,quality=94);print(str(a.out))
if __name__=='__main__':main()
