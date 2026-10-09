"""Finish the validated installation after safely refreshing the open PDF."""
from zipfile import ZipFile, ZIP_DEFLATED
import json
from workflow import H, ROOT, F, S, DECKS, sha, put

report = json.loads((H / 'verification.json').read_text())
assert report['visual_review_passed']
manifest = json.loads((H / 'archive/manifest.json').read_text())
for deck in DECKS:
    assert sha(deck) == report['decks'][deck.name]['sha256']
for name in ['script.json', 'sentence_prompts.json', 'Simple_speech.txt', 'build.py', 'README.txt']:
    assert sha(S / name) == sha(H / name), name
for path in [F / 'Simple_speech_updated.pdf', S / 'Simple_speech.pdf', F / 'Projector_Test_Versions/02_03_Improved_Speech.pdf']:
    assert sha(path) == sha(H / 'Simple_speech.pdf'), path
assert sha(S / 'verification.json') == sha(H / 'speech_verification.json')
put(H / 'READ_ME_FIRST.txt', F / 'Projector_Test_Versions/READ_ME_FIRST.txt')

names = [
    '01_Fallback_Original_Speech.pdf',
    '01_MP4_Light_Silent.pptx',
    '02_03_Improved_Speech.pdf',
    '02_WebM_Silent.pptx',
    '03_WMV_Silent.pptx',
    'READ_ME_FIRST.txt',
]
bundle = H / 'Projector_Test_Versions.zip'
with ZipFile(bundle, 'w', ZIP_DEFLATED, compresslevel=1) as archive:
    for name in names:
        archive.write(F / 'Projector_Test_Versions' / name, 'Projector_Test_Versions/' + name)
with ZipFile(bundle) as archive:
    import hashlib
    assert archive.testzip() is None
    assert archive.namelist() == ['Projector_Test_Versions/' + name for name in names]
    for name in names:
        with archive.open('Projector_Test_Versions/' + name) as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == sha(F / 'Projector_Test_Versions' / name)
put(bundle, F / 'Projector_Test_Versions.zip')
for name, digest in manifest['protected'].items():
    assert sha(ROOT / name) == digest, name
report.update(
    installed=True,
    atomic_replacement=True,
    zip_updated=True,
    zip_sha256=sha(bundle),
    speech_sha256=sha(H / 'Simple_speech.pdf'),
    matching_speech_pdf_refreshed_in_acrobat=True,
    acrobat_unsaved_changes_checked=True,
    acrobat_had_unsaved_changes=False,
    acrobat_page_preserved=True,
)
(H / 'verification.json').write_text(json.dumps(report, indent=2))
print('Complete: four decks, all speech copies, README and six-file ZIP synchronized; fallback preserved.')
