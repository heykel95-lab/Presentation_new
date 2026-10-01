from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,DictionaryObject,ContentStream
from PIL import ImageChops
import pypdfium2 as pdfium
import io,json,hashlib,copy

HERE=Path(__file__).resolve().parent
FINAL=HERE.parents[1]/'Final Presentation'
native=PdfReader(HERE/'native_export.pdf')
assert len(native.pages)==4
assert 'joint angles:' in native.pages[0].extract_text()
for i,name in enumerate(['cartesian_pose_position','cartesian_pose_orientation']):
    assert PdfReader(HERE/f'{name}.pdf').pages[0].mediabox==PdfReader(HERE/'archive'/f'{name}.pdf').pages[0].mediabox

def groups(page,reader):
    stream=ContentStream(page.get_contents(),reader)
    found=[];start=None;pos=None
    for j,(args,op) in enumerate(stream.operations):
        if op==b'BT':start=j;pos=None
        if op==b'Tm' and start is not None:pos=tuple(float(a) for a in args[-2:])
        if op==b'ET' and start is not None:
            found.append((pos,start,j+1));start=None
    return stream,found

def replace_text_groups(writer,target,source,positions):
    stream,before=groups(target,writer)
    src,after=groups(source,native)
    resources=DictionaryObject(dict(target['/Resources'].items()))
    fonts=DictionaryObject(dict(resources['/Font'].items()))
    resources[NameObject('/Font')]=fonts
    target[NameObject('/Resources')]=resources
    for n,pos in enumerate(positions):
        match=lambda p: p is not None and all(abs(a-b)<0.02 for a,b in zip(p,pos))
        old=next(g for g in before if match(g[0]))
        new=next(g for g in after if match(g[0]))
        new_ops=copy.deepcopy(src.operations[new[1]:new[2]])
        for args,op in new_ops:
            if op==b'Tf':
                fontkey=NameObject('/EETextFont'+str(n))
                fonts[fontkey]=source['/Resources']['/Font'].raw_get(args[0]).clone(writer)
                args[0]=fontkey
        # Iterate replacements from the end to preserve earlier operation indices.
        stream.operations[old[1]:old[2]]=new_ops
        _,before=groups_from_ops(stream)
    target[NameObject('/Contents')]=writer._add_object(stream)

def groups_from_ops(stream):
    found=[];start=None;pos=None
    for j,(args,op) in enumerate(stream.operations):
        if op==b'BT':start=j;pos=None
        if op==b'Tm' and start is not None:pos=tuple(float(a) for a in args[-2:])
        if op==b'ET' and start is not None:found.append((pos,start,j+1));start=None
    return stream,found

verification=json.loads((HERE/'verification.json').read_text())
for filename,prefix in [('Thesis_Defense_gg0_v3.pdf','presentation'),('Supplementary_slides.pdf','supplementary')]:
    original=(FINAL/filename).read_bytes()
    writer=PdfWriter(io.BytesIO(original),incremental=True)
    if prefix=='presentation':
        checkpoint=json.loads((HERE/'archive/pdf_before.json').read_text())
        assert hashlib.sha256(original).hexdigest()==checkpoint['sha256']
        page,source=writer.pages[4],native.pages[0]
        for key in ['/Contents','/Resources','/Group','/Annots']:
            if key in source:page[NameObject(key)]=source.raw_get(key).clone(writer)
            elif key in page:del page[key]
        replace_text_groups(writer,writer.pages[9],native.pages[1],[(80.016,407.52)])
        replace_text_groups(writer,writer.pages[18],native.pages[2],[(100.06,369.77),(550.1,161.3)])
        replace_text_groups(writer,writer.pages[27],native.pages[3],[(88.056,315.55)])
        expected=[5,10,19,28]
    else:
        assert original==(HERE/'archive/Supplementary_slides.pdf').read_bytes()
        replace_text_groups(writer,writer.pages[1],native.pages[3],[(88.056,315.55)])
        expected=[2]
    memory=io.BytesIO();writer.write(memory);updated=memory.getvalue()
    assert updated[:len(original)]==original
    tail=updated[len(original):]
    (HERE/f'{prefix}_pdf_update.bin').write_bytes(tail)
    (HERE/f'{prefix}_checkpoint.json').write_text(json.dumps({'original_size':len(original),
        'original_sha256':hashlib.sha256(original).hexdigest(),
        'updated_sha256':hashlib.sha256(updated).hexdigest(),'append_bytes':len(tail)},indent=2))
    before,after=pdfium.PdfDocument(original),pdfium.PdfDocument(updated)
    assert len(before)==len(after)==(31 if prefix=='presentation' else 5)
    changed=[]
    for i in range(len(before)):
        old_page,new_page=before[i],after[i]
        old_bitmap,new_bitmap=old_page.render(scale=1),new_page.render(scale=1)
        if ImageChops.difference(old_bitmap.to_pil().convert('RGB'),new_bitmap.to_pil().convert('RGB')).getbbox():changed.append(i+1)
        old_bitmap.close();new_bitmap.close();old_page.close();new_page.close()
    before.close();after.close()
    assert changed==expected,changed
    reader=PdfReader(io.BytesIO(updated))
    for i in expected:assert '(EE)' in reader.pages[i-1].extract_text(),(prefix,i)
    verification[prefix+'_changed_pages']=changed
    verification[prefix+'_other_pages_pixel_identical']=True
    verification[prefix+'_page_count']=len(reader.pages)
    print(prefix,': only expected pages changed;',len(tail),'incremental bytes.')
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
