from pathlib import Path
import json,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
source=json.loads((HERE/'archive/source.json').read_text())
v=json.loads((HERE/'verification.json').read_text())
assert v['all_existing_shapes_byte_preserved'] and v['all_pdf_pixels_outside_chapter_labels_identical']
for name,key in [('Thesis_Defense_gg0_v3.pptx','pptx_sha256'),('Thesis_Defense_gg0_v3.pdf','pdf_sha256')]:
    assert hashlib.sha256((FINAL/name).read_bytes()).hexdigest()==source[key], 'Source changed during editing'
shutil.copyfile(HERE/'updated.pptx',FINAL/'Thesis_Defense_gg0_v3.pptx')
shutil.copyfile(HERE/'updated.pdf',FINAL/'Thesis_Defense_gg0_v3.pdf')
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
agents=ROOT/'AGENTS.md';text=agents.read_text(encoding='utf-8');heading='# Thesis and presentation workspace\n';assert text.startswith(heading)
rule='''
## Visible chapter labels on existing slides (2026-10-02)

The user wants to see the current Overview chapter while advancing through
the existing slides. Keep the top-right chapter label on each main content
slide. Do not insert chapter divider slides. Use the exact six chapter names
and numbers from Overview. On the first content slide of each chapter, the
label is Arial 14 pt bold navy (#17365D); subsequent slides use Arial 12 pt
regular grey (#696969). The editable textbox is at (660, 21) pt with size
261.6 x 24 pt, aligned right and vertically centred above the title rule.

Chapter starts are physical slides 2 (Introduction), 4 (Cartesian controller),
10 (Contact experiments), 12 (Contact results), 18 (Null-space control and
experiments), and 25 (Conclusion and future work). Keep the title slide,
Overview and five hidden backups without this label. The 30-slide structure,
all original slide content and numbering, 29 native equations, five videos,
speaker notes and speaking files remain unchanged. The full PDF includes the
labels; Supplementary_slides.pdf is unchanged. See
experiments/chapter_labels_20261002/verification.json.
'''
agents.write_text(heading+rule+text[len(heading):],encoding='utf-8')
readme=FINAL/'README.txt';entry=('2026-10-02: Added the current Overview chapter name and number at the top right of every main content slide. Chapter starts (physical 2, 4, 10, 12, 18 and 25) use bold navy labels; continuing slides use smaller grey labels. No divider slides were inserted. Title, Overview and backups are unchanged. All existing slide content, numbering, notes, videos, native equations and speaking files are preserved. The full PDF is updated; the supplementary PDF is unchanged. See ../experiments/chapter_labels_20261002/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
v.update({'installed':True,'native_powerpoint_visual_review_passed':True,'all_six_chapter_starts_visually_reviewed':True,'final_pptx_sha256':hashlib.sha256((FINAL/'Thesis_Defense_gg0_v3.pptx').read_bytes()).hexdigest(),'final_pdf_sha256':hashlib.sha256((FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()).hexdigest()})
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Installed the chapter-labelled PowerPoint and matching PDF; all protected files remain unchanged.')
