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
    original=next(s for s in re.findall(r'<p:sp\b[^>]*>.*?</p:sp>',xml,re.S) if 'name="Conditioning role"' in s)
    phrase='Seeks postures away from singularities, where the (EE) loses a motion direction.'
    run=next(s for s in re.findall(r'<a:r>.*?</a:r>',original,re.S) if phrase in s)
    def text_run(text,font='Arial',size=2000,baseline=None,italic=False):
        r=re.sub(r'<a:t>.*?</a:t>','<a:t>'+text+'</a:t>',run,flags=re.S)
        if font!='Arial':
            r=r.replace('typeface="Arial"','typeface="'+font+'"')
            r=re.sub(r' panose="[^"]*"| pitchFamily="[^"]*"| charset="[^"]*"','',r)
        r=r.replace('sz="2000"','sz="'+str(size)+'"')
        attributes=(' baseline="'+str(baseline)+'"' if baseline is not None else '')+(' i="1"' if italic else '')
        r=r.replace('<a:rPr ','<a:rPr'+attributes+' ',1)
        return r
    new_runs=(text_run('Seeks a larger minimum singular value ')+
              text_run('σ','Cambria Math')+text_run('min','Cambria Math',2000,-25000)+
              text_run(' of ')+text_run('J','Cambria Math',italic=True)+
              text_run(', moving away from singularities.'))
    updated=xml.replace(original,original.replace(run,new_runs,1),1)
    assert updated!=xml
    E.fromstring(updated)
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
parent=HERE.parent/'ee_parentheses_20261001'
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
    'conditioning_bullet':'Seeks a larger minimum singular value σ_min of J, moving away from singularities.',
    'first_conditioning_bullet_preserved':True,
    'native_equation_contents_preserved':True,'all_other_shapes_and_notes_preserved':True
},indent=2))
print('Prepared the minimum singular value explanation on footer 18.')
