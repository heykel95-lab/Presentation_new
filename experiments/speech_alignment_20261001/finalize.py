from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
from pypdf import PdfReader
import hashlib, json, re, shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
DECK=FINAL/'Thesis_Defense_gg0_v3.pptx'
verification=json.loads((HERE/'verification.json').read_text())
assert verification['all_speech_pages_rendered']
assert verification['latex_no_overfull_boxes']
before=json.loads((ARCHIVE/'package_hashes_before.json').read_text())
checkpoint=json.loads((ARCHIVE/'zip_checkpoint.json').read_text())
updates=json.loads((HERE/'updated_sections.json').read_text(encoding='utf-8'))
inventory=json.loads((HERE/'deck_inventory.json').read_text())
parts=verification['notes_parts']
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(ARCHIVE/'speaking_files_before.zip') as backup:
    assert backup.testzip() is None
    previous={n:backup.read(n) for n in backup.namelist()}
assert all((FINAL/name).read_bytes()==data for name,data in previous.items())
with ZipFile(DECK) as deck:
    assert deck.start_dir==checkpoint['start_dir']
    assert set(deck.namelist())==set(before)
    assert all(hashlib.sha256(deck.read(n)).hexdigest()==h for n,h in before.items())
source_tex=previous['Speaking/Thesis_Defense_Speaking_Script.tex'].decode('utf-8').replace('\r\n','\n')
updated_tex=(HERE/'Thesis_Defense_Speaking_Script.tex').read_text(encoding='utf-8')
assert re.findall(r'\\\[(.*?)\\\]',source_tex,re.S)==re.findall(r'\\\[(.*?)\\\]',updated_tex,re.S)
assert len(PdfReader(HERE/'Thesis_Defense_Speaking_Script.pdf').pages)==7
try:
    with ZipFile(DECK,'a',ZIP_DEFLATED) as deck:
        entries={n:deck.getinfo(n) for n in parts}
        deck.filelist=[i for i in deck.filelist if i.filename not in entries]
        for name in parts:del deck.NameToInfo[name]
        for name in parts:deck.writestr(entries[name],(HERE/Path(name).name).read_bytes())
    with ZipFile(DECK) as deck:
        assert len(deck.namelist())==len(set(deck.namelist()))==len(before)
        changed=[n for n,h in before.items() if hashlib.sha256(deck.read(n)).hexdigest()!=h]
        assert set(changed)==set(parts)
        for number,(_,bullets) in updates.items():
            part=inventory[int(number)-1]['notes_path']
            root=E.fromstring(deck.read(part))
            body=next(s.find('p:txBody',NS) for s in root.findall('.//p:sp',NS)
                      if s.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None
                      and s.find('p:nvSpPr/p:nvPr/p:ph',NS).get('type')=='body')
            lines=[''.join(p.itertext()) for p in body.findall('a:p',NS)]
            assert lines[:len(bullets)]==bullets
    for name in ['Thesis_Defense_Speaking_Script.pdf','Thesis_Defense_Speaking_Script_updated.pdf']:
        shutil.copy2(HERE/'Thesis_Defense_Speaking_Script.pdf',FINAL/name)
    shutil.copy2(HERE/'Thesis_Defense_Speaking_Script.tex',FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex')
    shutil.copy2(HERE/'Speaker_notes_and_timing.txt',FINAL/'Speaker_notes_and_timing.txt')
except Exception:
    with DECK.open('r+b') as deck:
        deck.seek(checkpoint['start_dir'])
        deck.write((ARCHIVE/'original_zip_directory.bin').read_bytes());deck.truncate()
    for name,data in previous.items():(FINAL/name).write_bytes(data)
    raise
for name,digest in verification['unchanged_slide_pdf_hashes'].items():
    assert hashlib.sha256((FINAL/name).read_bytes()).hexdigest()==digest
assert (FINAL/'Thesis_Defense_Speaking_Script.pdf').read_bytes()==(FINAL/'Thesis_Defense_Speaking_Script_updated.pdf').read_bytes()
build=FINAL/'Speaking/BUILD.txt'
contents=build.read_text(encoding='utf-8')
contents=contents.replace('The two Disturbance demonstration sections are distinguished by Part 1 and Part 2.',
    'The two disturbance-video sections identify the current captions: without null-space control to damping, and conditioning only.')
contents+='\nLatest minimal speech alignment (2026-10-01): only the null-space controller, two disturbance videos and null-space experiment sections were adjusted after the slide changes. The other 27 sections are unchanged. The PDF remains seven pages. Sources and verification: ../../experiments/speech_alignment_20261001/.\n'
build.write_text(contents,encoding='utf-8')
readme=FINAL/'README.txt'
entry=('2026-10-01: At the user request, minimally reorganized the speech after the latest slide edits. '
       'Grouped redundancy and coordinated motion, separated the damping and conditioning explanation, '
       'aligned the two video descriptions with their captions, and put the pose hold before the disturbance '
       'and conditioning before damping in the experiment description. Only four sections and their '
       'PowerPoint spoken notes changed; the other 27 sections, all equations and source/reference notes '
       'are preserved. Both seven-page speaking PDFs, the LaTeX source and plain-text copy agree. All '
       'visible slides, media and presentation PDFs are unchanged. '
       'See ../experiments/speech_alignment_20261001/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md'
contents=agents.read_text(encoding='utf-8')
heading='# Thesis and presentation workspace\n'
assert contents.startswith(heading)
rule=('\n## Minimal speech alignment after slide edits (2026-10-01)\n\n'
      'The user explicitly requested reorganizing the current speech with minimal\n'
      'wording changes. Only physical sections 19-22 / footers 18-21 changed:\n'
      'the null-space controller explanation is grouped by the current bullets,\n'
      'the videos identify no null-space control followed by damping and then\n'
      'conditioning only, and the experiment introduces the pose hold before\n'
      'the disturbance and lists conditioning before damping. All four conditions\n'
      'include the disturbance. The other 27 sections and every equation remain\n'
      'unchanged. The LaTeX source, both seven-page speaking PDFs, plain-text\n'
      'copy and PowerPoint spoken notes agree. Preserve the revised speech\n'
      'during unrelated slide edits. See\n'
      'experiments/speech_alignment_20261001/verification.json.\n')
agents.write_text(heading+rule+contents[len(heading):],encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'all_seven_speech_pages_visually_checked':True,'spoken_notes_match_speech':True,
    'both_speaking_pdfs_identical':True,'all_speech_equations_preserved':True,
    'slide_pdfs_unchanged':True,'installed':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Updated speech PDFs, editable source, plain text and four PowerPoint notes. All visible slides are unchanged.')
