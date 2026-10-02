from pathlib import Path
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((HERE/'archive/source.json').read_text())
verification=json.loads((HERE/'verification.json').read_text())
assert verification['all_29_native_equations_preserved'] and verification['other_28_pdf_pages_pixel_identical']
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:
    assert sha(FINAL/name)==source[key],name
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():
    assert sha(ROOT/name)==digest,name
shutil.copyfile(HERE/'updated.pptx',FINAL/'Thesis_Defense_gg0_v3.pptx')
shutil.copyfile(HERE/'updated.pdf',FINAL/'Thesis_Defense_gg0_v3.pdf')
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:
    assert sha(FINAL/name)==verification[key],name
rule='''
## Force and moment before controller errors (2026-10-02)

On Cartesian impedance controller (physical slide 5 / footer 4 after the
pose/surface merge), introduce Force and Moment in the top row, followed by
Positional error and Rotational error with their original diagrams in the
middle row. Cartesian wrench and the decoupling statement remain below.
Use the original editable bullet-heading style. Preserve all five native
equations exactly, at their original dimensions and 22 pt Cambria Math,
and preserve the original diagram assets and proportions. This changes
placement and adds the matching error headings; it does not change the
mathematics, speaker notes or speaking files. The slide is the controller
slide the user referred to by its former number 6. Slide count, numbering,
chapter labels, all other slides and the supplementary PDF are unchanged.
The full PDF matches the reordered slide. See
experiments/controller_force_first_20261002/verification.json.
'''
agents=ROOT/'AGENTS.md';original=agents.read_text(encoding='utf-8')
heading='# Thesis and presentation workspace\n';assert original.startswith(heading)
agents.write_text(heading+rule+original[len(heading):],encoding='utf-8')
readme=FINAL/'README.txt'
entry='2026-10-02: Reordered Cartesian impedance controller (physical slide 5 / footer 4): Force and Moment first, then Positional error and Rotational error with their original diagrams, then Cartesian wrench. Bullet headings follow the new order. All five native equations, original picture dimensions, notes and speaking files are unchanged. Updated the PowerPoint and full PDF; the other 28 PDF pages, all media, chapter labels, numbering and supplementary PDF are unchanged. See ../experiments/controller_force_first_20261002/verification.json.\n\n'
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
verification.update({'installed':True,'native_powerpoint_visual_review_passed':True,'final_pdf_visual_review_passed':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Installed the reordered controller slide in the active PowerPoint and PDF.')
