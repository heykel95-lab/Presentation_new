"""Reorganize the authorized narration, preserving all slide and media bytes."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FINAL = ROOT / 'Final Presentation'
DECK = FINAL / 'Thesis_Defense_gg0_v3.pptx'
SCRIPT = FINAL / 'Speaking/Thesis_Defense_Speaking_Script.tex'
ARCHIVE = HERE / 'archive'
ARCHIVE.mkdir(exist_ok=True)
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
slides = json.loads((HERE / 'deck_inspection.json').read_text(encoding='utf-8'))
speech = json.loads((HERE / 'narration.json').read_text(encoding='utf-8'))
assert len(speech) == len(slides) == 31
assert sum(not s['hidden'] for s in slides) == 26
assert [(s['physical'], s['title']) for s in speech] == [(s['physical'], s['title']) for s in slides]
assert len({s['notes_path'] for s in slides}) == 31

for source in [SCRIPT, FINAL / 'Speaker_notes_and_timing.txt',
               FINAL / 'Thesis_Defense_Speaking_Script.pdf',
               FINAL / 'Thesis_Defense_Speaking_Script_updated.pdf',
               FINAL / 'Thesis_Defense_gg0_v3.pdf', FINAL / 'Supplementary_slides.pdf',
               FINAL / 'README.txt', FINAL / 'Speaking/BUILD.txt']:
    target = ARCHIVE / source.name
    if not target.exists():
        shutil.copy2(source, target)

def digest(value):
    return hashlib.sha256(value).hexdigest()

def paragraph(text):
    return '<a:p><a:r><a:t>' + escape(text) + '</a:t></a:r></a:p>'

def notes_body(xml):
    for match in re.finditer(r'<p:sp\b[^>]*>.*?</p:sp>', xml, re.S):
        if re.search(r'<p:ph\b[^>]*\btype="body"', match[0]):
            body = re.search(r'(<p:txBody>.*?<a:lstStyle\s*/>)(.*?)(</p:txBody>)', match[0], re.S)
            assert body
            return match, body
    raise ValueError('No notes body')

def source_tail(xml):
    match, body = notes_body(xml)
    for p in re.finditer(r'<a:p(?:\s[^>]*)?>.*?</a:p>|<a:p\s*/>', body[2], re.S):
        if '[Sources]' in p[0]:
            return body[2][p.start():]
    assert '[Sources]' not in body[2]
    return ''

notes_archive = ARCHIVE / 'original_notes.zip'
if not notes_archive.exists():
    with ZipFile(DECK) as original, ZipFile(notes_archive, 'w', ZIP_DEFLATED) as backup:
        for s in slides:
            backup.writestr(s['notes_path'], original.read(s['notes_path']))

updated = {}
with ZipFile(notes_archive) as original:
    for item, slide in zip(speech, slides):
        xml = original.read(slide['notes_path']).decode('utf-8')
        match, body = notes_body(xml)
        old_sources = source_tail(xml)
        refs = old_sources
        if not refs:
            refs = paragraph('[Sources]\n' + '\n'.join(item.get('sources', [])) + '\n[/Sources]')
        # Existing provenance remains byte-for-byte intact, with its date context explicit.
        if item['physical'] in [1, 17, 22, 23, 24, 25]:
            current = 'Narration follows the current 26-main-slide and five-backup deck. Earlier source and implementation records above are historical provenance.'
            if item['physical'] == 1:
                current += ' The robot photograph is on Motivation.'
            if item['physical'] == 17:
                current += ' The current CoC comparison spans -100 to +100 mm using 78 terminal reports. See experiments/coc_extension/README.md.'
            if item['physical'] in [22, 23, 24, 25]:
                current += ' Main results compare no torque, damping 2, conditioning 2, and combined 2+2. Removed parameter and all-settings slides are not part of the current talk.'
            if item['physical'] == 25:
                current += ' Both main joint-motion panels show 0-4 s, with an enlarged vertical view on the right.'
            refs += paragraph('[Narration update 2026-10-01]\n' + current)
        text = ''.join(paragraph(p) for p in item['bullets']) + refs
        shape = match[0][:body.start(2)] + text + match[0][body.end(2):]
        new_xml = xml[:match.start()] + shape + xml[match.end():]
        ET.fromstring(new_xml)
        if old_sources:
            assert old_sources in new_xml
        updated[slide['notes_path']] = new_xml.encode('utf-8')

staging = HERE / 'narration_updated.pptx'
before = {}
with ZipFile(DECK) as original, ZipFile(staging, 'w', ZIP_DEFLATED) as target:
    for info in original.infolist():
        value = original.read(info.filename)
        before[info.filename] = digest(value)
        target.writestr(info, updated.get(info.filename, value))

changed = []
with ZipFile(staging) as result:
    assert set(result.namelist()) == set(before)
    for info in result.infolist():
        if digest(result.read(info.filename)) != before[info.filename]:
            changed.append(info.filename)
    assert changed and all(name in updated for name in changed)
    for item, slide in zip(speech, slides):
        root = ET.fromstring(result.read(slide['notes_path']))
        body = next(s.find('p:txBody', NS) for s in root.findall('.//p:sp', NS)
                    if s.find('p:nvSpPr/p:nvPr/p:ph', NS) is not None
                    and s.find('p:nvSpPr/p:nvPr/p:ph', NS).get('type') == 'body')
        lines = [''.join(p.itertext()) for p in body.findall('a:p', NS)]
        assert lines[:len(item['bullets'])] == item['bullets']
staging.replace(DECK)

def latex(value):
    value = value.replace('–', '--').replace('—', '---').replace('’', "'")
    value = value.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')
    value = re.sub(r'\bt2\b', r'\\(t_2\\)', value)
    return value

equations = {
    8: {1: [r'\tau=J^\top(q)F', r'\begin{bmatrix}\dot p_{\mathrm{EE}}\\\omega_{\mathrm{EE}}\end{bmatrix}=J(q)\dot q']},
    13: {0: [r'F_{n,\mathrm{qs}}=(1000\,\mathrm{N/m})(-0.019650\,\mathrm{m})=-19.650\,\mathrm{N}']},
    14: {1: [r'M_{t_1,\mathrm{qs}}=(15\,\mathrm{N\,m/rad})\left(6.565\,\frac{\pi}{180}\,\mathrm{rad}\right)\approx1.719\,\mathrm{N\,m}']},
    28: {0: [r'N_\tau=I_7-J^\top J^{+\top}'],
         1: [r'\tau_{\mathrm{null}}=\tau_d+\tau_\sigma'],
         2: [r'\tau_d=-d_{\mathrm{null}}N_\tau\dot q'],
         3: [r'\tau_\sigma=k_\sigma N_\tau(s_\sigma v_7)']}
}
original_tex = (ARCHIVE / SCRIPT.name).read_text(encoding='utf-8')
preamble = original_tex[original_tex.index(r'\documentclass'):original_tex.index(r'\begin{document}')]
preamble = '\n'.join(line for line in preamble.splitlines() if not line.startswith('%'))
tex = '% 2026-10-01: authorized speech reorganization for 26 main slides and five hidden backups.\n'
tex += '% Spoken bullets match the current PowerPoint notes. Slide content and media are preserved.\n'
tex += preamble + '\n\\begin{document}\n\n'
plain = []
for item in speech:
    heading = item['title'] + (' - ' + item['caption'] if item.get('caption') else '')
    tex += '\\section*{' + latex(heading) + '}\n\\begin{itemize}\n'
    plain.extend([heading, '-' * len(heading)])
    for index, bullet in enumerate(item['bullets']):
        assert ';' not in bullet
        assert not re.search(r'\b(gains?|inferred|infered|signed)\b', bullet, re.I), bullet
        tex += '\\item ' + latex(bullet) + '\n'
        for equation in equations.get(item['physical'], {}).get(index, []):
            tex += '\\[\n' + equation + '\n\\]\n'
        plain.append(bullet)
    tex += '\\end{itemize}\n\n'
    plain.append('')
tex += '\\end{document}\n'
assert tex.count(r'\section*{') == 31
SCRIPT.write_text(tex, encoding='utf-8')
(FINAL / 'Speaker_notes_and_timing.txt').write_text('\n'.join(plain) + '\n', encoding='utf-8')
(HERE / 'package_hashes_before.json').write_text(json.dumps(before, indent=2), encoding='utf-8')
verification = {
    'date': '2026-10-01',
    'main_slides': 26, 'hidden_backups': 5, 'speaking_sections': 31,
    'changed_pptx_parts': changed,
    'slide_layouts_equations_images_media_order_visibility_unchanged': True,
    'existing_source_reference_xml_preserved': True,
    'narration_matches_powerpoint_notes': True,
    'spoken_words_main': sum(len(re.findall(r"\b[\w'-]+\b", b)) for s in speech[:26] for b in s['bullets']),
    'removed_obsolete_speaking_sections': ['Effect of conditioning torque', 'Cumulative joint motion: all settings', 'Jacobian conditioning: all settings', 'Joint motion: mean of three trials', 'Joint motion: all individual trials', 'Joint motion: one trial per setting'],
    'archive': str(ARCHIVE.relative_to(ROOT)),
    'pdf_build_and_visual_review': 'pending'
}
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in verification.items() if k != 'changed_pptx_parts'}, indent=2))
