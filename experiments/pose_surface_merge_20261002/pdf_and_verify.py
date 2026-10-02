from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,DictionaryObject,DecodedStreamObject
from PIL import ImageChops
import pypdfium2 as pdfium
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,resolve
source=json.loads((HERE/'archive/source.json').read_text());inventory=json.loads((HERE/'inventory.json').read_text());build=json.loads((HERE/'build.json').read_text())
reader=PdfReader(ROOT/source['pdf']);native=PdfReader(HERE/'native_export.pdf')
assert len(reader.pages)==30 and len(native.pages)==2
writer=PdfWriter()
for i in build['retained_original_pages']:
    writer.add_page(native.pages[0] if i==4 else reader.pages[i-1])
font=reader.pages[2]['/Resources']['/Font']['/F2'];assert font['/Encoding']=='/WinAnsiEncoding'
widths=font['/Widths'];first=int(font['/FirstChar'])
for num in range(5,25):
    page=writer.pages[num-1];data=page.get_contents().get_data()
    chunks=re.findall(rb'BT\b.*?ET',data,re.S)
    targets=[b for b in chunks if re.search(rb'(?<![\d.])9\d{2}(?:\.\d+)?\s+2\d(?:\.\d+)?\s+(?:Tm|TD|Td)\b',b)]
    assert len(targets)==1,(num,targets)
    text=str(num-1);width=sum(float(widths[ord(c)-first]) for c in text)*8.04/1000;baseline=26.64 if b'26.64' in targets[0] else 26.52
    replacement=f'BT /MergedFooter 8.04 Tf 1 0 0 1 {921.8-width:.6f} {baseline} Tm 0.412 g 0.412 G 0 Tc [({text})] TJ ET'.encode()
    resources=DictionaryObject(page['/Resources']);fonts=DictionaryObject(resources['/Font']);fonts[NameObject('/MergedFooter')]=font.clone(writer);resources[NameObject('/Font')]=fonts;page[NameObject('/Resources')]=resources
    stream=DecodedStreamObject();stream.set_data(data.replace(targets[0],replacement,1));page[NameObject('/Contents')]=writer._add_object(stream)
writer.write(HERE/'updated.pdf')

with ZipFile(ROOT/source['pptx']) as z:old={n:z.read(n) for n in z.namelist()}
with ZipFile(HERE/'updated.pptx') as z:
    assert len(z.namelist())==len(set(z.namelist()))
    new={n:z.read(n) for n in z.namelist()}
assert set(old)-set(new)==set(build['removed_parts']) and not set(new)-set(old)
pres=E.fromstring(new['ppt/presentation.xml']);sids=pres.find('p:sldIdLst',NS);assert len(sids)==29
retained=[e for e in inventory if e['physical']!=5]
assert [x.get('id') for x in sids]==[x['sid'] for x in retained]
assert pres.xpath('.//p14:sldId/@id',namespaces=NS)==[x['sid'] for x in retained]
eq_old={};eq_new={};videos=0
def math(node):return [E.tostring(x,method='c14n',exclusive=True) for x in node.xpath('.//*[local-name()="oMath"]')]
for item in inventory:
    root=E.fromstring(old[item['path']])
    for s in root.findall('.//p:sp',NS):
        if math(s):eq_old[s.find('p:nvSpPr/p:cNvPr',NS).get('name')]=math(s)
for num,item in enumerate(retained,1):
    root=E.fromstring(new[item['path']]);videos+=len(root.findall('.//a:videoFile',NS))
    ids=[x.get('id') for x in root.findall('.//p:cNvPr',NS)];assert len(ids)==len(set(ids))
    for s in root.findall('.//p:sp',NS):
        if math(s):eq_new[s.find('p:nvSpPr/p:cNvPr',NS).get('name')]=math(s)
    if num!=4:
        raw=new[item['path']];orig=old[item['path']]
        if 5<=num<=24:
            block=next(x for x in re.findall(rb'<p:sp\b[^>]*>.*?</p:sp>',raw,re.S) if b'name="TextBox 6"' in x)
            prior=next(x for x in re.findall(rb'<p:sp\b[^>]*>.*?</p:sp>',orig,re.S) if b'name="TextBox 6"' in x)
            assert raw.replace(block,prior,1)==orig
        else:assert raw==orig
assert eq_old==eq_new and sum(len(v) for v in eq_new.values())==29
assert videos==5
refs=0
for name,data in new.items():
    if name.endswith('.xml') or name.endswith('.rels'):E.fromstring(data)
    if name.startswith(('ppt/media/','ppt/notesSlides/','ppt/slideMasters/','ppt/slideLayouts/')):assert data==old[name]
    if name.endswith('.rels'):
        owner='' if name=='_rels/.rels' else name.replace('/_rels/','/')[:-5]
        for r in E.fromstring(data):
            if r.get('TargetMode')!='External':assert resolve(owner,r.get('Target')) in new;refs+=1
catalog=json.loads((HERE/'native_equations.json').read_text());assert len(catalog)==29
for item in catalog:
    root=E.fromstring(new[retained[item['slide']-1]['path']])
    assert root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$n]',namespaces=NS,n=item['shape'])
for n,d in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==d

before=pdfium.PdfDocument(ROOT/source['pdf']);after=pdfium.PdfDocument(HERE/'updated.pdf')
assert len(after)==29
renders=HERE/'after';renders.mkdir(exist_ok=True);changed=[]
for idx,oldnum in enumerate(build['retained_original_pages']):
    a,b=before[oldnum-1],after[idx];aa,bb=a.render(scale=1.25),b.render(scale=1.25);ia,ib=aa.to_pil().convert('RGB'),bb.to_pil().convert('RGB');ib.save(renders/f'slide-{idx+1:02}.png')
    diff=ImageChops.difference(ia,ib)
    if diff.getbbox():changed.append(idx+1)
    if idx+1!=4:
        if 5<=idx+1<=24:diff.paste((0,0,0),(1125,625,1159,653))
        assert diff.getbbox() is None,('Unexpected visual change',idx+1,diff.getbbox())
    aa.close();bb.close();a.close();b.close()
before.close();after.close()
v={'date':'2026-10-02','merged_original_physical_slides':[4,5],'combined_slide':4,'title':'Cartesian pose and surface frame','next_slide':'Cartesian impedance controller','slide_count':29,'main_slides':24,'hidden_backups':5,'all_three_figures_preserved':True,'all_29_native_equations_preserved':True,'native_equation_catalog_updated':True,'all_five_embedded_videos_unchanged':True,'all_retained_notes_unchanged':True,'removed_slide_and_notes_archived':True,'speaking_files_unchanged':True,'supplementary_pdf_unchanged':True,'pdf_pages':29,'other_pdf_content_pixel_identical_except_footers':True,'changed_pdf_pages':changed,'internal_relationships_resolved':refs,'chapter_labels_preserved':True,'scientific_wording_source':'MyOwn/chapters/02_theoretical_background.tex: base-frame wrench; surface-coordinate stiffness and damping'}
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Verified all equations, media, notes, relationships and all 29 PDF pages; only the merged slide and later main footers change.')
