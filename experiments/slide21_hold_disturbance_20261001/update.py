from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re, json, shutil, hashlib

HERE=Path(__file__).resolve().parent
FINAL=HERE.parents[1]/'Final Presentation'
ARCHIVE=HERE/'archive'
ARCHIVE.mkdir(exist_ok=True)
for name in ['Thesis_Defense_gg0_v3.pdf','Supplementary_slides.pdf']:
    if not (ARCHIVE/name).exists():shutil.copy2(FINAL/name,ARCHIVE/name)
PART='ppt/slides/slide13.xml'
updates={
    'Disturbance heading':{'cx':860},
    'Task description':{'x':60,'y':136,'cx':840,'cy':34},
    'Equation - null_experiment_disturbance':{'y':203},
    'Disturbance description':{'x':510,'y':202},
}
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx') as z:
    xml=z.read(PART).decode('utf-8')
    (ARCHIVE/'original_slide13.xml').write_bytes(z.read(PART))
    assert 'Null-space experiment' in xml
    seen=[]
    def edit(m):
        s=m[0]
        nv=re.search(r'<p:cNvPr\b[^>]*\bname="([^"]+)"',s)
        if not nv:return s
        name=nv[1]
        if name=='Task heading':
            seen.append(name)
            return ''
        if name not in updates:return s
        seen.append(name)
        if name=='Disturbance heading':
            assert s.count('Commanded joint disturbance')==1
            s=s.replace('Commanded joint disturbance','Cartesian pose hold with commanded disturbance')
        for key,value in updates[name].items():
            node='ext' if key.startswith('c') else 'off'
            s,n=re.subn(r'(<a:'+node+r'\b[^>]*\b'+key+r'=")\d+("[^>]*/>)',lambda mm:mm[1]+str(round(value*12700))+mm[2],s,count=1)
            assert n==1,(name,key)
        return s
    updated=re.sub(r'<p:sp\b[^>]*>.*?</p:sp>',edit,xml,flags=re.S)
    assert set(seen)==set(updates)|{'Task heading'}
    E.fromstring(updated)
    assert re.findall(r'<m:oMath\b.*?</m:oMath>',xml,re.S)==re.findall(r'<m:oMath\b.*?</m:oMath>',updated,re.S)
    before={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}
    (ARCHIVE/'package_hashes_before.json').write_text(json.dumps(before,indent=2))
    with ZipFile(HERE/'updated.pptx','w',ZIP_DEFLATED) as target:
        for info in z.infolist():target.writestr(info,updated.encode('utf-8') if info.filename==PART else z.read(info.filename))
with ZipFile(HERE/'updated.pptx') as z:
    changed=[n for n in z.namelist() if hashlib.sha256(z.read(n)).hexdigest()!=before[n]]
    assert changed==[PART]
verification={'date':'2026-10-01','footer':21,'physical_slide':22,'title':'Null-space experiment','combined_heading':'Cartesian pose hold with commanded disturbance','layout':'One heading, captured-pose statement, then native disturbance equation and virtual-force definition. Four-condition block unchanged.','changed_package_parts':changed,'all_notes_equations_media_other_slides_preserved':True}
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps(verification,indent=2))
