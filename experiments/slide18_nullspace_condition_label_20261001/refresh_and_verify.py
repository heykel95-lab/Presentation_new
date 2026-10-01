from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject
from PIL import ImageChops
import pypdfium2 as pdfium
import io,json,hashlib

HERE=Path(__file__).resolve().parent
FINAL=HERE.parents[1]/'Final Presentation'
original=(FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()
checkpoint=json.loads((HERE/'archive/pdf_before.json').read_text())
assert hashlib.sha256(original).hexdigest()==checkpoint['sha256']
native=PdfReader(HERE/'native_export.pdf')
assert len(native.pages)==1
assert 'Null-space condition:' in native.pages[0].extract_text()
output=PdfWriter(io.BytesIO(original),incremental=True)
page,source=output.pages[18],native.pages[0]
for key in ['/Contents','/Resources','/Group','/Annots']:
    if key in source:page[NameObject(key)]=source.raw_get(key).clone(output)
    elif key in page:del page[key]
memory=io.BytesIO();output.write(memory)
updated=memory.getvalue()
assert updated[:len(original)]==original
tail=updated[len(original):]
(HERE/'presentation_pdf_update.bin').write_bytes(tail)
(HERE/'pdf_checkpoint.json').write_text(json.dumps({
    'original_size':len(original),'original_sha256':hashlib.sha256(original).hexdigest(),
    'updated_sha256':hashlib.sha256(updated).hexdigest(),'append_bytes':len(tail)
},indent=2))
before,after=pdfium.PdfDocument(original),pdfium.PdfDocument(updated)
assert len(before)==len(after)==31
changed=[]
for i in range(31):
    old_page,new_page=before[i],after[i]
    old_bitmap,new_bitmap=old_page.render(scale=1),new_page.render(scale=1)
    if ImageChops.difference(old_bitmap.to_pil().convert('RGB'),new_bitmap.to_pil().convert('RGB')).getbbox():changed.append(i+1)
    old_bitmap.close();new_bitmap.close();old_page.close();new_page.close()
before.close();after.close()
assert changed==[19],changed
verification=json.loads((HERE/'verification.json').read_text())
verification.update({'full_pdf_pages':31,'other_30_pages_pixel_identical':True,
    'changed_physical_pages':changed,'pdf_increment_bytes':len(tail),
    'supplementary_pdf_sha256':hashlib.sha256((FINAL/'Supplementary_slides.pdf').read_bytes()).hexdigest(),
    'speaking_file_hashes':{str(p.relative_to(FINAL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        [FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',
         FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex',FINAL/'Speaker_notes_and_timing.txt']}})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('All pages checked; only physical slide 19 changed.')
