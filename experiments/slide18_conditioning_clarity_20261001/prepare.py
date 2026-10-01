from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re, json, hashlib, os, posixpath

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
ARCHIVE = HERE / 'archive'
ARCHIVE.mkdir(exist_ok=True)
PART = 'ppt/slides/slide10.xml'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
BULLETS = [
    'Adjusts joint posture in the null space.',
    'Seeks postures away from singularities, where the EE loses a motion direction.',
]

with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx') as source:
    before = {n: hashlib.sha256(source.read(n)).hexdigest() for n in source.namelist()}
    (ARCHIVE / 'package_hashes_before.json').write_text(json.dumps(before, indent=2))
    with (FINAL / 'Thesis_Defense_gg0_v3.pptx').open('rb') as original:
        original.seek(source.start_dir)
        (ARCHIVE / 'original_zip_directory.bin').write_bytes(original.read())
    (ARCHIVE / 'zip_checkpoint.json').write_text(json.dumps({'start_dir': source.start_dir}))
    xml = source.read(PART).decode('utf-8')
    (ARCHIVE / 'original_slide10.xml').write_bytes(source.read(PART))
    edited = []

    def edit_shape(match):
        shape = match[0]
        if 'name="Conditioning role"' not in shape:
            return shape
        paragraphs = re.findall(r'<a:p>.*?</a:p>', shape, re.S)
        assert len(paragraphs) == 3
        replacements = []
        for paragraph, text in zip(paragraphs, BULLETS):
            replacement, count = re.subn(r'<a:t>.*?</a:t>', '<a:t>' + text + '</a:t>', paragraph, count=1, flags=re.S)
            assert count == 1
            replacements.append(replacement)
        edited.append('Conditioning role')
        return shape.replace(''.join(paragraphs), ''.join(replacements))

    updated = re.sub(r'<p:sp\b[^>]*>.*?</p:sp>', edit_shape, xml, flags=re.S)
    assert edited == ['Conditioning role']
    E.fromstring(updated)
    assert re.findall(r'<a14:m>.*?</a14:m>', xml, re.S) == re.findall(r'<a14:m>.*?</a14:m>', updated, re.S)
    (HERE / 'slide10.xml').write_text(updated, encoding='utf-8')
    overrides = {PART: updated.encode('utf-8')}

    presentation = E.fromstring(source.read('ppt/presentation.xml'))
    slides = presentation.find('{' + P + '}sldIdLst')
    keep = list(slides)[18].get('{' + R + '}id')
    for child in list(slides):
        if child.get('{' + R + '}id') != keep:
            slides.remove(child)
    for tag in ['extLst', 'custShowLst']:
        child = presentation.find('{' + P + '}' + tag)
        if child is not None:
            presentation.remove(child)
    rels = E.fromstring(source.read('ppt/_rels/presentation.xml.rels'))
    for rel in list(rels):
        if rel.get('Type').endswith('/slide') and rel.get('Id') != keep:
            rels.remove(rel)
    overrides['ppt/presentation.xml'] = E.tostring(presentation, encoding='utf-8', xml_declaration=True)
    overrides['ppt/_rels/presentation.xml.rels'] = E.tostring(rels, encoding='utf-8', xml_declaration=True)
    names, included, pending = set(source.namelist()), set(), ['']
    while pending:
        part = pending.pop()
        if part in included:
            continue
        if part:
            included.add(part)
        rels_name = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels') if part else '_rels/.rels'
        if rels_name not in names:
            continue
        included.add(rels_name)
        for rel in E.fromstring(overrides.get(rels_name, source.read(rels_name))):
            if rel.get('TargetMode') == 'External':
                continue
            target = rel.get('Target')
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part), target))
            assert target in names
            if target not in included:
                pending.append(target)
    types = E.fromstring(source.read('[Content_Types].xml'))
    for child in list(types):
        if child.tag.endswith('Override') and child.get('PartName').lstrip('/') not in included:
            types.remove(child)
    overrides['[Content_Types].xml'] = E.tostring(types, encoding='utf-8', xml_declaration=True)
    included.add('[Content_Types].xml')
    with ZipFile(HERE / 'preview_deck.pptx', 'w', ZIP_DEFLATED) as preview:
        for info in source.infolist():
            if info.filename in included:
                preview.writestr(info, overrides.get(info.filename, source.read(info.filename)))

if not (ARCHIVE / 'Thesis_Defense_gg0_v3.pdf').exists():
    os.link(FINAL / 'Thesis_Defense_gg0_v3.pdf', ARCHIVE / 'Thesis_Defense_gg0_v3.pdf')
verification = {
    'date': '2026-10-01', 'footer': 18, 'physical_slide': 19,
    'title': 'Null-space controller', 'conditioning_bullets': BULLETS,
    'rationale': 'Explain joint-posture adjustment and directly connect its purpose to singularities. It is not reference joint-position tracking.',
    'only_edited_shape': 'Conditioning role',
    'equations_other_slide_content_and_notes_preserved': True,
}
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))
