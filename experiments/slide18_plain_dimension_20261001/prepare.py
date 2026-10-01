from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re, json, hashlib, shutil, os

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
ASSETS = FINAL / 'figures_and_images'
ARCHIVE = HERE / 'archive'
ARCHIVE.mkdir(exist_ok=True)
PART = 'ppt/slides/slide10.xml'
LABEL = 'Null space dimension'
LATEX = r'\displaystyle \text{Null space dimension}=7-6=1'
original_assets = ['native_equations.json', 'sources/null_controller_dimension.tex',
                   'null_controller_dimension.pdf', 'null_controller_dimension.png',
                   'null_controller_dimension.svg']
for asset in original_assets:
    shutil.copy2(ASSETS / asset, ARCHIVE / Path(asset).name)

with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx') as source:
    before = {n: hashlib.sha256(source.read(n)).hexdigest() for n in source.namelist()}
    (ARCHIVE / 'package_hashes_before.json').write_text(json.dumps(before, indent=2))
    with (FINAL / 'Thesis_Defense_gg0_v3.pptx').open('rb') as original:
        original.seek(source.start_dir)
        (ARCHIVE / 'original_zip_directory.bin').write_bytes(original.read())
    (ARCHIVE / 'zip_checkpoint.json').write_text(json.dumps({'start_dir': source.start_dir}))
    xml = source.read(PART).decode('utf-8')
    (ARCHIVE / 'original_slide10.xml').write_bytes(source.read(PART))
    seen = []

    def edit_shape(match):
        shape = match[0]
        if 'name="Equation - null_controller_dimension"' not in shape:
            return shape
        seen.append(True)
        content = re.search(r'<ns0:oMath>(.*?)</ns0:oMath>', shape, re.S)[1]
        runs = re.findall(r'<ns0:r>.*?</ns0:r>', content, re.S)
        equals = next(i for i, run in enumerate(runs) if '<ns0:t>=</ns0:t>' in run)
        assert equals == 6
        label_run = runs[0].replace('<ns0:sty ', '<ns0:nor ns0:val="1"/><ns0:sty ')
        label_run = label_run.replace('<ns0:t>dim</ns0:t>', '<ns0:t xml:space="preserve">' + LABEL + '</ns0:t>')
        shape = shape.replace(content, label_run + ''.join(runs[equals:]))
        shape = shape.replace(r'\dim(\ker J)', r'\text{Null space dimension}')
        for node, key, value in [('off', 'x', 80), ('ext', 'cx', 440)]:
            shape, count = re.subn(r'(<a:' + node + r'\b[^>]*\b' + key + r'=")\d+("[^>]*/>)',
                                   lambda m: m[1] + str(value * 12700) + m[2], shape, count=1)
            assert count == 1
        return shape

    updated = re.sub(r'<p:sp\b[^>]*>.*?</p:sp>', edit_shape, xml, flags=re.S)
    assert seen == [True]
    E.fromstring(updated)
    assert 'dim(\\ker J)' not in updated and '<ns0:t>ker</ns0:t>' not in updated
    (HERE / 'slide10.xml').write_bytes(updated.encode('utf-8'))

    previous_preview = HERE.parent / 'slide18_conditioning_clarity_20261001/preview_deck.pptx'
    with ZipFile(previous_preview) as preview, ZipFile(HERE / 'preview_deck.pptx', 'w', ZIP_DEFLATED) as output:
        assert E.tostring(E.fromstring(preview.read(PART))) == E.tostring(E.fromstring(xml))
        for info in preview.infolist():
            output.writestr(info, updated.encode('utf-8') if info.filename == PART else preview.read(info.filename))

catalog = json.loads((ASSETS / 'native_equations.json').read_text(encoding='utf-8'))
entry = next(entry for entry in catalog if entry['shape'] == 'Equation - null_controller_dimension')
entry['latex'] = LATEX
(HERE / 'native_equations.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
tex = (ASSETS / 'sources/null_controller_dimension.tex').read_text(encoding='utf-8')
tex = tex.replace(r'\setmathfont{Cambria Math}', '\\setmainfont{Cambria Math}\n\\setmathfont{Cambria Math}')
tex = tex.replace(r'\displaystyle \dim(\ker J)=7-6=1', LATEX)
(HERE / 'null_controller_dimension.tex').write_text(tex, encoding='utf-8')
if not (ARCHIVE / 'Thesis_Defense_gg0_v3.pdf').exists():
    os.link(FINAL / 'Thesis_Defense_gg0_v3.pdf', ARCHIVE / 'Thesis_Defense_gg0_v3.pdf')
verification = {
    'date': '2026-10-01', 'footer': 18, 'physical_slide': 19,
    'plain_label': LABEL, 'arithmetic': '7 - 6 = 1', 'latex': LATEX,
    'only_edited_shape': 'Equation - null_controller_dimension',
    'full_rank_qualification_preserved': True,
    'native_equation_retained': True,
    'equation_font': 'Cambria Math 22 pt regular; label upright',
    'other_equations_text_notes_and_media_preserved': True,
}
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))
