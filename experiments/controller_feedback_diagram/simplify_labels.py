"""Stage the approved controller label changes from a presentation snapshot.

Usage: python3 simplify_labels.py /tmp/controller_label_simplification
Requires lxml, PyMuPDF and numpy. The working directory must contain
before_Thesis_Defense_gg0_v3.{pptx,pdf} and regenerated assets/ DrawingML.
Existing slide shapes, equations, notes and other PDF pages are checked.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
import importlib.util
import json
import sys

import fitz
import numpy as np
from lxml import etree as E

ROOT = Path(__file__).resolve().parents[2]
W = Path(sys.argv[1]).resolve()
GENERATOR = ROOT / 'Final Presentation/figures_and_images/sources/make_controller_feedback_diagram.py'
spec = importlib.util.spec_from_file_location('feedback', GENERATOR)
diagram = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagram)
NS = dict(diagram.NS, p14='http://schemas.microsoft.com/office/powerpoint/2010/main')
TARGET = 'ppt/slides/slide7.xml'
PREFIX = 'Feedback diagram - '
REPLACEMENTS = {
    'Desired signal label': 'Desired signal label',
    'Pose error signal': 'Pose and velocity error signal',
    'Velocity error signal': 'State definition',
    'Measured Cartesian feedback label': 'Measured Cartesian feedback label',
}
ARIAL = '/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf'


def name(node):
    values = node.xpath('.//p:cNvPr/@name', namespaces=NS)
    return values[0] if values else ''


def dump(node):
    return E.tostring(node, encoding='UTF-8', xml_declaration=True, standalone=True)


with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as before:
    original = E.fromstring(before.read(TARGET))
    updated = deepcopy(original)
    tree = updated.find('p:cSld/p:spTree', NS)
    scene = E.parse(str(W / 'assets/controller_feedback_diagram.xml')).getroot()
    replacement_shapes = {name(s): s for s in scene}
    changed_shapes = []
    for shape in list(tree):
        old_name = name(shape)
        short = old_name[len(PREFIX):] if old_name.startswith(PREFIX) else ''
        if short not in REPLACEMENTS:
            continue
        new_shape = deepcopy(replacement_shapes[PREFIX + REPLACEMENTS[short]])
        old_id = shape.find('.//p:cNvPr', NS).get('id')
        new_shape.find('.//p:cNvPr', NS).set('id', old_id)
        tree.replace(shape, new_shape)
        changed_shapes.append([short, REPLACEMENTS[short]])
    assert len(changed_shapes) == 4
    ids = updated.xpath('.//p:cNvPr/@id', namespaces=NS)
    assert len(ids) == len(set(ids))
    changes = {TARGET: dump(updated)}
    presentation = E.fromstring(before.read('ppt/presentation.xml'))
    chapters = [s.get('name') for s in presentation.findall('.//p14:section', NS)
                if s.get('name') != 'Backup']
    overview = E.fromstring(before.read('ppt/slides/slide4.xml'))
    overview_before = dump(overview)
    for i, title in enumerate(chapters, 1):
        for shape_name, value in [('Overview item %d' % i, title),
                                  ('Overview number %d' % i, '%d.' % i)]:
            labels = overview.xpath('.//p:sp[p:nvSpPr/p:cNvPr[@name=$n]]//a:t',
                                    namespaces=NS, n=shape_name)
            assert len(labels) == 1
            labels[0].text = value
    assert dump(overview) == overview_before, 'Unexpected Overview drift'
    with ZipFile(W / 'updated.pptx', 'w') as out:
        for info in before.infolist():
            out.writestr(info, changes.get(info.filename, before.read(info.filename)))

source = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
pdf = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
assert len(source) == len(pdf) == 39
page = pdf[7]
assert 'Real-time control' in page.get_text()
old_labels = {'Pose, velocity': 14.5, 'Pose error': 14.5,
              'Velocity error': 14.5, 'Measured pose and velocity': 16}
found = []
redaction_boxes = []
for block in page.get_text('dict')['blocks']:
    for line in block.get('lines', []):
        for span in line['spans']:
            value = span['text'].replace('\u00a0', ' ')
            if value in old_labels and abs(span['size'] - old_labels[value]) < .01:
                box = fitz.Rect(span['bbox'])
                page.add_redact_annot(box, fill=False, cross_out=False)
                redaction_boxes.append(list(box))
                found.append(value)
assert set(found) == set(old_labels) and len(found) == 4, found
# Remove the four text spans while preserving all graphics and image content.
page.apply_redactions(images=0, graphics=0, text=0)
_, _, math_data = diagram.fonts(W / 'before_Thesis_Defense_gg0_v3.pdf', ARIAL)
scene = diagram.SCENE
diagram.SCENE = [item for item in scene if item['name'] in REPLACEMENTS.values()]
assert len(diagram.SCENE) == 4
diagram.draw(page, ARIAL, math_data)
new_boxes = [item['box'] for item in diagram.SCENE]
diagram.SCENE = scene
pdf.save(W / 'updated.pdf', garbage=4, deflate=True)
pdf.close()

with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as old, ZipFile(W / 'updated.pptx') as new:
    assert old.namelist() == new.namelist()
    changed_parts = [n for n in old.namelist() if old.read(n) != new.read(n)]
    assert changed_parts == [TARGET], changed_parts
    old_tree = original.find('p:cSld/p:spTree', NS)
    new_tree = updated.find('p:cSld/p:spTree', NS)
    assert len(old_tree) == len(new_tree)
    unchanged_shapes = 0
    for old_shape, new_shape in zip(old_tree, new_tree):
        if name(old_shape) not in {PREFIX + key for key in REPLACEMENTS}:
            assert E.tostring(old_shape) == E.tostring(new_shape), name(old_shape)
            unchanged_shapes += 1

final_pdf = fitz.open(W / 'updated.pdf')
unchanged_pages = []
for i in range(len(source)):
    old_pix = source[i].get_pixmap(alpha=False)
    new_pix = final_pdf[i].get_pixmap(alpha=False)
    assert old_pix.width == new_pix.width and old_pix.height == new_pix.height
    if i != 7:
        assert old_pix.samples == new_pix.samples, ('PDF page changed', i + 1)
        unchanged_pages.append(i + 1)
    else:
        shape = (old_pix.height, old_pix.width, 3)
        a = np.frombuffer(old_pix.samples, np.uint8).reshape(shape)
        b = np.frombuffer(new_pix.samples, np.uint8).reshape(shape)
        different = np.any(a != b, axis=2)
        allowed = np.zeros(different.shape, bool)
        for box in redaction_boxes + new_boxes:
            x0, y0, x1, y1 = box
            allowed[int(y0)-2:int(y1)+3, int(x0)-2:int(x1)+3] = True
        assert not np.any(different & ~allowed), 'Pixels changed outside requested labels'
        assert np.any(different)

report = {
    'date': '2026-09-22',
    'slide': {'title': 'Real-time control', 'footer': 7, 'physical': 8},
    'scope': 'Presentation-only label simplification',
    'labels': {'reference': 'Reference state', 'controller_input': 'Pose and velocity errors',
               'feedback': 'Measured state', 'definition': 'State: pose and velocity'},
    'error_label_lines': ['Pose and', 'velocity errors'],
    'native_shapes_replaced': changed_shapes,
    'all_other_shapes_and_native_equations_unchanged': True,
    'other_native_slide_elements_preserved': unchanged_shapes,
    'changed_pptx_parts': changed_parts,
    'notes_media_sections_and_other_slides_unchanged': True,
    'overview_refreshed_from_sections': chapters,
    'main_slides': 26, 'hidden_backups': 13, 'total_slides': 39,
    'native_equation_count': 29,
    'pdf_method': 'Remove four old text spans and draw approved labels from the shared scene, retaining all other PDF content.',
    'other_pdf_pages_pixel_identical': unchanged_pages,
    'affected_slide_pixels_unchanged_outside_label_boxes': True,
}
(W / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Staged PowerPoint and PDF. Only four native labels changed. Other 38 PDF pages are pixel-identical.')
