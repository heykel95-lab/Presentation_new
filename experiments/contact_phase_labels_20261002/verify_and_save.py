from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject
from PIL import ImageChops
import pypdfium2 as pdfium
import io,json,hashlib,sys,shutil,copy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,resolve
NS['m']='http://schemas.openxmlformats.org/officeDocument/2006/math'
sha=lambda b:hashlib.sha256(b).hexdigest()
source=json.loads((HERE/'archive/source.json').read_text());layout=json.loads((HERE/'layout.json').read_text());part=source['part'];physical=source['physical']
for ext in ['pptx','pdf']:assert sha((FINAL/('Thesis_Defense_gg0_v3.'+ext)).read_bytes())==source[ext+'_sha256']
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert sha((ROOT/name).read_bytes())==digest,name
with ZipFile(ROOT/source['pptx']) as original:
 oldroot=E.fromstring(original.read(part));newroot=E.fromstring((HERE/'updated_slide.xml').read_bytes())
 shapes=lambda r:{s.find('.//p:cNvPr',NS).get('name'):s for s in r.xpath('p:cSld/p:spTree/p:sp|p:cSld/p:spTree/p:pic',namespaces=NS)}
 previous,current=shapes(oldroot),shapes(newroot);assert set(current)-set(previous)=={layout['heading']['name']}
 allowed=set(layout['labels'])|{'Contact phases'}
 for name,s in previous.items():
  if name not in allowed:assert E.tostring(s,method='c14n')==E.tostring(current[name],method='c14n'),name
 for name,value in layout['labels'].items():assert ''.join(current[name].xpath('.//a:t/text()',namespaces=NS))==value
 heading=current[layout['heading']['name']]
 assert heading.find('.//a:buChar',NS).get('char')=='\u2022'
 assert heading.find('.//a:buClr/a:srgbClr',NS).get('val')=='17365D'
 assert ''.join(heading.xpath('.//a:t/text()',namespaces=NS))=='Experiment phases:'
 assert [E.tostring(x,method='c14n') for x in oldroot.findall('.//m:oMath',NS)]==[E.tostring(x,method='c14n') for x in newroot.findall('.//m:oMath',NS)]
 original_pdf=(ROOT/source['pdf']).read_bytes();native=PdfReader(HERE/'native_export.pdf');assert len(native.pages)==1
 text=native.pages[0].extract_text()
 for value in [layout['heading']['text'],*layout['labels'].values()]:assert value in text,value
 writer=PdfWriter(io.BytesIO(original_pdf),incremental=True);assert len(writer.pages)==30
 target=writer.pages[physical-1]
 for key in ['/Contents','/Resources','/Group','/Annots']:
  if key in native.pages[0]:target[NameObject(key)]=native.pages[0].raw_get(key).clone(writer)
  elif key in target:del target[key]
 memory=io.BytesIO();writer.write(memory);pdfbytes=memory.getvalue();assert pdfbytes.startswith(original_pdf)
 (HERE/'updated.pdf').write_bytes(pdfbytes)
 before,after=pdfium.PdfDocument(original_pdf),pdfium.PdfDocument(pdfbytes);changed=[]
 for i in range(30):
  a,b=before[i],after[i];aa,bb=a.render(scale=1.25),b.render(scale=1.25);ia,ib=aa.to_pil().convert('RGB'),bb.to_pil().convert('RGB')
  if ImageChops.difference(ia,ib).getbbox():changed.append(i+1)
  if i==physical-1:ib.save(HERE/'pdf-slide.png')
  aa.close();bb.close();a.close();b.close()
 before.close();after.close();assert changed==[physical],changed
 print('Checked all 30 PDF pages; only Contact experiment changes.',flush=True)
 # Rebuild the ZIP in memory so disk space is not consumed by a second full deck.
 # Fresh local records also avoid the orphan records of append-style ZIP updates.
 package=io.BytesIO()
 with ZipFile(package,'w',ZIP_DEFLATED) as out:
  for info in original.infolist():out.writestr(copy.copy(info),(HERE/'updated_slide.xml').read_bytes() if info.filename==part else original.read(info.filename))
 packagebytes=package.getvalue()
 with ZipFile(io.BytesIO(packagebytes)) as new:
  assert len(new.namelist())==len(set(new.namelist()))
  changedparts=[n for n in original.namelist() if sha(original.read(n))!=sha(new.read(n))];assert changedparts==[part],changedparts
  assert new.testzip() is None
 (FINAL/'Thesis_Defense_gg0_v3.pptx').write_bytes(packagebytes)
 (FINAL/'Thesis_Defense_gg0_v3.pdf').write_bytes(pdfbytes)
 assert sha((FINAL/'Thesis_Defense_gg0_v3.pptx').read_bytes())==sha(packagebytes)
v={'date':'2026-10-02','title':'Contact experiment','physical_slide':physical,'footer':9,'slide_count':30,'main_slides':25,'hidden_backups':5,'native_equations':31,'experiment_phases_heading_navy_bullet_and_colon':True,'normal_translation_compliant':True,'tangential_translation_stiff':True,'normal_rotation_stiff':True,'tangent_rotations_compliant':True,'phase_names_unchanged':True,'all_equations_and_settings_unchanged':True,'figure_unchanged':True,'notes_speech_media_catalog_and_supplementary_unchanged':True,'other_29_slides_byte_identical':True,'other_29_pdf_pages_pixel_identical':True,'changed_pdf_pages':changed,'changed_package_parts':changedparts,'native_powerpoint_render_visually_reviewed':True,'disk_space_workaround':'Rebuilt complete ZIP in memory; prior full source retained in coc_introduction_20261002/updated.pptx. Removed only redundant motivation_video_20261002/native_preview.pptx.','pptx_sha256':sha(packagebytes),'pdf_sha256':sha(pdfbytes),'installed':True}
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
rule='''
## Contact phase heading and directional labels (2026-10-02)

On Contact experiment (physical slide 10 / footer 9, called slide 8 by the
user), introduce the unchanged phase sequence with Experiment phases: as
an editable navy 22 pt bullet, matching the contact-settings heading.
Keep the four existing phase names and arrows in navy 20 pt beneath it.
The heading box is (60, 68, 840, 30) pt and phase box (80, 109, 840, 30) pt.

The four 18 pt navy setting headings read Normal translation (compliant),
Tangential translation (stiff), Rotation about the surface normal (stiff),
and Rotations about the surface tangents (compliant). These directional
labels follow the thesis Contact Establishment design. Preserve all four
native equations, values, positions, the surface figure, notes and speaking
material. The 30-slide structure and all other slides remain unchanged;
the full PDF is synchronized and supplementary PDF is unchanged. See
experiments/contact_phase_labels_20261002/verification.json.
'''
agents=ROOT/'AGENTS.md';t=agents.read_text(encoding='utf-8');header='# Thesis and presentation workspace\n';assert t.startswith(header);agents.write_text(header+rule+t[len(header):],encoding='utf-8')
readme=FINAL/'README.txt';readme.write_text('2026-10-02: Contact experiment now introduces its sequence with the navy bullet Experiment phases: and labels the four directional stiffness headings as compliant or stiff. Native equations, values, figure, notes and other slides are unchanged. PowerPoint and full PDF synchronized. See ../experiments/contact_phase_labels_20261002/verification.json.\n\n'+readme.read_text(encoding='utf-8'),encoding='utf-8')
print('Installed and verified the PowerPoint and PDF.',flush=True)
