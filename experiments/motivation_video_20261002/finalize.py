from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import hashlib,json,shutil
from prepare import HERE, ROOT, FINAL, ARCHIVE

verification=json.loads((HERE/'verification.json').read_text())
assert verification['all_pdf_content_outside_requested_regions_pixel_identical']
native=json.loads((HERE/'native_media_inspection.json').read_text(encoding='utf-8-sig'))
assert native['durationMs']==51003 and native['playOnEntry']==0 and native['volume']==0.8
assert native['width']==native['height']==400
for name in ['Thesis_Defense_gg0_v3.pptx','Thesis_Defense_gg0_v3.pdf']:
    assert hashlib.sha256((FINAL/name).read_bytes()).hexdigest()==hashlib.sha256((ARCHIVE/name).read_bytes()).hexdigest(), 'Source changed during editing'

shutil.copyfile(HERE/'updated.pptx',FINAL/'Thesis_Defense_gg0_v3.pptx')
shutil.copyfile(HERE/'updated.pdf',FINAL/'Thesis_Defense_gg0_v3.pdf')
shutil.copyfile(HERE/'native_equations.json',FINAL/'figures_and_images/native_equations.json')
manifest=FINAL/'figures_and_images/manifest.json'
shutil.copy2(manifest,ARCHIVE/'manifest.json')
items=json.loads(manifest.read_text(encoding='utf-8'))
for item in items:
    if item.get('asset')=='title_robot':item['changes']='Moved from Motivation back to the title slide on 2026-10-02 at the user request. Full photograph on the right at (592, 103) pt, width 329.6 pt, unchanged aspect ratio and original image bytes. Motivation now contains the original embedded Contact demonstration video.'
manifest.write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

rule='''
## Title photograph and Motivation contact video (2026-10-02)

The robot photograph is back on the title slide, on the right at (592, 103) pt
with width 329.6 pt and its original uncropped aspect ratio. Keep the title
text, university logos and date unchanged. On Motivation, retain Problem and
Idea on the left and the original Contact.mp4 demonstration on the right in
a 400 pt square at (521.6, 75) pt. Preserve its original poster, complete
51.003-second recording, audio, 80% playback volume and click-to-play setting.
This supersedes the earlier requirement to show the photo on Motivation.

The separate Contact demonstration slide was removed at the user's request.
Its original slide, notes and media are archived in
experiments/motivation_video_20261002/archive/removed_contact_demonstration.pptx
and its matching PDF. Do not restore that separate slide automatically.

There are now 25 main slides and five hidden backups, 30 slides total.
Overview is physical slide 3 / footer 2, Conclusion is physical 25 / footer 24,
and B1-B5 occupy physical slides 26-30. All slides formerly at physical 4-31
shift down by one; main footer numbers shift down by one. Backup B labels
and the six Overview chapters are unchanged. In particular, Null-space
controller is physical 18 / footer 17, the two disturbance videos are physical
19-20 / footers 18-19, and Null-space experiment is physical 21 / footer 20.
Keep every retained slide's body, all 29 native equations, all five original
video streams, the retained notes and the speaking files unchanged. The
30-page full PDF matches the edited deck; the five-page supplementary PDF
remains unchanged. See experiments/motivation_video_20261002/verification.json.
'''
agents=ROOT/'AGENTS.md';contents=agents.read_text(encoding='utf-8');heading='# Thesis and presentation workspace\n'
assert contents.startswith(heading)
agents.write_text(heading+rule+contents[len(heading):],encoding='utf-8')
readme=FINAL/'README.txt'
entry=('2026-10-02: Moved the full robot photo from Motivation to the title slide and placed the original Contact demonstration video on Motivation. Removed and archived the separate Contact demonstration slide at the user request. The deck and full PDF have 30 slides/pages: 25 main slides and five hidden backups. Overview is physical 3, Conclusion is physical 25, and backups are physical 26-30. Main footers and the native-equation catalog are renumbered. Retained slide bodies, all native equations, all video streams and audio, retained notes and speaking files are unchanged. The five-page supplementary PDF is unchanged. See ../experiments/motivation_video_20261002/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
for name,digest in json.loads((ARCHIVE/'protected_files.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
verification.update({'installed':True,'powerpoint_native_preview_checked':True,'powerpoint_media_inspection':native,'title_and_motivation_visually_reviewed':True,'final_deck_sha256':hashlib.sha256((FINAL/'Thesis_Defense_gg0_v3.pptx').read_bytes()).hexdigest(),'final_pdf_sha256':hashlib.sha256((FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()).hexdigest()})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Installed the verified presentation and PDF; recorded the new slide structure and preserved speaking files.')
