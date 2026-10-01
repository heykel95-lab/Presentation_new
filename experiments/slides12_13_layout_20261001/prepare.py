from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re, json, hashlib, os, posixpath

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
ARCHIVE = HERE / 'archive'
ARCHIVE.mkdir(exist_ok=True)
PARTS = ['ppt/slides/slide14.xml', 'ppt/slides/slide15.xml']
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
changed = {}

def edit_shape(match):
    shape = match[0]
    name_match = re.search(r'<p:cNvPr\b[^>]*\bname="([^"]+)"', shape)
    if not name_match:
        return shape
    name = name_match[1]
    if name.startswith('Equation - equation_'):
        coords = {'x': 60, 'y': 360}
    elif name.startswith('Figure ') and '_plausibility' in name:
        coords = {'y': 89}
    elif name == 'Validation input heading':
        coords = {'x': 60, 'y': 61, 'cx': 840, 'cy': 30}
        shape = shape.replace('algn="ctr"', 'algn="l"')
        shape = shape.replace('sz="1800"', 'sz="2200"')
        shape = shape.replace('<a:srgbClr val="000000"/>', '<a:srgbClr val="17365D"/>')
    else:
        return shape
    for key, value in coords.items():
        node = 'ext' if key.startswith('c') else 'off'
        shape, count = re.subn(
            r'(<a:' + node + r'\b[^>]*\b' + key + r'=")\d+("[^>]*/>)',
            lambda m: m[1] + str(round(value * 12700)) + m[2], shape, count=1)
        assert count == 1, (name, key)
    return shape

with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx') as source:
    before = {n: hashlib.sha256(source.read(n)).hexdigest() for n in source.namelist()}
    (ARCHIVE / 'package_hashes_before.json').write_text(json.dumps(before, indent=2))
    # Preserve the exact original central directory for an in-place ZIP rollback.
    with (FINAL / 'Thesis_Defense_gg0_v3.pptx').open('rb') as original:
        original.seek(source.start_dir)
        (ARCHIVE / 'original_zip_directory.bin').write_bytes(original.read())
    (ARCHIVE / 'zip_checkpoint.json').write_text(json.dumps({'start_dir': source.start_dir}))
    for part in PARTS:
        original = source.read(part)
        (ARCHIVE / Path(part).name).write_bytes(original)
        xml = original.decode('utf-8')
        updated = re.sub(r'<p:(?:sp|pic)\b[^>]*>.*?</p:(?:sp|pic)>', edit_shape, xml, flags=re.S)
        assert updated != xml
        E.fromstring(updated)
        assert re.findall(r'<a14:m>.*?</a14:m>', xml, re.S) == re.findall(r'<a14:m>.*?</a14:m>', updated, re.S)
        assert re.findall(r'<a:t>.*?</a:t>', xml, re.S) == re.findall(r'<a:t>.*?</a:t>', updated, re.S)
        changed[part] = updated.encode('utf-8')
        (HERE / Path(part).name).write_bytes(changed[part])

    # Native rendering only needs the two edited slides. Keep their complete
    # relationship graph, including inherited masters, notes and figure assets.
    presentation = E.fromstring(source.read('ppt/presentation.xml'))
    slides = presentation.find('{' + P + '}sldIdLst')
    keep_ids = {list(slides)[i].get('{' + R + '}id') for i in [12, 13]}
    for child in list(slides):
        if child.get('{' + R + '}id') not in keep_ids:
            slides.remove(child)
    for tag in ['extLst', 'custShowLst']:
        child = presentation.find('{' + P + '}' + tag)
        if child is not None:
            presentation.remove(child)
    presentation_rels = E.fromstring(source.read('ppt/_rels/presentation.xml.rels'))
    for rel in list(presentation_rels):
        if rel.get('Type').endswith('/slide') and rel.get('Id') not in keep_ids:
            presentation_rels.remove(rel)
    overrides = dict(changed)
    overrides['ppt/presentation.xml'] = E.tostring(presentation, encoding='utf-8', xml_declaration=True)
    overrides['ppt/_rels/presentation.xml.rels'] = E.tostring(presentation_rels, encoding='utf-8', xml_declaration=True)
    names = set(source.namelist())
    included = set()
    pending = ['']
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
        rels = E.fromstring(overrides.get(rels_name, source.read(rels_name)))
        for rel in rels:
            if rel.get('TargetMode') == 'External':
                continue
            target = rel.get('Target')
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part), target))
            assert target in names, target
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

# Hard links retain the original PDF bytes without duplicating them on a full
# disk. Final PDFs are installed by replacement, never by overwriting the inode.
for name in ['Thesis_Defense_gg0_v3.pdf', 'Supplementary_slides.pdf']:
    if not (ARCHIVE / name).exists():
        os.link(FINAL / name, ARCHIVE / name)

verification = {
    'date': '2026-10-01', 'footers': [12, 13], 'physical_slides': [13, 14],
    'equation_origin_pt': [60, 360], 'heading_origin_pt': [60, 61],
    'heading_style': 'Arial 22 pt regular, navy 17365D, left aligned',
    'plot_origin_pt': [155, 89], 'plot_size_pt': [650, 269.6105511811024],
    'original_equation_xml_and_visible_text_preserved': True,
    'planned_changed_package_parts': PARTS,
}
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))
print('Preview deck bytes:', (HERE / 'preview_deck.pptx').stat().st_size)
