"""Append the corrected former Motivation figure as hidden backup B13.

Usage: python3 add_surface_entry_backup.py /tmp/surface_entry_correction
Requires lxml/PyMuPDF, before_* deck/PDF snapshots and corrected figure assets
under figure/. Outputs are staged, leaving active documents untouched.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import posixpath
import re
import sys

import fitz
from lxml import etree as E

W = Path(sys.argv[1]).resolve()
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
ARIAL = '/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf'
TITLE = 'Sources of angular offset'


def tag(s):
    a, b = s.split(':')
    return '{' + NS[a] + '}' + b


def dump(root):
    return E.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)


def relpath(path):
    return posixpath.dirname(path) + '/_rels/' + posixpath.basename(path) + '.rels'


def resolve(owner, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(owner), target))


def shape(root, name):
    found = root.xpath('.//*[p:nvSpPr/p:cNvPr/@name=$n or p:nvPicPr/p:cNvPr/@name=$n]', namespaces=NS, n=name)
    assert len(found) == 1
    return found[0]


def settext(sh, value):
    ts = sh.findall('.//a:t', NS)
    assert len(ts) == 1
    ts[0].text = value


with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as z:
    parts = {n: z.read(n) for n in z.namelist()}
original = dict(parts)
pres = E.fromstring(parts['ppt/presentation.xml'])
prels = E.fromstring(parts['ppt/_rels/presentation.xml.rels'])
ids = pres.find('p:sldIdLst', NS)
lookup = {r.get('Id'): resolve('ppt/presentation.xml', r.get('Target')) for r in prels}
old_paths = [lookup[s.get(tag('r:id'))] for s in ids]
assert len(old_paths) == 38
template_path = old_paths[-1]
assert template_path == 'ppt/slides/slide39.xml'
slide = E.fromstring(parts[template_path])
settext(shape(slide, 'Slide title'), TITLE)
settext(shape(slide, 'TextBox 6'), 'B13')
assert slide.get('show') == '0'
picture = shape(slide, 'Opposing moment video')
props = picture.find('p:nvPicPr/p:cNvPr', NS)
props.set('name', 'Surface entry concept')
props.set('descr', 'Sources of angular offset at surface entry. Configured surface: solid red. Physical surface: solid blue. Desired tool orientation: dashed black. Achieved tool orientation: solid green. Matching thesis Figure 1.1.')
for child in list(props):
    props.remove(child)
nv = picture.find('p:nvPicPr/p:nvPr', NS)
for child in list(nv):
    nv.remove(child)
timing = slide.find('p:timing', NS)
if timing is not None:
    slide.remove(timing)
figure = fitz.open(W / 'figure/thesis_figure_1_1.pdf')
width = 820
height = width * figure[0].rect.height / figure[0].rect.width
box = fitz.Rect(70, 275 - height / 2, 890, 275 + height / 2)
assert 55 < box.y0 and box.y1 < 495
off = picture.find('p:spPr/a:xfrm/a:off', NS)
ext = picture.find('p:spPr/a:xfrm/a:ext', NS)
for key, val in [('x', box.x0), ('y', box.y0)]:
    off.set(key, str(round(val * 12700)))
for key, val in [('cx', box.width), ('cy', box.height)]:
    ext.set(key, str(round(val * 12700)))
picture.find('p:blipFill/a:blip', NS).set(tag('r:embed'), 'rIdSurfaceEntryFigure')
new_num = max(int(re.search(r'slide(\d+)\.xml$', n)[1]) for n in parts if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)) + 1
new_path = 'ppt/slides/slide%d.xml' % new_num
new_note_num = max(int(re.search(r'notesSlide(\d+)\.xml$', n)[1]) for n in parts if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)) + 1
new_note_path = 'ppt/notesSlides/notesSlide%d.xml' % new_note_num
rels = E.fromstring(parts[relpath(template_path)])
old_note = next(r for r in rels if r.get('Type').endswith('/notesSlide'))
old_note_path = resolve(template_path, old_note.get('Target'))
old_note.set('Target', '../notesSlides/' + posixpath.basename(new_note_path))
for r in list(rels):
    if r.get('Id').startswith('rIdNullspace2'):
        rels.remove(r)
image_part = 'ppt/media/thesis_figure_1_1_corrected.png'
E.SubElement(rels, '{' + PKG + '}Relationship', Id='rIdSurfaceEntryFigure', Type=NS['r'] + '/image', Target='../media/' + posixpath.basename(image_part))
notes = E.fromstring(parts[old_note_path])
for body in notes.findall('.//p:txBody', NS):
    for paragraph in body.findall('a:p', NS):
        body.remove(paragraph)
    E.SubElement(body, tag('a:p'))
note_rels = E.fromstring(parts[relpath(old_note_path)])
next(r for r in note_rels if r.get('Type').endswith('/slide')).set('Target', '../slides/' + posixpath.basename(new_path))
parts[new_path], parts[relpath(new_path)] = dump(slide), dump(rels)
parts[new_note_path], parts[relpath(new_note_path)] = dump(notes), dump(note_rels)
parts[image_part] = (W / 'figure/thesis_figure_1_1.png').read_bytes()
sid = str(max(int(s.get('id')) for s in ids) + 1)
rid = 'rIdSurfaceEntryBackup'
E.SubElement(prels, '{' + PKG + '}Relationship', Id=rid, Type=NS['r'] + '/slide', Target='slides/' + posixpath.basename(new_path))
sld = E.SubElement(ids, tag('p:sldId'), id=sid)
sld.set(tag('r:id'), rid)
sections = pres.findall('.//p14:section', NS)
backup = next(s for s in sections if s.get('name') == 'Backup')
E.SubElement(backup.find('p14:sldIdLst', NS), tag('p14:sldId'), id=sid)
chapters = [s.get('name') for s in sections if s.get('name') != 'Backup']
overview = E.fromstring(parts[old_paths[3]])
ov_before = dump(overview)
for i, chapter in enumerate(chapters, 1):
    settext(shape(overview, 'Overview number %d' % i), '%d.' % i)
    settext(shape(overview, 'Overview item %d' % i), chapter)
if dump(overview) != ov_before:
    parts[old_paths[3]] = dump(overview)
parts['ppt/presentation.xml'], parts['ppt/_rels/presentation.xml.rels'] = dump(pres), dump(prels)
ct = E.fromstring(parts['[Content_Types].xml'])
for owner, kind in [(new_path, 'slide'), (new_note_path, 'notesSlide')]:
    E.SubElement(ct, '{' + CT + '}Override', PartName='/' + owner, ContentType='application/vnd.openxmlformats-officedocument.presentationml.' + kind + '+xml')
parts['[Content_Types].xml'] = dump(ct)
app = E.fromstring(parts['docProps/app.xml'])
for key, value in [('Slides', '39'), ('Notes', '39'), ('HiddenSlides', '13')]:
    app.xpath('//*[local-name()=$k]', k=key)[0].text = value
app.xpath('//*[local-name()="HeadingPairs"]//*[local-name()="i4"]')[-1].text = '39'
vector = app.xpath('//*[local-name()="TitlesOfParts"]/*')[0]
n = deepcopy(vector[-1])
n.text = TITLE
vector.append(n)
vector.set('size', str(len(vector)))
parts['docProps/app.xml'] = dump(app)
with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as zin, ZipFile(W / 'updated.pptx', 'w', compression=ZIP_DEFLATED) as out:
    for info in zin.infolist():
        out.writestr(info, parts[info.filename])
    for name in sorted(parts.keys() - original.keys()):
        out.writestr(name, parts[name])

source_pdf = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
pdf = fitz.open()
pdf.insert_pdf(source_pdf)
pdf.insert_pdf(source_pdf, from_page=37, to_page=37)
page = pdf[38]
for rect in [fitz.Rect(38, 16, 920, 45), fitz.Rect(40, 55, 920, 500), fitz.Rect(899, 501, 926, 521)]:
    page.add_redact_annot(rect, fill=(1, 1, 1))
page.apply_redactions(images=2, graphics=1, text=0)
bold_xref = next(f[0] for f in source_pdf[37].get_fonts() if 'Arial-Bold' in f[3])
bold_buf = source_pdf.extract_font(bold_xref)[3]
assert all(fitz.Font(fontbuffer=bold_buf).has_glyph(ord(c)) for c in TITLE)
page.insert_font(fontname='ArialSurfaceEntryBold', fontbuffer=bold_buf)
page.insert_text((44.64, 39.36), TITLE, fontname='ArialSurfaceEntryBold', fontsize=17.544, color=(23 / 255, 54 / 255, 93 / 255))
font = fitz.Font(fontfile=ARIAL)
page.insert_font(fontname='ArialSurfaceEntry', fontfile=ARIAL)
page.insert_text((921.8 - font.text_length('B13', fontsize=8.04), 513.48), 'B13', fontname='ArialSurfaceEntry', fontsize=8.04, color=(.412, .412, .412))
page.show_pdf_page(box, figure, 0)
pdf.save(W / 'updated.pdf', garbage=4, deflate=True)
supp = fitz.open()
supp.insert_pdf(pdf, from_page=26, to_page=38)
supp.save(W / 'supplementary.pdf', garbage=4, deflate=True)

assert [s.get('id') for s in ids] == [s.get('id') for section in sections for s in section.find('p14:sldIdLst', NS)]
for name in original:
    if name.startswith(('ppt/slides/', 'ppt/notesSlides/', 'ppt/media/')):
        assert parts[name] == original[name], name
for name in parts:
    if not name.endswith('.rels'):
        continue
    owner = name.replace('/_rels/', '/')[:-5] if name != '_rels/.rels' else ''
    for r in E.fromstring(parts[name]):
        if r.get('TargetMode') != 'External':
            assert resolve(owner, r.get('Target')).lstrip('/') in parts
report = {
    'date': '2026-09-22', 'new_slide': {'title': TITLE, 'physical': 39, 'footer': 'B13', 'path': new_path, 'hidden': True},
    'main_slides': 26, 'hidden_backups': 13, 'total_slides': 39, 'supplementary_pages': 13,
    'figure_box_pt': list(box), 'figure_png_sha256': hashlib.sha256(parts[image_part]).hexdigest(),
    'all_existing_slides_notes_and_media_unchanged': True, 'all_relationships_resolve': True,
    'new_slide_notes_empty': True, 'overview_chapters': chapters,
    'changed_existing_parts': [n for n in original if parts[n] != original[n]],
    'new_parts': sorted(parts.keys() - original.keys()),
    'pdf_method': 'All 38 existing PowerPoint PDF pages retained. New backup uses the corrected shared vector figure.',
}
(W / 'presentation_verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print('Staged corrected figure as hidden B13: 26 main slides, 13 backups, 39 PDF pages.')
