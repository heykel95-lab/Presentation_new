from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
import hashlib,json,shutil,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import select,NS,resolve,relpath
if __name__=='__main__':
    archive=HERE/'archive';archive.mkdir(exist_ok=True)
    prior=HERE.parent/'controller_force_first_20261002'
    source={}
    for ext in ['pptx','pdf']:
        p=prior/('updated.'+ext);assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((FINAL/('Thesis_Defense_gg0_v3.'+ext)).read_bytes()).digest()
        source[ext]=str(p.relative_to(ROOT));source[ext+'_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    (archive/'source.json').write_text(json.dumps(source,indent=2))
    with ZipFile(ROOT/source['pptx']) as z:
        part='ppt/slides/slide5.xml';root=E.fromstring(z.read(part));(archive/'slide5.xml').write_bytes(z.read(part))
        (archive/'package_hashes_before.json').write_text(json.dumps({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()},indent=2))
        select(z,{4},HERE/'source_slide.pptx')
        shapes=[]
        for s in root.xpath('.//p:sp|.//p:pic',namespaces=NS):
            n=s.find('.//p:cNvPr',NS);xf=s.find('p:spPr/a:xfrm',NS)
            d={'name':n.get('name'),'text':' '.join(s.xpath('.//a:t/text()',namespaces=NS))}
            if xf is not None:d['rect']=[int(x)/12700 for x in [xf.find('a:off',NS).get('x'),xf.find('a:off',NS).get('y'),xf.find('a:ext',NS).get('cx'),xf.find('a:ext',NS).get('cy')]]
            shapes.append(d)
            if n.get('name')=='Equation - pose_joint_configuration':(archive/'equation.xml').write_bytes(E.tostring(s,pretty_print=True))
        (HERE/'inventory.json').write_text(json.dumps(shapes,indent=2))
        rels={r.get('Id'):resolve(part,r.get('Target')) for r in E.fromstring(z.read(relpath(part)))}
        pic=root.xpath('.//p:pic[p:nvPicPr/p:cNvPr/@name="End effector position figure"]',namespaces=NS)[0]
        rid=pic.find('.//a:blip',NS).get('{'+NS['r']+'}embed');source['position_media']=rels[rid]
        (archive/'position_original.png').write_bytes(z.read(rels[rid]))
    (archive/'source.json').write_text(json.dumps(source,indent=2))
    for rel in ['native_equations.json','manifest.json','sources/pose_joint_configuration.tex','sources/cartesian_pose_position.tex','sources/pose_gripper.tikz','pose_joint_configuration.pdf','pose_joint_configuration.png','pose_joint_configuration.svg','cartesian_pose_position.pdf','cartesian_pose_position.png','cartesian_pose_position.svg']:
        dest=archive/'assets'/rel;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(ASSETS/rel,dest)
    tex=(ASSETS/'sources/cartesian_pose_position.tex').read_text(encoding='utf-8');assert tex.count('{$p$}')==1
    (HERE/'assets/sources/cartesian_pose_position.tex').write_text(tex.replace('{$p$}',r'{$p_{\mathrm{EE}}$}'),encoding='utf-8')
    shutil.copy2(ASSETS/'sources/pose_gripper.tikz',HERE/'assets/sources/pose_gripper.tikz')
    protected=[FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaker_notes_and_timing.txt',FINAL/'Supplementary_slides.pdf']+list((FINAL/'Speaking').rglob('*.tex'))
    (archive/'protected_files.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2))
    p=PdfReader(ROOT/source['pdf']);w=PdfWriter();w.add_page(p.pages[3]);w.write(archive/'slide_before.pdf')
    (HERE/'source-notes.txt').write_text('Revise physical slide 4 / footer 3. Use p_EE in its existing position diagram and kinematic equation. Spell out end-effector (EE) once, introduce the pose as a two-row local position/orientation coordinate vector, then branch to the existing position and roll-pitch-yaw diagrams. Retain surface frame and force/moment/impedance transition. No speaker-note edits. The user explicitly requests this new native equation and layout, superseding fixed earlier geometry. Original Office Math cannot round-trip through artifact-tool (unsupported a14:m); use artifact-tool text assets and preserve the original package with targeted OOXML edits. No thesis changes.\n')
    print('Archived slide 4 and its sources. Position image part: '+source['position_media'])
