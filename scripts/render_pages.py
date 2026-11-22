"""Render original pages; no source PDF is written. Reruns skip existing images."""
import json,sys
from pathlib import Path
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
for m in json.loads((ROOT/'content/modules.json').read_text(encoding='utf8')):
 out=ROOT/'public/assets/sources'/m['id'];out.mkdir(parents=True,exist_ok=True)
 doc=fitz.open(ROOT/m['path'])
 for p in doc:
  dest=out/f'{p.number+1}.webp'
  if dest.exists():continue
  scale=min(1600/p.rect.width,1800/p.rect.height)
  pix=p.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False)
  Image.frombytes('RGB',[pix.width,pix.height],pix.samples).save(dest,'WEBP',quality=86,method=3)
 print(m['id'],len(doc),'pages rendered',flush=True)
