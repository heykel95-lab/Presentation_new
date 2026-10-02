from pathlib import Path
from zipfile import ZipFile
from pypdf import PdfReader,PdfWriter
import hashlib,json,shutil,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import select
if __name__=='__main__':
    archive=HERE/'archive';archive.mkdir(exist_ok=True)
    source={}
    for ext in ['pptx','pdf']:
        p=HERE.parent/'pose_vector_20261002'/('updated.'+ext)
        assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((FINAL/('Thesis_Defense_gg0_v3.'+ext)).read_bytes()).digest()
        source[ext]=str(p.relative_to(ROOT));source[ext+'_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    (archive/'source.json').write_text(json.dumps(source,indent=2))
    with ZipFile(ROOT/source['pptx']) as z:
        select(z,{6},HERE/'source_slide.pptx');(archive/'slide7.xml').write_bytes(z.read('ppt/slides/slide7.xml'))
        (archive/'package_hashes_before.json').write_text(json.dumps({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()},indent=2))
    assets=['native_equations.json','manifest.json']
    for name in ['cartesian_torque_mapping','jacobian_velocity_mapping']:assets+=['sources/'+name+'.tex',name+'.pdf',name+'.png',name+'.svg']
    for rel in assets:
        dest=archive/'assets'/rel;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(ASSETS/rel,dest)
    protected=[FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaker_notes_and_timing.txt',FINAL/'Supplementary_slides.pdf']+list((FINAL/'Speaking').rglob('*.tex'))
    (archive/'protected_files.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2))
    p=PdfReader(ROOT/source['pdf']);w=PdfWriter();w.add_page(p.pages[5]);w.write(archive/'slide_before.pdf')
    (HERE/'source-notes.txt').write_text('User referred to slide 7; the unique equations identify Real-time control, now physical 6 / footer 5, underlying slide7.xml. Replace the stacked p-dot/omega with compact x-dot_EE notation, explicitly described here as geometric linear/angular velocity, rather than the derivative of the RPY coordinates on slide 4. The torque equation retains tau = J^T(q)F; remove only the repeated wrench definition. Label it as the Cartesian contribution because the preserved diagram adds model and null-space torques before the motor command tau_cmd. Add colons after both bullet headings. Native equation typography and all notes, diagram elements, videos and other slides stay intact. Artifact-tool authors new caption assets; targeted OOXML edits preserve native equations that artifact-tool cannot import (unsupported a14:m payload).\n')
    print('Archived the current real-time-control slide and matching equation assets.')
