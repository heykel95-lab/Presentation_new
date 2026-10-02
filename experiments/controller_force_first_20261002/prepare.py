from pathlib import Path
from zipfile import ZipFile
from pypdf import PdfReader,PdfWriter
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive';ARCHIVE.mkdir(exist_ok=True)
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import select
if __name__=='__main__':
    prior=HERE.parent/'pose_surface_merge_20261002';source=prior/'updated.pptx';pdf=prior/'updated.pdf'
    for current,backup in [(FINAL/'Thesis_Defense_gg0_v3.pptx',source),(FINAL/'Thesis_Defense_gg0_v3.pdf',pdf)]:assert hashlib.sha256(current.read_bytes()).digest()==hashlib.sha256(backup.read_bytes()).digest()
    with ZipFile(source) as z:
        select(z,{5},HERE/'source_slide.pptx')
        (ARCHIVE/'slide6.xml').write_bytes(z.read('ppt/slides/slide6.xml'))
        (ARCHIVE/'package_hashes_before.json').write_text(json.dumps({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()},indent=2))
    r=PdfReader(pdf);w=PdfWriter();w.add_page(r.pages[4]);w.write(ARCHIVE/'controller_before.pdf')
    (ARCHIVE/'source.json').write_text(json.dumps({'pptx':str(source.relative_to(ROOT)),'pdf':str(pdf.relative_to(ROOT)),'pptx_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()},indent=2))
    protected=[FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaker_notes_and_timing.txt',FINAL/'Supplementary_slides.pdf',FINAL/'figures_and_images/native_equations.json']+list((FINAL/'Speaking').rglob('*.tex'))
    (ARCHIVE/'protected_files.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2))
    (HERE/'source-notes.txt').write_text('Edit Cartesian impedance controller, now physical slide 5 / footer 4 after the prior merge. User referred to its earlier number 6; the requested force/moment/error content uniquely identifies it. Reorder existing equations and diagrams. Preserve notes, equations, all other slides and numbering.\n')
    print('Archived the current controller slide and recorded the protected files.')
