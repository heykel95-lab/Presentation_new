from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import hashlib,json,shutil,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive';ARCHIVE.mkdir(exist_ok=True)
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import select,NS,resolve

if __name__=='__main__':
    prior=HERE.parent/'motivation_video_20261002'
    source=prior/'updated.pptx';pdf=prior/'updated.pdf'
    for current,backup in [(FINAL/'Thesis_Defense_gg0_v3.pptx',source),(FINAL/'Thesis_Defense_gg0_v3.pdf',pdf)]:
        assert hashlib.sha256(current.read_bytes()).digest()==hashlib.sha256(backup.read_bytes()).digest(), 'Source changed since preceding edit'
    with ZipFile(source) as z:
        p=E.fromstring(z.read('ppt/presentation.xml'))
        rels={x.get('Id'):resolve('ppt/presentation.xml',x.get('Target')) for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
        sections=p.findall('.//p14:section',NS)
        chapter_by_id={x.get('id'):(i+1,s.get('name')) for i,s in enumerate(sections[:6]) for x in s.findall('p14:sldIdLst/p14:sldId',NS)}
        seen=set();inventory=[]
        for i,s in enumerate(p.find('p:sldIdLst',NS),1):
            path=rels[s.get('{'+NS['r']+'}id')];root=E.fromstring(z.read(path));sid=s.get('id')
            title=root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name="Slide title"]//a:t/text()',namespaces=NS)
            ch=chapter_by_id.get(sid);marked=ch is not None and i not in [1,3]
            first=marked and ch[0] not in seen
            if marked:seen.add(ch[0])
            inventory.append({'physical':i,'path':path,'sid':sid,'title':''.join(title),'chapter':ch[0] if ch else None,'chapter_name':ch[1] if ch else None,'label':f'{ch[0]}. {ch[1]}' if marked else None,'first_in_chapter':bool(first),'variant':(ch[0]-1)*2+(0 if first else 1) if marked else None})
        select(z,{3},HERE/'overview_source.pptx')
        (ARCHIVE/'package_hashes_before.json').write_text(json.dumps({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()},indent=2))
    (HERE/'inventory.json').write_text(json.dumps(inventory,indent=2))
    protected=[FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaker_notes_and_timing.txt',FINAL/'Supplementary_slides.pdf',FINAL/'figures_and_images/native_equations.json']
    protected+=list((FINAL/'Speaking').rglob('*.tex'))
    (ARCHIVE/'protected_files.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2))
    (ARCHIVE/'source.json').write_text(json.dumps({'pptx':str(source.relative_to(ROOT)),'pdf':str(pdf.relative_to(ROOT)),'pptx_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()},indent=2))
    (HERE/'source-notes.txt').write_text('Chapter names and boundaries copied from the six Overview chapters and native PowerPoint sections. User clarified that the chapter should be visible while advancing between existing slides. Add chapter labels only, no divider slides. All source slides, notes and media are preserved.\n')
    (HERE/'template-frame-map.json').write_text(json.dumps({'outputSlides':[{'outputSlide':x['physical'],'sourceSlide':x['physical'],'reuseMode':'duplicate-slide','editTargets':[{'action':'add','name':'Current overview chapter','zone_pt':[660,21,261.6,24],'reason':'Requested visible chapter marker'}] if x['label'] else []} for x in inventory]},indent=2))
    print('Identified 23 content slides and six chapter starts; title, Overview and backups stay unchanged.')
