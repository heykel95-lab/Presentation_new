from pathlib import Path
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((HERE/'archive/source.json').read_text());v=json.loads((HERE/'verification.json').read_text())
assert v['other_28_pdf_pages_pixel_identical'] and v['control_diagram_and_cycle_statement_unchanged']
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:assert sha(FINAL/name)==source[key],name
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert sha(ROOT/name)==digest,name
assets=['native_equations.json','manifest.json']
for asset in ['cartesian_torque_mapping','jacobian_velocity_mapping']:assets+=['sources/'+asset+'.tex',asset+'.pdf',asset+'.png',asset+'.svg']
for name in assets:assert (HERE/'assets'/name).is_file(),name
shutil.copyfile(HERE/'updated.pptx',FINAL/'Thesis_Defense_gg0_v3.pptx');shutil.copyfile(HERE/'updated.pdf',FINAL/'Thesis_Defense_gg0_v3.pdf')
for name in assets:shutil.copyfile(HERE/'assets'/name,ASSETS/name)
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:assert sha(FINAL/name)==v[key]
rule='''
## Compact Cartesian velocity and motor-torque mapping (2026-10-02)

On Real-time control (physical slide 6 / footer 5, referred to by the user
as slide 7), the two bullet headings are Commanded joint torques (motors):
and Jacobian:, including their colons. Keep only tau = J^T(q)F in the
left native equation. Both headings match the existing 22 pt navy style;
the Jacobian heading's stale 20 pt black native override is corrected.
The repeated F = [f; m] definition is removed.
Its caption is Cartesian contribution, since the unchanged diagram adds
model and null-space torques before the motor command tau_cmd.

The right native equation uses x-dot_EE = J(q)q-dot. Its caption identifies
Linear and angular velocity (geometric). Here x-dot_EE is shorthand for
the geometric Cartesian velocity [p-dot_EE; omega_EE]; do not reinterpret
it as derivatives of the roll-pitch-yaw coordinates on the pose slide.
The notation convention is recorded in the equation source, catalog and
alternative description. Both equations remain editable 22 pt regular
Cambria Math with synchronized LaTeX and PDF/PNG/SVG assets.

All native feedback-diagram shapes, arrows, labels, signs, the model and
null-space summation, and the 1 ms cycle statement remain unchanged.
Keep all other slides, 28 other equations, notes, speaking files, videos
and the supplementary PDF unchanged. The deck/full PDF retain 29
slides/pages, five hidden backups and 30 native equations. See
experiments/realtime_velocity_20261002/verification.json.
'''
agents=ROOT/'AGENTS.md';text=agents.read_text(encoding='utf-8');header='# Thesis and presentation workspace\n';assert text.startswith(header)
agents.write_text(header+rule+text[len(header):],encoding='utf-8')
readme=FINAL/'README.txt';entry='2026-10-02: Real-time control (physical 6 / footer 5, formerly called slide 7) uses compact x-dot_EE = J(q)q-dot notation for geometric linear/angular Cartesian velocity. Its left equation keeps only tau = J^T(q)F, removing the repeated wrench definition. The headings are Commanded joint torques (motors): and Jacobian:, with colons; the torque caption identifies the Cartesian contribution. All diagram shapes, signals, summations, the 1 ms cycle statement, notes, speaking files and other slides are unchanged. Native equations, their source/asset files, catalog and full PDF agree. See ../experiments/realtime_velocity_20261002/verification.json.\n\n'
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
v.update({'installed':True,'native_powerpoint_visual_review_passed':True,'final_pdf_visual_review_passed':True,'equation_sources_and_assets_synchronized':True})
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Installed the revised real-time-control slide in the PowerPoint, PDF and equation assets.')
