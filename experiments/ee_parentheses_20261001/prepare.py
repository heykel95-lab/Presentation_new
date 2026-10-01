from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re,json,hashlib,posixpath

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
ARCHIVE.mkdir(exist_ok=True)
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
targets={'ppt/slides/slide5.xml':1,'ppt/slides/slide8.xml':1,'ppt/slides/slide10.xml':2,'ppt/slides/slide25.xml':1}
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx') as deck:
    hashes={n:hashlib.sha256(deck.read(n)).hexdigest() for n in deck.namelist()}
    (ARCHIVE/'package_hashes_before.json').write_text(json.dumps(hashes,indent=2))
    with (FINAL/'Thesis_Defense_gg0_v3.pptx').open('rb') as f:
        f.seek(deck.start_dir);(ARCHIVE/'original_zip_directory.bin').write_bytes(f.read())
    (ARCHIVE/'zip_checkpoint.json').write_text(json.dumps({'start_dir':deck.start_dir}))
    overrides={}
    for part,count in targets.items():
        data=deck.read(part);xml=data.decode('utf-8')
        (ARCHIVE/posixpath.basename(part)).write_bytes(data)
        changes=[]
        def sub(m):
            text,n=re.subn(r'(?<![\w(])EE(?![\w)])','(EE)',m[1])
            changes.extend([m[1]]*n)
            return '<a:t>'+text+'</a:t>'
        updated=re.sub(r'<a:t>(.*?)</a:t>',sub,xml,flags=re.S)
        assert len(changes)==count,(part,changes)
        if part=='ppt/slides/slide5.xml':
            # The added parentheses need a slightly longer bottom row.
            updated=updated.replace('cx="7684770"','cx="8001000"',1)
            updated=updated.replace('x="8548370"','x="9080500"',1)
        E.fromstring(updated)
        (HERE/posixpath.basename(part)).write_text(updated,encoding='utf-8')
        overrides[part]=updated.encode('utf-8')
    for part,name in [('ppt/media/image5.png','cartesian_pose_position'),('ppt/media/image6.png','cartesian_pose_orientation')]:
        (ARCHIVE/posixpath.basename(part)).write_bytes(deck.read(part))
        overrides[part]=(HERE/f'{name}.png').read_bytes()
    # Only the preview copy unhides B2, so it is included in native rendering.
    overrides['ppt/slides/slide25.xml']=overrides['ppt/slides/slide25.xml'].replace(b' show="0"',b'',1)
    presentation=E.fromstring(deck.read('ppt/presentation.xml'))
    slides=presentation.find('{'+P+'}sldIdLst')
    keep={list(slides)[i].get('{'+R+'}id') for i in [4,9,18,27]}
    for child in list(slides):
        if child.get('{'+R+'}id') not in keep:slides.remove(child)
    for tag in ['extLst','custShowLst']:
        child=presentation.find('{'+P+'}'+tag)
        if child is not None:presentation.remove(child)
    rels=E.fromstring(deck.read('ppt/_rels/presentation.xml.rels'))
    for rel in list(rels):
        if rel.get('Type').endswith('/slide') and rel.get('Id') not in keep:rels.remove(rel)
    overrides['ppt/presentation.xml']=E.tostring(presentation,encoding='utf-8',xml_declaration=True)
    overrides['ppt/_rels/presentation.xml.rels']=E.tostring(rels,encoding='utf-8',xml_declaration=True)
    def read(name):return overrides[name] if name in overrides else deck.read(name)
    included,pending,names=set(),[''],set(deck.namelist())
    while pending:
        part=pending.pop()
        if part in included:continue
        if part:included.add(part)
        relname=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels') if part else '_rels/.rels'
        if relname not in names:continue
        included.add(relname)
        for rel in E.fromstring(read(relname)):
            if rel.get('TargetMode')=='External':continue
            target=rel.get('Target')
            target=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),target))
            if target not in included:pending.append(target)
    types=E.fromstring(deck.read('[Content_Types].xml'))
    for child in list(types):
        if child.tag.endswith('Override') and child.get('PartName').lstrip('/') not in included:types.remove(child)
    overrides['[Content_Types].xml']=E.tostring(types,encoding='utf-8',xml_declaration=True)
    included.add('[Content_Types].xml')
    with ZipFile(HERE/'preview_deck.pptx','w',ZIP_DEFLATED) as preview:
        for name in sorted(included):preview.writestr(name,read(name))
parent=HERE.parent/'slide18_nullspace_condition_label_20261001'
prior=json.loads((parent/'pdf_checkpoint.json').read_text())
current=(FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()
assert hashlib.sha256(current).hexdigest()==prior['updated_sha256']
(ARCHIVE/'pdf_before.json').write_text(json.dumps({
    'parent_recipe':str((parent/'archive/pdf_before.json').relative_to(ROOT)),
    'append_file':str((parent/'presentation_pdf_update.bin').relative_to(ROOT)),
    'sha256':prior['updated_sha256'],'size':len(current)
},indent=2))
supp=FINAL/'Supplementary_slides.pdf'
supp_archive=ARCHIVE/'Supplementary_slides.pdf'
supp_archive.write_bytes(supp.read_bytes())
(ARCHIVE/'supplementary_before.json').write_text(json.dumps({'source':str(supp_archive.relative_to(ROOT)),
    'sha256':hashlib.sha256(supp.read_bytes()).hexdigest(),'size':supp.stat().st_size},indent=2))
(HERE/'verification.json').write_text(json.dumps({'physical_slides':[5,10,19,28],
    'text_replacements':5,'diagram_label_replacements':2,'native_mathematics_preserved':True,
    'speaking_file_hashes':{str(p.relative_to(FINAL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        [FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',
         FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex',FINAL/'Speaker_notes_and_timing.txt']}},indent=2))
print('Prepared five replacements on four slides; native equations unchanged.')
