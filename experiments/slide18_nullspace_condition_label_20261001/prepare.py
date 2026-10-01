from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re,json,hashlib,posixpath,uuid

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
ARCHIVE.mkdir(exist_ok=True)
PART='ppt/slides/slide10.xml'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx') as deck:
    hashes={n:hashlib.sha256(deck.read(n)).hexdigest() for n in deck.namelist()}
    (ARCHIVE/'package_hashes_before.json').write_text(json.dumps(hashes,indent=2))
    with (FINAL/'Thesis_Defense_gg0_v3.pptx').open('rb') as file:
        file.seek(deck.start_dir);(ARCHIVE/'original_zip_directory.bin').write_bytes(file.read())
    (ARCHIVE/'zip_checkpoint.json').write_text(json.dumps({'start_dir':deck.start_dir}))
    xml=deck.read(PART).decode('utf-8')
    (ARCHIVE/'slide10.xml').write_bytes(deck.read(PART))
    def shape(name):
        return next(s for s in re.findall(r'<p:sp\b[^>]*>.*?</p:sp>',xml,re.S) if 'name="'+name+'"' in s)
    original_equation=shape('Equation - null_controller_velocity')
    equation=original_equation.replace('x="8247883"','x="9410700"',1)
    assert equation!=original_equation
    label=shape('Damping heading')
    maximum=max(map(int,re.findall(r'<p:cNvPr\b[^>]*\bid="(\d+)"',xml)))
    label=label.replace('id="21" name="Damping heading"',f'id="{maximum+1}" name="Null-space condition label"',1)
    label=re.sub(r'(<a16:creationId\b[^>]*\bid=")[^"]+("[^>]*/>)',
                 lambda m:m[1]+'{'+str(uuid.uuid4()).upper()+'}'+m[2],label,count=1)
    label=label.replace('x="1016000" y="3302000"','x="6731000" y="2768600"',1)
    label=label.replace('cx="4699000"','cx="2603500"',1)
    label=label.replace('Damping torque','Null-space condition:')
    label=label.replace('val="17365D"','val="000000"').replace('typeface="Arial"','typeface="Cambria Math"')
    label=re.sub(r' panose="[^"]*"| pitchFamily="[^"]*"| charset="[^"]*"','',label)
    updated=xml.replace(original_equation,label+equation,1)
    E.fromstring(updated)
    assert updated.count('name="Null-space condition label"')==1
    assert re.findall(r'<ns0:oMath>.*?</ns0:oMath>',updated,re.S)==re.findall(r'<ns0:oMath>.*?</ns0:oMath>',xml,re.S)
    (HERE/'slide10.xml').write_text(updated,encoding='utf-8')
    overrides={PART:updated.encode('utf-8')}
    presentation=E.fromstring(deck.read('ppt/presentation.xml'))
    slides=presentation.find('{'+P+'}sldIdLst')
    keep=list(slides)[18].get('{'+R+'}id')
    for child in list(slides):
        if child.get('{'+R+'}id')!=keep:slides.remove(child)
    for tag in ['extLst','custShowLst']:
        child=presentation.find('{'+P+'}'+tag)
        if child is not None:presentation.remove(child)
    rels=E.fromstring(deck.read('ppt/_rels/presentation.xml.rels'))
    for rel in list(rels):
        if rel.get('Type').endswith('/slide') and rel.get('Id')!=keep:rels.remove(rel)
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
parent=HERE.parent/'slide17_single_legend_20261001'
prior=json.loads((parent/'pdf_checkpoint.json').read_text())
current=(FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()
assert hashlib.sha256(current).hexdigest()==prior['updated_sha256']
(ARCHIVE/'pdf_before.json').write_text(json.dumps({
    'parent_recipe':str((parent/'archive/pdf_before.json').relative_to(ROOT)),
    'append_file':str((parent/'presentation_pdf_update.bin').relative_to(ROOT)),
    'sha256':prior['updated_sha256'],'size':len(current)
},indent=2))
(HERE/'verification.json').write_text(json.dumps({
    'date':'2026-10-01','physical_slide':19,'footer':18,
    'added_label':'Null-space condition:', 'label_position_pt':[530,218,205,30],
    'label_font':'Cambria Math 22 pt, regular, black; matches the dimension label',
    'native_equation_retained_unchanged':True,'equation_left_pt':741,
    'all_other_shapes_and_notes_preserved':True
},indent=2))
print('Prepared a native label before the unchanged null-space equation.')
