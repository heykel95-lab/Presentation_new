from pathlib import Path
import json,re,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[1];BASE=H.parent/'connected_notes_20261009';S=ROOT/'Final Presentation/Speaking/simple_speech'
data=json.loads((S/'script.json').read_text(encoding='utf-8'))

# Five focused expansions follow the user's explicit preference for a little
# more speaking time. Preserve the connected speech on every other slide.
s=data[5]
s['paragraphs'][0]+=' If I push the tool and hold it still, the damping term vanishes, but the spring term remains because the position error remains. Once I release the tool, that spring term drives it back, while damping slows the return.'
s['paragraphs'][1]+=' During contact, lower rotational stiffness therefore lets the surface moment turn the tool more easily, even with a fixed desired orientation.'
s=data[6]
s['paragraphs'][0]+=' After each update, we compare the reference and measured state again. If contact changes the tool pose, these errors change the wrench in the next cycle, so the response adapts continuously.'
s=data[7]
s['paragraphs'][0]+=' For a force parallel to r c, the cross product is zero, so this added moment vanishes.'
s=data[9]
s['paragraphs'].append('We transform stiffness and damping separately; the coupling is between translation and rotation within each matrix. When the CoC coincides with the TCP, r c is zero and A becomes the identity, recovering the original uncoupled matrices.')
s=data[18]
s['paragraphs'][1]=s['paragraphs'][1].replace('It moves the posture towards a larger minimum singular value of J, called sigma min, helping avoid directions in which tool motion becomes difficult.','It seeks a posture with a larger minimum singular value of J, called sigma min. A small sigma min means that tool motion in one direction requires large joint velocities, so increasing it helps move away from such a posture.')
s['paragraphs'].append('Damping can therefore bring motion to rest in an unfavourable posture. Conditioning addresses the posture itself, which is why combining the two can be useful.')
(H/'script.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['workflow.py','author.mjs','check_notes.ps1','check_full_decks.ps1','render_qa.py']:
 shutil.copy2(BASE/name,H/name)
shutil.copy2(S/'build.py',H/'build.py')
w=(H/'workflow.py').read_text()
w=w.replace("protected=[FALLBACK,", "protected=[FALLBACK,F/'Projector_Test_Versions/01_Fallback_Original_Speech.pdf',")
w=w.replace("   changes[src['notes']]=dump(r)","   if dump(r)!=old.read(src['notes']):changes[src['notes']]=dump(r)")
w=w.replace("changes confined to 31 notes bodies.","changes confined to the five expanded notes.")
w=w.replace(" put(H/'archive/speech.pdf',F/'Projector_Test_Versions/01_Fallback_Original_Speech.pdf')\n",'')
(H/'workflow.py').write_text(w,encoding='utf-8')
b=(H/'build.py').read_text()
b=b.replace(" assert times['130']<15"," assert times['130']<17  # User explicitly allows slightly longer explanations.")
b=b.replace('outside the 15-minute main talk','outside the main talk')
(H/'build.py').write_text(b,encoding='utf-8')
count=lambda ss:sum(len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*",' '.join([s['opening'],*s['paragraphs'],s.get('after_video','')]))) for s in ss)
words=count(data[:25]);video=sum(s.get('video_seconds',0) for s in data[:25]);timing=words/130+(video+30)/60
print(json.dumps({'main_words':words,'estimated_minutes_at_130':round(timing,2),'at_125':round(words/125+(video+30)/60,2),'expanded_physical_slides':[6,7,8,10,19]},indent=2))
