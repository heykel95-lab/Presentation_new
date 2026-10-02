from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader,PdfWriter,Transformation
from pypdf.generic import NameObject
from PIL import ImageChops
import pypdfium2 as pdfium
import hashlib,io,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,resolve
NS['m']='http://schemas.openxmlformats.org/officeDocument/2006/math'
source=json.loads((HERE/'archive/source.json').read_text());layout=json.loads((HERE/'layout.json').read_text());PART='ppt/slides/slide7.xml'
sha=lambda data:hashlib.sha256(data).hexdigest()
native=PdfReader(HERE/'native_export.pdf');assert len(native.pages)==1
text=native.pages[0].extract_text()
for label in ['Commanded joint torques (motors):','Jacobian:','Cartesian contribution','Linear and angular velocity (geometric)','Real-time control with a 1 ms cycle']:assert label in text,label
original=(ROOT/source['pdf']).read_bytes();assert sha(original)==source['pdf_sha256']
writer=PdfWriter(io.BytesIO(original),incremental=True);assert len(writer.pages)==29
page,native_page=writer.pages[5],native.pages[0];assert list(page.mediabox)==list(native_page.mediabox)
for key in ['/Contents','/Resources','/Group','/Annots']:
    if key in native_page:page[NameObject(key)]=native_page.raw_get(key).clone(writer)
    elif key in page:del page[key]
memory=io.BytesIO();writer.write(memory);updated_pdf=memory.getvalue();assert updated_pdf[:len(original)]==original
(HERE/'updated.pdf').write_bytes(updated_pdf);(HERE/'presentation_pdf_update.bin').write_bytes(updated_pdf[len(original):])
for name,box in layout['equations'].items():
    asset=name.removeprefix('Equation - ');x,y,w,h=box;crop=PdfWriter();p=crop.add_blank_page(width=w+4,height=h+4)
    p.merge_transformed_page(native.pages[0],Transformation().translate(-x+2,-(540-y-h)+2),expand=False)
    crop.write(HERE/'assets'/f'{asset}.pdf')

with ZipFile(ROOT/source['pptx']) as old,ZipFile(HERE/'updated.pptx') as new:
    assert set(old.namelist())==set(new.namelist()) and len(new.namelist())==len(set(new.namelist()))
    changed=[n for n in old.namelist() if sha(old.read(n))!=sha(new.read(n))];assert changed==[PART],changed
    oldroot,newroot=E.fromstring(old.read(PART)),E.fromstring(new.read(PART))
    shapes=lambda root:{s.find('p:nvSpPr/p:cNvPr',NS).get('name'):s for s in root.findall('.//p:sp',NS)}
    previous,current=shapes(oldroot),shapes(newroot)
    permitted=set(layout['headings'])|set(layout['equations'])
    for name,s in previous.items():
        if name not in permitted:assert E.tostring(s,method='c14n',exclusive=True)==E.tostring(current[name],method='c14n',exclusive=True),name
    assert set(current)-set(previous)=={x['name'] for x in layout['captions']}
    velocity=current['Equation - jacobian_velocity_mapping'].find('.//m:oMath',NS)
    assert velocity.find('m:d',NS) is None
    assert velocity.find('m:sSub/m:e/m:acc/m:e/m:r/m:t',NS).text=='x'
    assert velocity.find('m:sSub/m:sub/m:r/m:t',NS).text=='EE'
    assert velocity.find('m:sSub/m:e/m:acc/m:accPr/m:chr',NS).get('{'+NS['m']+'}val')=='̇'
    torque=current['Equation - cartesian_torque_mapping'].find('.//m:oMath',NS)
    assert torque.find('m:d',NS) is None
    assert ''.join(torque.xpath('.//m:t/text()',namespaces=NS))=='τ=J⊤(q)F'
    for name in layout['equations']:
        for rpr in current[name].findall('.//a:rPr',NS):assert rpr.get('sz')=='2200' and rpr.get('b')=='0'
    ids=[x.get('id') for x in newroot.findall('.//p:cNvPr',NS)];assert len(ids)==len(set(ids))
    pres=E.fromstring(new.read('ppt/presentation.xml'));rels={r.get('Id'):r.get('Target') for r in E.fromstring(new.read('ppt/_rels/presentation.xml.rels'))}
    paths=[resolve('ppt/presentation.xml',rels[s.get('{'+NS['r']+'}id')]) for s in pres.find('p:sldIdLst',NS)];assert len(paths)==29 and paths[5]==PART
    count=videos=hidden=0
    for path in paths:
        root=E.fromstring(new.read(path));count+=len(root.findall('.//m:oMath',NS));videos+=len(root.findall('.//a:videoFile',NS));hidden+=root.get('show')=='0'
    assert (count,videos,hidden)==(30,5,5)
    catalog=json.loads((HERE/'assets/native_equations.json').read_text(encoding='utf-8'));assert len(catalog)==30
    for c in catalog:
        rr=E.fromstring(new.read(paths[c['slide']-1]));assert rr.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$n]',namespaces=NS,n=c['shape'])
    old_catalog=json.loads((HERE/'archive/assets/native_equations.json').read_text(encoding='utf-8'))
    for a,b in zip(old_catalog,catalog):
        if a['shape'] not in layout['equations']:assert a==b
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert sha((ROOT/name).read_bytes())==digest,name
assert len(PdfReader(ROOT/'Final Presentation/Supplementary_slides.pdf').pages)==5
before,after=pdfium.PdfDocument(original),pdfium.PdfDocument(updated_pdf);assert len(before)==len(after)==29
changed_pages=[]
for i in range(29):
    a,b=before[i],after[i];aa,bb=a.render(scale=1.25),b.render(scale=1.25);ia,ib=aa.to_pil().convert('RGB'),bb.to_pil().convert('RGB')
    if ImageChops.difference(ia,ib).getbbox():changed_pages.append(i+1)
    if i==5:ib.save(HERE/'pdf-slide.png')
    aa.close();bb.close();a.close();b.close()
before.close();after.close();assert changed_pages==[6],changed_pages
v={'date':'2026-10-02','title':'Real-time control','physical_slide':6,'footer':5,'slide_count':29,'main_slides':24,'hidden_backups':5,'native_equations':30,
 'compact_xdot_EE_velocity_notation':True,'geometric_linear_angular_velocity_identified':True,'repeated_wrench_definition_removed':True,'motor_torque_heading_and_two_colons':True,
 'cartesian_torque_contribution_identified':True,'control_diagram_and_cycle_statement_unchanged':True,'other_28_native_equations_preserved':True,'all_five_embedded_videos_unchanged':True,
 'all_notes_unchanged':True,'speaking_files_unchanged':True,'supplementary_pdf_unchanged':True,'equation_catalog_updated':True,
 'pdf_pages':29,'changed_pdf_pages':changed_pages,'other_28_pdf_pages_pixel_identical':True,'changed_package_parts':changed,'native_powerpoint_rendered':True,
 'pptx_sha256':sha((HERE/'updated.pptx').read_bytes()),'pdf_sha256':sha(updated_pdf)}
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Verified the compact velocity and torque mappings; diagram, notes, media and the other 28 PDF pages are unchanged.')
