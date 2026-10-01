from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re, json, hashlib, posixpath, io
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINAL = ROOT / 'Final Presentation'
ARCHIVE = HERE / 'archive'
ARCHIVE.mkdir(exist_ok=True)
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'p': P, 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
PARTS = ['ppt/slides/slide36.xml', 'ppt/slides/slide37.xml', 'ppt/slides/slide13.xml']
LABELS = ['Without null-space control → Damping only', 'Conditioning only',
          'Disturbance without null-space control torque']

with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx') as source:
    before = {name: hashlib.sha256(source.read(name)).hexdigest() for name in source.namelist()}
    (ARCHIVE / 'package_hashes_before.json').write_text(json.dumps(before, indent=2))
    with (FINAL / 'Thesis_Defense_gg0_v3.pptx').open('rb') as original:
        original.seek(source.start_dir)
        (ARCHIVE / 'original_zip_directory.bin').write_bytes(original.read())
    (ARCHIVE / 'zip_checkpoint.json').write_text(json.dumps({'start_dir': source.start_dir}))
    overrides = {}
    for part, label in zip(PARTS, LABELS):
        original = source.read(part)
        (ARCHIVE / Path(part).name).write_bytes(original)
        xml = original.decode('utf-8')
        shape_name = 'Nullspace2 label' if 'slide13' not in part else 'Setting no torque'
        old = next(s for s in re.findall(r'<p:sp\b[^>]*>.*?</p:sp>', xml, re.S)
                   if 'name="' + shape_name + '"' in s)
        if shape_name == 'Setting no torque':
            # One bullet with two deliberate lines, using the existing font.
            run = re.search(r'<a:r>.*?</a:r>', old, re.S)[0]
            first = re.sub(r'<a:t>.*?</a:t>', '<a:t>Disturbance without</a:t>', run, count=1, flags=re.S)
            second = re.sub(r'<a:t>.*?</a:t>', '<a:t>null-space control torque</a:t>', run, count=1, flags=re.S)
            new = old.replace(run, first + '<a:br/>' + second)
            new = new.replace('cy="431800"', 'cy="736600"')
            xml = xml.replace(old, new)
            # Give the expanded first row room while retaining the two-column grid.
            for name in ['Setting conditioning', 'Setting combined']:
                row = next(s for s in re.findall(r'<p:sp\b[^>]*>.*?</p:sp>', xml, re.S)
                           if 'name="' + name + '"' in s)
                moved = row.replace('y="5181600"', 'y="5524500"')
                assert row != moved
                xml = xml.replace(row, moved)
        else:
            new = re.sub(r'<a:t>.*?</a:t>', '<a:t>' + label + '</a:t>', old, count=1, flags=re.S)
            xml = xml.replace(old, new)
        E.fromstring(xml)
        overrides[part] = xml.encode('utf-8')
        (HERE / Path(part).name).write_bytes(overrides[part])

    # Small static QA deck: exact slide shapes and posters, with video payloads
    # omitted only from this throwaway preview. Active video parts are untouched.
    preview_overrides = dict(overrides)
    for name in ['ppt/media/Nullspace2_part1_0000-0023_poster.png',
                 'ppt/media/Nullspace2_part2_0023-end_poster.png']:
        picture = Image.open(io.BytesIO(source.read(name)))
        picture.thumbnail((600,600), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        picture.save(buffer, format='PNG', optimize=True)
        preview_overrides[name] = buffer.getvalue()
    for part in PARTS[:2]:
        xml = preview_overrides[part].decode('utf-8')
        xml = re.sub(r'<a:videoFile\b[^>]*/>', '', xml)
        xml = re.sub(r'<p14:media\b[^>]*/>', '', xml)
        xml = re.sub(r'<a:hlinkClick\b[^>]*action="ppaction://media"[^>]*/>', '', xml)
        xml = xml.replace('<p:nvPr><p:extLst><p:ext uri="{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}"></p:ext></p:extLst></p:nvPr>', '<p:nvPr/>')
        xml = re.sub(r'<p:timing\b[^>]*>.*?</p:timing>', '', xml, flags=re.S)
        preview_overrides[part] = xml.encode('utf-8')
        relname = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')
        rels = E.fromstring(source.read(relname))
        for rel in list(rels):
            if rel.get('Type').endswith('/video') or rel.get('Type').endswith('/media'):
                rels.remove(rel)
        preview_overrides[relname] = E.tostring(rels, encoding='utf-8', xml_declaration=True)
    presentation = E.fromstring(source.read('ppt/presentation.xml'))
    slides = presentation.find('{' + P + '}sldIdLst')
    keep = [list(slides)[i].get('{' + R + '}id') for i in [19,20,21]]
    for child in list(slides):
        if child.get('{' + R + '}id') not in keep:
            slides.remove(child)
    for tag in ['extLst', 'custShowLst']:
        child = presentation.find('{' + P + '}' + tag)
        if child is not None: presentation.remove(child)
    rels = E.fromstring(source.read('ppt/_rels/presentation.xml.rels'))
    for rel in list(rels):
        if rel.get('Type').endswith('/slide') and rel.get('Id') not in keep: rels.remove(rel)
    preview_overrides['ppt/presentation.xml'] = E.tostring(presentation, encoding='utf-8', xml_declaration=True)
    preview_overrides['ppt/_rels/presentation.xml.rels'] = E.tostring(rels, encoding='utf-8', xml_declaration=True)
    def read(name): return preview_overrides[name] if name in preview_overrides else source.read(name)
    included, pending, names = set(), [''], set(source.namelist())
    while pending:
        part = pending.pop()
        if part in included: continue
        if part: included.add(part)
        relname = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part)+'.rels') if part else '_rels/.rels'
        if relname not in names: continue
        included.add(relname)
        for rel in E.fromstring(read(relname)):
            if rel.get('TargetMode') == 'External': continue
            target = rel.get('Target')
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part), target))
            if target not in included: pending.append(target)
    types = E.fromstring(source.read('[Content_Types].xml'))
    for child in list(types):
        if child.tag.endswith('Override') and child.get('PartName').lstrip('/') not in included: types.remove(child)
    preview_overrides['[Content_Types].xml'] = E.tostring(types, encoding='utf-8', xml_declaration=True)
    included.add('[Content_Types].xml')
    assert not any(name.endswith('.mp4') for name in included)
    with ZipFile(HERE / 'preview_deck.pptx', 'w', ZIP_DEFLATED) as output:
        for name in sorted(included): output.writestr(name, read(name))

