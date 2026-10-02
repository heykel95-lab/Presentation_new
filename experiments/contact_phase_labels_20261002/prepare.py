from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
import hashlib,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,select,resolve
NS['m']='http://schemas.openxmlformats.org/officeDocument/2006/math'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
archive=HERE/'archive';archive.mkdir(exist_ok=True)
source={}
for ext in ['pptx','pdf']:
 p=HERE.parent/'coc_introduction_20261002'/('updated.'+ext)
 assert sha(p)==sha(FINAL/('Thesis_Defense_gg0_v3.'+ext))
 source[ext]=str(p.relative_to(ROOT));source[ext+'_sha256']=sha(p)
with ZipFile(ROOT/source['pptx']) as z:
 p=E.fromstring(z.read('ppt/presentation.xml'));rels={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};inventory=[]
 for i,sid in enumerate(p.find('p:sldIdLst',NS),1):
  part=resolve('ppt/presentation.xml',rels[sid.get('{'+NS['r']+'}id')]);root=E.fromstring(z.read(part))
  inventory.append({'physical':i,'part':part,'text':root.xpath('.//a:t/text()',namespaces=NS)})
  if 'Contact experiment' in inventory[-1]['text']:
   source['physical']=i;source['part']=part;(archive/'original_slide.xml').write_bytes(z.read(part))
   for s in root.findall('p:cSld/p:spTree/p:sp',NS):
    name=s.find('p:nvSpPr/p:cNvPr',NS).get('name')
    if name in ['Contact phases','Contact settings heading','Normal label','Rotation label']:
     print(name+': '+E.tostring(s,encoding='unicode').encode('ascii','backslashreplace').decode('ascii'))
 select(z,{source['physical']},archive/'original_contact_slide.pptx')
 (archive/'package_hashes.json').write_text(json.dumps({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()},indent=2))
(archive/'source.json').write_text(json.dumps(source,indent=2))
(HERE/'inventory.json').write_text(json.dumps(inventory,indent=2))
protected=[FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaker_notes_and_timing.txt',FINAL/'Supplementary_slides.pdf',FINAL/'figures_and_images/native_equations.json',FINAL/'figures_and_images/manifest.json']+list((FINAL/'Speaking').rglob('*.tex'))
(archive/'protected_files.json').write_text(json.dumps({str(p.relative_to(ROOT)):sha(p) for p in protected},indent=2))
pdf=PdfReader(ROOT/source['pdf']);out=PdfWriter();out.add_page(pdf.pages[source['physical']-1]);out.write(archive/'original_contact_slide.pdf')
(HERE/'source-notes.txt').write_text('User-provided Contact experiment slide. Directional compliant/stiff terminology checked against MyOwn/chapters/03_software_implementation.tex, Contact Establishment, and the common gains table in chapter 4. Existing notes and speaking material are preserved. Artifact-tool cannot import the original Office Math payload; use the established text authoring and package-preserving workflow.\n')
