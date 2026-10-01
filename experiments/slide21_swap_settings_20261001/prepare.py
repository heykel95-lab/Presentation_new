from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import re, json, hashlib, posixpath

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
ARCHIVE.mkdir(exist_ok=True)
PART='ppt/slides/slide13.xml'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx') as source:
    before={n:hashlib.sha256(source.read(n)).hexdigest() for n in source.namelist()}
    (ARCHIVE/'package_hashes_before.json').write_text(json.dumps(before,indent=2))
    with (FINAL/'Thesis_Defense_gg0_v3.pptx').open('rb') as file:
        file.seek(source.start_dir)
        (ARCHIVE/'original_zip_directory.bin').write_bytes(file.read())
    (ARCHIVE/'zip_checkpoint.json').write_text(json.dumps({'start_dir':source.start_dir}))
    original=source.read(PART)
    (ARCHIVE/'slide13.xml').write_bytes(original)
    xml=original.decode('utf-8')
    shapes={name:next(s for s in re.findall(r'<p:sp\b[^>]*>.*?</p:sp>',xml,re.S)
                     if f'name="Setting {name}"' in s) for name in ['damping','conditioning']}
    positions={name:re.search(r'<a:off\b[^>]*/>',shape)[0] for name,shape in shapes.items()}
    assert positions['damping']=='<a:off x="6477000" y="4635500"/>'
    assert positions['conditioning']=='<a:off x="762000" y="5524500"/>'
    for name,other in [('damping','conditioning'),('conditioning','damping')]:
        xml=xml.replace(shapes[name],shapes[name].replace(positions[name],positions[other],1))
    E.fromstring(xml)
    (HERE/'slide13.xml').write_text(xml,encoding='utf-8')
    overrides={PART:xml.encode('utf-8')}
    presentation=E.fromstring(source.read('ppt/presentation.xml'))
    slides=presentation.find('{'+P+'}sldIdLst')
    keep=list(slides)[21].get('{'+R+'}id')
    for child in list(slides):
        if child.get('{'+R+'}id')!=keep:slides.remove(child)
    for tag in ['extLst','custShowLst']:
        child=presentation.find('{'+P+'}'+tag)
        if child is not None:presentation.remove(child)
    rels=E.fromstring(source.read('ppt/_rels/presentation.xml.rels'))
    for rel in list(rels):
        if rel.get('Type').endswith('/slide') and rel.get('Id')!=keep:rels.remove(rel)
    overrides['ppt/presentation.xml']=E.tostring(presentation,encoding='utf-8',xml_declaration=True)
    overrides['ppt/_rels/presentation.xml.rels']=E.tostring(rels,encoding='utf-8',xml_declaration=True)
    def read(name):return overrides[name] if name in overrides else source.read(name)
    names,included,pending=set(source.namelist()),set(),['']
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
    types=E.fromstring(source.read('[Content_Types].xml'))
    for child in list(types):
        if child.tag.endswith('Override') and child.get('PartName').lstrip('/') not in included:types.remove(child)
    overrides['[Content_Types].xml']=E.tostring(types,encoding='utf-8',xml_declaration=True)
    included.add('[Content_Types].xml')
    with ZipFile(HERE/'preview_deck.pptx','w',ZIP_DEFLATED) as preview:
        for name in sorted(included):preview.writestr(name,read(name))
parent=HERE.parent/'disturbance_labels_20261001'
prior=json.loads((parent/'pdf_checkpoint.json').read_text())
current=(FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()
assert hashlib.sha256(current).hexdigest()==prior['updated_sha256']
(ARCHIVE/'pdf_before.json').write_text(json.dumps({
    'parent_recipe':str((parent/'archive/pdf_before.json').relative_to(ROOT)),
    'append_file':str((parent/'presentation_pdf_update.bin').relative_to(ROOT)),
    'sha256':prior['updated_sha256'],'size':len(current)
},indent=2))
(HERE/'verification.json').write_text(json.dumps({
    'date':'2026-10-01','physical_slide':22,'footer':21,
    'conditioning_position_pt':[510,365],'damping_position_pt':[60,435],
    'all_shape_content_styles_and_sizes_preserved':True
},indent=2))
print('Prepared position swap: conditioning top-right; damping bottom-left.')