parent = HERE.parent / 'slide17_individual_legends_20261001'
prior = json.loads((parent / 'pdf_checkpoint.json').read_text())
current = (FINAL / 'Thesis_Defense_gg0_v3.pdf').read_bytes()
assert hashlib.sha256(current).hexdigest() == prior['updated_sha256']
(ARCHIVE / 'pdf_before.json').write_text(json.dumps({
    'parent_recipe': str((parent / 'archive/pdf_before.json').relative_to(ROOT)),
    'append_file': str((parent / 'presentation_pdf_update.bin').relative_to(ROOT)),
    'sha256': prior['updated_sha256'], 'size': len(current)
}, indent=2))
verification = {'date':'2026-10-01', 'physical_slides':[20,21,22], 'footers':[19,20,21],
    'video_captions': LABELS[:2], 'baseline_label': LABELS[2],
    'video_settings_source':'User description on 2026-10-01; no numerical gains inferred.',
    'notes_and_speaking_files_unchanged':True, 'video_playback_audio_posters_and_split_unchanged':True}
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2, ensure_ascii=False)+'\n',encoding='utf-8')
(HERE / 'source-notes.txt').write_text('Edit three existing labels according to the user description. Keep inherited Arial fonts and sizes, all original videos, playback, notes and equations. Artifact-tool import previously failed on native a14:m Office Math; narrow package edits preserve that content. Preview deck omits video binaries only for static rendering.\n', encoding='utf-8')
print('Prepared three labels and a static QA deck.')
