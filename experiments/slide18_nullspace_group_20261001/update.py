from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re, json, shutil, hashlib

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
ARCHIVE = HERE / 'archive'
ARCHIVE.mkdir(exist_ok=True)
PART = 'ppt/slides/slide10.xml'
HEADING = 'Redundancy and null-space motion:'
BODY = ('At full Jacobian rank, one null-space direction allows several joints '
        'to move together without changing the instantaneous motion of the EE.')
for name in ['Thesis_Defense_gg0_v3.pdf', 'Supplementary_slides.pdf']:
    if not (ARCHIVE / name).exists():
        shutil.copy2(FINAL / name, ARCHIVE / name)

with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx') as source:
    xml = source.read(PART).decode('utf-8')
    assert 'Primary Cartesian task:' in xml, 'Expected the original slide.'
    (ARCHIVE / 'original_slide10.xml').write_bytes(source.read(PART))
    seen = []

    def edit(match):
        shape = match[0]
        nv = re.search(r'<p:cNvPr\b[^>]*\bname="([^"]+)"', shape)
        if not nv:
            return shape
        name = nv[1]
        if name in {'Cartesian task heading', 'Kinematic preservation'}:
            seen.append(name)
            return ''
        if name not in {'Redundancy heading', 'Rank qualification'}:
            return shape
        seen.append(name)
        if name == 'Redundancy heading':
            shape = shape.replace('Redundant direction:', HEADING)
        else:
            paragraphs = re.findall(r'<a:p>.*?</a:p>', shape, re.S)
            assert len(paragraphs) == 2
            merged = paragraphs[0].replace(
                'One null-space direction at full Jacobian rank.', BODY)
            shape = shape.replace(paragraphs[0] + paragraphs[1], merged)
            assert shape.count('<a:buChar ') == 1
        shape, count = re.subn(
            r'(<a:ext\b[^>]*\bcx=")\d+("[^>]*/>)',
            lambda m: m[1] + str(820 * 12700) + m[2], shape, count=1)
        assert count == 1
        return shape

    updated = re.sub(r'<p:sp\b[^>]*>.*?</p:sp>', edit, xml, flags=re.S)
    assert set(seen) == {'Cartesian task heading', 'Kinematic preservation',
                         'Redundancy heading', 'Rank qualification'}
    E.fromstring(updated)
    assert 'Primary Cartesian task' not in updated
    assert re.findall(r'<m:oMath\b.*?</m:oMath>', xml, re.S) == re.findall(
        r'<m:oMath\b.*?</m:oMath>', updated, re.S)
    before = {n: hashlib.sha256(source.read(n)).hexdigest()
              for n in source.namelist()}
    (ARCHIVE / 'package_hashes_before.json').write_text(json.dumps(before, indent=2))
    with ZipFile(HERE / 'updated.pptx', 'w', ZIP_DEFLATED) as target:
        for info in source.infolist():
            target.writestr(info, updated.encode('utf-8') if info.filename == PART
                           else source.read(info.filename))

with ZipFile(HERE / 'updated.pptx') as result:
    assert set(result.namelist()) == set(before)
    changed = [n for n in result.namelist()
               if hashlib.sha256(result.read(n)).hexdigest() != before[n]]
    assert changed == [PART]

verification = {
    'date': '2026-10-01', 'footer': 18, 'physical_slide': 19,
    'title': 'Null-space controller', 'combined_heading': HEADING,
    'single_bullet': BODY, 'removed_label': 'Primary Cartesian task:',
    'changed_package_parts': changed,
    'all_native_equations_preserved': True,
    'damping_and_conditioning_sections_unchanged': True,
    'notes_media_and_all_other_slides_preserved': True,
}
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))
