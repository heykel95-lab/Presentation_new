from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
from pypdf import PdfReader
import re, json, hashlib, posixpath, uuid, shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINAL = ROOT / 'Final Presentation'
ARCHIVE = HERE / 'archive'
ARCHIVE.mkdir(exist_ok=True)
PART = 'ppt/slides/slide20.xml'
RELS = 'ppt/slides/_rels/slide20.xml.rels'
MEDIA = 'ppt/media/contact_legend_per_plot.png'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
pdf = PdfReader(HERE / 'contact_legend_per_plot.pdf')
width, height = float(pdf.pages[0].mediabox.width), float(pdf.pages[0].mediabox.height)
positions = [{'plot': label, 'x': centre - width/2, 'y': 398, 'width': width, 'height': height}
             for label, centre in zip(['angular error', 'normal force', 'TCP moment'], [206, 506, 806])]
assert 398 + height < 485
shutil.copy2(FINAL / 'figures_and_images/manifest.json', ARCHIVE / 'manifest.json')

with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx') as source:
    before = {n: hashlib.sha256(source.read(n)).hexdigest() for n in source.namelist()}
    (ARCHIVE / 'package_hashes_before.json').write_text(json.dumps(before, indent=2))
    with (FINAL / 'Thesis_Defense_gg0_v3.pptx').open('rb') as original:
        original.seek(source.start_dir)
        (ARCHIVE / 'original_zip_directory.bin').write_bytes(original.read())
    (ARCHIVE / 'zip_checkpoint.json').write_text(json.dumps({'start_dir': source.start_dir}))
    xml = source.read(PART).decode('utf-8')
    (ARCHIVE / 'original_slide20.xml').write_bytes(source.read(PART))
    (ARCHIVE / 'original_slide20.xml.rels').write_bytes(source.read(RELS))
    maximum_id = max(map(int, re.findall(r'<p:cNvPr\b[^>]*\bid="(\d+)"', xml)))
    original_legend = next(s for s in re.findall(r'<p:pic\b[^>]*>.*?</p:pic>', xml, re.S)
                           if 'name="Figure - contact_legend"' in s)
    legends = []
    for i, position in enumerate(positions):
        shape = original_legend.replace('name="Figure - contact_legend"',
                                         'name="Legend - ' + position['plot'] + '"')
        if i:
            shape = re.sub(r'(<p:cNvPr\b[^>]*\bid=")\d+("[^>]*>)',
                           lambda m: m[1] + str(maximum_id + i) + m[2], shape, count=1)
            shape = re.sub(r'(<a16:creationId\b[^>]*\bid=")[^"]+("[^>]*/>)',
                           lambda m: m[1] + '{' + str(uuid.uuid4()).upper() + '}' + m[2], shape, count=1)
        for node, key, value in [('off', 'x', position['x']), ('off', 'y', position['y']),
                                 ('ext', 'cx', width), ('ext', 'cy', height)]:
            shape, count = re.subn(r'(<a:' + node + r'\b[^>]*\b' + key + r'=")\d+("[^>]*/>)',
                                   lambda m: m[1] + str(round(value * 12700)) + m[2], shape, count=1)
            assert count == 1
        legends.append(shape)
    updated = xml.replace(original_legend, ''.join(legends))
    E.fromstring(updated)
    assert updated.count('name="Legend - ') == 3
    relationships = source.read(RELS).decode('utf-8')
    assert relationships.count('../media/image51.png') == 1
    relationships = relationships.replace('../media/image51.png', '../media/contact_legend_per_plot.png')
    E.fromstring(relationships)
    overrides = {PART: updated.encode('utf-8'), RELS: relationships.encode('utf-8'),
                 MEDIA: (HERE / 'contact_legend_per_plot.png').read_bytes()}
    (HERE / 'slide20.xml').write_bytes(overrides[PART])
    (HERE / 'slide20.xml.rels').write_bytes(overrides[RELS])

    presentation = E.fromstring(source.read('ppt/presentation.xml'))
    slides = presentation.find('{' + P + '}sldIdLst')
    keep = list(slides)[17].get('{' + R + '}id')
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
    names, included, pending = set(source.namelist()) | {MEDIA}, set(), ['']
    def read(part):
        return overrides[part] if part in overrides else source.read(part)
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
        for rel in E.fromstring(read(rels_name)):
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
        for part in sorted(included):
            preview.writestr(part, read(part))

# The current PDF is exactly reconstructable from the previous turn's lossless
# original archive and verified append stream, without another full-size copy.
parent = HERE.parent / 'slide18_plain_dimension_20261001'
checkpoint = json.loads((parent / 'pdf_checkpoint.json').read_text())
current_hash = hashlib.sha256((FINAL / 'Thesis_Defense_gg0_v3.pdf').read_bytes()).hexdigest()
assert current_hash == checkpoint['updated_sha256']
(ARCHIVE / 'pdf_before.json').write_text(json.dumps({
    'base_delta_zip': str((parent / 'archive/Thesis_Defense_gg0_v3.pdf.delta.zip').relative_to(ROOT)),
    'append_files': [str((parent / 'presentation_pdf_update.bin').relative_to(ROOT))],
    'sha256': current_hash, 'size': (FINAL / 'Thesis_Defense_gg0_v3.pdf').stat().st_size,
}, indent=2))
verification = {'date': '2026-10-01', 'footer': 17, 'physical_slide': 18,
                'legend_layout': 'Three identical three-row colour keys, one centred beneath each plot.',
                'legend_positions_pt': positions, 'plot_sizes_positions_data_labels_and_timing_unchanged': True,
                'original_shared_legend_asset_preserved': True, 'notes_equations_media_and_other_slides_unchanged': True}
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))
