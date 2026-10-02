from pathlib import Path
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((HERE/'archive/source.json').read_text());v=json.loads((HERE/'verification.json').read_text())
assert v['other_28_pdf_pages_pixel_identical'] and v['native_equations']==30
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:assert sha(FINAL/name)==source[key],name
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert sha(ROOT/name)==digest,name
asset_names=['native_equations.json','manifest.json']
for asset in ['cartesian_pose_position','pose_joint_configuration','cartesian_pose_vector']:
    asset_names+=['sources/'+asset+'.tex',asset+'.pdf',asset+'.png',asset+'.svg']
for name in asset_names:assert (HERE/'assets'/name).is_file(),name
shutil.copyfile(HERE/'updated.pptx',FINAL/'Thesis_Defense_gg0_v3.pptx')
shutil.copyfile(HERE/'updated.pdf',FINAL/'Thesis_Defense_gg0_v3.pdf')
for name in asset_names:shutil.copyfile(HERE/'assets'/name,ASSETS/name)
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:assert sha(FINAL/name)==v[key]
rule='''
## Full Cartesian pose and end-effector position (2026-10-02)

On Cartesian pose and surface frame (physical slide 4 / footer 3), write
Cartesian pose of the end-effector (EE) once above the position/orientation
area. Show the native two-row coordinate vector x_EE = [p_EE; eta_EE],
expanded as [(x,y,z)^T; (phi,theta,psi)^T], centred above the split into
Position: 3 translations and Orientation: 3 rotations. Eta_EE denotes the
roll-pitch-yaw coordinates illustrated by the existing orientation diagram.
Retain the native branch lines and the two original diagrams, scaled
proportionally to this new layout.

Use p_EE in the position diagram and in both sides of p_EE = p_EE(q).
Mathematical EE subscripts remain upright without parentheses; standalone
diagram labels remain (EE). The position diagram's editable TikZ and its
PDF/PNG/SVG assets match the embedded image. Preserve its other geometry.
Both revised/new equations use native editable 22 pt regular Cambria Math,
with matching LaTeX, catalog and PDF/PNG/SVG assets. There are now 30 native
equations; the other 28 are unchanged.

Retain the surface-frame figure and definitions, the distinction between
surface-relative gain directions and base-frame calculations, and the
preview of force, moment, stiffness and damping before the controller.
All notes and speaking files remain unchanged. The deck/full PDF still
contain 29 slides/pages, including five hidden backups. The supplementary
PDF and the other 28 slides are unchanged. This supersedes the former
plain p = p(q) notation and fixed sizes/positions on this slide. See
experiments/pose_vector_20261002/verification.json.
'''
agents=ROOT/'AGENTS.md';text=agents.read_text(encoding='utf-8');header='# Thesis and presentation workspace\n';assert text.startswith(header)
agents.write_text(header+rule+text[len(header):],encoding='utf-8')
readme=FINAL/'README.txt';entry='2026-10-02: Slide 4 now introduces Cartesian pose of the end-effector (EE) with a centred two-row native pose vector, expanded to position and roll-pitch-yaw coordinates, then branches into the existing position and orientation diagrams. The position diagram and kinematic equation both use p_EE. Surface-frame content and the transition to force, moment, stiffness and damping remain. The full PDF, edited sources, PDF/PNG/SVG assets and 30-entry native-equation catalog agree. All other slides, notes, speaking files, videos and the supplementary PDF are unchanged. See ../experiments/pose_vector_20261002/verification.json.\n\n'
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
v.update({'installed':True,'native_powerpoint_visual_review_passed':True,'final_pdf_visual_review_passed':True,'equation_and_diagram_assets_synchronized':True})
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Installed the revised pose slide, full PDF, and matching diagram/equation sources and assets.')
