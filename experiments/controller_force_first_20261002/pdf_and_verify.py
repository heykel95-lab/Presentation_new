from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from PIL import ImageChops
import pypdfium2 as pdfium
import hashlib, io, json, re, sys

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS, resolve
source=json.loads((HERE/'archive/source.json').read_text())
layout=json.loads((HERE/'layout.json').read_text())
PART='ppt/slides/slide6.xml'
sha=lambda data:hashlib.sha256(data).hexdigest()
original=(ROOT/source['pdf']).read_bytes()
assert sha(original)==source['pdf_sha256']
native=PdfReader(HERE/'native_export.pdf'); assert len(native.pages)==1
text=native.pages[0].extract_text()
for phrase in ['Force','Moment','Positional error','Rotational error','Cartesian wrench']:
    assert phrase in text,phrase
writer=PdfWriter(io.BytesIO(original),incremental=True)
assert len(writer.pages)==29
page,native_page=writer.pages[4],native.pages[0]
assert list(page.mediabox)==list(native_page.mediabox)
for key in ['/Contents','/Resources','/Group','/Annots']:
    if key in native_page:page[NameObject(key)]=native_page.raw_get(key).clone(writer)
    elif key in page:del page[key]
memory=io.BytesIO();writer.write(memory);updated_pdf=memory.getvalue()
assert updated_pdf[:len(original)]==original
(HERE/'updated.pdf').write_bytes(updated_pdf)
(HERE/'presentation_pdf_update.bin').write_bytes(updated_pdf[len(original):])

with ZipFile(ROOT/source['pptx']) as old,ZipFile(HERE/'updated.pptx') as new:
    assert set(old.namelist())==set(new.namelist())
    assert len(new.namelist())==len(set(new.namelist()))
    changed=[n for n in old.namelist() if sha(old.read(n))!=sha(new.read(n))]
    assert changed==[PART],changed
    oldraw,newraw=old.read(PART),new.read(PART)
    oldroot,newroot=E.fromstring(oldraw),E.fromstring(newraw)
    math=lambda raw:re.findall(rb'<[A-Za-z0-9_]+:oMath\b.*?</[A-Za-z0-9_]+:oMath>',raw,re.S)
    assert len(math(oldraw))==5 and math(oldraw)==math(newraw)
    shapes=lambda root:{s.find('p:nvSpPr/p:cNvPr',NS).get('name'):s for s in root.findall('.//p:sp',NS)}
    previous,current=shapes(oldroot),shapes(newroot)
    assert set(current)-set(previous)=={'Positional error heading','Rotational error heading'}
    ids=[x.get('id') for x in newroot.findall('.//p:cNvPr',NS)]
    assert len(ids)==len(set(ids))
    for name,item in layout['headings'].items():
        assert ''.join(current[name].itertext()).strip()==item['text']
    for item in layout['newHeadings']:
        assert ''.join(current[item['name']].itertext()).strip()==item['text']
    for name in previous:
        oldext=previous[name].find('.//a:xfrm/a:ext',NS)
        newext=current[name].find('.//a:xfrm/a:ext',NS)
        if oldext is not None:assert oldext.attrib==newext.attrib,name
    pres=E.fromstring(new.read('ppt/presentation.xml'))
    rels={r.get('Id'):r.get('Target') for r in E.fromstring(new.read('ppt/_rels/presentation.xml.rels'))}
    slide_paths=[resolve('ppt/presentation.xml',rels[s.get('{'+NS['r']+'}id')]) for s in pres.find('p:sldIdLst',NS)]
    assert len(slide_paths)==29 and slide_paths[4]==PART
    native_count=0;video_count=0;hidden_count=0
    for path in slide_paths:
        raw=new.read(path);root=E.fromstring(raw)
        native_count+=len(math(raw))
        video_count+=len(root.findall('.//a:videoFile',NS))
        hidden_count+=root.get('show')=='0'
    assert (native_count,video_count,hidden_count)==(29,5,5)

for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():
    assert sha((ROOT/name).read_bytes())==digest,name
assert len(PdfReader(ROOT/'Final Presentation/Supplementary_slides.pdf').pages)==5
before,after=pdfium.PdfDocument(original),pdfium.PdfDocument(updated_pdf)
assert len(before)==len(after)==29
changed_pages=[]
for i in range(29):
    a,b=before[i],after[i];aa,bb=a.render(scale=1.25),b.render(scale=1.25)
    ia,ib=aa.to_pil().convert('RGB'),bb.to_pil().convert('RGB')
    if ImageChops.difference(ia,ib).getbbox():changed_pages.append(i+1)
    if i==4:ib.save(HERE/'pdf-slide.png')
    aa.close();bb.close();a.close();b.close()
before.close();after.close()
assert changed_pages==[5],changed_pages
verification={
    'date':'2026-10-02','title':'Cartesian impedance controller','physical_slide':5,'footer':4,
    'reading_order':['Force and Moment','Positional error and Rotational error','Cartesian wrench'],
    'slide_count':29,'main_slides':24,'hidden_backups':5,'changed_package_parts':changed,
    'all_29_native_equations_preserved':True,'all_original_shape_dimensions_preserved':True,
    'all_five_embedded_videos_unchanged':True,'all_notes_unchanged':True,
    'speaking_files_unchanged':True,'equation_catalog_unchanged':True,
    'supplementary_pdf_unchanged':True,'pdf_pages':29,'changed_pdf_pages':changed_pages,
    'other_28_pdf_pages_pixel_identical':True,'native_powerpoint_rendered':True,
    'pptx_sha256':sha((HERE/'updated.pptx').read_bytes()),'pdf_sha256':sha(updated_pdf)
}
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Verified: only controller layout changed; all equations, notes, media and the other 28 PDF pages are unchanged.')
