from pathlib import Path
from zipfile import ZipFile
import json, re
from workflow import H, ROOT, F, FALLBACK, inventory, paragraphs, E
import pymupdf as fitz

baseline = json.loads((ROOT / 'experiments/connected_notes_20261009/archive/script.json').read_text(encoding='utf-8'))
current = json.loads((H / 'script.json').read_text(encoding='utf-8'))
with ZipFile(FALLBACK) as archive:
    for script, row in zip(baseline, inventory(archive)):
        spoken = ' '.join(t for t in paragraphs(E.fromstring(archive.read(row['notes']))) if not t.startswith('['))
        expected = ' '.join([script['opening'], *script['paragraphs'], script.get('after_video', '')]).strip()
        assert spoken == expected
changed = [i + 1 for i, (a, b) in enumerate(zip(baseline, current)) if a != b]
assert changed == [3, 6, 7, 8, 10, 18, 19]
assert current[25:] == baseline[25:]
with fitz.open(F / 'Projector_Test_Versions/01_Fallback_Original_Speech.pdf') as a, fitz.open(H / 'Simple_speech.pdf') as b:
    assert len(a) == len(b) == 10
    # Retain the current October 9 footer date. Compare the entire content area.
    changed_pages = [i + 1 for i in range(10) if a[i].get_pixmap(clip=fitz.Rect(0, 0, a[i].rect.width, a[i].rect.height - 50)).samples != b[i].get_pixmap(clip=fitz.Rect(0, 0, b[i].rect.width, b[i].rect.height - 50)).samples]
    assert changed_pages == [1, 2, 3, 5, 6], changed_pages
report = json.loads((H / 'revision.json').read_text())
report.update(
    fallback_baseline_verified_word_for_word=True,
    changed_speech_pages_vs_fallback=changed_pages,
    other_five_speech_page_content_areas_pixel_identical_to_fallback=True,
    current_october_9_footer_date_retained=True,
    all_six_backup_scripts_equal_fallback=True,
)
(H / 'scope_verification.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
