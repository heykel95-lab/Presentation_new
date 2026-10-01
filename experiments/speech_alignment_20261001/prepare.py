"""Minimal speech alignment after the latest slide-label and layout changes."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
from xml.sax.saxutils import escape
import re, json, hashlib, difflib, posixpath

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
ARCHIVE.mkdir(exist_ok=True)
SCRIPT=FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex'
PLAIN=FINAL/'Speaker_notes_and_timing.txt'
tex=SCRIPT.read_text(encoding='utf-8')
plain=PLAIN.read_text(encoding='utf-8')
sections=list(re.finditer(r'\\section\*\{([^}]+)\}\n\\begin\{itemize\}\n(.*?)\\end\{itemize\}',tex,re.S))
assert len(sections)==31
updates={
    19:('Null-space controller',[
        'Another study in this work analysed null-space behaviour. Our Cartesian pose has six degrees of freedom, while the robot has seven joints, leaving one redundant direction when the Jacobian has full rank. Several joints can move together in this direction without changing the instantaneous Cartesian motion.',
        'We introduced a damping torque to oppose this motion.',
        'The conditioning torque seeks a configuration with a larger minimum singular value of the Jacobian. At a singularity, the Jacobian loses rank and the end effector loses an instantaneous motion direction. Near a singularity, some motions require very high joint velocities.'
    ]),
    20:('Disturbance - Without null-space control to damping',[
        'This first video shows the response to a torque disturbance, first without null-space control and then with damping. It gives a qualitative view of how the joints respond.'
    ]),
    21:('Disturbance - Conditioning only',[
        'This is the continuation of the same demonstration, now with conditioning only. The following experiment gives the quantitative comparison between the null-space settings.'
    ]),
    22:('Null-space experiment',[
        'To study this case, we held the captured Cartesian pose as the reference and added a commanded torque disturbance equivalent to a virtual force of 20 newtons on link three. Through the Jacobian mapping, this disturbance acted mainly on joint one.',
        'With the disturbance applied, we compare four conditions with three trials each: no null-space control torque, conditioning alone, damping alone, and both torques together. The enabled settings are 2 newton metres for conditioning and 2 newton metre seconds per radian for damping.',
        'The following plots show the same four-second interval after disturbance onset. The curves are three-trial means, and the shading shows one sample standard deviation.'
    ])
}
paths=[SCRIPT,PLAIN,FINAL/'Thesis_Defense_Speaking_Script.pdf',
       FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaking/BUILD.txt']
with ZipFile(ARCHIVE/'speaking_files_before.zip','w',ZIP_DEFLATED) as backup:
    for path in paths:backup.write(path,path.relative_to(FINAL).as_posix())
old_bullets={}
updated_tex,updated_plain=tex,plain
for number,(heading,bullets) in updates.items():
    section=sections[number-1]
    old_bullets[number]=re.findall(r'^\\item (.*)$',section[2],re.M)
    assert '\\[' not in section[2]
    new='\\section*{'+heading+'}\n\\begin{itemize}\n'
    new+=''.join('\\item '+line+'\n' for line in bullets)+'\\end{itemize}'
    updated_tex=updated_tex.replace(section[0],new,1)
    old_plain=section[1]+'\n'+'-'*len(section[1])+'\n'+'\n'.join(old_bullets[number])
    assert old_plain in updated_plain,number
    new_plain=heading+'\n'+'-'*len(heading)+'\n'+'\n'.join(bullets)
    updated_plain=updated_plain.replace(old_plain,new_plain,1)
new_sections=list(re.finditer(r'\\section\*\{([^}]+)\}\n\\begin\{itemize\}\n(.*?)\\end\{itemize\}',updated_tex,re.S))
assert len(new_sections)==31
assert [i+1 for i,(a,b) in enumerate(zip(sections,new_sections)) if a[0]!=b[0]]==[19,20,21,22]
(HERE/SCRIPT.name).write_text(updated_tex,encoding='utf-8')
(HERE/PLAIN.name).write_text(updated_plain,encoding='utf-8')
(HERE/'speech_changes.diff').write_text(''.join(difflib.unified_diff(tex.splitlines(True),updated_tex.splitlines(True),fromfile='previous speech',tofile='aligned speech')),encoding='utf-8')

NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
patches={}
inventory=[]
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx') as deck:
    hashes={n:hashlib.sha256(deck.read(n)).hexdigest() for n in deck.namelist()}
    (ARCHIVE/'package_hashes_before.json').write_text(json.dumps(hashes,indent=2))
    with (FINAL/'Thesis_Defense_gg0_v3.pptx').open('rb') as original:
        original.seek(deck.start_dir)
        (ARCHIVE/'original_zip_directory.bin').write_bytes(original.read())
    (ARCHIVE/'zip_checkpoint.json').write_text(json.dumps({'start_dir':deck.start_dir}))
    presentation=E.fromstring(deck.read('ppt/presentation.xml'))
    rels={r.get('Id'):posixpath.normpath('ppt/'+r.get('Target'))
          for r in E.fromstring(deck.read('ppt/_rels/presentation.xml.rels'))}
    for number,slide in enumerate(presentation.find('p:sldIdLst',NS),1):
        part=rels[slide.get('{'+NS['r']+'}id')]
        root=E.fromstring(deck.read(part))
        title=root.find('.//a:t',NS).text
        title_tex=title.replace('–','--')
        assert sections[number-1][1]==title_tex or (number in [20,21] and sections[number-1][1].startswith(title))
        note_rels=posixpath.dirname(part)+'/_rels/'+posixpath.basename(part)+'.rels'
        target=next(r.get('Target') for r in E.fromstring(deck.read(note_rels)) if r.get('Type').endswith('/notesSlide'))
        note_path=posixpath.normpath(posixpath.dirname(part)+'/'+target)
        inventory.append({'physical':number,'footer':number-1 if number<=26 else 'B'+str(number-26),
                          'title':title,'notes_path':note_path,'hidden':root.get('show')=='0'})
        if number not in updates:continue
        xml=deck.read(note_path).decode('utf-8')
        (ARCHIVE/Path(note_path).name).write_text(xml,encoding='utf-8')
        shape=next(s for s in re.finditer(r'<p:sp\b[^>]*>.*?</p:sp>',xml,re.S) if re.search(r'<p:ph\b[^>]*\btype="body"',s[0]))
        body=re.search(r'(<p:txBody>.*?<a:lstStyle\s*/>)(.*?)(</p:txBody>)',shape[0],re.S)
        paragraphs=list(re.finditer(r'<a:p(?:\s[^>]*)?>.*?</a:p>',body[2],re.S))
        source_start=next(p.start() for p in paragraphs if '[Sources]' in p[0])
        old_spoken=body[2][:source_start]
        extracted=[''.join(E.fromstring('<root xmlns:a="'+NS['a']+'">'+p[0]+'</root>').itertext()) for p in paragraphs if p.start()<source_start]
        assert extracted==old_bullets[number],number
        spoken=''.join('<a:p><a:r><a:t>'+escape(line)+'</a:t></a:r></a:p>' for line in updates[number][1])
        changed_shape=shape[0][:body.start(2)]+spoken+body[2][source_start:]+shape[0][body.end(2):]
        new_xml=xml[:shape.start()]+changed_shape+xml[shape.end():]
        E.fromstring(new_xml)
        assert body[2][source_start:] in new_xml
        patches[note_path]=new_xml.encode('utf-8')
        (HERE/Path(note_path).name).write_bytes(patches[note_path])
assert len(patches)==4
assert sum(s['hidden'] for s in inventory)==5
(HERE/'deck_inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
(HERE/'updated_sections.json').write_text(json.dumps(updates,indent=2,ensure_ascii=False),encoding='utf-8')
unchanged_files={str(p.relative_to(FINAL)):hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in [FINAL/'Thesis_Defense_gg0_v3.pdf',FINAL/'Supplementary_slides.pdf']}
verification={'date':'2026-10-01','changed_physical_sections':[19,20,21,22],
              'changed_footers':[18,19,20,21],'other_27_sections_unchanged':True,
              'main_sections':26,'backup_sections':5,'notes_parts':list(patches),
              'existing_source_notes_preserved':True,'unchanged_slide_pdf_hashes':unchanged_files}
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Prepared four minimally edited sections; the other 27 sections are unchanged.')
