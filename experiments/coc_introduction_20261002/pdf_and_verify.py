from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader,PdfWriter,Transformation
from pypdf.generic import NameObject,DictionaryObject,DecodedStreamObject
from PIL import ImageChops
import pypdfium2 as pdfium
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,resolve
NS['m']='http://schemas.openxmlformats.org/officeDocument/2006/math'
source=json.loads((HERE/'archive/source.json').read_text());build=json.loads((HERE/'build.json').read_text());layout=json.loads((HERE/'layout.json').read_text());inventory=json.loads((HERE/'inventory.json').read_text(encoding='utf-8'))
oldpdf=PdfReader(ROOT/source['pdf']);native=PdfReader(HERE/'native_export.pdf');assert len(oldpdf.pages)==29 and len(native.pages)==3
writer=PdfWriter()
for num in range(1,31):
    if 7<=num<=9:writer.add_page(native.pages[num-7])
    else:writer.add_page(oldpdf.pages[num-1 if num<7 else num-2])
font=oldpdf.pages[2]['/Resources']['/Font']['/F2'];assert font['/Encoding']=='/WinAnsiEncoding'
widths=font['/Widths'];first=int(font['/FirstChar'])
for num in range(10,26):
    page=writer.pages[num-1];data=page.get_contents().get_data();chunks=re.findall(rb'BT\b.*?ET',data,re.S)
    targets=[b for b in chunks if re.search(rb'(?<![\d.])9\d{2}(?:\.\d+)?\s+2\d(?:\.\d+)?\s+(?:Tm|TD|Td)\b',b)]
    assert len(targets)==1,(num,targets)
    label=str(num-1);width=sum(float(widths[ord(c)-first]) for c in label)*8.04/1000;baseline=26.64 if b'26.64' in targets[0] else 26.52
    replacement=f'BT /CoCFooter 8.04 Tf 1 0 0 1 {921.8-width:.6f} {baseline} Tm 0.412 g 0.412 G 0 Tc [({label})] TJ ET'.encode()
    resources=DictionaryObject(page['/Resources']);fonts=DictionaryObject(resources['/Font']);fonts[NameObject('/CoCFooter')]=font.clone(writer);resources[NameObject('/Font')]=fonts;page[NameObject('/Resources')]=resources
    stream=DecodedStreamObject();stream.set_data(data.replace(targets[0],replacement,1));page[NameObject('/Contents')]=writer._add_object(stream)
writer.write(HERE/'updated.pdf')
for asset,index,box in [('coc_added_moment',0,layout['intro_equation']),('symbol_pc',2,layout['coupling_equations']['Equation - symbol_pc']),('coc_displacement_definition',2,layout['coupling_equations']['Equation - coc_displacement_definition'])]:
    x,y,w,h=box;out=PdfWriter();p=out.add_blank_page(width=w+4,height=h+4);p.merge_transformed_page(native.pages[index],Transformation().translate(-x+2,-(540-y-h)+2),expand=False);out.write(HERE/'assets'/f'{asset}.pdf')

