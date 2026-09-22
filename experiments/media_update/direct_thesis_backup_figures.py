"""Stage B6/B8 using figure crops directly from the compiled thesis.

Usage: python3 direct_thesis_backup_figures.py WORKDIR
WORKDIR contains before_Thesis_Defense_gg0_v3.{pptx,pdf}, before_Thesis.pdf,
and thesis_build/Thesis.pdf. The page clips below are checked against captions.
No diagram is reconstructed or independently rendered for the presentation.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import posixpath
import subprocess
import sys

import fitz
import numpy as np
from lxml import etree as E

W = Path(sys.argv[1]).resolve()
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
targets = [
    dict(asset='angular_quantities', physical=32, footer='B6',
         slide='ppt/slides/slide12.xml', shape='Figure - angular_quantities',
         thesis_page=79, caption='Figure 4.2:', clip=[120, 230, 472, 373]),
    dict(asset='thesis_figure_1_1', physical=34, footer='B8',
         slide='ppt/slides/slide40.xml', shape='Surface entry concept',
         thesis_page=28, caption='Figure 1.1:', clip=[108, 574, 479, 695.5]),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def named(root, name):
    result = root.xpath('.//*[p:nvSpPr/p:cNvPr/@name=$n or '
                        'p:nvPicPr/p:cNvPr/@name=$n]', namespaces=NS, n=name)
    assert len(result) == 1
    return result[0]


def box(shape):
    off = shape.find('p:spPr/a:xfrm/a:off', NS)
    ext = shape.find('p:spPr/a:xfrm/a:ext', NS)
    x, y = int(off.get('x')) / 12700, int(off.get('y')) / 12700
    return fitz.Rect(x, y, x + int(ext.get('cx')) / 12700,
                     y + int(ext.get('cy')) / 12700)


thesis = fitz.open(W / 'thesis_build/Thesis.pdf')
assert len(thesis) == 122
(W / 'assets').mkdir(exist_ok=True)
for t in targets:
    page = thesis[t['thesis_page'] - 1]
    clip = fitz.Rect(t['clip'])
    assert t['caption'] in page.get_text()
    assert t['caption'] not in page.get_text(clip=clip)
    out = fitz.open()
    out.new_page(width=clip.width, height=clip.height)
    out[0].show_pdf_page(out[0].rect, thesis, t['thesis_page'] - 1, clip=clip)
    stem = W / 'assets' / t['asset']
    out.save(stem.with_suffix('.pdf'), garbage=4, deflate=True)
    # Embed a direct raster export of the thesis figure, preserving every mark.
    page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip, alpha=False).save(
        stem.with_suffix('.png'))
    subprocess.run(['pdftocairo', '-svg', str(stem.with_suffix('.pdf')),
                    str(stem.with_suffix('.svg'))], check=True)
    t['pdf_sha256'] = sha(stem.with_suffix('.pdf'))
    t['png_sha256'] = sha(stem.with_suffix('.png'))

with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as old:
    changes = {}
    for t in targets:
        original = E.fromstring(old.read(t['slide']))
        slide = deepcopy(original)
        pic = named(slide, t['shape'])
        area = box(pic)
        t['old_box_pt'] = list(area)
        clip = fitz.Rect(t['clip'])
        height = area.width * clip.height / clip.width
        centre_y = (area.y0 + area.y1) / 2
        pic.find('p:spPr/a:xfrm/a:off', NS).set(
            'y', str(round((centre_y - height / 2) * 12700)))
        pic.find('p:spPr/a:xfrm/a:ext', NS).set('cy', str(round(height * 12700)))
        pic.find('p:nvPicPr/p:cNvPr', NS).set(
            'descr', 'Direct extract of thesis %s on PDF page %d. Original '
            'thesis geometry, labels and colours retained.' %
            (t['caption'].rstrip(':'), t['thesis_page']))
        t['new_box_pt'] = list(box(pic))
        rid = pic.find('p:blipFill/a:blip', NS).get('{' + NS['r'] + '}embed')
        rp = posixpath.dirname(t['slide']) + '/_rels/' + posixpath.basename(t['slide']) + '.rels'
        rel = next(r for r in E.fromstring(old.read(rp)) if r.get('Id') == rid)
        media = posixpath.normpath(posixpath.join(posixpath.dirname(t['slide']), rel.get('Target')))
        t['media_part'] = media
        changes[media] = (W / 'assets' / (t['asset'] + '.png')).read_bytes()
        changes[t['slide']] = E.tostring(slide, encoding='UTF-8', xml_declaration=True, standalone=True)
        assert slide.get('show') == '0'
        assert ''.join(named(slide, 'TextBox 6').xpath('.//a:t/text()', namespaces=NS)) == t['footer']
        restored = deepcopy(slide)
        rpic = named(restored, t['shape'])
        rpic.getparent().replace(rpic, deepcopy(named(original, t['shape'])))
        assert E.tostring(restored) == E.tostring(original)
    with ZipFile(W / 'updated.pptx', 'w') as new:
        for info in old.infolist():
            new.writestr(info, changes.get(info.filename, old.read(info.filename)))

pdf = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
assert len(pdf) == 34
for t in targets:
    page = pdf[t['physical'] - 1]
    area = fitz.Rect(t['new_box_pt'])
    clear = (area | fitz.Rect(t['old_box_pt'])) + (-1, -1, 1, 1)
    page.add_redact_annot(clear, fill=(1, 1, 1))
    page.apply_redactions(images=1, graphics=1, text=0)
    page.show_pdf_page(area, thesis, t['thesis_page'] - 1, clip=fitz.Rect(t['clip']))
pdf.save(W / 'updated.pdf', garbage=4, deflate=True)
supp = fitz.open()
supp.insert_pdf(pdf, from_page=26, to_page=33)
supp.save(W / 'supplementary.pdf', garbage=4, deflate=True)

with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as old, ZipFile(W / 'updated.pptx') as new:
    assert old.namelist() == new.namelist()
    changed = [n for n in old.namelist() if old.read(n) != new.read(n)]
    assert set(changed) == set(changes)
    assert new.testzip() is None
    for t in targets:
        assert hashlib.sha256(new.read(t['media_part'])).hexdigest() == t['png_sha256']
original = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
updated = fitz.open(W / 'updated.pdf')
supp = fitz.open(W / 'supplementary.pdf')
for i in range(34):
    a, b = original[i].get_pixmap(alpha=False), updated[i].get_pixmap(alpha=False)
    t = next((t for t in targets if t['physical'] == i + 1), None)
    if t:
        diff = np.any(np.frombuffer(a.samples, np.uint8).reshape(a.height, a.width, 3) !=
                      np.frombuffer(b.samples, np.uint8).reshape(b.height, b.width, 3), axis=2)
        area = fitz.Rect(t['old_box_pt']) | fitz.Rect(t['new_box_pt'])
        diff[int(area.y0)-3:int(area.y1)+4, int(area.x0)-3:int(area.x1)+4] = False
        assert not diff.any()
        updated[i].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(
            W / ('slide_%d.png' % (i + 1)))
    else:
        assert a.samples == b.samples, i + 1
    if i >= 26:
        assert b.samples == supp[i-26].get_pixmap(alpha=False).samples
before_thesis = fitz.open(W / 'before_Thesis.pdf')
changed_thesis_pages = []
for i in range(122):
    assert before_thesis[i].get_text('dict') == thesis[i].get_text('dict')
    if before_thesis[i].get_pixmap().samples != thesis[i].get_pixmap().samples:
        changed_thesis_pages.append(i+1)
assert changed_thesis_pages == [28]
report = dict(date='2026-09-22', method='Direct crops from compiled Thesis.pdf',
              thesis_pdf_sha256=sha(W / 'thesis_build/Thesis.pdf'), targets=targets,
              changed_pptx_parts=changed, main_slides=26, hidden_backups=8,
              total_slides=34, supplementary_pages=8, thesis_pages=122,
              changed_thesis_pages=changed_thesis_pages,
              thesis_text_and_text_positions_unchanged=True,
              other_32_slides_pixel_identical=True,
              notes_videos_equations_order_sections_unchanged=True,
              affected_slides_unchanged_outside_figure=True,
              supplementary_matches_full_pdf=True)
(W / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print('Staged direct thesis figures in B6/B8. Only thesis page 28 changed.')
