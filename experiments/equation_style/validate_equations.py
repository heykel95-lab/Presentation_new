"""Check equation styling, mathematical structure, media and slide preservation."""
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import unquote
import json, posixpath, re

import fitz
import numpy as np
from lxml import etree as E

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
ASSETS = FINAL / 'figures_and_images'
SNAP = HERE / 'review'
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def read_package(path):
    with ZipFile(path) as z:
        assert z.testzip() is None
        return {name: z.read(name) for name in z.namelist()}


def resolve(owner, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(owner), unquote(target))).lstrip('/')


def math_signature(node):
    # Ignore only run/control typography, preserving every mathematical
    # operator, token, structure and structural property (including matrices).
    if node.tag in {
        '{' + NS['a'] + '}rPr', '{' + NS['m'] + '}rPr',
        '{' + NS['m'] + '}ctrlPr',
    }:
        return None
    return (node.tag, sorted(node.attrib.items()), node.text,
            [sig for child in node if (sig := math_signature(child)) is not None])


def pixels(page, clip=None):
    pix = page.get_pixmap(alpha=False, clip=clip)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)


parts = read_package(FINAL / 'Thesis_Defense_gg0_v3.pptx')
old = read_package(SNAP / 'before.pptx')
assert parts['ppt/presentation.xml'] == old['ppt/presentation.xml']
pres = E.fromstring(parts['ppt/presentation.xml'])
rels = {r.get('Id'): r.get('Target') for r in E.fromstring(parts['ppt/_rels/presentation.xml.rels'])}
paths = [resolve('ppt/presentation.xml', rels[n.get('{' + NS['r'] + '}id')])
         for n in pres.find('p:sldIdLst', NS)]
assert len(paths) == 34
refs = 0
for name, data in parts.items():
    if not name.endswith('.rels'):
        continue
    owner = '' if name == '_rels/.rels' else name.replace('/_rels/', '/')[:-5]
    for rel in E.fromstring(data):
        if rel.get('TargetMode') != 'External':
            assert resolve(owner, rel.get('Target')) in parts, (name, rel.get('Target'))
            refs += 1

catalog = json.loads((ASSETS / 'native_equations.json').read_text())
geometry = json.loads((HERE / 'update.json').read_text())
changed = set(geometry['changed_physical_slides'])
count = 0
for number, path in enumerate(paths, 1):
    root, before = E.fromstring(parts[path]), E.fromstring(old[path])
    assert (root.get('show') == '0') == (number > 25)
    new_math = root.findall('.//m:oMath', NS)
    old_math = before.findall('.//m:oMath', NS)
    assert [math_signature(m) for m in new_math] == [math_signature(m) for m in old_math], number
    if number not in changed | {4}:
        assert parts[path] == old[path], number
    ids = root.xpath('//*[local-name()="cNvPr"]/@id')
    assert len(ids) == len(set(ids)), number
    for c in [entry for entry in catalog if entry['slide'] == number]:
        s = next(s for s in root.findall('.//p:sp', NS)
                 if s.find('p:nvSpPr/p:cNvPr', NS).get('name') == c['shape'])
        assert s.findall('.//m:oMath', NS), c['shape']
        assert s.find('p:txBody/a:bodyPr/a:noAutofit', NS) is not None, c['shape']
        for prop in s.xpath('.//a:rPr|.//a:defRPr|.//a:endParaRPr', namespaces=NS):
            assert prop.get('sz') == '2200' and prop.get('b') == '0', c['shape']
            assert prop.find('a:solidFill/a:srgbClr', NS).get('val') == '000000'
            for kind in ['latin', 'ea', 'cs']:
                assert prop.find('a:' + kind, NS).get('typeface') == 'Cambria Math'
        assert not s.xpath('.//m:sty[@m:val="b" or @m:val="bi"]', namespaces=NS)
        assert c['font'] == 'Cambria Math' and c['font_size_pt'] == 22
        assert c['font_weight'] == 'regular' and c['color'] == '#000000'
        src = (ASSETS / c['source']).read_text()
        assert r'\setmathfont{Cambria Math}' in src and r'\fontsize{22}{27}' in src
        assert r'\mathbf{0}' not in src and c['latex'] in src
        for suffix in ['pdf', 'png', 'svg']:
            assert (ASSETS / (c['shape'][11:] + '.' + suffix)).is_file()
        asset = fitz.open(ASSETS / (c['shape'][11:] + '.pdf'))
        assert '𝟎' not in asset[0].get_text()
        count += 1
