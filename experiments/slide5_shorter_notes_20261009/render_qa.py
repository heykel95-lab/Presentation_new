from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
sys.path.insert(0,str(ROOT/'tmp/remove_b5_20260922/deps'))
import pymupdf as fitz
from PIL import Image,ImageOps
for name,folder in [('Simple_speech.pdf','speech_pages'),('notes_preview.pdf','notes_pages')]:
 out=H/folder;out.mkdir(exist_ok=True)
 doc=fitz.open(H/name)
 for i,page in enumerate(doc,1):
  page.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(out/f'page-{i:02}.png')
 print(name,len(doc),'pages rendered')
 doc.close()
