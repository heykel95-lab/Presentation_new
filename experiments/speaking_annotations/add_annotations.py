"""Insert requested parenthetical review comments without rewriting narration."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import posixpath
import re
import shutil

from lxml import etree as E

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
SNAP = HERE / 'review'
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def latex(text):
    math = {'t₂': r'\(t_2\)', 'Kₚ,ₙ': r'\(K_{p,n}\)', 'Kᵣ,ₜ₁': r'\(K_{R,t_1}\)'}
    for index, key in enumerate(math):
        text = text.replace(key, 'MATHPLACEHOLDER' + str(index))
    text = text.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')
    text = text.replace('’', "'").replace('–', '--').replace('−', r'\ensuremath{-}')
    for index, value in enumerate(math.values()):
        text = text.replace('MATHPLACEHOLDER' + str(index), value)
    return text


def resolve(owner, target):
    return posixpath.normpath(posixpath.dirname(owner) + '/' + target)


def relpath(owner):
    return posixpath.dirname(owner) + '/_rels/' + posixpath.basename(owner) + '.rels'


def note_body(root):
    return next(s.find('p:txBody', NS) for s in root.findall('.//p:sp', NS)
                if s.find('p:nvSpPr/p:nvPr/p:ph', NS) is not None
                and s.find('p:nvSpPr/p:nvPr/p:ph', NS).get('type') == 'body')


def paragraph_text(p):
    return ''.join(p.xpath('.//a:t/text()', namespaces=NS))


SNAP.mkdir(exist_ok=True)
for name, source in {
    'before.pptx': FINAL / 'Thesis_Defense_gg0_v3.pptx',
    'before_script.tex': FINAL / 'Speaking/Thesis_Defense_Speaking_Script.tex',
    'before_notes.txt': FINAL / 'Speaker_notes_and_timing.txt',
    'before_speaking.pdf': FINAL / 'Thesis_Defense_Speaking_Script.pdf',
}.items():
    if not (SNAP / name).exists():
        shutil.copyfile(source, SNAP / name)

comments = json.loads((HERE / 'annotations.json').read_text())
original = json.loads((HERE.parent / 'speaking_grammar/corrected_narration.json').read_text())
annotated = json.loads(json.dumps(original))
for title, entries in comments.items():
    for entry in entries:
        assert '(' not in entry['note'] and ')' not in entry['note']
        text = annotated[title][entry['item']]
        addition = ' (' + entry['note'] + ')'
        if 'after' in entry:
            assert text.count(entry['after']) == 1
            text = text.replace(entry['after'], entry['after'] + addition, 1)
        else:
            text += addition
        annotated[title][entry['item']] = text

script = (SNAP / 'before_script.tex').read_text()
notes = (SNAP / 'before_notes.txt').read_text()
replacements = []
for title, entries in comments.items():
    for item in sorted({entry['item'] for entry in entries}):
        old, new = original[title][item], annotated[title][item]
        assert script.count(latex(old)) == notes.count(old) == 1, (title, item)
        script = script.replace(latex(old), latex(new), 1)
        notes = notes.replace(old, new, 1)
        replacements.append((title, item, old, new))
# The following inverse check ensures every original sentence, equation and
# formatting command stays intact when only the new comments are removed.
restored_script, restored_notes = script, notes
for title, item, old, new in replacements:
    restored_script = restored_script.replace(latex(new), latex(old), 1)
    restored_notes = restored_notes.replace(new, old, 1)
assert restored_script == (SNAP / 'before_script.tex').read_text()
assert restored_notes == (SNAP / 'before_notes.txt').read_text()

with ZipFile(SNAP / 'before.pptx') as z:
    old_parts = {name: z.read(name) for name in z.namelist()}
parts = dict(old_parts)
pres = E.fromstring(parts['ppt/presentation.xml'])
rs = {r.get('Id'): r.get('Target') for r in E.fromstring(parts['ppt/_rels/presentation.xml.rels'])}
paths = [resolve('ppt/presentation.xml', rs[n.get('{' + NS['r'] + '}id')])
         for n in pres.find('p:sldIdLst', NS)]
changed = []
for number, path in enumerate(paths, 1):
    root = E.fromstring(parts[path])
    title = 'Master Thesis Presentation' if number == 1 else paragraph_text(next(
        s for s in root.findall('.//p:sp', NS)
        if s.find('p:nvSpPr/p:cNvPr', NS).get('name') == 'Slide title'))
    if title not in comments:
        continue
    rel = next(r for r in E.fromstring(parts[relpath(path)]) if r.get('Type').endswith('/notesSlide'))
    note_path = resolve(path, rel.get('Target'))
    note = E.fromstring(parts[note_path])
    body = note_body(note)
    paragraphs = body.findall('a:p', NS)
    boundary = next(i for i, p in enumerate(paragraphs) if '[Sources]' in paragraph_text(p))
    assert [paragraph_text(p) for p in paragraphs[:boundary]] == original[title]
    for item in sorted({entry['item'] for entry in comments[title]}):
        nodes = paragraphs[item].findall('.//a:t', NS)
        assert len(nodes) == 1
        nodes[0].text = annotated[title][item]
    parts[note_path] = E.tostring(note, xml_declaration=True, encoding='UTF-8', standalone=True)
    old_body = note_body(E.fromstring(old_parts[note_path]))
    assert [E.tostring(p) for p in old_body.findall('a:p', NS)[boundary:]] == [E.tostring(p) for p in paragraphs[boundary:]]
    changed.append({'physical_slide': number, 'title': title, 'notes_part': note_path})

changed_parts = {entry['notes_part'] for entry in changed}
assert len(changed) == len(comments)
assert all(parts[name] == data for name, data in old_parts.items() if name not in changed_parts)
assert len(paths) == 34
assert sum(len(E.fromstring(parts[p]).xpath('//*[local-name()="sp"][.//*[local-name()="oMath"]]')) for p in paths) == 35

slide_pdf = FINAL / 'Thesis_Defense_gg0_v3.pdf'
pdf_hash = hashlib.sha256(slide_pdf.read_bytes()).hexdigest()
with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx', 'w', ZIP_DEFLATED) as z:
    for name, data in parts.items():
        z.writestr(name, data)
(FINAL / 'Speaking/Thesis_Defense_Speaking_Script.tex').write_text(script)
(FINAL / 'Speaker_notes_and_timing.txt').write_text(notes)
(HERE / 'annotated_narration.json').write_text(json.dumps(annotated, ensure_ascii=False, indent=2) + '\n')
with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx') as z:
    assert z.testzip() is None
    assert all(z.read(name) == data for name, data in parts.items())
report = {
    'parenthetical_comments': sum(len(entries) for entries in comments.values()),
    'annotated_sections': len(changed),
    'changed_note_parts': changed,
    'all_original_narration_preserved': True,
    'all_existing_speaking_equations_and_formatting_preserved': True,
    'all_source_and_technical_note_paragraphs_preserved': True,
    'all_visible_slide_xml_media_relationships_and_equations_byte_identical': True,
    'native_editable_equations': 35,
    'slides': 34,
    'visible_slide_pdf_unchanged_sha256': pdf_hash,
    'notes_and_speaking_source_synchronized': True,
}
(HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print('Inserted', report['parenthetical_comments'], 'parenthetical comments in', len(changed), 'sections.')
