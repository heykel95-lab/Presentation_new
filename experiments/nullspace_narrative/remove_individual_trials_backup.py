"""Remove requested backups while preserving native equations, media, and notes.

Prepare a four-slide reference for artifact-tool, then apply its slide order and
footer text to the original package without round-tripping protected content.
Run with the workspace directory, prepare or finish, and optional b3_b4 profile.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import posixpath
import shutil
import sys

W = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(W / 'deps'))
sys.path.append(str(W.parent / 'remove_b5_20260922' / 'deps'))
import pymupdf as fitz
import numpy as np
from lxml import etree as E

ROOT = Path(__file__).resolve().parents[2]
FINAL = ROOT / 'Final Presentation'
PROFILE = sys.argv[3] if len(sys.argv) > 3 else 'b5'
assert PROFILE in ('b5', 'b3_b4')
REMOVE = {31: 'Joint motion: all individual trials'} if PROFILE == 'b5' else {
    29: 'Cumulative joint motion: all settings',
    30: 'Jacobian conditioning: all settings'}
OLD_COUNT = 34 if PROFILE == 'b5' else 33
NEW_COUNT = OLD_COUNT - len(REMOVE)
ARCHIVE = 'removed_B5_individual_trials_20260922' if PROFILE == 'b5' else 'removed_B3_B4_all_settings_20260922'
FIRST = min(REMOVE)
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'}


def dump(node):
    return E.tostring(node, encoding='UTF-8', xml_declaration=True, standalone=True)


def relpath(owner):
    return posixpath.dirname(owner) + '/_rels/' + posixpath.basename(owner) + '.rels'


def resolve(owner, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(owner), target)).lstrip('/')


def shape(root, name):
    found = root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$n]', namespaces=NS, n=name)
    assert len(found) == 1, name
    return found[0]


def txt(node):
    return ''.join(node.xpath('.//a:t/text()', namespaces=NS))


def settext(node, value):
    labels = node.findall('.//a:t', NS)
    assert len(labels) == 1
    labels[0].text = value


def read_package(path):
    with ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def entries(package):
    pres = E.fromstring(package['ppt/presentation.xml'])
    rels = E.fromstring(package['ppt/_rels/presentation.xml.rels'])
    targets = {r.get('Id'): resolve('ppt/presentation.xml', r.get('Target')) for r in rels}
    result = []
    for number, item in enumerate(pres.find('p:sldIdLst', NS), 1):
        rid = item.get('{' + NS['r'] + '}id')
        path = targets[rid]
        slide = E.fromstring(package[path])
        title_nodes = slide.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name="Slide title"]', namespaces=NS)
        result.append({'old_physical': number, 'path': path, 'sid': item.get('id'),
                       'rid': rid, 'title': txt(title_nodes[0]) if title_nodes else 'Master Thesis Presentation',
                       'hidden': slide.get('show') == '0'})
    return result


def select(package, chosen, original_count):
    result = dict(package)
    pres = E.fromstring(package['ppt/presentation.xml'])
    rels = E.fromstring(package['ppt/_rels/presentation.xml.rels'])
    ids = {e['sid'] for e in chosen}
    rids = {e['rid'] for e in chosen}
    for node in list(pres.find('p:sldIdLst', NS)):
        if node.get('id') not in ids:
            node.getparent().remove(node)
    for node in list(rels):
        if node.get('Type').endswith('/slide') and node.get('Id') not in rids:
            rels.remove(node)
    for section in pres.findall('.//p14:section', NS):
        members = section.find('p14:sldIdLst', NS)
        for node in list(members):
            if node.get('id') not in ids:
                members.remove(node)
        if not len(members):
            section.getparent().remove(section)
    assert [n.get('id') for n in pres.findall('.//p14:section/p14:sldIdLst/p14:sldId', NS)] == [e['sid'] for e in chosen]
    result['ppt/presentation.xml'] = dump(pres)
    result['ppt/_rels/presentation.xml.rels'] = dump(rels)
    app = E.fromstring(package['docProps/app.xml'])
    for key, value in [('Slides', len(chosen)), ('Notes', len(chosen)), ('HiddenSlides', sum(e['hidden'] for e in chosen))]:
        app.xpath('//*[local-name()=$n]', n=key)[0].text = str(value)
    app.xpath('//*[local-name()="HeadingPairs"]//*[local-name()="i4"]')[-1].text = str(len(chosen))
    vector = app.xpath('//*[local-name()="TitlesOfParts"]/*')[0]
    old_titles = list(vector)[-original_count:]
    for node in old_titles:
        vector.remove(node)
    for entry in chosen:
        vector.append(deepcopy(old_titles[entry['old_physical'] - 1]))
    vector.set('size', str(len(vector)))
    result['docProps/app.xml'] = dump(app)
    return result


def trim(package):
    reached = {'_rels/.rels'}
    pending = ['']
    while pending:
        owner = pending.pop()
        rp = '_rels/.rels' if owner == '' else relpath(owner)
        if rp not in package:
            continue
        reached.add(rp)
        for rel in E.fromstring(package[rp]):
            if rel.get('TargetMode') != 'External':
                target = resolve(owner, rel.get('Target'))
                assert target in package, (rp, target)
                if target not in reached:
                    reached.add(target)
                    pending.append(target)
    result = {n: v for n, v in package.items() if n in reached}
    ct = E.fromstring(package['[Content_Types].xml'])
    for node in list(ct):
        if node.get('PartName') and node.get('PartName').lstrip('/') not in result:
            ct.remove(node)
    result['[Content_Types].xml'] = dump(ct)
    return result


def write_package(path, package):
    with ZipFile(path, 'w', ZIP_DEFLATED) as z:
        for name, data in package.items():
            z.writestr(name, data)


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sys.argv[2] == 'prepare':
    W.mkdir(parents=True, exist_ok=True)
    for name in ['Thesis_Defense_gg0_v3.pptx', 'Thesis_Defense_gg0_v3.pdf', 'Supplementary_slides.pdf']:
        target = W / ('before_' + name)
        assert not target.exists(), 'Refusing to overwrite rollback snapshot'
        shutil.copy2(FINAL / name, target)
    protected = [FINAL / 'Speaker_notes_and_timing.txt', FINAL / 'Speaking/Thesis_Defense_Speaking_Script.tex',
                 FINAL / 'Thesis_Defense_Speaking_Script.pdf', FINAL / 'Thesis_Defense_Speaking_Script_updated.pdf',
                 FINAL / 'figures_and_images/native_equations.json']
    (W / 'protected-files.json').write_text(json.dumps({str(p): hash_file(p) for p in protected}, indent=2))
    package = read_package(W / 'before_Thesis_Defense_gg0_v3.pptx')
    slides = entries(package)
    assert len(slides) == OLD_COUNT and sum(e['hidden'] for e in slides) == OLD_COUNT - 26
    for number, title in REMOVE.items():
        assert slides[number - 1]['title'] == title and slides[number - 1]['hidden']
        assert txt(shape(E.fromstring(package[slides[number - 1]['path']]), 'TextBox 6')) == 'B%d' % (number - 26)
    write_package(W / 'reference.pptx', trim(select(package, slides[FIRST - 1:], OLD_COUNT)))
    (W / 'source-notes.txt').write_text('Source: current active PowerPoint and matching PDF. Remove requested backups and renumber later footers. Preserve all other content and remaining notes. Artifact-tool edits a focused reference; final package retains original native equations, media, and notes.\n')
    (W / 'slide-order-before.json').write_text(json.dumps(slides, indent=2))
    with fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf') as pdf:
        assert len(pdf) == OLD_COUNT
        for number in REMOVE:
            pdf[number - 1].get_pixmap().save(W / ('removed-b%d.png' % (number - 26)))
    print('Prepared requested backup reference and protected-file hashes.')
    sys.exit(0)

original = read_package(W / 'before_Thesis_Defense_gg0_v3.pptx')
slides = entries(original)
removed = [e for e in slides if e['old_physical'] in REMOVE]
retained = [e for e in slides if e['old_physical'] not in REMOVE]
assert len(slides) == OLD_COUNT and len(retained) == NEW_COUNT
assert all(e['title'] == REMOVE[e['old_physical']] for e in removed)
edited = read_package(W / 'edited-reference.pptx')
edited_entries = entries(edited)
assert [e['title'] for e in edited_entries] == [e['title'] for e in retained[-3:]]
parts = select(original, retained, OLD_COUNT)
deleted = set()
removed_notes = []
for entry in removed:
    removed_rels = E.fromstring(original[relpath(entry['path'])])
    note = resolve(entry['path'], next(r.get('Target') for r in removed_rels if r.get('Type').endswith('/notesSlide')))
    removed_notes.append(note)
    deleted.update([entry['path'], relpath(entry['path']), note, relpath(note)])
for name in deleted:
    del parts[name]
ct = E.fromstring(parts['[Content_Types].xml'])
for node in list(ct):
    if node.get('PartName', '').lstrip('/') in deleted:
        ct.remove(node)
parts['[Content_Types].xml'] = dump(ct)
for i, (entry, authored) in enumerate(zip(retained[-3:], edited_entries), FIRST - 26):
    label = txt(shape(E.fromstring(edited[authored['path']]), 'TextBox 6'))
    assert label == 'B%d' % i
    slide = E.fromstring(parts[entry['path']])
    entry['old_footer'] = txt(shape(slide, 'TextBox 6'))
    entry['footer'] = label
    settext(shape(slide, 'TextBox 6'), label)
    parts[entry['path']] = dump(slide)

# Refresh Overview from current native sections. Chapter rows are unchanged.
chapters = [s.get('name') for s in E.fromstring(parts['ppt/presentation.xml']).findall('.//p14:section', NS) if s.get('name') != 'Backup']
overview = E.fromstring(parts[retained[3]['path']])
before_overview = dump(overview)
for i, title in enumerate(chapters, 1):
    settext(shape(overview, 'Overview item %d' % i), title)
    settext(shape(overview, 'Overview number %d' % i), '%d.' % i)
assert dump(overview) == before_overview

archive = trim(select(original, removed, OLD_COUNT))
for entry in removed:
    assert archive[entry['path']] == original[entry['path']]
for note in removed_notes:
    assert archive[note] == original[note]
write_package(W / (ARCHIVE + '.pptx'), archive)
write_package(W / 'updated.pptx', parts)

source = fitz.open(W / 'before_Thesis_Defense_gg0_v3.pdf')
pdf = fitz.open()
arial = str(Path('C:/Windows/Fonts/arial.ttf'))
font = fitz.Font(fontfile=arial)
for entry in retained:
    old = entry['old_physical'] - 1
    pdf.insert_pdf(source, from_page=old, to_page=old)
    if 'old_footer' in entry:
        page = pdf[-1]
        spans = [s for b in page.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']
                 if s['text'] == entry['old_footer'] and s['bbox'][0] > 899 and s['bbox'][1] > 499]
        assert len(spans) == 1, entry['title']
        span = spans[0]
        page.add_redact_annot(fitz.Rect(span['bbox']), fill=False, cross_out=False)
        page.apply_redactions(images=0, graphics=0, text=0)
        page.insert_font(fontname='BackupFooterArial', fontfile=arial)
        color = tuple(((span['color'] >> shift) & 255) / 255 for shift in [16, 8, 0])
        x = span['bbox'][2] - font.text_length(entry['footer'], fontsize=span['size'])
        page.insert_text((x, span['origin'][1]), entry['footer'], fontname='BackupFooterArial', fontsize=span['size'], color=color)
pdf.save(W / 'updated.pdf', garbage=4, deflate=True)
supp = fitz.open()
supp.insert_pdf(pdf, from_page=26, to_page=NEW_COUNT - 1)
supp.save(W / 'Supplementary_slides.pdf', garbage=4, deflate=True)
archive_pdf = fitz.open()
for entry in removed:
    old_page = entry['old_physical'] - 1
    archive_pdf.insert_pdf(source, from_page=old_page, to_page=old_page)
archive_pdf.save(W / (ARCHIVE + '.pdf'), garbage=4, deflate=True)

allowed = {'ppt/presentation.xml', 'ppt/_rels/presentation.xml.rels', 'docProps/app.xml', '[Content_Types].xml'} | {e['path'] for e in retained[-3:]}
changed = [n for n in parts if parts[n] != original[n]]
assert set(changed) == allowed
for entry in retained[-3:]:
    slide = E.fromstring(parts[entry['path']])
    settext(shape(slide, 'TextBox 6'), entry['old_footer'])
    assert E.tostring(slide) == E.tostring(E.fromstring(original[entry['path']]))
for name, data in parts.items():
    if name.startswith(('ppt/notesSlides/', 'ppt/media/')):
        assert data == original[name]
for name, data in parts.items():
    if name.endswith('.rels'):
        owner = '' if name == '_rels/.rels' else posixpath.join(posixpath.dirname(posixpath.dirname(name)), posixpath.basename(name)[:-5])
        for rel in E.fromstring(data):
            if rel.get('TargetMode') != 'External':
                assert resolve(owner, rel.get('Target')) in parts
for path, expected in json.loads((W / 'protected-files.json').read_text()).items():
    assert hash_file(Path(path)) == expected
catalog = json.loads((FINAL / 'figures_and_images/native_equations.json').read_text(encoding='utf-8'))
assert len(catalog) == 29
for item in catalog:
    assert E.fromstring(parts[retained[item['slide'] - 1]['path']]).xpath('.//p:cNvPr[@name=$n]', n=item['shape'], namespaces=NS)
render_dir = W / 'rendered'
render_dir.mkdir(exist_ok=True)
for i, entry in enumerate(retained):
    before = source[entry['old_physical'] - 1].get_pixmap(alpha=False)
    after = pdf[i].get_pixmap(alpha=False)
    after.save(render_dir / ('slide-%02d.png' % (i + 1)))
    if 'old_footer' in entry:
        a = np.frombuffer(before.samples, np.uint8).reshape(before.height, before.width, 3)
        b = np.frombuffer(after.samples, np.uint8).reshape(after.height, after.width, 3)
        diff = np.any(a != b, axis=2)
        diff[499:522, 898:927] = False
        assert not diff.any(), entry['title']
    else:
        assert before.samples == after.samples, entry['title']
    if i >= 26:
        assert after.samples == supp[i - 26].get_pixmap(alpha=False).samples
    entry['physical'] = i + 1
    if i >= 26:
        entry['footer'] = 'B%d' % (i - 25)
assert len(pdf) == NEW_COUNT and len(supp) == NEW_COUNT - 26
assert sum(e['hidden'] for e in entries(parts)) == NEW_COUNT - 26
with ZipFile(W / 'updated.pptx') as z:
    assert z.testzip() is None
report = {'date': '2026-09-22', 'removed_slides': removed, 'main_slides': 26, 'hidden_backups': NEW_COUNT - 26,
          'total_slides': NEW_COUNT, 'supplementary_pages': NEW_COUNT - 26, 'native_equation_count': 29,
          'remaining_notes_and_media_byte_identical': True, 'speaking_files_unchanged': True,
          'retained_slide_content_unchanged_except_three_footers': True,
          'pdf_pages_pixel_identical_except_three_footers': True,
          'supplementary_pages_match_full_pdf': True, 'removed_slide_and_notes_archived_exactly': True,
          'package_relationships_valid': True, 'overview_refreshed_from_sections': chapters,
          'changed_pptx_parts': changed, 'removed_pptx_parts': sorted(deleted), 'slide_order': retained}
(W / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('Verified: %d slides, %d hidden backups and supplementary pages. Other content and notes preserved.' % (NEW_COUNT, NEW_COUNT - 26))
