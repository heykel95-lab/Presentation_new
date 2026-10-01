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
assert len(native.pages)==3
output=PdfWriter(io.BytesIO(original),incremental=True)
indices=[19,20,21]
for index,source in zip(indices,native.pages):
    target=output.pages[index]
    if index in [19,20]:
        # Reuse the exact original high-resolution PDF poster. Only the small
        # QA deck had a downsampled preview image to avoid duplicating media.
        old_images=target['/Resources']['/XObject']
        poster=max(old_images.values(),key=lambda obj:obj.get_object().get('/Width',0))
        assert poster.get_object()['/Width']==1440
        new_images=source['/Resources']['/XObject']
        name=max(new_images,key=lambda key:new_images[key].get_object().get('/Width',0))
        assert new_images[name].get_object()['/Width']>200
        new_images[name]=poster
    for key in ['/Contents','/Resources','/Group','/Annots']:
        if key in source: target[NameObject(key)]=source.raw_get(key).clone(output)
        elif key in target: del target[key]
memory=io.BytesIO();output.write(memory)
updated=memory.getvalue()
assert updated[:len(original)]==original
tail=updated[len(original):]
(HERE/'presentation_pdf_update.bin').write_bytes(tail)
(HERE/'pdf_checkpoint.json').write_text(json.dumps({
    'original_size':len(original),'original_sha256':hashlib.sha256(original).hexdigest(),
    'updated_sha256':hashlib.sha256(updated).hexdigest(),'append_bytes':len(tail)
},indent=2))
reader=PdfReader(io.BytesIO(updated))
assert len(reader.pages)==31
texts=[reader.pages[index].extract_text() for index in indices]
assert 'Damping only' in texts[0] and 'Conditioning only' in texts[1]
assert 'Disturbance without' in texts[2] and 'null-space control torque' in texts[2]
for index in indices[:2]:
    assert max(obj.get_object().get('/Width',0) for obj in reader.pages[index]['/Resources']['/XObject'].values())==1440

before,after=pdfium.PdfDocument(original),pdfium.PdfDocument(updated)
changed=[]
for index in range(31):
    old_page,new_page=before[index],after[index]
    old_bitmap,new_bitmap=old_page.render(scale=1000/960),new_page.render(scale=1000/960)
    old_image,new_image=old_bitmap.to_pil().convert('RGB'),new_bitmap.to_pil().convert('RGB')
    if ImageChops.difference(old_image,new_image).getbbox():changed.append(index+1)
    if index in indices:new_image.save(HERE/f'qa-{index+1}.png')
    old_bitmap.close();new_bitmap.close();old_page.close();new_page.close()
before.close();after.close()
assert changed==[20,21,22],changed
verification=json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
verification.update({'visually_changed_physical_pages':changed,'other_28_pages_pixel_identical':True,
    'full_pdf_pages':31,'pdf_increment_bytes':len(tail),'original_pdf_poster_images_preserved':True,
    'supplementary_pdf_sha256':hashlib.sha256((FINAL/'Supplementary_slides.pdf').read_bytes()).hexdigest(),
    'supplementary_pdf_pages':len(PdfReader(FINAL/'Supplementary_slides.pdf').pages)})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('All 31 pages rendered; only physical slides 20, 21 and 22 changed.')
