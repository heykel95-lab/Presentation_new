from pathlib import Path
from zipfile import ZipFile
import hashlib, json, os

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FOLDER = (ROOT / 'Final Presentation/Video/Projector_compatible').resolve()
DECK = ROOT / 'Final Presentation/Thesis_Defense_gg0_v3.pptx'
ROWS = [
    ('1', 2, '01_Motivation_contact.mp4', 'Slide_01_Motivation_contact.mp4', 'ppt/media/media1.mp4'),
    ('11', 12, '11_Impedance_response.mp4', 'Slide_11_Impedance_response.mp4', 'ppt/media/Plausibility_experiment_presentation.mp4'),
    ('19', 20, '19_Nullspace_damping.mp4', 'Slide_19_Nullspace_damping.mp4', 'ppt/media/Nullspace2_part1_0000-0023.mp4'),
    ('20', 21, '20_Nullspace_conditioning.mp4', 'Slide_20_Nullspace_conditioning.mp4', 'ppt/media/Nullspace2_part2_0023-end.mp4'),
    ('B1', 26, 'B1_Opposing_CoC_moment.mp4', 'Slide_B1_Opposing_CoC_moment.mp4', 'ppt/media/Opposing_moment_presentation.mp4'),
]

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

assert FOLDER.is_relative_to(ROOT.resolve())
deck_hash = sha(DECK)
report = []
with ZipFile(DECK) as archive:
    for footer, physical, old, new, part in ROWS:
        source, target = FOLDER / old, FOLDER / new
        assert source.resolve().parent == FOLDER and target.resolve().parent == FOLDER
        assert source.is_file() and not target.exists()
        digest = sha(source)
        with archive.open(part) as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest
        report.append({'printed_slide': footer, 'powerpoint_position': physical, 'old_name': old, 'new_name': new, 'sha256': digest, 'matches_embedded_video': True})

for row in report:
    (FOLDER / row['old_name']).rename(FOLDER / row['new_name'])
    assert sha(FOLDER / row['new_name']) == row['sha256']

readme = FOLDER / 'README.txt'
(HERE / 'original_README.txt').write_bytes(readme.read_bytes())
lines = [
    'VIDEOS USED IN THE PRESENTATION', '',
    'Names use the slide number printed on the slide, including backup B1.',
    'PowerPoint counts the title slide, so its slide positions differ.', '',
    'Printed slide | PowerPoint position | Video file',
]
lines.extend(f"{row['printed_slide']:>13} | {row['powerpoint_position']:>19} | {row['new_name']}" for row in report)
lines += ['', 'These are the five compatible standalone MP4 copies of the videos embedded',
          'in the main presentation. Play them in your video player if PowerPoint',
          'playback fails. The original recordings remain in the parent Video folder.',
          'Renaming these copies does not affect the embedded presentation videos.',
          'See ../../Projector_playback_help.txt for projector troubleshooting.', '']
pending = readme.with_name(readme.name + '.pending')
assert not pending.exists()
pending.write_text('\n'.join(lines), encoding='utf-8')
os.replace(pending, readme)
assert sha(DECK) == deck_hash
(HERE / 'verification.json').write_text(json.dumps({'videos': report, 'main_deck_unchanged': True, 'video_content_unchanged': True, 'main_deck_sha256': deck_hash}, indent=2))
print('Renamed all five used standalone videos by their printed slide numbers. Video contents and presentation are unchanged.')
