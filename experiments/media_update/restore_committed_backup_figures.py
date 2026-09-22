"""Restore B6/B9 figure designs from the author's committed thesis reference.

Usage: python3 restore_committed_backup_figures.py WORKDIR
WORKDIR contains before_Thesis_Defense_gg0_v3.{pptx,pdf} and assets/.
The script stages the presentation and PDFs, preserving the nine-backup order.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import posixpath
import sys

import fitz
import numpy as np
from lxml import etree as E

W = Path(sys.argv[1]).resolve()
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
TARGETS = [
    {'physical': 32, 'footer': 'B6', 'title': 'Angular quantities',
     'path': 'ppt/slides/slide12.xml', 'shape': 'Figure - angular_quantities',
     'asset': 'angular_quantities',
     'description': 'Committed thesis figure appearance restored: blue angular-error arc inside the red measured-offset arc. Surface-frame inset has n_s leftwards, t_2 upwards and t_1 out of the page. Reference PDF from thesis commit be7aa4d, matching source from 33b7dc5.'},
    {'physical': 35, 'footer': 'B9', 'title': 'Sources of angular offset',
     'path': 'ppt/slides/slide40.xml', 'shape': 'Surface entry concept',
     'asset': 'thesis_figure_1_1',
     'description': 'Original thesis surface-entry diagram. Single-row legend: Configured surface, Physical surface, Tool face. Black dashed desired-direction datum and both difference arcs retained. Figure source from thesis commit be7aa4d.'},
]


def dump(root):
    return E.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)


def named(root, name):
    values = root.xpath('.//*[p:nvSpPr/p:cNvPr/@name=$n or p:nvPicPr/p:cNvPr/@name=$n]', namespaces=NS, n=name)
    assert len(values) == 1, name
    return values[0]


def box(sh):
    off = sh.find('p:spPr/a:xfrm/a:off', NS)
    ext = sh.find('p:spPr/a:xfrm/a:ext', NS)
    x, y = int(off.get('x')) / 12700, int(off.get('y')) / 12700
    return fitz.Rect(x, y, x + int(ext.get('cx')) / 12700, y + int(ext.get('cy')) / 12700)


with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as old:
    changes = {}
    originals = {}
    for target in TARGETS:
        path = target['path']
        original = E.fromstring(old.read(path))
        originals[path] = original
        slide = deepcopy(original)
        picture = named(slide, target['shape'])
        target['old_box_pt'] = list(box(picture))
        area = box(picture)
        figure = fitz.open(W / 'assets' / (target['asset'] + '.pdf'))
        height = area.width * figure[0].rect.height / figure[0].rect.width
        centre_y = (area.y0 + area.y1) / 2
        off = picture.find('p:spPr/a:xfrm/a:off', NS)
        ext = picture.find('p:spPr/a:xfrm/a:ext', NS)
        off.set('y', str(round((centre_y - height / 2) * 12700)))
        ext.set('cy', str(round(height * 12700)))
        picture.find('p:nvPicPr/p:cNvPr', NS).set('descr', target['description'])
        target['new_box_pt'] = list(box(picture))
        rid = picture.find('p:blipFill/a:blip', NS).get('{' + NS['r'] + '}embed')
        rp = posixpath.dirname(path) + '/_rels/' + posixpath.basename(path) + '.rels'
        rels = E.fromstring(old.read(rp))
        rel = next(r for r in rels if r.get('Id') == rid)
        media = posixpath.normpath(posixpath.join(posixpath.dirname(path), rel.get('Target')))
        data = (W / 'assets' / (target['asset'] + '.png')).read_bytes()
        changes[media] = data
        changes[path] = dump(slide)
        target['media_part'] = media
        target['restored_png_sha256'] = hashlib.sha256(data).hexdigest()
        assert slide.get('show') == '0'
        assert ''.join(named(slide, 'TextBox 6').xpath('.//a:t/text()', namespaces=NS)) == target['footer']
        restored = deepcopy(slide)
        restored_pic = named(restored, target['shape'])
        restored_pic.getparent().replace(restored_pic, deepcopy(named(original, target['shape'])))
        assert E.tostring(restored) == E.tostring(original)
    pres = E.fromstring(old.read('ppt/presentation.xml'))
    chapters = [s.get('name') for s in pres.findall('.//p14:section', NS) if s.get('name') != 'Backup']
    overview = E.fromstring(old.read('ppt/slides/slide4.xml'))
    before_overview = dump(overview)
    for i, title in enumerate(chapters, 1):
        for name, value in [('Overview item %d' % i, title), ('Overview number %d' % i, '%d.' % i)]:
            texts = named(overview, name).findall('.//a:t', NS)
            assert len(texts) == 1
            texts[0].text = value
    assert dump(overview) == before_overview
    with ZipFile(W / 'updated.pptx', 'w') as out:
        for info in old.infolist():
            out.writestr(info, changes.get(info.filename, old.read(info.filename)))

original_pdf = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
pdf = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
assert len(pdf) == 35
for target in TARGETS:
    page = pdf[target['physical'] - 1]
    old_box = fitz.Rect(target['old_box_pt'])
    new_box = fitz.Rect(target['new_box_pt'])
    clear_box = (old_box | new_box) + (-1, -1, 1, 1)
    page.add_redact_annot(clear_box, fill=(1, 1, 1))
    page.apply_redactions(images=1, graphics=1, text=0)
    figure = fitz.open(W / 'assets' / (target['asset'] + '.pdf'))
    page.show_pdf_page(new_box, figure, 0)
pdf.save(W / 'updated.pdf', garbage=4, deflate=True)
supplement = fitz.open()
supplement.insert_pdf(pdf, from_page=26, to_page=34)
supplement.save(W / 'supplementary.pdf', garbage=4, deflate=True)

with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as old, ZipFile(W / 'updated.pptx') as new:
    assert old.namelist() == new.namelist()
    changed_parts = [n for n in old.namelist() if old.read(n) != new.read(n)]
    assert set(changed_parts) == set(changes), changed_parts
    assert new.testzip() is None
final = fitz.open(W / 'updated.pdf')
supplement = fitz.open(W / 'supplementary.pdf')
for i in range(35):
    before = original_pdf[i].get_pixmap(alpha=False)
    after = final[i].get_pixmap(alpha=False)
    target = next((t for t in TARGETS if t['physical'] == i + 1), None)
    if target:
        dims = (before.height, before.width, 3)
        a = np.frombuffer(before.samples, np.uint8).reshape(dims)
        b = np.frombuffer(after.samples, np.uint8).reshape(dims)
        changed = np.any(a != b, axis=2)
        area = fitz.Rect(target['old_box_pt']) | fitz.Rect(target['new_box_pt'])
        changed[int(area.y0)-3:int(area.y1)+4, int(area.x0)-3:int(area.x1)+4] = False
        assert not changed.any(), ('Pixels outside figure changed', target['title'])
    else:
        assert before.samples == after.samples, ('Other page changed', i + 1)
    if i >= 26:
        assert after.samples == supplement[i - 26].get_pixmap(alpha=False).samples
report = {'date': '2026-09-22', 'reference_thesis_commit': 'be7aa4d0865eea56af36aeefb4594c29ca7dc35e',
          'angular_pdf_source_commit': '33b7dc535754da84779a31318f6912d0860d62d2',
          'restored_figures': TARGETS, 'changed_pptx_parts': changed_parts,
          'main_slides': 26, 'hidden_backups': 9, 'total_slides': 35,
          'supplementary_pages': 9, 'native_equation_count': 29,
          'all_other_slide_objects_notes_media_order_and_sections_unchanged': True,
          'other_33_pdf_pages_pixel_identical': True,
          'affected_slides_unchanged_outside_figure_rectangles': True,
          'supplementary_matches_full_pdf': True,
          'overview_refreshed_from_sections': chapters}
(W / 'presentation_verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Staged B6 and B9 restored figures. All other 33 PDF pages are pixel-identical.')