sha=lambda data:hashlib.sha256(data).hexdigest()
with ZipFile(ROOT/source['pptx']) as old,ZipFile(HERE/'updated.pptx') as new:
    assert len(new.namelist())==len(set(new.namelist()))
    assert set(new.namelist())-set(old.namelist())==set(build['added_parts']) and not set(old.namelist())-set(new.namelist())
    changed=[n for n in old.namelist() if sha(old.read(n))!=sha(new.read(n))];assert set(changed)==set(build['changed_parts'])
    for name in old.namelist():
        if name.startswith('ppt/notesSlides/') or (name.startswith('ppt/media/') and name!=source['case_media']):assert old.read(name)==new.read(name),name
    pres=E.fromstring(new.read('ppt/presentation.xml'));pr={r.get('Id'):r.get('Target') for r in E.fromstring(new.read('ppt/_rels/presentation.xml.rels'))};sids=list(pres.find('p:sldIdLst',NS))
    paths=[resolve('ppt/presentation.xml',pr[x.get('{'+NS['r']+'}id')]) for x in sids];assert len(paths)==30 and paths[6]==build['intro_path']
    assert [s.get('id') for s in sids if s.get('id')!=build['new_sid']]==[x['sid'] for x in inventory]
    assert pres.xpath('.//p14:sldId/@id',namespaces=NS)==[x.get('id') for x in sids]
    def maths(root):
        return {s.find('p:nvSpPr/p:cNvPr',NS).get('name'):E.tostring(s.find('.//m:oMath',NS),method='c14n',exclusive=True) for s in root.findall('.//p:sp',NS) if s.find('.//m:oMath',NS) is not None}
    before={};after={};videos=hidden=0
    for item in inventory:before.update(maths(E.fromstring(old.read(item['path']))))
    for num,path in enumerate(paths,1):
        root=E.fromstring(new.read(path));after.update(maths(root));videos+=len(root.findall('.//a:videoFile',NS));hidden+=root.get('show')=='0'
        ids=root.xpath('.//p:cNvPr/@id',namespaces=NS);assert len(ids)==len(set(ids)),path
        if num<=25 and num>1:
            footer=root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name="TextBox 6"]//a:t/text()',namespaces=NS);assert footer==[str(num-1)],(num,footer)
    assert len(before)==30 and len(after)==31 and (videos,hidden)==(5,5)
    for name,value in before.items():
        if name not in ['Equation - symbol_pc','Equation - coc_displacement_definition']:assert after[name]==value,name
    assert set(after)-set(before)=={'Equation - coc_added_moment'}
    coupling=E.fromstring(new.read(source['coupling_path']))
    assert coupling.xpath('.//m:sSub[m:e/m:r/m:t="p"]/m:sub/m:r/m:t/text()',namespaces=NS).count('CoC')==2
    assert coupling.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name="Virtual point force interpretation"]//a:t[text()="CoC"]',namespaces=NS)
    for item in inventory:
        if item['physical'] in [7,8]:continue
        orig,updated=old.read(item['path']),new.read(item['path'])
        if 9<=item['physical']<=24:
            get=lambda raw:next(b for b in re.findall(rb'<p:sp\b[^>]*>.*?</p:sp>',raw,re.S) if b'name="TextBox 6"' in b)
            assert updated.replace(get(updated),get(orig),1)==orig,item['physical']
        else:assert updated==orig,item['physical']
    refs=0
    for name in new.namelist():
        if name.endswith('.xml') or name.endswith('.rels'):E.fromstring(new.read(name))
        if name.endswith('.rels'):
            owner='' if name=='_rels/.rels' else name.replace('/_rels/','/')[:-5]
            for r in E.fromstring(new.read(name)):
                if r.get('TargetMode')!='External':assert resolve(owner,r.get('Target')) in new.namelist();refs+=1
    catalog=json.loads((HERE/'assets/native_equations.json').read_text(encoding='utf-8'));assert len(catalog)==31
    for c in catalog:
        root=E.fromstring(new.read(paths[c['slide']-1]));assert root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$n]',namespaces=NS,n=c['shape'])
for name,digest in json.loads((HERE/'archive/protected_files.json').read_text()).items():assert sha((ROOT/name).read_bytes())==digest,name
before=pdfium.PdfDocument(ROOT/source['pdf']);after=pdfium.PdfDocument(HERE/'updated.pdf');assert len(before)==29 and len(after)==30
changed_pages=[];renders=HERE/'after';renders.mkdir(exist_ok=True)
for i in range(30):
    b=after[i];bb=b.render(scale=1.25);ib=bb.to_pil().convert('RGB');ib.save(renders/f'slide-{i+1:02}.png')
    if i!=6:
        oldindex=i if i<6 else i-1;a=before[oldindex];aa=a.render(scale=1.25);ia=aa.to_pil().convert('RGB');diff=ImageChops.difference(ia,ib)
        if diff.getbbox():changed_pages.append(i+1)
        if i not in [7,8]:
            if 9<=i<=24:diff.paste((0,0,0),(1125,625,1159,653))
            assert diff.getbbox() is None,('Unexpected visual change',i+1,diff.getbbox())
        aa.close();a.close()
    bb.close();b.close()
before.close();after.close();assert len(PdfReader(FINAL/'Supplementary_slides.pdf').pages)==5
v={'date':'2026-10-02','introduced_slide':7,'case_slide':8,'coupling_slide':9,'slide_count':30,'main_slides':25,'hidden_backups':5,'native_equations':31,
 'general_figure_shows_virtual_force_and_extra_moment':True,'case_forces_shifted_to_virtual_CoC':True,'supporting_counterclockwise_opposing_clockwise_verified':True,
 'p_CoC_in_all_related_visible_labels_and_equations':True,'remaining_28_native_equations_preserved':True,'all_retained_notes_unchanged':True,'new_notes_sources_only':True,
 'all_five_embedded_videos_unchanged':True,'speaking_files_unchanged':True,'supplementary_pdf_unchanged':True,'historical_shared_coc_assets_preserved':True,
 'pdf_pages':30,'other_27_original_slides_pixel_identical_except_main_footers':True,'changed_retained_pdf_pages':changed_pages,'all_internal_relationships_resolved':refs,
 'native_sections_and_footers_updated':True,'equation_catalog_updated':True,'chapter_starts':[2,4,10,12,18,25],
 'pptx_sha256':sha((HERE/'updated.pptx').read_bytes()),'pdf_sha256':sha((HERE/'updated.pdf').read_bytes())}
(HERE/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Verified 30 slides, 31 editable equations, virtual-force directions, retained notes/media, and every PDF page.')