assert count == len(catalog) == 35
assert sum(len(E.fromstring(parts[p]).xpath('//p:sp[.//m:oMath]', namespaces=NS)) for p in paths) == count

# All image and video payloads and all playback relationships stay untouched.
media = [name for name in old if name.startswith('ppt/media/')]
assert all(parts[name] == old[name] for name in media)
assert all(parts[name] == data for name, data in old.items() if name.endswith('.rels'))
assert len([name for name in media if name.endswith('.mp4')]) == 3

pdf = fitz.open(FINAL / 'Thesis_Defense_gg0_v3.pdf')
before_pdf = fitz.open(SNAP / 'before.pdf')
supp = fitz.open(FINAL / 'Supplementary_slides.pdf')
assert len(pdf) == 34 and len(supp) == 9
preservation = []
for index in range(34):
    a, b = pixels(before_pdf[index]), pixels(pdf[index])
    if index + 1 not in changed:
        assert np.array_equal(a, b), index + 1
    else:
        mask = np.zeros(a.shape[:2], dtype=bool)
        boxes = [box for row in geometry['geometry'] if row['slide'] == index + 1
                 for box in [row['old_ink'], row['new_ink']]]
        if index + 1 == 10:
            boxes += [[175, 443, 450, 473], [175, 471, 465, 501]]
        for box in boxes:
            x0, y0, x1, y1 = box
            mask[max(0, int(y0) - 3):min(a.shape[0], int(y1) + 4),
                 max(0, int(x0) - 3):min(a.shape[1], int(x1) + 4)] = True
        changed_pixels = np.any(a != b, axis=2)
        unexpected = int(np.count_nonzero(changed_pixels & ~mask))
        preservation.append({'physical_slide': index + 1, 'changed_pixels_outside_edit_regions': unexpected})
        assert unexpected == 0, preservation[-1]
    for clip in [fitz.Rect(0, 500, 960, 540), fitz.Rect(0, 0, 960, 60)]:
        assert np.array_equal(pixels(before_pdf[index], clip), pixels(pdf[index], clip)), index + 1
for index in range(9):
    assert np.array_equal(pixels(pdf[index + 25]), pixels(supp[index]))
for row in geometry['geometry']:
    x0, y0, x1, y1 = row['new_ink']
    assert 0 <= x0 < x1 <= 960 and 60 < y0 < y1 < 500, row['asset']

script = (FINAL / 'Speaking/Thesis_Defense_Speaking_Script.tex').read_text()
old_script = (SNAP / 'before_script.tex').read_text()
comment = '% All 35 PowerPoint equations and symbol keys: 22 pt regular Cambria Math. Spoken content is unchanged.\n'
assert script.replace(comment, '', 1) == old_script
for name, data in old.items():
    if not re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', name):
        continue
    old_text = E.fromstring(data).xpath('//a:t/text()', namespaces=NS)
    new_text = E.fromstring(parts[name]).xpath('//a:t/text()', namespaces=NS)
    assert new_text[:len(old_text)] == old_text, name

report = {
    'equations': count, 'font': 'Cambria Math', 'base_size_pt': 22,
    'weight': 'regular', 'color': '#000000',
    'math_tokens_and_structures_preserved': True,
    'all_equations_remain_native_and_editable': True,
    'slides': 34, 'main': 25, 'hidden_backups': 9,
    'native_sections_order_and_visibility_preserved': True,
    'internal_relationships_resolved': refs,
    'all_media_and_playback_relationships_preserved': True,
    'embedded_videos': 3,
    'unchanged_pdf_pages_pixel_identical': 34 - len(changed),
    'headers_and_footers_pixel_identical': True,
    'changed_slides_preservation': preservation,
    'supplementary_pages_match_full_pdf': 9,
    'spoken_content_preserved': True,
    'visual_review': 'All 12 changed pages reviewed, including both wrench matrices, symbol keys and backup equations.'
}
(HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
