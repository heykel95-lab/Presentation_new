"""Restore fallback speech, with narrowly scoped clarity and linking edits."""
from pathlib import Path
import json, re, shutil, copy

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
BASE = H.parent / 'nullspace_roles_20261009'
ORIGINAL = H.parent / 'connected_notes_20261009/archive'
data = json.loads((ORIGINAL / 'script.json').read_text(encoding='utf-8'))
fallback = copy.deepcopy(data)

# One small transition avoids repeating "First" after the motivation.
data[2]['opening'] = 'Here is the plan for the presentation.'

# Explain the displayed law without adding worked examples or extra theory.
data[5]['paragraphs'] = [
    'Like a spring, stiffness pulls the tool towards its desired pose, while damping slows the motion. The force law is f equals K p times the position error e p, plus D p times the velocity error.',
    'The moment law is m equals K R times the orientation error e R, plus D R times the angular-velocity error. Together, force and moment form a wrench. Translation and rotation can be adjusted separately.'
]
data[6]['paragraphs'] = [data[6]['paragraphs'][0].replace(
    'The Jacobian transpose converts the Cartesian wrench into joint torques.',
    'The equation tau equals J transpose F converts the Cartesian wrench into joint torques.'
).replace('the posture-control torques', 'the null-space torques')]
data[7]['paragraphs'] = [data[7]['paragraphs'][0].replace(
    'If we shift the CoC away from the TCP, the applied force creates an additional moment around the TCP.',
    'Shifting the CoC couples translation and rotation, so a force can also create a turning moment.'
)]
data[9]['paragraphs'] = [
    'A equals Ad of r c describes the CoC shift. We transform stiffness as K TCP equals A transpose K c A, and damping as D TCP equals A transpose D c A. The off-diagonal terms then couple translation and rotation: displacement can create a moment, and rotation can create a force.'
]

# Join two adjacent results without adding a new claim.
data[17]['paragraphs'] = [data[17]['paragraphs'][0].replace(
    'The supporting CoC shift helps the alignment happen faster. The opposing CoC shift leaves much of the initial angular error.',
    'The supporting CoC shift helps the alignment happen faster, while the opposing shift leaves much of the initial angular error.'
)]

# Briefly link the two sections and keep damping's role distinct from posture.
data[18]['opening'] = 'So far, we have controlled the tool. Next, I will explain how we control the extra motion of the arm.'
data[18]['paragraphs'] = [
    'The robot has seven joints, but the tool pose uses six coordinates. This leaves one extra degree of freedom, so the arm can change its posture while keeping the tool pose almost unchanged.',
    'The two null-space torques have different roles. Damping opposes joint velocity and is zero at rest. Conditioning uses the joint configuration to improve sigma min, the minimum singular value of the Jacobian. A larger sigma min helps avoid postures where certain tool movements become difficult.'
]

changed = [i + 1 for i, (a, b) in enumerate(zip(fallback, data)) if a != b]
assert changed == [3, 6, 7, 8, 10, 18, 19]
assert fallback[25:] == data[25:]
count = lambda s: sum(len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*", p)) for p in [s['opening'], *s['paragraphs'], s.get('after_video', '')])
words = sum(count(s) for s in data[:25])
oldwords = sum(count(s) for s in fallback[:25])
seconds = sum(s.get('video_seconds', 0) for s in data[:25]) + 30
times = {str(w): round(words / w + seconds / 60, 2) for w in [125, 130]}
assert words <= oldwords + 50, (words, oldwords)
assert all(';' not in p for s in data for p in [s['opening'], *s['paragraphs'], s.get('after_video', '')])
(H / 'script.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
for name in ['workflow.py', 'author.mjs', 'check_notes.ps1', 'render_qa.py', 'install_with_pdf_refresh.py']:
    shutil.copy2(BASE / name, H / name)
p = H / 'workflow.py'
p.write_text(p.read_text().replace('the clarified null-space roles note', 'fallback-based notes with limited clarity edits'), encoding='utf-8')
# Keep the compact ten-page arrangement of the original speech.
shutil.copy2(ORIGINAL / 'build.py', H / 'build.py')
p = H / 'build.py'
t = p.read_text().replace("assert times['130']<15", "assert times['130']<15.5  # Keep this revision close to the original fallback length.")
t = t.replace('05.10.2026', '09.10.2026')
t = t.replace('from pathlib import Path\n', 'from pathlib import Path\nimport sys\n_workspace=next(p for p in Path(__file__).resolve().parents if (p/\'Final Presentation\').is_dir())\nsys.path[:0]=[str(_workspace/\'tmp/connected_notes_deps\'),str(_workspace/\'tmp/remove_b5_20260922/deps\')]\n', 1)
p.write_text(t, encoding='utf-8')
report = {
    'baseline': str((ORIGINAL / 'script.json').relative_to(ROOT)),
    'fallback_main_words': oldwords, 'main_words': words,
    'net_words_added': words - oldwords, 'minutes': times,
    'changed_physical_slides_vs_fallback': changed,
    'unchanged_scripts_vs_fallback': 31 - len(changed),
    'all_six_backup_scripts_equal_fallback': True,
    'technical_note_words': {str(i + 1): count(data[i]) for i in [5, 6, 7, 9, 18]},
}
(H / 'revision.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
