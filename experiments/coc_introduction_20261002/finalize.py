from pathlib import Path
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((HERE/'archive/source.json').read_text());v=json.loads((HERE/'verification.json').read_text())
assert v['other_27_original_slides_pixel_identical_except_main_footers'] and v['all_retained_notes_unchanged']
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:assert sha(FINAL/name)==source[key],name
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert sha(ROOT/name)==digest,name
for name in ['CoC_moment.pdf','CoC_moment.png','CoC_moment.svg','sources/CoC_moment.tex']:assert sha(ASSETS/name)==sha(HERE/'archive/assets'/name),name
assets=['native_equations.json','manifest.json']
for asset in ['coc_force_shift_general','coc_force_shift_cases','coc_added_moment','symbol_pc','coc_displacement_definition']:assets+=['sources/'+asset+'.tex',asset+'.pdf',asset+'.png',asset+'.svg']
for name in assets:assert (HERE/'assets'/name).is_file(),name
shutil.copyfile(HERE/'updated.pptx',FINAL/'Thesis_Defense_gg0_v3.pptx');shutil.copyfile(HERE/'updated.pdf',FINAL/'Thesis_Defense_gg0_v3.pdf')
for name in assets:shutil.copyfile(HERE/'assets'/name,ASSETS/name)
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:assert sha(FINAL/name)==v[key]
rule='''
## General CoC introduction and shifted-force cases (2026-10-02)

A new Centre of compliance (CoC) introduction is physical slide 7 / footer 6,
before the existing two-case slide, now physical 8 / footer 7. It defines
the TCP and virtual CoC, shows force f as if applied at p_CoC, the offset
r_c from p_TCP, and the resulting additional moment about TCP. The new native
equation is Delta m = r_c cross f, 22 pt regular Cambria Math. This is the
additional coupling contribution, not the complete rotational-impedance
moment. The physical contact location is not moved by this virtual depiction.

Both Supporting moment and Opposing moment now show f_n at the virtual CoC.
The curved arrows show the resulting moment about TCP, not a second applied
moment. Preserve the supporting counterclockwise and opposing clockwise
directions for the illustrated downward force and left/right displacements.
Use p_CoC (upright CoC subscript) in both cases and throughout the following
Translation-rotation coupling slide, now physical 9 / footer 8: the native
position symbol, displacement equation and inline force-interpretation text.
Keep r_c unchanged. Retain the original tool tilt, surface, normal arrows,
displacement signs and Supporting/Opposing labels.

The active diagrams are presentation-specific coc_force_shift_general and
coc_force_shift_cases, with matching editable TikZ and PDF/PNG/SVG assets.
The historical shared CoC_moment source/assets and thesis files remain intact.
The general and case diagrams deliberately portray virtual-force equivalence;
do not infer unchanged commanded force across different controller settings.

There are now 25 main slides and five hidden backups, 30 total. Conclusion
is physical 25 / footer 24; backups B1-B5 are physical 26-30. Chapter starts
are physical 2, 4, 10, 12, 18 and 25. Native sections, main footers and the
31-entry equation catalog follow this order. All retained notes, speaking
files, videos and other slide bodies remain unchanged. The new notes contain
source information only. The full PDF has 30 pages; the five-page supplementary
PDF is unchanged. This supersedes the earlier force-at-TCP and p_c depiction
on the active CoC slides. See experiments/coc_introduction_20261002/verification.json.
'''
agents=ROOT/'AGENTS.md';text=agents.read_text(encoding='utf-8');header='# Thesis and presentation workspace\n';assert text.startswith(header);agents.write_text(header+rule+text[len(header):],encoding='utf-8')
readme=FINAL/'README.txt';entry='2026-10-02: Added a general CoC introduction at physical 7 / footer 6, showing the virtual shifted force and its additional moment Delta m = r_c cross f about the TCP. The two supporting/opposing cases follow at physical 8 with force arrows at p_CoC; the next coupling slide at physical 9 uses p_CoC consistently. All three figure/equation source sets and PDFs agree. The active diagrams are presentation-specific variants; historical shared figure assets remain intact. There are now 30 slides/pages (25 main plus five hidden backups) and 31 native equations. Native sections, main footers and the equation catalog are updated. Retained notes, speaking files, videos, other slide bodies and supplementary PDF are unchanged. See ../experiments/coc_introduction_20261002/verification.json.\n\n';readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
v.update({'installed':True,'three_native_slides_visually_reviewed':True,'final_pdf_visually_reviewed':True,'diagram_and_equation_sources_assets_synchronized':True})
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Installed the 30-slide deck and PDF with the CoC introduction, shifted-force cases and consistent p_CoC notation.')
