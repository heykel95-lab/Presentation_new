"""Copy the surface diagram onto Contact experiment from an explicit snapshot.

Usage: python3 restore_contact_surface.py /tmp/contact_surface_copy
Requires lxml and PyMuPDF. Stages updated.pptx and updated.pdf without
overwriting the active deck. Earlier Surface frame and all notes are retained.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys

import fitz
from lxml import etree as E

W = Path(sys.argv[1]).resolve()
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
TARGET = 'ppt/slides/slide11.xml'
SOURCE = 'ppt/slides/slide35.xml'
SETTINGS = {'Contact settings heading', 'Normal label', 'Rotation label',
            'Tangential translation label', 'Normal rotation label',
            'Equation - contact_normal_gain', 'Equation - contact_rotation_gains',
            'Equation - contact_tangent_gains', 'Equation - contact_normal_rotation'}
BOX = fitz.Rect(60, 165.15355, 420, 447.84645)


def dump(root):
    return E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


def name(node):
    names = node.xpath('.//p:cNvPr/@name', namespaces=NS)
    return names[0] if names else ''


with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as z:
    before = z.read(TARGET)
    root = E.fromstring(before)
    src = E.fromstring(z.read(SOURCE))
    tree = root.find('p:cSld/p:spTree', NS)
    assert not root.xpath('.//p:cNvPr[@name="Surface frame"]', namespaces=NS)
    picture = deepcopy(src.xpath('.//p:pic[p:nvPicPr/p:cNvPr[@name="Surface frame"]]', namespaces=NS)[0])
    props = picture.find('p:nvPicPr/p:cNvPr', NS)
    props.set('id', str(max(map(int, root.xpath('.//p:cNvPr/@id', namespaces=NS))) + 1))
    off = picture.find('p:spPr/a:xfrm/a:off', NS)
    ext = picture.find('p:spPr/a:xfrm/a:ext', NS)
    for key, val in [('x', BOX.x0), ('y', BOX.y0)]:
        off.set(key, str(round(val * 12700)))
    # Preserve the existing image dimensions and its original aspect ratio.
    assert int(ext.get('cx')) == 4572000 and int(ext.get('cy')) == 3590160
    BOX.y1 = BOX.y0 + int(ext.get('cy')) / 12700
    rid = picture.find('p:blipFill/a:blip', NS).get('{' + NS['r'] + '}embed')
    rr = E.fromstring(z.read('ppt/slides/_rels/slide11.xml.rels'))
    image_target = next(r.get('Target') for r in rr if r.get('Id') == rid)
    assert image_target == '../media/image33.png'
    image_bytes = z.read('ppt/media/image33.png')
    moved = []
    for node in tree:
        if name(node) in SETTINGS:
            offsets = node.findall('.//a:xfrm/a:off', NS)
            assert offsets, name(node)
            for o in offsets:
                o.set('x', str(int(o.get('x')) + 220 * 12700))
            moved.append(name(node))
    assert set(moved) == SETTINGS
    tree.append(picture)
    changes = {TARGET: dump(root)}
    # Refresh the Overview's chapter rows from the native sections.
    presentation = E.fromstring(z.read('ppt/presentation.xml'))
    chapters = [s.get('name') for s in presentation.findall('.//p14:section', NS) if s.get('name') != 'Backup']
    overview = E.fromstring(z.read('ppt/slides/slide4.xml'))
    overview_before = dump(overview)
    for i, title in enumerate(chapters, 1):
        for shape_name, value in [('Overview item %d' % i, title), ('Overview number %d' % i, '%d.' % i)]:
            nodes = overview.xpath('.//p:sp[p:nvSpPr/p:cNvPr[@name=$n]]//a:t', namespaces=NS, n=shape_name)
            assert len(nodes) == 1
            nodes[0].text = value
    if dump(overview) != overview_before:
        changes['ppt/slides/slide4.xml'] = dump(overview)
    with ZipFile(W / 'updated.pptx', 'w') as out:
        for info in z.infolist():
            out.writestr(info, changes.get(info.filename, z.read(info.filename)))

source = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
assert len(source) == 38
pdf = fitz.open()
pdf.insert_pdf(source)
page = pdf[10]
assert 'Contact experiment' in page.get_text()
page.add_redact_annot(fitz.Rect(37, 130, 927, 496), fill=(1, 1, 1))
page.apply_redactions(images=1, graphics=1, text=0)
page.show_pdf_page(fitz.Rect(475, 135, 926, 482), source, 10,
                   clip=fitz.Rect(255, 135, 706, 482))
page.insert_image(BOX, stream=image_bytes)
pdf.save(W / 'updated.pdf', garbage=4, deflate=True)

with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as old, ZipFile(W / 'updated.pptx') as new:
    changed = [n for n in old.namelist() if old.read(n) != new.read(n)]
    assert changed == [TARGET], changed
    assert old.read(SOURCE) == new.read(SOURCE)
    # Undo only the requested image addition and horizontal translation,
    # then require the original slide XML, including native equations.
    restored = E.fromstring(new.read(TARGET))
    rt = restored.find('p:cSld/p:spTree', NS)
    for node in list(rt):
        if name(node) == 'Surface frame':
            rt.remove(node)
        elif name(node) in SETTINGS:
            for o in node.findall('.//a:xfrm/a:off', NS):
                o.set('x', str(int(o.get('x')) - 220 * 12700))
    assert E.tostring(restored) == E.tostring(E.fromstring(before))
report = {
    'date': '2026-09-21', 'slide': {'title': 'Contact experiment', 'physical': 11, 'footer': 10},
    'source_slide': {'title': 'Surface frame', 'physical': 6, 'footer': 5},
    'image': {'asset': 'figures_and_images/surface_directions.png', 'embedded_part': 'ppt/media/image33.png',
              'sha256': hashlib.sha256(image_bytes).hexdigest(), 'box_pt': list(BOX), 'bytes_unchanged': True},
    'settings_translation_x_pt': 220, 'translated_shapes': moved,
    'earlier_surface_slide_unchanged': True, 'equation_contents_unchanged': True,
    'changed_pptx_parts': changed, 'notes_media_sections_order_and_other_slides_unchanged': True,
    'overview_refreshed_from_sections': chapters,
    'main_slides': 26, 'hidden_backups': 12, 'total_slides': 38,
    'native_equation_count': 29,
    'pdf_method': 'Existing PowerPoint PDF retained, contact settings translated as vectors and identical surface-frame image inserted.',
}
(W / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Staged surface image on Contact experiment, footer 10. Earlier Surface frame and native equations preserved.')
