"""Remove backup demonstration B2 and simplify the two main clip captions.

Usage: python3 remove_backup_demo.py /tmp/remove_backup_demo_20260922
The directory must contain before_Thesis_Defense_gg0_v3.{pptx,pdf}.
Requires PyMuPDF, lxml and numpy. Stages outputs without replacing active files.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
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
REMOVE = {28: ('Disturbance demonstration', 'Backup B2 removed at the user’s request.')}
CAPTIONS = {
    'ppt/slides/slide36.xml': 'Demonstration · Part 1',
    'ppt/slides/slide37.xml': 'Demonstration · Part 2',
}
ARIAL = '/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf'


def dump(node):
    return E.tostring(node, encoding='UTF-8', xml_declaration=True, standalone=True)


def relpath(owner):
    return posixpath.dirname(owner) + '/_rels/' + posixpath.basename(owner) + '.rels'


def resolve(owner, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(owner), target))


def shape(root, name):
    found = root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$n]', namespaces=NS, n=name)
    assert len(found) == 1, name
    return found[0]


def settext(sh, value):
    labels = sh.findall('.//a:t', NS)
    assert len(labels) == 1
    labels[0].text = value


def update_properties(data, chosen, hidden, clips):
    app = E.fromstring(data)
    for name, value in [('Slides', len(chosen)), ('Notes', len(chosen)),
                        ('HiddenSlides', hidden), ('MMClips', clips)]:
        app.xpath('//*[local-name()=$n]', n=name)[0].text = str(value)
    app.xpath('//*[local-name()="HeadingPairs"]//*[local-name()="i4"]')[-1].text = str(len(chosen))
    vector = app.xpath('//*[local-name()="TitlesOfParts"]/*')[0]
    old_titles = list(vector)[-35:]
    assert len(vector) == 38
    for node in old_titles:
        vector.remove(node)
    for entry in chosen:
        vector.append(deepcopy(old_titles[entry['old_physical'] - 1]))
    vector.set('size', str(len(vector)))
    return dump(app)


with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as z:
    original = {n: z.read(n) for n in z.namelist()}
pres = E.fromstring(original['ppt/presentation.xml'])
prels = E.fromstring(original['ppt/_rels/presentation.xml.rels'])
targets = {r.get('Id'): resolve('ppt/presentation.xml', r.get('Target')) for r in prels}
entries = []
for number, item in enumerate(pres.find('p:sldIdLst', NS), 1):
    rid = item.get('{' + NS['r'] + '}id')
    path = targets[rid]
    slide = E.fromstring(original[path])
    title = ''.join(shape(slide, 'Slide title').xpath('.//a:t/text()', namespaces=NS)) if number > 1 else 'Master Thesis Presentation'
    entries.append({'old_physical': number, 'path': path, 'sid': item.get('id'),
                    'rid': rid, 'title': title, 'hidden': slide.get('show') == '0'})
assert len(entries) == 35 and sum(e['hidden'] for e in entries) == 9
removed = [e for e in entries if e['old_physical'] in REMOVE]
retained = [e for e in entries if e not in removed]
for entry in removed:
    expected, reason = REMOVE[entry['old_physical']]
    assert entry['title'] == expected and entry['hidden']
    entry['reason'] = reason
assert len(retained) == 34


def select_slide_list(chosen):
    selected = {e['sid'] for e in chosen}
    relationships = {e['rid'] for e in chosen}
    p = E.fromstring(original['ppt/presentation.xml'])
    r = E.fromstring(original['ppt/_rels/presentation.xml.rels'])
    lst = p.find('p:sldIdLst', NS)
    for item in list(lst):
        if item.get('id') not in selected:
            lst.remove(item)
    for rel in list(r):
        if rel.get('Type').endswith('/slide') and rel.get('Id') not in relationships:
            r.remove(rel)
    sections = p.findall('.//p14:section', NS)
    for section in sections:
        members = section.find('p14:sldIdLst', NS)
        for item in list(members):
            if item.get('id') not in selected:
                members.remove(item)
        if len(members) == 0:
            section.getparent().remove(section)
    assert [n.get('id') for n in p.findall('.//p14:section/p14:sldIdLst/p14:sldId', NS)] == [e['sid'] for e in chosen]
    return dump(p), dump(r)


parts = dict(original)
parts['ppt/presentation.xml'], parts['ppt/_rels/presentation.xml.rels'] = select_slide_list(retained)
deleted = set()
removed_notes = []
for entry in removed:
    path = entry['path']
    rels = E.fromstring(parts[relpath(path)])
    note_rel = next(r for r in rels if r.get('Type').endswith('/notesSlide'))
    note = resolve(path, note_rel.get('Target'))
    removed_notes.append(note)
    deleted.update([path, relpath(path), note, relpath(note)])
for path in deleted:
    del parts[path]
ct = E.fromstring(parts['[Content_Types].xml'])
for entry in list(ct):
    if entry.get('PartName', '').lstrip('/') in deleted:
        ct.remove(entry)
parts['[Content_Types].xml'] = dump(ct)
parts['docProps/app.xml'] = update_properties(original['docProps/app.xml'], retained, 8, 5)

# Only changed backup footers are rewritten. All other shape XML stays exact.
changed_footers = []
for number, entry in enumerate(retained, 1):
    entry['physical'] = number
    entry['footer'] = str(number - 1) if number <= 26 else 'B%d' % (number - 26)
    if number <= 26:
        continue
    slide = E.fromstring(parts[entry['path']])
    footer = shape(slide, 'TextBox 6')
    before = ''.join(footer.xpath('.//a:t/text()', namespaces=NS))
    if before != entry['footer']:
        settext(footer, entry['footer'])
        parts[entry['path']] = dump(slide)
        changed_footers.append(entry)
    assert slide.get('show') == '0'

for path, text in CAPTIONS.items():
    slide = E.fromstring(parts[path])
    label = shape(slide, 'Nullspace2 label')
    assert 'Demonstration 2' in ''.join(label.xpath('.//a:t/text()', namespaces=NS))
    settext(label, text)
    parts[path] = dump(slide)

sections = E.fromstring(parts['ppt/presentation.xml']).findall('.//p14:section', NS)
chapters = [s.get('name') for s in sections if s.get('name') != 'Backup']
overview_path = retained[3]['path']
overview = E.fromstring(parts[overview_path])
overview_before = dump(overview)
for i, title in enumerate(chapters, 1):
    settext(shape(overview, 'Overview item %d' % i), title)
    settext(shape(overview, 'Overview number %d' % i), '%d.' % i)
assert dump(overview) == overview_before


def check_relationships(package):
    for name, data in package.items():
        if not name.endswith('.rels'):
            continue
        owner = '' if name == '_rels/.rels' else posixpath.join(posixpath.dirname(posixpath.dirname(name)), posixpath.basename(name)[:-5])
        for rel in E.fromstring(data):
            if rel.get('TargetMode') != 'External':
                target = resolve(owner, rel.get('Target')).lstrip('/')
                assert target in package, (name, target)


check_relationships(parts)
with ZipFile(W / 'before_Thesis_Defense_gg0_v3.pptx') as old, ZipFile(W / 'updated.pptx', 'w') as out:
    for info in old.infolist():
        if info.filename in parts:
            out.writestr(info, parts[info.filename])

# Standalone archive: original B2, its notes, video and all dependencies.
archive = dict(original)
archive['ppt/presentation.xml'], archive['ppt/_rels/presentation.xml.rels'] = select_slide_list(removed)
archive['docProps/app.xml'] = update_properties(original['docProps/app.xml'], removed, 1, 1)
reachable = {'_rels/.rels'}
pending = ['']
while pending:
    owner = pending.pop()
    rp = '_rels/.rels' if owner == '' else relpath(owner)
    if rp not in archive:
        continue
    reachable.add(rp)
    for rel in E.fromstring(archive[rp]):
        if rel.get('TargetMode') == 'External':
            continue
        target = resolve(owner, rel.get('Target')).lstrip('/')
        assert target in archive, (rp, target)
        if target not in reachable:
            reachable.add(target)
            pending.append(target)
archive = {name: value for name, value in archive.items() if name in reachable}
ct = E.fromstring(original['[Content_Types].xml'])
for entry in list(ct):
    if entry.get('PartName') and entry.get('PartName').lstrip('/') not in archive:
        ct.remove(entry)
archive['[Content_Types].xml'] = dump(ct)
check_relationships(archive)
for entry in removed:
    assert archive[entry['path']] == original[entry['path']]
for note in removed_notes:
    assert archive[note] == original[note]
with ZipFile(W / 'removed_backup_demo_20260922.pptx', 'w', ZIP_DEFLATED) as out:
    for name, value in archive.items():
        out.writestr(name, value)

source = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
assert len(source) == 35
pdf = fitz.open()
font = fitz.Font(fontfile=ARIAL)
for entry in retained:
    old = entry['old_physical'] - 1
    pdf.insert_pdf(source, from_page=old, to_page=old)
    if entry['path'] in CAPTIONS:
        page = pdf[-1]
        spans = [s for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])
                 for s in l['spans'] if s['text'].startswith('Demonstration') and '00:' in s['text']]
        assert len(spans) == 1
        span = spans[0]
        page.add_redact_annot(fitz.Rect(span['bbox']), fill=False, cross_out=False)
        page.apply_redactions(images=0, graphics=0, text=0)
        page.insert_font(fontname='DemoCaptionArial', fontfile=ARIAL)
        colour = tuple(((span['color'] >> shift) & 255) / 255 for shift in [16, 8, 0])
        text = CAPTIONS[entry['path']]
        x = (960 - font.text_length(text, fontsize=span['size'])) / 2
        page.insert_text((x, span['origin'][1]), text, fontname='DemoCaptionArial', fontsize=span['size'], color=colour)
    if entry not in changed_footers:
        continue
    page = pdf[-1]
    old_footer = 'B%d' % (entry['old_physical'] - 26)
    spans = [s for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])
             for s in l['spans'] if s['text'] == old_footer and s['bbox'][0] > 899 and s['bbox'][1] > 499]
    assert len(spans) == 1, (entry['title'], spans)
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
removed_pdf = fitz.open()
for entry in removed:
    old = entry['old_physical'] - 1
    removed_pdf.insert_pdf(source, from_page=old, to_page=old)
removed_pdf.save(W / 'removed_backup_demo_20260922.pdf', garbage=4, deflate=True)

changed_parts = [n for n in parts if parts[n] != original[n]]
allowed_changes = {'ppt/presentation.xml', 'ppt/_rels/presentation.xml.rels',
                   '[Content_Types].xml', 'docProps/app.xml'} | {e['path'] for e in changed_footers} | set(CAPTIONS)
assert set(changed_parts) == allowed_changes, changed_parts
for entry in changed_footers:
    current = E.fromstring(parts[entry['path']])
    settext(shape(current, 'TextBox 6'), 'B%d' % (entry['old_physical'] - 26))
    assert E.tostring(current) == E.tostring(E.fromstring(original[entry['path']])), entry['title']
for path in CAPTIONS:
    current = E.fromstring(parts[path])
    previous = E.fromstring(original[path])
    prior_label = ''.join(shape(previous, 'Nullspace2 label').xpath('.//a:t/text()', namespaces=NS))
    settext(shape(current, 'Nullspace2 label'), prior_label)
    assert E.tostring(current) == E.tostring(previous)
for name, data in parts.items():
    if name.startswith(('ppt/media/', 'ppt/notesSlides/')):
        assert data == original[name]

final = fitz.open(W / 'updated.pdf')
final_supp = fitz.open(W / 'Supplementary_slides.pdf')
assert len(final) == 34 and len(final_supp) == 8
for i, entry in enumerate(retained):
    before = source[entry['old_physical'] - 1].get_pixmap(alpha=False)
    after = final[i].get_pixmap(alpha=False)
    assert (before.width, before.height) == (after.width, after.height)
    if entry in changed_footers or entry['path'] in CAPTIONS:
        dims = (before.height, before.width, 3)
        a = np.frombuffer(before.samples, np.uint8).reshape(dims)
        b = np.frombuffer(after.samples, np.uint8).reshape(dims)
        changed = np.any(a != b, axis=2)
        if entry in changed_footers:
            changed[500:520, 900:925] = False
        if entry['path'] in CAPTIONS:
            changed[470:497, 240:721] = False
        assert not changed.any(), ('Content outside caption/footer changed', entry['title'])
    else:
        assert before.samples == after.samples, entry['title']
    if i >= 26:
        assert after.samples == final_supp[i - 26].get_pixmap(alpha=False).samples

report = {'date': '2026-09-22', 'removed_slides': removed,
          'retained_nullspace_plot_backups': [e for e in retained if e['physical'] in [28, 29, 30]],
          'main_slides': 26, 'hidden_backups': 8, 'total_slides': 34,
          'supplementary_pages': 8, 'native_equation_count': 29, 'active_video_count': 5,
          'main_demo_captions': CAPTIONS,
          'main_slides_unchanged_except_two_demo_captions': True,
          'retained_backup_contents_unchanged_except_footer': True,
          'all_remaining_notes_and_embedded_media_byte_identical': True,
          'removed_slides_and_notes_preserved_exactly_in_archive': True,
          'pdf_archive_contains_original_B2': True,
          'supplementary_pdf_matches_active_backup_pages': True,
          'all_package_relationships_resolve': True,
          'overview_refreshed_from_sections': chapters,
          'changed_pptx_parts': changed_parts, 'removed_pptx_parts': sorted(deleted),
          'slide_order': retained}
(W / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Staged 34-slide deck and PDF, eight-page supplementary PDF and original B2 archive.')
print('Only two main captions and seven backup footers changed. All figure shapes, video bytes and remaining notes are unchanged.')
