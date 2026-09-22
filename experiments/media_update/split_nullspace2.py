"""Build the 2026-09-21 Nullspace2 split from an explicit pre-edit snapshot.

Usage: PYTHONPATH=<PyMuPDF path> python3 split_nullspace2.py /tmp/disturbance_video_split
The directory must contain before_* copies of the deck, PDFs and equation
catalog, plus the two prepared MP4 clips and their PNG poster frames.
Outputs are staged there; this script does not overwrite the active deck.
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

WORK = Path(sys.argv[1]).resolve()
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
}
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
ARIAL = '/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf'
NAVY = (23 / 255, 54 / 255, 93 / 255)
VIDEO_BOX = fitz.Rect(282.5, 63, 677.5, 458)
CAPTION_BOX = fitz.Rect(240, 471, 720, 499)
CLIPS = ['Nullspace2_part1_0000-0023', 'Nullspace2_part2_0023-end']
TITLES = ['Disturbance demonstration', 'Disturbance demonstration']
INTERVALS = ['00:00–00:23', '00:23–end']
CAPTIONS = ['Demonstration 2 · Part 1 · 00:00–00:23', 'Demonstration 2 · Part 2 · 00:23–end']


def tag(s):
    prefix, local = s.split(':')
    return '{' + NS[prefix] + '}' + local


def dump(r):
    return E.tostring(r, encoding='UTF-8', xml_declaration=True, standalone=True)


def relpath(path):
    return posixpath.dirname(path) + '/_rels/' + posixpath.basename(path) + '.rels'


def resolve(owner, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(owner), target))


def shape(root, name):
    matches = root.xpath('.//*[p:nvSpPr/p:cNvPr/@name=$n or p:nvPicPr/p:cNvPr/@name=$n]',
                         namespaces=NS, n=name)
    assert len(matches) == 1, name
    return matches[0]


def text(sh, value):
    nodes = sh.findall('.//a:t', NS)
    assert len(nodes) == 1
    nodes[0].text = value


def move(sh, box):
    off = sh.find('p:spPr/a:xfrm/a:off', NS)
    ext = sh.find('p:spPr/a:xfrm/a:ext', NS)
    for key, val in [('x', box.x0), ('y', box.y0)]:
        off.set(key, str(round(val * 12700)))
    for key, val in [('cx', box.width), ('cy', box.height)]:
        ext.set(key, str(round(val * 12700)))


def remove_shape(root, name):
    sh = shape(root, name)
    sh.getparent().remove(sh)


def prune_timing(root, keep):
    for node in root.findall('.//p:video', NS):
        if node.find('.//p:spTgt', NS).get('spid') not in keep:
            node.getparent().remove(node)


with ZipFile(WORK / 'before_Thesis_Defense_gg0_v3.pptx') as z:
    parts = {n: z.read(n) for n in z.namelist()}
original = dict(parts)
pres = E.fromstring(parts['ppt/presentation.xml'])
prels = E.fromstring(parts['ppt/_rels/presentation.xml.rels'])
ids = pres.find('p:sldIdLst', NS)
lookup = {r.get('Id'): resolve('ppt/presentation.xml', r.get('Target')) for r in prels}
old_paths = [lookup[s.get(tag('r:id'))] for s in ids]
assert len(old_paths) == 34
assert old_paths[18] == 'ppt/slides/slide13.xml'
backup_path = old_paths[24]
assert backup_path == 'ppt/slides/slide26.xml'
template = E.fromstring(parts[backup_path])
template_rels = E.fromstring(parts[relpath(backup_path)])
assert ''.join(shape(template, 'Slide title').xpath('.//a:t/text()', namespaces=NS)) == 'Disturbance demonstration'

# Demonstration 1 remains in B2, centred at its existing size.
backup = deepcopy(template)
remove_shape(backup, 'Nullspace2 video')
remove_shape(backup, 'Nullspace2 label')
move(shape(backup, 'Nullspace1 video'), VIDEO_BOX)
move(shape(backup, 'Nullspace1 label'), CAPTION_BOX)
prune_timing(backup, {'8'})
backup_rels = deepcopy(template_rels)
for r in list(backup_rels):
    if r.get('Id').startswith('rIdNullspace2'):
        backup_rels.remove(r)
parts[backup_path] = dump(backup)
parts[relpath(backup_path)] = dump(backup_rels)

max_slide = max(int(re.search(r'slide(\d+)\.xml$', n)[1]) for n in parts
                if re.fullmatch(r'ppt/slides/slide\d+\.xml', n))
max_note = max(int(re.search(r'notesSlide(\d+)\.xml$', n)[1]) for n in parts
               if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n))
max_sid = max(int(n.get('id')) for n in ids)
ct = E.fromstring(parts['[Content_Types].xml'])
sections = pres.findall('.//p14:section', NS)
null_section = next(s for s in sections if s.get('name') == 'Null-space control and experiments')
null_ids = null_section.find('p14:sldIdLst', NS)
note_rel = next(r for r in template_rels if r.get('Type').endswith('/notesSlide'))
template_note = resolve(backup_path, note_rel.get('Target'))
new_paths = []

for i, basename in enumerate(CLIPS):
    path = 'ppt/slides/slide%d.xml' % (max_slide + i + 1)
    note_path = 'ppt/notesSlides/notesSlide%d.xml' % (max_note + i + 1)
    sid = str(max_sid + i + 1)
    rid = 'rIdNullspace2Part%d' % (i + 1)
    slide = deepcopy(template)
    slide.attrib.pop('show', None)
    remove_shape(slide, 'Nullspace1 video')
    remove_shape(slide, 'Nullspace1 label')
    text(shape(slide, 'Slide title'), TITLES[i])
    text(shape(slide, 'Nullspace2 label'), CAPTIONS[i])
    video = shape(slide, 'Nullspace2 video')
    props = video.find('p:nvPicPr/p:cNvPr', NS)
    props.set('name', 'Nullspace2 part %d video' % (i + 1))
    props.set('descr', 'Nullspace2.mp4, original interval %s. Upright video with audio. Click to play.' % INTERVALS[i])
    move(video, VIDEO_BOX)
    move(shape(slide, 'Nullspace2 label'), CAPTION_BOX)
    prune_timing(slide, {'22'})
    # Cloned shapes receive no duplicated creation IDs.
    for ext in slide.xpath('//*[local-name()="creationId"]'):
        ext.getparent().remove(ext)
    rels = deepcopy(template_rels)
    for r in list(rels):
        if r.get('Id') in {'rId1', 'rId2', 'rId6'}:
            rels.remove(r)
        elif r.get('Id') in {'rIdNullspace2Video', 'rIdNullspace2Media'}:
            r.set('Target', '../media/' + basename + '.mp4')
        elif r.get('Id') == 'rIdNullspace2Poster':
            r.set('Target', '../media/' + basename + '_poster.png')
        elif r.get('Type').endswith('/notesSlide'):
            r.set('Target', '../notesSlides/' + posixpath.basename(note_path))
    # Existing notes are frozen. The new slides receive empty notes.
    note = E.fromstring(parts[template_note])
    for body in note.findall('.//p:txBody', NS):
        for paragraph in body.findall('a:p', NS):
            body.remove(paragraph)
        E.SubElement(body, tag('a:p'))
    nr = E.fromstring(parts[relpath(template_note)])
    next(r for r in nr if r.get('Type').endswith('/slide')).set('Target', '../slides/' + posixpath.basename(path))
    parts[path], parts[relpath(path)] = dump(slide), dump(rels)
    parts[note_path], parts[relpath(note_path)] = dump(note), dump(nr)
    parts['ppt/media/' + basename + '.mp4'] = (WORK / (basename + '.mp4')).read_bytes()
    parts['ppt/media/' + basename + '_poster.png'] = (WORK / (basename + '_poster.png')).read_bytes()
    E.SubElement(prels, '{' + PKG + '}Relationship', Id=rid, Type=NS['r'] + '/slide', Target='slides/' + posixpath.basename(path))
    sld_id = E.Element(tag('p:sldId'), id=sid)
    sld_id.set(tag('r:id'), rid)
    ids.insert(18 + i, sld_id)
    null_ids.insert(1 + i, E.Element(tag('p14:sldId'), id=sid))
    for owner, kind in [(path, 'slide'), (note_path, 'notesSlide')]:
        E.SubElement(ct, '{' + CT + '}Override', PartName='/' + owner,
                     ContentType='application/vnd.openxmlformats-officedocument.presentationml.' + kind + '+xml')
    new_paths.append(path)

# Remove only the now unreferenced full-length embedded copy. Its source file is retained.
removed_parts = ['ppt/media/Nullspace2_presentation.mp4', 'ppt/media/Nullspace2_poster.png']
for name in removed_parts:
    del parts[name]
for node in list(ct):
    if node.get('PartName', '').lstrip('/') in removed_parts:
        ct.remove(node)

ordered = old_paths[:18] + new_paths + old_paths[18:]
footers = {}
order = []
for i, path in enumerate(ordered):
    root = E.fromstring(parts[path])
    if i:
        label = str(i) if i < 25 else 'B' + str(i - 24)
        sh = shape(root, 'TextBox 6')
        if ''.join(sh.xpath('.//a:t/text()', namespaces=NS)) != label:
            text(sh, label)
            parts[path] = dump(root)
            footers[i] = label
    order.append({'physical': i + 1, 'path': path,
                  'title': ''.join(shape(root, 'Slide title').xpath('.//a:t/text()', namespaces=NS)) if i else 'Master Thesis Presentation',
                  'footer': (str(i) if i < 25 else 'B' + str(i - 24)) if i else '',
                  'hidden': i >= 25})

# Portable Overview maintenance: regenerate its six rows from native sections.
chapters = [s.get('name') for s in sections if s.get('name') != 'Backup']
overview = E.fromstring(parts[old_paths[3]])
old_overview = dump(overview)
for i, name in enumerate(chapters, 1):
    text(shape(overview, 'Overview number %d' % i), '%d.' % i)
    text(shape(overview, 'Overview item %d' % i), name)
if dump(overview) != old_overview:
    parts[old_paths[3]] = dump(overview)
parts['ppt/presentation.xml'] = dump(pres)
parts['ppt/_rels/presentation.xml.rels'] = dump(prels)
parts['[Content_Types].xml'] = dump(ct)
app = E.fromstring(parts['docProps/app.xml'])
for key, value in [('Slides', '36'), ('Notes', '36'), ('HiddenSlides', '11'), ('MMClips', '4')]:
    app.xpath('//*[local-name()=$key]', key=key)[0].text = value
app.xpath('//*[local-name()="HeadingPairs"]//*[local-name()="i4"]')[-1].text = '36'
vector = app.xpath('//*[local-name()="TitlesOfParts"]/*')[0]
sample = deepcopy(vector[3])
for n in list(vector)[3:]:
    vector.remove(n)
for entry in order:
    n = deepcopy(sample)
    n.text = entry['title']
    vector.append(n)
vector.set('size', str(len(vector)))
parts['docProps/app.xml'] = dump(app)

catalog = json.loads((WORK / 'before_native_equations.json').read_text())
for equation in catalog:
    equation['slide'] = ordered.index(old_paths[equation['slide'] - 1]) + 1
(WORK / 'updated_native_equations.json').write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n')
with ZipFile(WORK / 'before_Thesis_Defense_gg0_v3.pptx') as z, ZipFile(WORK / 'updated.pptx', 'w', compression=ZIP_DEFLATED) as out:
    for info in z.infolist():
        if info.filename in parts:
            out.writestr(info, parts[info.filename])
    for name in sorted(parts.keys() - original.keys()):
        out.writestr(name, parts[name])

# Preserve the original PDF pages and compose the three changed video pages.
source = fitz.open(WORK / 'before_Thesis_Defense_gg0_v3.pdf')
pdf = fitz.open()
page_map = list(range(18)) + [24, 24] + list(range(18, 34))
for old in page_map:
    pdf.insert_pdf(source, from_page=old, to_page=old)
font = fitz.Font(fontfile=ARIAL)
bold_xref = next(f[0] for f in source[24].get_fonts() if 'Arial-Bold' in f[3])
bold = source.extract_font(bold_xref)[3]


def clear(page, rect):
    page.add_redact_annot(rect, fill=(1, 1, 1))
    page.apply_redactions(images=2, graphics=1, text=0)


def centre_caption(page, value):
    page.insert_font(fontname='ArialVideoSplit', fontfile=ARIAL)
    x = 480 - font.text_length(value, fontsize=19) / 2
    page.insert_text((x, 490), value, fontname='ArialVideoSplit', fontsize=19, color=NAVY)


for i in [18, 19, 26]:
    page = pdf[i]
    clear(page, fitz.Rect(40, 55, 920, 500))
    if i < 20:
        part = i - 18
        clear(page, fitz.Rect(38, 16, 920, 45))
        page.insert_font(fontname='ArialVideoSplitBold', fontbuffer=bold)
        page.insert_text((44.64, 39.36), TITLES[part], fontname='ArialVideoSplitBold', fontsize=17.544, color=NAVY)
        poster = (WORK / (CLIPS[part] + '_poster.png')).read_bytes()
        caption = CAPTIONS[part]
    else:
        poster = original['ppt/media/Nullspace1_poster.png']
        caption = 'Null-space demonstration 1'
    page.insert_image(VIDEO_BOX, stream=poster)
    centre_caption(page, caption)

for i, label in footers.items():
    page = pdf[i]
    stream = b'\n'.join(pdf.xref_stream(x) for x in page.get_contents())
    removed = []

    def strip(match):
        obj = match.group()
        tm = re.search(rb'1\s+0\s+0\s+1\s+([\d.]+)\s+([\d.]+)\s+Tm', obj)
        if tm and float(tm[1]) > 900 and 15 < float(tm[2]) < 35 and re.search(rb'8\.04\s+Tf', obj):
            removed.append(obj)
            return b''
        return obj

    stream = re.sub(rb'\bBT\b.*?\bET\b', strip, stream, flags=re.S)
    assert len(removed) == 1, (i, len(removed))
    xref = pdf.get_new_xref()
    pdf.update_object(xref, '<<>>')
    pdf.update_stream(xref, stream)
    page.set_contents(xref)
    page.insert_font(fontname='ArialVideoSplit', fontfile=ARIAL)
    page.insert_text((921.8 - font.text_length(label, fontsize=8.04), 513.48), label,
                     fontname='ArialVideoSplit', fontsize=8.04, color=(.412, .412, .412))
pdf.save(WORK / 'updated.pdf', garbage=4, deflate=True)
supp = fitz.open()
supp.insert_pdf(pdf, from_page=25, to_page=35)
supp.save(WORK / 'supplementary.pdf', garbage=4, deflate=True)

# Structural verification, including preservation of all original notes.
assert [n.get('id') for n in ids] == [n.get('id') for s in sections for n in s.find('p14:sldIdLst', NS)]
assert len(catalog) == 29
for path in original:
    if path.startswith('ppt/notesSlides/'):
        assert parts[path] == original[path]
for entry in order:
    root = E.fromstring(parts[entry['path']])
    assert (root.get('show') == '0') == entry['hidden']
    for equation in [e for e in catalog if e['slide'] == entry['physical']]:
        assert shape(root, equation['shape']).find('.//m:oMath', NS) is not None
for name in parts:
    if not name.endswith('.rels'):
        continue
    owner = name.replace('/_rels/', '/')[:-5]
    if name == '_rels/.rels':
        owner = ''
    for r in E.fromstring(parts[name]):
        if r.get('TargetMode') != 'External':
            target = resolve(owner, r.get('Target')).lstrip('/')
            assert target in parts, (name, target)
for name in old_paths:
    if name == backup_path:
        continue
    before, after = E.fromstring(original[name]), E.fromstring(parts[name])
    for root in [before, after]:
        for t in root.xpath('.//p:sp[p:nvSpPr/p:cNvPr[@name="TextBox 6"]]//a:t', namespaces=NS):
            t.text = 'FOOTER'
    assert E.tostring(before) == E.tostring(after), name
report = {
    'date': '2026-09-21', 'source_video': 'Video/Nullspace2_presentation.mp4',
    'cut_seconds': 23, 'main_slides': 25, 'hidden_backups': 11, 'total_slides': 36,
    'supplementary_pages': 11, 'slide_order': order, 'page_map_zero_based': page_map,
    'changed_video_pages': [19, 20, 27], 'changed_footer_pages': [i + 1 for i in footers],
    'native_equation_count': len(catalog), 'existing_notes_unchanged': True,
    'other_slide_contents_unchanged_except_footer': True, 'overview_chapters': chapters,
    'all_internal_relationships_resolve': True,
    'removed_embedded_parts': removed_parts,
    'changed_existing_parts': [n for n in original if n in parts and parts[n] != original[n]],
    'new_parts': sorted(parts.keys() - original.keys()),
    'pdf_method': 'Original PowerPoint PDF pages retained, with video posters, captions, titles and affected footers updated.',
}
(WORK / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Staged 36-slide deck: 25 main slides, 11 hidden backups. Native equations and existing notes preserved.')
