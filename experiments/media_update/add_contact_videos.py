"""Stage the requested contact videos from a 36-slide pre-edit snapshot.

Usage: python3 add_contact_videos.py /tmp/contact_video_additions
Requires lxml, PyMuPDF, before_* snapshot files and prepared upright clips.
Does not overwrite the active presentation. Existing notes remain unchanged.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
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
VIDEO_BOX = fitz.Rect(270, 65, 690, 485)
VIDEOS = [
    {'title': 'Plausibility experiment', 'base': 'Plausibility_experiment_presentation',
     'source': 'Plausibility Experiment.mp4', 'hidden': False},
    {'title': 'Opposing moment', 'base': 'Opposing_moment_presentation',
     'source': 'Opposing Moment.mp4', 'hidden': True},
]


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


with ZipFile(WORK / 'before_Thesis_Defense_gg0_v3.pptx') as z:
    parts = {n: z.read(n) for n in z.namelist()}
original = dict(parts)
pres = E.fromstring(parts['ppt/presentation.xml'])
prels = E.fromstring(parts['ppt/_rels/presentation.xml.rels'])
ids = pres.find('p:sldIdLst', NS)
lookup = {r.get('Id'): resolve('ppt/presentation.xml', r.get('Target')) for r in prels}
old_paths = [lookup[s.get(tag('r:id'))] for s in ids]
assert len(old_paths) == 36
assert old_paths[11] == 'ppt/slides/slide14.xml'
template_path = old_paths[18]
template = E.fromstring(parts[template_path])
template_rels = E.fromstring(parts[relpath(template_path)])
assert len(template.findall('.//p:video', NS)) == 1

max_slide = max(int(re.search(r'slide(\d+)\.xml$', n)[1]) for n in parts
                if re.fullmatch(r'ppt/slides/slide\d+\.xml', n))
max_note = max(int(re.search(r'notesSlide(\d+)\.xml$', n)[1]) for n in parts
               if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n))
max_sid = max(int(n.get('id')) for n in ids)
ct = E.fromstring(parts['[Content_Types].xml'])
sections = pres.findall('.//p14:section', NS)
note_rel = next(r for r in template_rels if r.get('Type').endswith('/notesSlide'))
template_note = resolve(template_path, note_rel.get('Target'))
new_paths = []

for i, info in enumerate(VIDEOS):
    path = 'ppt/slides/slide%d.xml' % (max_slide + i + 1)
    note_path = 'ppt/notesSlides/notesSlide%d.xml' % (max_note + i + 1)
    sid = str(max_sid + i + 1)
    rid = 'rIdContactVideo%d' % (i + 1)
    slide = deepcopy(template)
    if info['hidden']:
        slide.set('show', '0')
    else:
        slide.attrib.pop('show', None)
    caption = shape(slide, 'Nullspace2 label')
    caption.getparent().remove(caption)
    text(shape(slide, 'Slide title'), info['title'])
    move(shape(slide, 'TextBox 6'), fitz.Rect(900, 505.44, 921.6, 515.1337795))
    video = shape(slide, 'Nullspace2 part 1 video')
    props = video.find('p:nvPicPr/p:cNvPr', NS)
    props.set('name', info['title'] + ' video')
    props.set('descr', info['source'] + '. Upright presentation copy with full duration and original audio. Click to play.')
    move(video, VIDEO_BOX)
    for ext in slide.xpath('//*[local-name()="creationId"]'):
        ext.getparent().remove(ext)
    rels = deepcopy(template_rels)
    for r in rels:
        if r.get('Id') in {'rIdNullspace2Video', 'rIdNullspace2Media'}:
            r.set('Target', '../media/' + info['base'] + '.mp4')
        elif r.get('Id') == 'rIdNullspace2Poster':
            r.set('Target', '../media/' + info['base'] + '_poster.png')
        elif r.get('Type').endswith('/notesSlide'):
            r.set('Target', '../notesSlides/' + posixpath.basename(note_path))
    note = E.fromstring(parts[template_note])
    for body in note.findall('.//p:txBody', NS):
        for paragraph in body.findall('a:p', NS):
            body.remove(paragraph)
        E.SubElement(body, tag('a:p'))
    nr = E.fromstring(parts[relpath(template_note)])
    next(r for r in nr if r.get('Type').endswith('/slide')).set('Target', '../slides/' + posixpath.basename(path))
    parts[path], parts[relpath(path)] = dump(slide), dump(rels)
    parts[note_path], parts[relpath(note_path)] = dump(note), dump(nr)
    for suffix in ['.mp4', '_poster.png']:
        parts['ppt/media/' + info['base'] + suffix] = (WORK / (info['base'] + suffix)).read_bytes()
    E.SubElement(prels, '{' + PKG + '}Relationship', Id=rid, Type=NS['r'] + '/slide', Target='slides/' + posixpath.basename(path))
    sld_id = E.Element(tag('p:sldId'), id=sid)
    sld_id.set(tag('r:id'), rid)
    if info['hidden']:
        ids.append(sld_id)
        section_name = 'Backup'
    else:
        ids.insert(11, sld_id)
        section_name = 'Contact experiments'
    section = next(s for s in sections if s.get('name') == section_name)
    section.find('p14:sldIdLst', NS).append(E.Element(tag('p14:sldId'), id=sid))
    for owner, kind in [(path, 'slide'), (note_path, 'notesSlide')]:
        E.SubElement(ct, '{' + CT + '}Override', PartName='/' + owner,
                     ContentType='application/vnd.openxmlformats-officedocument.presentationml.' + kind + '+xml')
    new_paths.append(path)

ordered = old_paths[:11] + [new_paths[0]] + old_paths[11:] + [new_paths[1]]
footers = {}
order = []
for i, path in enumerate(ordered):
    root = E.fromstring(parts[path])
    label = (str(i) if i < 26 else 'B' + str(i - 25)) if i else ''
    if i:
        sh = shape(root, 'TextBox 6')
        if ''.join(sh.xpath('.//a:t/text()', namespaces=NS)) != label:
            text(sh, label)
            parts[path] = dump(root)
            footers[i] = label
    order.append({'physical': i + 1, 'path': path,
                  'title': ''.join(shape(root, 'Slide title').xpath('.//a:t/text()', namespaces=NS)) if i else 'Master Thesis Presentation',
                  'footer': label, 'hidden': i >= 26})

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
for key, value in [('Slides', '38'), ('Notes', '38'), ('HiddenSlides', '12'), ('MMClips', '6')]:
    app.xpath('//*[local-name()=$key]', key=key)[0].text = value
app.xpath('//*[local-name()="HeadingPairs"]//*[local-name()="i4"]')[-1].text = '38'
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
        out.writestr(info, parts[info.filename])
    for name in sorted(parts.keys() - original.keys()):
        out.writestr(name, parts[name])

# Compose only the new pages, preserving all existing PDF page content.
source = fitz.open(WORK / 'before_Thesis_Defense_gg0_v3.pdf')
pdf = fitz.open()
page_map = list(range(11)) + [18] + list(range(11, 36)) + [18]
for old in page_map:
    pdf.insert_pdf(source, from_page=old, to_page=old)
font = fitz.Font(fontfile=ARIAL)
bold_xref = next(f[0] for f in source[18].get_fonts() if 'Arial-Bold' in f[3])
bold = source.extract_font(bold_xref)[3]
bold_font = fitz.Font(fontbuffer=bold)
for info in VIDEOS:
    assert all(bold_font.has_glyph(ord(c)) for c in info['title']), info['title']

for i, info in zip([11, 37], VIDEOS):
    page = pdf[i]
    for rect in [fitz.Rect(40, 55, 920, 500), fitz.Rect(38, 16, 920, 45)]:
        page.add_redact_annot(rect, fill=(1, 1, 1))
    page.apply_redactions(images=2, graphics=1, text=0)
    page.insert_font(fontname='ArialContactVideoBold', fontbuffer=bold)
    page.insert_text((44.64, 39.36), info['title'], fontname='ArialContactVideoBold', fontsize=17.544, color=NAVY)
    page.insert_image(VIDEO_BOX, filename=str(WORK / (info['base'] + '_poster.png')))

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
    page.insert_font(fontname='ArialContactVideo', fontfile=ARIAL)
    page.insert_text((921.8 - font.text_length(label, fontsize=8.04), 513.48), label,
                     fontname='ArialContactVideo', fontsize=8.04, color=(.412, .412, .412))
pdf.save(WORK / 'updated.pdf', garbage=4, deflate=True)
supp = fitz.open()
supp.insert_pdf(pdf, from_page=26, to_page=37)
supp.save(WORK / 'supplementary.pdf', garbage=4, deflate=True)

assert [n.get('id') for n in ids] == [n.get('id') for s in sections for n in s.find('p14:sldIdLst', NS)]
assert len(catalog) == 29
for path in original:
    if path.startswith(('ppt/notesSlides/', 'ppt/media/')):
        assert parts[path] == original[path]
for entry in order:
    root = E.fromstring(parts[entry['path']])
    assert (root.get('show') == '0') == entry['hidden']
    for equation in [e for e in catalog if e['slide'] == entry['physical']]:
        assert shape(root, equation['shape']).find('.//m:oMath', NS) is not None
for name in parts:
    if name.endswith('.rels'):
        owner = name.replace('/_rels/', '/')[:-5] if name != '_rels/.rels' else ''
        for r in E.fromstring(parts[name]):
            if r.get('TargetMode') != 'External':
                target = resolve(owner, r.get('Target')).lstrip('/')
                assert target in parts, (name, target)
for name in old_paths:
    before, after = E.fromstring(original[name]), E.fromstring(parts[name])
    for root in [before, after]:
        for t in root.xpath('.//p:sp[p:nvSpPr/p:cNvPr[@name="TextBox 6"]]//a:t', namespaces=NS):
            t.text = 'FOOTER'
    assert E.tostring(before) == E.tostring(after), name
report = {
    'date': '2026-09-21', 'new_videos': VIDEOS,
    'main_slides': 26, 'hidden_backups': 12, 'total_slides': 38,
    'supplementary_pages': 12, 'slide_order': order, 'page_map_zero_based': page_map,
    'new_video_pages': [12, 38], 'changed_footer_pages': [i + 1 for i in footers],
    'native_equation_count': len(catalog), 'existing_notes_and_media_unchanged': True,
    'existing_slide_contents_unchanged_except_footer': True, 'overview_chapters': chapters,
    'all_internal_relationships_resolve': True,
    'changed_existing_parts': [n for n in original if parts[n] != original[n]],
    'new_parts': sorted(parts.keys() - original.keys()),
    'pdf_method': 'Original PowerPoint PDF pages retained, with two new video poster pages and affected footers composed.',
}
(WORK / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Staged 38-slide deck: 26 main slides, 12 hidden backups. Existing slide content, notes and media preserved.')
