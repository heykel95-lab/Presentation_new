from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from PIL import ImageChops
import pypdfium2 as pdfium
import io, hashlib, json

HERE=Path(__file__).resolve().parent
FINAL=HERE.parents[1]/'Final Presentation'
original=(FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()
checkpoint=json.loads((HERE/'archive/pdf_before.json').read_text())
assert hashlib.sha256(original).hexdigest()==checkpoint['sha256']
native=PdfReader(HERE/'native_export.pdf')
assert len(native.pages)==1
output=PdfWriter(io.BytesIO(original),incremental=True)
page,source=output.pages[21],native.pages[0]
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
assert len(after)==31
changed=[]
for index in range(31):
    old_page,new_page=before[index],after[index]
    old_bitmap,new_bitmap=old_page.render(scale=1000/960),new_page.render(scale=1000/960)
    old_image,new_image=old_bitmap.to_pil().convert('RGB'),new_bitmap.to_pil().convert('RGB')
    if ImageChops.difference(old_image,new_image).getbbox():changed.append(index+1)
    if index==21:new_image.save(HERE/'qa-22.png')
    old_bitmap.close();new_bitmap.close();old_page.close();new_page.close()
before.close();after.close()
assert changed==[22],changed
verification=json.loads((HERE/'verification.json').read_text())
verification.update({'visually_changed_physical_pages':changed,'other_30_pages_pixel_identical':True,
    'full_pdf_pages':31,'pdf_increment_bytes':len(tail),
    'supplementary_pdf_sha256':hashlib.sha256((FINAL/'Supplementary_slides.pdf').read_bytes()).hexdigest(),
    'supplementary_pdf_pages':len(PdfReader(FINAL/'Supplementary_slides.pdf').pages)})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Verified: only slide 21 / physical page 22 changed.')
