from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
import hashlib,json,sys,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive';ARCHIVE.mkdir(exist_ok=True)
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,resolve,select
if __name__=='__main__':
    prior=HERE.parent/'chapter_labels_20261002';source=prior/'updated.pptx';pdf=prior/'updated.pdf'
    for current,backup in [(FINAL/'Thesis_Defense_gg0_v3.pptx',source),(FINAL/'Thesis_Defense_gg0_v3.pdf',pdf)]:assert hashlib.sha256(current.read_bytes()).digest()==hashlib.sha256(backup.read_bytes()).digest()
    with ZipFile(source) as z:
        select(z,{4,5},ARCHIVE/'original_pose_and_surface.pptx')
        p=E.fromstring(z.read('ppt/presentation.xml'));rels={x.get('Id'):resolve('ppt/presentation.xml',x.get('Target')) for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
        inventory=[]
        for i,s in enumerate(p.find('p:sldIdLst',NS),1):
            path=rels[s.get('{'+NS['r']+'}id')];root=E.fromstring(z.read(path))
            title=''.join(root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name="Slide title"]//a:t/text()',namespaces=NS))
            inventory.append({'physical':i,'path':path,'sid':s.get('id'),'rid':s.get('{'+NS['r']+'}id'),'title':title})
        (ARCHIVE/'package_hashes_before.json').write_text(json.dumps({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()},indent=2))
    r=PdfReader(pdf);w=PdfWriter();w.add_page(r.pages[3]);w.add_page(r.pages[4]);w.write(ARCHIVE/'original_pose_and_surface.pdf')
    (HERE/'inventory.json').write_text(json.dumps(inventory,indent=2))
    (ARCHIVE/'source.json').write_text(json.dumps({'pptx':str(source.relative_to(ROOT)),'pdf':str(pdf.relative_to(ROOT)),'pptx_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()},indent=2))
    protected=[FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaker_notes_and_timing.txt',FINAL/'Supplementary_slides.pdf']+list((FINAL/'Speaking').rglob('*.tex'))
    (ARCHIVE/'protected_files.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2))
    shutil.copy2(FINAL/'figures_and_images/native_equations.json',ARCHIVE/'native_equations.json')
    (HERE/'source-notes.txt').write_text('User requested combining physical slides 4 and 5. Reuse all three exact figures and all three native equations/symbols. Technical wording checked against MyOwn/chapters/02_theoretical_background.tex, lines 407-416 and 535-670: impedance evaluated in base frame, diagonal gains chosen in surface coordinates. No thesis changes. Retained notes and speaking files remain unchanged.\n')
    print('Archived both source slides and their notes; mapped the current 30-slide deck.')
