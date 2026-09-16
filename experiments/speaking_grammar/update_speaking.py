"""Apply the user's grammar-edited narration without changing slide content."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
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


def tag(prefix, local):
    return '{' + NS[prefix] + '}' + local


def resolve(owner, target):
    return posixpath.normpath(posixpath.dirname(owner) + '/' + target)


def relpath(owner):
    return posixpath.dirname(owner) + '/_rels/' + posixpath.basename(owner) + '.rels'


def latex(text):
    math = {'t₂': r'\(t_2\)', 'Kₚ,ₙ': r'\(K_{p,n}\)', 'Kᵣ,ₜ₁': r'\(K_{R,t_1}\)'}
    for index, key in enumerate(math):
        text = text.replace(key, 'MATHPLACEHOLDER' + str(index))
    text = text.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')
    text = text.replace('’', "'").replace('–', '--').replace('−', r'\ensuremath{-}')
    for index, value in enumerate(math.values()):
        text = text.replace('MATHPLACEHOLDER' + str(index), value)
    return text


SNAP.mkdir(exist_ok=True)
files = {
    'before.pptx': FINAL / 'Thesis_Defense_gg0_v3.pptx',
    'before_script.tex': FINAL / 'Speaking/Thesis_Defense_Speaking_Script.tex',
    'before_notes.txt': FINAL / 'Speaker_notes_and_timing.txt',
    'before_speaking.pdf': FINAL / 'Thesis_Defense_Speaking_Script.pdf',
}
for name, source in files.items():
    if not (SNAP / name).exists():
        shutil.copyfile(source, SNAP / name)
spoken = json.loads((HERE / 'corrected_narration.json').read_text())
with ZipFile(SNAP / 'before.pptx') as z:
    parts = {name: z.read(name) for name in z.namelist()}
pres = E.fromstring(parts['ppt/presentation.xml'])
rels = {r.get('Id'): r.get('Target') for r in E.fromstring(parts['ppt/_rels/presentation.xml.rels'])}
paths = [resolve('ppt/presentation.xml', rels[n.get(tag('r', 'id'))])
         for n in pres.find('p:sldIdLst', NS)]
titles = []
changed = []
for number, path in enumerate(paths, 1):
    root = E.fromstring(parts[path])
    if number == 1:
        title = 'Master Thesis Presentation'
    else:
        title_shape = next(s for s in root.findall('.//p:sp', NS)
                           if s.find('p:nvSpPr/p:cNvPr', NS).get('name') == 'Slide title')
        title = ''.join(title_shape.xpath('.//a:t/text()', namespaces=NS))
    titles.append(title)
    if title not in spoken:
        continue
    rs = E.fromstring(parts[relpath(path)])
    note_rel = next(r for r in rs if r.get('Type').endswith('/notesSlide'))
    note_path = resolve(path, note_rel.get('Target'))
    note = E.fromstring(parts[note_path])
    body = next(s.find('p:txBody', NS) for s in note.findall('.//p:sp', NS)
                if s.find('p:nvSpPr/p:nvPr/p:ph', NS) is not None
                and s.find('p:nvSpPr/p:nvPr/p:ph', NS).get('type') == 'body')
    paras = body.findall('a:p', NS)
    boundary = next(i for i, p in enumerate(paras)
                    if '[Sources]' in ''.join(p.xpath('.//a:t/text()', namespaces=NS)))
    # Preserve every source, reference and technical-note paragraph as XML.
    reference_paragraph = paras[boundary]
    for p in paras[:boundary]:
        body.remove(p)
    for line in spoken[title]:
        p = E.Element(tag('a', 'p'))
        r = E.SubElement(p, tag('a', 'r'))
        E.SubElement(r, tag('a', 't')).text = line
        body.insert(list(body).index(reference_paragraph), p)
    parts[note_path] = E.tostring(note, xml_declaration=True, encoding='UTF-8', standalone=True)
    changed.append({'physical_slide': number, 'title': title, 'notes_part': note_path})
assert set(spoken) <= set(titles)
with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx', 'w', ZIP_DEFLATED) as z:
    for name, data in parts.items():
        z.writestr(name, data)

script = (SNAP / 'before_script.tex').read_text()
chunks = re.split(r'(\\section\*\{[^}]+\})', script)
assert len(chunks) == 69
equation_after = {'Real-time control': {0: [0, 1]},
                  'Normal-force plausibility assessment': {0: [0]},
                  'Moment plausibility assessment': {0: [0]}}
for index in range(1, len(chunks), 2):
    title = re.fullmatch(r'\\section\*\{([^}]+)\}', chunks[index])[1]
    if title not in spoken:
        continue
    old_body = chunks[index + 1]
    equations = re.findall(r'\\\[.*?\\\]', old_body, re.S)
    body = '\n\\begin{itemize}\n'
    for item, text in enumerate(spoken[title]):
        body += '\\item ' + latex(text) + '\n'
        for equation in equation_after.get(title, {}).get(item, []):
            body += equations[equation] + '\n'
    body += '\\end{itemize}\n\n'
    # Keep the final document terminator if a later request edits the last section.
    if '\\end{document}' in old_body:
        body += '\\end{document}\n'
    chunks[index + 1] = body
chunks[0] = chunks[0].replace(
    '% All 35 PowerPoint equations and symbol keys: 22 pt regular Cambria Math. Spoken content is unchanged.',
    '% All 35 PowerPoint equations and symbol keys: 22 pt regular Cambria Math.')
chunks[0] = '% 2026-09-16: user-supplied narration, grammar-only edit. Technical review is separate.\n' + chunks[0]
(FINAL / 'Speaking/Thesis_Defense_Speaking_Script.tex').write_text(''.join(chunks))

notes = (SNAP / 'before_notes.txt').read_text()
for i, title in enumerate(titles):
    if title not in spoken:
        continue
    heading = title + '\n' + '-' * len(title) + '\n'
    # Existing headings occasionally have a different underline length.
    match = re.search(r'^' + re.escape(title) + r'\n-+\n', notes, re.M)
    assert match, title
    start = match.start()
    if i + 1 < len(titles):
        following = re.search(r'^' + re.escape(titles[i + 1]) + r'\n-+\n', notes[match.end():], re.M)
        assert following
        end = match.end() + following.start()
    else:
        end = len(notes)
    notes = notes[:start] + heading + '\n'.join(spoken[title]) + '\n\n' + notes[end:]
(FINAL / 'Speaker_notes_and_timing.txt').write_text(notes)
(HERE / 'update.json').write_text(json.dumps({'updated_sections': len(changed), 'slides': changed,
    'unchanged_sections': [title for title in titles if title not in spoken],
    'scope': 'Grammar-only narration update. Visible slides, figures, equations and media unchanged.'}, indent=2) + '\n')
print('Updated narration for', len(changed), 'slides. Preserved', len(titles) - len(changed), 'other sections.')
