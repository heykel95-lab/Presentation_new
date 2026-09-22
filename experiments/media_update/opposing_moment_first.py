"""Move Opposing moment to B1, preserving all contents and playback settings.

Usage: python3 opposing_moment_first.py /tmp/opposing_moment_first_20260922
Stages PowerPoint, full/supplementary PDFs and updated placement metadata.
Requires PyMuPDF, lxml and numpy. Active files are not overwritten.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
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
ARIAL = '/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf'


def dump(node):
    return E.tostring(node, encoding='UTF-8', xml_declaration=True, standalone=True)


def shape(slide, name):
    found = slide.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$name]', name=name, namespaces=NS)
    assert len(found) == 1, name
    return found[0]


def settext(sh, value):
    text = sh.findall('.//a:t', NS)
    assert len(text) == 1
    text[0].text = value


with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as before:
    pres = E.fromstring(before.read('ppt/presentation.xml'))
    rels = {r.get('Id'): r.get('Target') for r in E.fromstring(before.read('ppt/_rels/presentation.xml.rels'))}
    old_ids = list(pres.find('p:sldIdLst', NS))
    entries = []
    for i, item in enumerate(old_ids, 1):
        path = posixpath.normpath('ppt/' + rels[item.get('{' + NS['r'] + '}id')])
        slide = E.fromstring(before.read(path))
        title = ''.join(shape(slide, 'Slide title').xpath('.//a:t/text()', namespaces=NS)) if i > 1 else 'Master Thesis Presentation'
        entries.append({'old_physical': i, 'path': path, 'sid': item.get('id'), 'title': title})
    assert len(entries) == 34
    assert entries[32]['title'] == 'Opposing moment'
    ordered = entries[:26] + [entries[32]] + entries[26:32] + entries[33:]
    assert len(ordered) == 34 and len({e['path'] for e in ordered}) == 34
    main_list = pres.find('p:sldIdLst', NS)
    for node in list(main_list):
        main_list.remove(node)
    for entry in ordered:
        main_list.append(deepcopy(old_ids[entry['old_physical'] - 1]))
    sections = pres.findall('.//p14:section', NS)
    backup = next(s for s in sections if s.get('name') == 'Backup')
    members = backup.find('p14:sldIdLst', NS)
    for node in list(members):
        members.remove(node)
    for entry in ordered[26:]:
        E.SubElement(members, '{' + NS['p14'] + '}sldId', id=entry['sid'])
    assert [n.get('id') for s in sections for n in s.findall('.//p14:sldId', NS)] == [e['sid'] for e in ordered]
    changes = {'ppt/presentation.xml': dump(pres)}
    footer_updates = []
    for i, entry in enumerate(ordered, 1):
        entry['physical'] = i
        entry['footer'] = str(i - 1) if i <= 26 else 'B%d' % (i - 26)
        if i <= 26:
            continue
        slide = E.fromstring(before.read(entry['path']))
        assert slide.get('show') == '0'
        footer = shape(slide, 'TextBox 6')
        label = ''.join(footer.xpath('.//a:t/text()', namespaces=NS))
        if label != entry['footer']:
            entry['old_footer'] = label
            settext(footer, entry['footer'])
            changes[entry['path']] = dump(slide)
            footer_updates.append(entry)
            settext(footer, label)
            assert E.tostring(slide) == E.tostring(E.fromstring(before.read(entry['path'])))
    assert len(footer_updates) == 7
    app = E.fromstring(before.read('docProps/app.xml'))
    vector = app.xpath('//*[local-name()="TitlesOfParts"]/*')[0]
    assert len(vector) == 37
    titles = list(vector)[-34:]
    for node in titles:
        vector.remove(node)
    for entry in ordered:
        vector.append(deepcopy(titles[entry['old_physical'] - 1]))
    changes['docProps/app.xml'] = dump(app)
    chapters = [s.get('name') for s in sections if s.get('name') != 'Backup']
    overview = E.fromstring(before.read('ppt/slides/slide4.xml'))
    old_overview = dump(overview)
    for i, title in enumerate(chapters, 1):
        settext(shape(overview, 'Overview item %d' % i), title)
        settext(shape(overview, 'Overview number %d' % i), '%d.' % i)
    assert dump(overview) == old_overview
    with ZipFile(W / 'updated.pptx', 'w') as out:
        for info in before.infolist():
            out.writestr(info, changes.get(info.filename, before.read(info.filename)))

catalog = json.loads((W / 'before_native_equations.json').read_text())
old_catalog = deepcopy(catalog)
new_positions = {e['old_physical']: e['physical'] for e in ordered}
for item in catalog:
    item['slide'] = new_positions[item['slide']]
assert len(catalog) == 29
assert sum(a != b for a, b in zip(catalog, old_catalog)) == 3
(W / 'native_equations.json').write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n')
manifest = json.loads((W / 'before_manifest.json').read_text())
for item in manifest:
    old_position = item.get('physical_slide')
    if isinstance(old_position, int) and 'backup_slide' in item and old_position in new_positions:
        new_position = new_positions[old_position]
        if new_position != old_position:
            item['physical_slide'] = new_position
            item['backup_slide'] = 'B%d' % (new_position - 26)
            item['placement_update'] = '2026-09-22: renumbered after Opposing moment moved to B1. Figure assets unchanged.'
(W / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')

source = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
assert len(source) == 34
pdf = fitz.open()
font = fitz.Font(fontfile=ARIAL)
for entry in ordered:
    i = entry['old_physical'] - 1
    pdf.insert_pdf(source, from_page=i, to_page=i)
    if 'old_footer' not in entry:
        continue
    page = pdf[-1]
    spans = [s for b in page.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']
             if s['text'] == entry['old_footer'] and s['bbox'][0] > 899 and s['bbox'][1] > 499]
    assert len(spans) == 1, entry['title']
    span = spans[0]
    page.add_redact_annot(fitz.Rect(span['bbox']), fill=False, cross_out=False)
    page.apply_redactions(images=0, graphics=0, text=0)
    page.insert_font(fontname='BackupFooterArial', fontfile=ARIAL)
    colour = tuple(((span['color'] >> shift) & 255) / 255 for shift in [16, 8, 0])
    x = span['bbox'][2] - font.text_length(entry['footer'], fontsize=span['size'])
    page.insert_text((x, span['origin'][1]), entry['footer'], fontname='BackupFooterArial', fontsize=span['size'], color=colour)
pdf.save(W / 'updated.pdf', garbage=4, deflate=True)
supp = fitz.open()
supp.insert_pdf(pdf, from_page=26, to_page=33)
supp.save(W / 'Supplementary_slides.pdf', garbage=4, deflate=True)

with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as before, ZipFile(W / 'updated.pptx') as after:
    assert before.namelist() == after.namelist()
    changed_parts = [n for n in before.namelist() if before.read(n) != after.read(n)]
    assert set(changed_parts) == set(changes)
    assert after.testzip() is None
    for item, old in zip(catalog, old_catalog):
        slide = E.fromstring(after.read(ordered[item['slide'] - 1]['path']))
        assert slide.xpath('.//p:cNvPr[@name=$n]', n=item['shape'], namespaces=NS)
        check = dict(item, slide=old['slide'])
        assert check == old
final = fitz.open(W / 'updated.pdf')
supp = fitz.open(W / 'Supplementary_slides.pdf')
for i, entry in enumerate(ordered):
    old = source[entry['old_physical'] - 1].get_pixmap(alpha=False)
    new = final[i].get_pixmap(alpha=False)
    if 'old_footer' in entry:
        dims = (old.height, old.width, 3)
        a = np.frombuffer(old.samples, np.uint8).reshape(dims)
        b = np.frombuffer(new.samples, np.uint8).reshape(dims)
        changed = np.any(a != b, axis=2)
        changed[500:520, 900:925] = False
        assert not changed.any(), entry['title']
    else:
        assert old.samples == new.samples, entry['title']
    if i >= 26:
        assert new.samples == supp[i - 26].get_pixmap(alpha=False).samples
report = {'date': '2026-09-22', 'move': 'Opposing moment from B7 / physical 33 to B1 / physical 27',
          'main_slides': 26, 'hidden_backups': 8, 'total_slides': 34, 'supplementary_pages': 8,
          'main_slide_contents_and_order_unchanged': True,
          'backup_contents_unchanged_except_footer': True,
          'notes_media_playback_and_all_other_package_parts_unchanged': True,
          'pdf_content_pixel_identical_except_footer': True,
          'supplementary_pdf_matches_full_pdf': True,
          'native_equation_count': 29, 'catalog_entries_reindexed': 3,
          'all_native_equations_verified': True,
          'overview_refreshed_from_sections': chapters,
          'changed_pptx_parts': changed_parts, 'slide_order': ordered}
(W / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Opposing moment staged as B1. Contents, video playback and notes preserved. All 29 equations verified.')
