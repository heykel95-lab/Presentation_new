from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
import hashlib, json, posixpath, shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINAL = ROOT / 'Final Presentation'
ARCHIVE = HERE / 'archive'
ARCHIVE.mkdir(exist_ok=True)
NS = {'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p14':'http://schemas.microsoft.com/office/powerpoint/2010/main'}
def dump(x): return E.tostring(x, encoding='UTF-8', xml_declaration=True, standalone=True)
def relpath(p): return posixpath.dirname(p)+'/_rels/'+posixpath.basename(p)+'.rels' if p else '_rels/.rels'
def resolve(p,t): return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def select(z, indices, dest):
    overrides={}
    p=E.fromstring(z.read('ppt/presentation.xml'))
    ids=p.find('p:sldIdLst',NS)
    keep={x.get('{'+NS['r']+'}id') for i,x in enumerate(ids,1) if i in indices}
    for i,x in reversed(list(enumerate(list(ids),1))):
        if i not in indices: ids.remove(x)
    for tag in ['extLst','custShowLst']:
        x=p.find('p:'+tag,NS)
        if x is not None:p.remove(x)
    overrides['ppt/presentation.xml']=dump(p)
    rels=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
    for x in list(rels):
        if x.get('Type').endswith('/slide') and x.get('Id') not in keep:rels.remove(x)
    overrides['ppt/_rels/presentation.xml.rels']=dump(rels)
    names=set(z.namelist()); included=set(); pending=['']
    def read(n):return overrides[n] if n in overrides else z.read(n)
    while pending:
        owner=pending.pop()
        if owner in included:continue
        if owner:included.add(owner)
        rp=relpath(owner)
        if rp not in names:continue
        included.add(rp)
        for r in E.fromstring(read(rp)):
            if r.get('TargetMode')!='External':pending.append(resolve(owner,r.get('Target')))
    ct=E.fromstring(z.read('[Content_Types].xml'))
    for x in list(ct):
        if x.tag.endswith('Override') and x.get('PartName').lstrip('/') not in included:ct.remove(x)
    overrides['[Content_Types].xml']=dump(ct);included.add('[Content_Types].xml')
    with ZipFile(dest,'w',ZIP_DEFLATED) as out:
        for n in sorted(included):out.writestr(n,read(n))

if __name__=='__main__':
    for name in ['Thesis_Defense_gg0_v3.pptx','Thesis_Defense_gg0_v3.pdf','Supplementary_slides.pdf']:
        dest=ARCHIVE/name
        if not dest.exists():shutil.copy2(FINAL/name,dest)
    with ZipFile(ARCHIVE/'Thesis_Defense_gg0_v3.pptx') as z:
        hashes={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}
        (ARCHIVE/'package_hashes_before.json').write_text(json.dumps(hashes,indent=2))
        select(z,{1,2},HERE/'source_first_two.pptx')
        select(z,{3},ARCHIVE/'removed_contact_demonstration.pptx')
        (HERE/'contact_poster.png').write_bytes(z.read('ppt/media/image3.png'))
    reader=PdfReader(ARCHIVE/'Thesis_Defense_gg0_v3.pdf')
    out=PdfWriter();out.add_page(reader.pages[2]);out.write(ARCHIVE/'removed_contact_demonstration.pdf')
    renders=HERE/'before';renders.mkdir(exist_ok=True)
    doc=pdfium.PdfDocument(ARCHIVE/'Thesis_Defense_gg0_v3.pdf')
    for i in range(len(doc)):
        page=doc[i];bitmap=page.render(scale=1.25);bitmap.to_pil().save(renders/f'slide-{i+1:02}.png');bitmap.close();page.close()
    doc.close()
    protected=[FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaker_notes_and_timing.txt']
    protected+=list((FINAL/'Speaking').rglob('*.tex'))
    (ARCHIVE/'protected_files.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2))
    shutil.copy2(FINAL/'figures_and_images/native_equations.json',ARCHIVE/'native_equations.json')
    (HERE/'source-notes.txt').write_text('User-provided active deck, robot photo, Contact.mp4 and embedded video poster. Preserve every retained note, native equation, image asset and media stream. The user requested removal of the separate Contact demonstration slide.\n')
    print('Archived originals and removed slide; rendered all 31 source slides.')
