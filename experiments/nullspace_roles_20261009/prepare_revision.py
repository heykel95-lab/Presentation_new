from pathlib import Path
import json, re, shutil

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
BASE = H.parent / 'slide5_shorter_notes_20261009'
S = ROOT / 'Final Presentation/Speaking/simple_speech'
old = 'Damping can therefore bring motion to rest in an unfavourable posture. Conditioning addresses the posture itself, which is why combining the two can be useful.'
new = 'When combined, conditioning guides the arm towards a better configuration, while damping slows the resulting null-space motion.'
data = json.loads((S / 'script.json').read_text(encoding='utf-8'))
assert data[18]['label'] == 'Slide 18'
assert data[18]['paragraphs'][-1] == old
data[18]['paragraphs'][-1] = new
(H / 'script.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
for name in ['workflow.py', 'author.mjs', 'check_notes.ps1', 'render_qa.py']:
    shutil.copy2(BASE / name, H / name)
shutil.copy2(S / 'build.py', H / 'build.py')
p = H / 'workflow.py'
p.write_text(p.read_text().replace('the shortened slide 5 note', 'the clarified null-space roles note'), encoding='utf-8')
count = lambda s: sum(len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*", p)) for p in [s['opening'], *s['paragraphs'], s.get('after_video', '')])
words = sum(count(s) for s in data[:25])
seconds = sum(s.get('video_seconds', 0) for s in data[:25]) + 30
times = {str(w): round(words / w + seconds / 60, 2) for w in [125, 130]}
for name in ['README.txt', 'READ_ME_FIRST.txt']:
    t = (BASE / name).read_text(encoding='utf-8')
    t = t.replace('1,724', f'{words:,}').replace('15.36', f'{times["130"]:.2f}').replace('15.89', f'{times["125"]:.2f}')
    t = t.replace('Revision of 9 October 2026: shortened slide 5 impedance-law speech; all other notes retained.', 'Revision of 9 October 2026: clarified the separate roles of null-space damping and conditioning. The shortened slide 5 speech is retained.')
    t = t.replace('approximately 15.4 minutes', f'approximately {times["130"]:.1f} minutes')
    t = t.replace('experiments/slide5_shorter_notes_20261009/', 'experiments/nullspace_roles_20261009/')
    (H / name).write_text(t, encoding='utf-8')
(H / 'revision.json').write_text(json.dumps({'physical': 19, 'footer': 18, 'old_text': old, 'new_text': new, 'main_words': words, 'minutes': times}, indent=2))
print(json.dumps({'main_words': words, 'minutes': times, 'replacement': new}, indent=2))
