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
source=json.loads((HERE/'archive/source.json').read_text());layout=json.loads((HERE/'layout.json').read_text())
PART='ppt/slides/slide5.xml';sha=lambda data:hashlib.sha256(data).hexdigest()
native=PdfReader(HERE/'native_export.pdf');assert len(native.pages)==1
text=native.pages[0].extract_text()
assert 'Cartesian pose of the end-effector (EE)' in text
for label in ['Position: 3 translations','Orientation: 3 rotations','Surface frame','stiffness K and damping D']:assert label in text,label
original=(ROOT/source['pdf']).read_bytes();assert sha(original)==source['pdf_sha256']
writer=PdfWriter(io.BytesIO(original),incremental=True);assert len(writer.pages)==29
page,native_page=writer.pages[3],native.pages[0];assert list(page.mediabox)==list(native_page.mediabox)
for key in ['/Contents','/Resources','/Group','/Annots']:
    if key in native_page:page[NameObject(key)]=native_page.raw_get(key).clone(writer)
    elif key in page:del page[key]
memory=io.BytesIO();writer.write(memory);updated_pdf=memory.getvalue()
assert updated_pdf[:len(original)]==original
(HERE/'updated.pdf').write_bytes(updated_pdf)
(HERE/'presentation_pdf_update.bin').write_bytes(updated_pdf[len(original):])

# Exact native PowerPoint vectors become the matching standalone math assets.
for name,box in layout['equations'].items():
    asset=name.removeprefix('Equation - ');x,y,w,h=box
    crop=PdfWriter();p=crop.add_blank_page(width=w+2,height=h+2)
    p.merge_transformed_page(native.pages[0],Transformation().translate(-x+1,-(540-y-h)+1),expand=False)
    crop.write(HERE/'assets'/f'{asset}.pdf')

with ZipFile(ROOT/source['pptx']) as old,ZipFile(HERE/'updated.pptx') as new:
    assert set(old.namelist())==set(new.namelist()) and len(new.namelist())==len(set(new.namelist()))
    changed=[n for n in old.namelist() if sha(old.read(n))!=sha(new.read(n))]
    assert set(changed)=={PART,source['position_media']},changed
    oldroot,newroot=E.fromstring(old.read(PART)),E.fromstring(new.read(PART))
    def equations(root):
        return {s.find('p:nvSpPr/p:cNvPr',NS).get('name'):s.find('.//m:oMath',NS) for s in root.findall('.//p:sp',NS) if s.find('.//m:oMath',NS) is not None}
    previous,current=equations(oldroot),equations(newroot)
    assert len(previous)==3 and len(current)==4
    for name in ['Equation - symbol_ns','Equation - symbol_tangents']:
        assert E.tostring(previous[name],method='c14n',exclusive=True)==E.tostring(current[name],method='c14n',exclusive=True)
    kin=current['Equation - pose_joint_configuration']
    assert kin.xpath('.//m:sSub/m:sub/m:r/m:t/text()',namespaces=NS)==['EE','EE']
    full=current['Equation - cartesian_pose_vector']
    assert len(full.findall('m:d',NS))==2
    assert full.xpath('.//m:d/m:e/m:m/m:mr/m:e/m:sSub/m:e/m:r/m:t/text()',namespaces=NS)==['p','η']
    assert full.xpath('.//m:sSup/m:e/m:r/m:t/text()',namespaces=NS)==['(x,y,z)','(φ,θ,ψ)']
    for name in ['Equation - cartesian_pose_vector','Equation - pose_joint_configuration']:
        shape=current[name].getparent().getparent().getparent().getparent()
        for rpr in shape.findall('.//a:rPr',NS):assert rpr.get('sz')=='2200' and rpr.get('b')=='0'
    ids=[x.get('id') for x in newroot.findall('.//p:cNvPr',NS)];assert len(ids)==len(set(ids))
    pres=E.fromstring(new.read('ppt/presentation.xml'));rels={r.get('Id'):r.get('Target') for r in E.fromstring(new.read('ppt/_rels/presentation.xml.rels'))}
    paths=[resolve('ppt/presentation.xml',rels[s.get('{'+NS['r']+'}id')]) for s in pres.find('p:sldIdLst',NS)]
    assert len(paths)==29 and paths[3]==PART
    count=videos=hidden=0
    for path in paths:
        root=E.fromstring(new.read(path));count+=len(root.findall('.//m:oMath',NS));videos+=len(root.findall('.//a:videoFile',NS));hidden+=root.get('show')=='0'
    assert (count,videos,hidden)==(30,5,5),(count,videos,hidden)
    # The replaced diagram is referenced by this slide only.
    refs=[n for n in new.namelist() if n.startswith('ppt/slides/_rels/') and b'../media/image5.png' in new.read(n)]
    assert refs==['ppt/slides/_rels/slide5.xml.rels'],refs
    catalog=json.loads((HERE/'assets/native_equations.json').read_text(encoding='utf-8'));assert len(catalog)==30
    for c in catalog:
        rr=E.fromstring(new.read(paths[c['slide']-1]));assert rr.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$n]',namespaces=NS,n=c['shape'])
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert sha((ROOT/name).read_bytes())==digest,name
oldtex=(HERE/'archive/assets/sources/cartesian_pose_position.tex').read_text(encoding='utf-8')
newtex=(HERE/'assets/sources/cartesian_pose_position.tex').read_text(encoding='utf-8')
assert newtex==oldtex.replace('{$p$}',r'{$p_{\mathrm{EE}}$}')
oldfig=PdfReader(HERE/'archive/assets/cartesian_pose_position.pdf').pages[0]
newfig=PdfReader(HERE/'assets/cartesian_pose_position.pdf').pages[0]
assert all(abs(float(a)-float(b))<.02 for a,b in zip(oldfig.mediabox,newfig.mediabox))
assert len(PdfReader(ROOT/'Final Presentation/Supplementary_slides.pdf').pages)==5
before,after=pdfium.PdfDocument(original),pdfium.PdfDocument(updated_pdf)
assert len(before)==len(after)==29
changed_pages=[]
for i in range(29):
    a,b=before[i],after[i];aa,bb=a.render(scale=1.25),b.render(scale=1.25)
    ia,ib=aa.to_pil().convert('RGB'),bb.to_pil().convert('RGB')
    if ImageChops.difference(ia,ib).getbbox():changed_pages.append(i+1)
    if i==3:ib.save(HERE/'pdf-slide.png')
    aa.close();bb.close();a.close();b.close()
before.close();after.close();assert changed_pages==[4],changed_pages
verification={'date':'2026-10-02','title':'Cartesian pose and surface frame','physical_slide':4,'footer':3,
 'slide_count':29,'main_slides':24,'hidden_backups':5,'native_equations':30,
 'p_EE_in_diagram_and_kinematic_equation':True,'end_effector_written_in_full':True,
 'two_row_full_pose_vector_with_six_coordinates':True,'position_orientation_split':True,
 'other_28_native_equations_preserved':True,'all_five_embedded_videos_unchanged':True,'all_notes_unchanged':True,
 'speaking_files_unchanged':True,'supplementary_pdf_unchanged':True,'only_position_diagram_label_changed':True,
 'equation_catalog_updated':True,'pdf_pages':29,'changed_pdf_pages':changed_pages,'other_28_pdf_pages_pixel_identical':True,
 'changed_package_parts':changed,'native_powerpoint_rendered':True,'pptx_sha256':sha((HERE/'updated.pptx').read_bytes()),'pdf_sha256':sha(updated_pdf)}
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Verified the revised pose slide, 30 editable equations, unchanged notes/media, and all 29 PDF pages.')
