from pathlib import Path
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
source=json.loads((HERE/'archive/source.json').read_text());v=json.loads((HERE/'verification.json').read_text())
assert v['all_29_native_equations_preserved'] and v['other_pdf_content_pixel_identical_except_footers']
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:assert hashlib.sha256((FINAL/name).read_bytes()).hexdigest()==source[key]
shutil.copyfile(HERE/'updated.pptx',FINAL/'Thesis_Defense_gg0_v3.pptx')
shutil.copyfile(HERE/'updated.pdf',FINAL/'Thesis_Defense_gg0_v3.pdf')
shutil.copyfile(HERE/'native_equations.json',FINAL/'figures_and_images/native_equations.json')
for n,d in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==d
agents=ROOT/'AGENTS.md';text=agents.read_text(encoding='utf-8');heading='# Thesis and presentation workspace\n';assert text.startswith(heading)
rule='''
## Combined Cartesian pose and surface frame (2026-10-02)

The user combined physical slides 4 and 5 into Cartesian pose and surface
frame at physical slide 4 / footer 3. Keep the three original diagrams in
three columns: position, orientation and surface frame. The position figure
is 240 pt wide, the orientation figure 220 pt and the surface figure 266 pt;
all retain their original aspect ratios, asset bytes and editable sources.
Preserve the native p = p(q), n_s and t_1, t_2 equations at 22 pt Cambria Math.
The merged layout supersedes the separate Surface frame slide requirement
and the former Cartesian pose takeaway/equation box positions.

The merged slide introduces force f, moment m, stiffness K and damping D,
leading directly to Cartesian impedance controller at physical 5 / footer 4.
Distinguish the frames: surface axes define force/moment components and the
directions for impedance gains; pose and the evaluated controller equations
use the robot base frame. This follows the thesis's theoretical-background
chapter. Do not claim that the implemented controller wrench is evaluated
only in surface coordinates.

There are 24 main slides and five hidden backups, 29 slides total. Conclusion
is physical 24 / footer 23, and B1-B5 are physical 25-29. Chapter starts are
physical 2, 4, 9, 11, 17 and 24; preserve their existing chapter-label styles.
All other original slides retain their contents, with later main footers and
the native-equation catalog renumbered. There remain 29 native equations and
five embedded videos. Speaking files and all retained speaker notes are
unchanged. The original two slides and notes are archived in
experiments/pose_surface_merge_20261002/archive/original_pose_and_surface.pptx
and its matching PDF. The full PDF has 29 pages; the five-page supplementary
PDF is unchanged. See experiments/pose_surface_merge_20261002/verification.json.
'''
agents.write_text(heading+rule+text[len(heading):],encoding='utf-8')
readme=FINAL/'README.txt';entry=('2026-10-02: Combined Cartesian pose and Surface frame (former physical slides 4 and 5) into Cartesian pose and surface frame at physical 4 / footer 3. Reused all three diagrams and all three native equations/symbols. Added a clear preview of force f, moment m, stiffness K and damping D before the controller slide, distinguishing surface-relative component/gain directions from base-frame controller calculations. The controller now follows at physical 5. The deck/full PDF have 29 slides/pages: 24 main slides plus five hidden backups. Later main footers and the equation catalog are renumbered. Retained notes, speaking files, all original media, equations and the supplementary PDF are unchanged. Original slides and notes are archived. See ../experiments/pose_surface_merge_20261002/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
v.update({'installed':True,'native_powerpoint_visual_review_passed':True,'merged_slide_and_following_controller_reviewed':True,'pptx_sha256':hashlib.sha256((FINAL/'Thesis_Defense_gg0_v3.pptx').read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256((FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()).hexdigest()})
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Installed the verified 29-slide presentation and PDF. Original media, equations, retained notes and speaking files are preserved.')
