from pathlib import Path
import json,shutil,re
H=Path(__file__).resolve().parent;ROOT=H.parents[1];BASE=H.parent/'expanded_explanations_20261009';S=ROOT/'Final Presentation/Speaking/simple_speech'
data=json.loads((S/'script.json').read_text(encoding='utf-8'))
fixes={
 'alignment; on the right':'alignment, while on the right',
 'CoC; A transpose':'CoC, and A transpose',
 'separately; the coupling':'separately. The coupling',
 'surface; closer':'surface. Closer',
 'the tool; the null-space':'the tool, while the null-space',
 'posture response; the two':'posture response. The two',
 'remaining error; this comparison':'remaining error. This comparison',
}
changed=[]
for s in data:
 before=json.dumps(s)
 for key in ['opening','paragraphs','after_video']:
  if key not in s:continue
  values=s[key] if isinstance(s[key],list) else [s[key]]
  new=[]
  for t in values:
   for old,replacement in fixes.items():t=t.replace(old,replacement)
   assert ';' not in t
   new.append(t)
  s[key]=new if isinstance(s[key],list) else new[0]
 if json.dumps(s)!=before:changed.append(s['physical'])
assert changed==[9,10,16,19,25,29]
(H/'script.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['workflow.py','author.mjs','check_notes.ps1','render_qa.py']:
 shutil.copy2(BASE/name,H/name)
shutil.copy2(S/'build.py',H/'build.py')
p=H/'workflow.py';t=p.read_text();t=t.replace('the five expanded notes','six notes with punctuation corrections');p.write_text(t,encoding='utf-8')
for name in ['README.txt','READ_ME_FIRST.txt']:
 t=(BASE/name).read_text(encoding='utf-8').replace('1,813','1,816').replace('16.05','16.08').replace('16.60','16.63').replace('experiments/expanded_explanations_20261009/','experiments/notes_punctuation_20261009/')
 (H/name).write_text(t,encoding='utf-8')
words=sum(len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*",' '.join([s['opening'],*s['paragraphs'],s.get('after_video','')]))) for s in data[:25])
assert words==1816,words
print('Prepared seven punctuation fixes across six notes. Main speech: 1,816 words.')
