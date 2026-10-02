from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
import hashlib,json,shutil,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,select,resolve,relpath
NS['m']='http://schemas.openxmlformats.org/officeDocument/2006/math'
if __name__=='__main__':
    archive=HERE/'archive';archive.mkdir(exist_ok=True)
    (HERE/'assets/sources').mkdir(exist_ok=True,parents=True)
    source={}
    for ext in ['pptx','pdf']:
        p=HERE.parent/'realtime_velocity_20261002'/('updated.'+ext)
        assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((FINAL/('Thesis_Defense_gg0_v3.'+ext)).read_bytes()).digest()
        source[ext]=str(p.relative_to(ROOT));source[ext+'_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    with ZipFile(ROOT/source['pptx']) as z:
        p=E.fromstring(z.read('ppt/presentation.xml'));rels={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};inventory=[]
        for number,sid in enumerate(p.find('p:sldIdLst',NS),1):
            rid=sid.get('{'+NS['r']+'}id');part=resolve('ppt/presentation.xml',rels[rid]);root=E.fromstring(z.read(part));shapes=[]
            for s in root.xpath('.//p:sp|.//p:pic',namespaces=NS):
                cn=s.find('.//p:cNvPr',NS);xf=s.find('p:spPr/a:xfrm',NS)
                item={'name':cn.get('name'),'text':' '.join(s.xpath('.//a:t/text()',namespaces=NS)),'math':' '.join(s.xpath('.//m:t/text()',namespaces=NS))}
                if xf is not None:item['box']=[int(v)/12700 for v in [xf.find('a:off',NS).get('x'),xf.find('a:off',NS).get('y'),xf.find('a:ext',NS).get('cx'),xf.find('a:ext',NS).get('cy')]]
                shapes.append(item)
            inventory.append({'physical':number,'sid':sid.get('id'),'rid':rid,'path':part,'hidden':root.get('show')=='0','shapes':shapes})
            if number in [7,8]:
                (archive/Path(part).name).write_bytes(z.read(part));(archive/(Path(part).name+'.rels')).write_bytes(z.read(relpath(part)))
        source['case_path']=inventory[6]['path'];source['coupling_path']=inventory[7]['path']
        case=E.fromstring(z.read(source['case_path']));rs={r.get('Id'):resolve(source['case_path'],r.get('Target')) for r in E.fromstring(z.read(relpath(source['case_path'])))}
        pics=case.findall('.//p:pic',NS)
        print('Case pictures: '+str([s.find('p:nvPicPr/p:cNvPr',NS).get('name') for s in pics]))
        picture=next(s for s in pics if 'CoC' in s.find('p:nvPicPr/p:cNvPr',NS).get('name'))
        source['case_media']=rs[picture.find('.//a:blip',NS).get('{'+NS['r']+'}embed')]
        (HERE/'inventory.json').write_text(json.dumps(inventory,indent=2,ensure_ascii=False),encoding='utf-8')
        select(z,{7,8},HERE/'source_slides.pptx')
        (archive/'package_hashes_before.json').write_text(json.dumps({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()},indent=2))
    (archive/'source.json').write_text(json.dumps(source,indent=2))
    for rel in ['native_equations.json','manifest.json','sources/CoC_moment.tex','CoC_moment.pdf','CoC_moment.png','CoC_moment.svg','sources/coc_displacement_definition.tex','coc_displacement_definition.pdf','coc_displacement_definition.png','coc_displacement_definition.svg']:
        dest=archive/'assets'/rel;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(ASSETS/rel,dest)
    protected=[FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',FINAL/'Speaker_notes_and_timing.txt',FINAL/'Supplementary_slides.pdf']+list((FINAL/'Speaking').rglob('*.tex'))
    (archive/'protected_files.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2))
    reader=PdfReader(ROOT/source['pdf']);out=PdfWriter()
    for i in [6,7]:out.add_page(reader.pages[i])
    out.write(archive/'original_coc_and_coupling.pdf')
    pdf=pdfium.PdfDocument(ROOT/source['pdf'])
    for i in [6,7]:
        page=pdf[i];b=page.render(scale=1.25);b.to_pil().save(HERE/f'before-{i+1}.png');b.close();page.close()
    pdf.close()
    print(json.dumps(inventory[6:8],indent=2,ensure_ascii=True))
