from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,DictionaryObject,DecodedStreamObject,ArrayObject,NumberObject
from PIL import ImageChops,Image
import pypdfium2 as pdfium
import json,hashlib,io,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,resolve
source=json.loads((HERE/'archive/source.json').read_text())
inventory=json.loads((HERE/'inventory.json').read_text())
before=(ROOT/source['pdf']).read_bytes()
assert hashlib.sha256(before).hexdigest()==source['pdf_sha256']
writer=PdfWriter(io.BytesIO(before),incremental=True)
labels=PdfReader(HERE/'labels_native.pdf');assert len(labels.pages)==12
forms={}
for item in inventory:
    if not item['label']:continue
    vi=item['variant']
    if vi not in forms:
        lp=labels.pages[vi];form=DecodedStreamObject()
        form.set_data(lp.get_contents().get_data())
        form.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),NameObject('/FormType'):NumberObject(1),NameObject('/BBox'):ArrayObject([NumberObject(x) for x in [660,495,922,519]]),NameObject('/Resources'):lp['/Resources'].clone(writer)})
        forms[vi]=writer._add_object(form)
    page=writer.pages[item['physical']-1]
    resources=DictionaryObject(page['/Resources']);xobjects=DictionaryObject(resources.get('/XObject') or {})
    assert '/CurrentChapter' not in xobjects
    xobjects[NameObject('/CurrentChapter')]=forms[vi];resources[NameObject('/XObject')]=xobjects;page[NameObject('/Resources')]=resources
    stream=DecodedStreamObject();stream.set_data(b'\nq\n/CurrentChapter Do\nQ\n')
    contents=page.raw_get('/Contents')
    refs=ArrayObject(list(contents.get_object())) if isinstance(contents.get_object(),ArrayObject) else ArrayObject([contents])
    refs.append(writer._add_object(stream));page[NameObject('/Contents')]=refs
memory=io.BytesIO();writer.write(memory);after_bytes=memory.getvalue()
assert after_bytes.startswith(before)
(HERE/'updated.pdf').write_bytes(after_bytes)
(HERE/'pdf_update.bin').write_bytes(after_bytes[len(before):])

with ZipFile(ROOT/source['pptx']) as z:original={n:z.read(n) for n in z.namelist()}
with ZipFile(HERE/'updated.pptx') as z:
    assert len(z.namelist())==len(set(z.namelist()))
    updated={n:z.read(n) for n in z.namelist()}
assert set(original)==set(updated)
changed=[n for n in original if original[n]!=updated[n]]
assert set(changed)=={x['path'] for x in inventory if x['label']}
equations=video_count=0
for item in inventory:
    raw=updated[item['path']];root=E.fromstring(raw)
    equations+=len(root.xpath('//*[local-name()="oMath"]'))
    video_count+=len(root.findall('.//a:videoFile',NS))
    if item['label']:
        matching=root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name="Current overview chapter"]',namespaces=NS)
        assert len(matching)==1
        label=matching[0]
        assert ''.join(label.xpath('.//a:t/text()',namespaces=NS))==item['label']
        runs=label.findall('.//a:rPr',NS)
        assert all(x.get('sz')==str(1400 if item['first_in_chapter'] else 1200) for x in runs)
        assert all(x.get('b')==('1' if item['first_in_chapter'] else '0') for x in runs)
        # Source content was retained byte-for-byte, with one new shape added.
        chunks=re.findall(rb'<p:sp\b[^>]*>.*?</p:sp>',raw,re.S)
        chunk=next(c for c in chunks if b'name="Current overview chapter"' in c)
        assert raw.replace(chunk,b'',1)==original[item['path']],item['physical']
    ids=[x.get('id') for x in root.findall('.//p:cNvPr',NS)]
    assert len(ids)==len(set(ids))
assert equations==29 and video_count==5
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest

old=pdfium.PdfDocument(before);new=pdfium.PdfDocument(after_bytes)
assert len(old)==len(new)==30
renders=HERE/'after';renders.mkdir(exist_ok=True)
scale=1.25;visual_changes=[];images=[]
for item in inventory:
    i=item['physical']-1;a,b=old[i],new[i];aa,bb=a.render(scale=scale),b.render(scale=scale)
    ia,ib=aa.to_pil().convert('RGB'),bb.to_pil().convert('RGB')
    ib.save(renders/f'slide-{i+1:02}.png')
    if item['first_in_chapter']:images.append(ib.resize((600,338)))
    diff=ImageChops.difference(ia,ib)
    if diff.getbbox():visual_changes.append(i+1)
    if item['label']:
        tp=b.get_textpage();label_text=tp.get_text_bounded(660,495,922,519).strip();tp.close()
        # Some existing pages retain clipped, invisible text from earlier
        # layouts. The new visible label is the final line in this region.
        assert label_text.splitlines()[-1]==item['label'],(i+1,repr(label_text))
        diff.paste((0,0,0),(825,26,1154,57))
    assert diff.getbbox() is None,('Unexpected visual change',i+1,diff.getbbox())
    aa.close();bb.close();a.close();b.close()
old.close();new.close()
assert visual_changes==[x['physical'] for x in inventory if x['label']]
montage=Image.new('RGB',(1200,1014),'white')
for i,img in enumerate(images):montage.paste(img,((i%2)*600,(i//2)*338))
montage.save(HERE/'chapter-starts.png')
result={'date':'2026-10-02','chapter_names':[x['chapter_name'] for x in inventory if x['first_in_chapter']],'chapter_start_slides':[x['physical'] for x in inventory if x['first_in_chapter']],'labelled_slides':visual_changes,'slide_count':30,'main_slides':25,'hidden_backups':5,'no_slides_inserted_or_reordered':True,'footers_and_native_sections_unchanged':True,'all_existing_shapes_byte_preserved':True,'native_equations_preserved':equations,'original_embedded_videos_preserved':video_count,'all_notes_and_media_byte_identical':True,'speaking_files_unchanged':True,'supplementary_pdf_unchanged':True,'full_pdf_pages':30,'all_pdf_pixels_outside_chapter_labels_identical':True,'label_box_pt':[660,21,261.6,24],'first_slide_style':'Arial 14 pt bold navy #17365D','continuing_style':'Arial 12 pt regular grey #696969','changed_parts':changed}
(HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('Verified labels and rendered all 30 pages; every original object and all PDF pixels outside the label area are preserved.')
