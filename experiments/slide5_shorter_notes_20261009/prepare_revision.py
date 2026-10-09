from pathlib import Path
import json,re,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[1];BASE=H.parent/'notes_punctuation_20261009';S=ROOT/'Final Presentation/Speaking/simple_speech'
data=json.loads((S/'script.json').read_text(encoding='utf-8'))
count=lambda s:sum(len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*",p)) for p in [s['opening'],*s['paragraphs'],s.get('after_video','')])
old=count(data[5]);assert data[5]['label']=='Slide 5'
data[5]['opening']='Cartesian impedance control makes the tool behave like a spring and a damper.'
data[5]['paragraphs']=[
 'The force law is f equals K p times e p, plus D p times the velocity error. Here, e p is desired minus measured position. Stiffness pulls the tool towards its target, while damping opposes motion for a fixed target.',
 'The moment law has the same form: m equals K R times e R, plus D R times the angular-velocity error. Here, e R is the rotation angle times its axis. Together, force and moment form the wrench F. The zero off-diagonal blocks keep translation and rotation separate.'
]
(H/'script.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['workflow.py','author.mjs','check_notes.ps1','render_qa.py']:
 shutil.copy2(BASE/name,H/name)
shutil.copy2(S/'build.py',H/'build.py')
p=H/'workflow.py';t=p.read_text().replace('six notes with punctuation corrections','the shortened slide 5 note');p.write_text(t,encoding='utf-8')
words=sum(count(s) for s in data[:25]);seconds=sum(s.get('video_seconds',0) for s in data[:25])+30
minutes130=round(words/130+seconds/60,2);minutes125=round(words/125+seconds/60,2)
for name in ['README.txt','READ_ME_FIRST.txt']:
 t=(BASE/name).read_text(encoding='utf-8')
 t=t.replace('1,816',f'{words:,}').replace('16.07',f'{minutes130:.2f}').replace('16.63',f'{minutes125:.2f}')
 t=t.replace('Revision of 9 October 2026: expanded explanations after approval of a slightly longer talk.','Revision of 9 October 2026: shortened slide 5 impedance-law speech; all other notes retained.')
 t=t.replace('approximately 16.1 minutes',f'approximately {minutes130:.1f} minutes').replace('roughly 16-17 minutes','roughly 15-16 minutes')
 t=t.replace('experiments/notes_punctuation_20261009/','experiments/slide5_shorter_notes_20261009/')
 (H/name).write_text(t,encoding='utf-8')
report={'physical':6,'footer':5,'old_note_words':old,'new_note_words':count(data[5]),'main_words':words,'minutes_at_130':minutes130,'minutes_at_125':minutes125}
(H/'revision.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
