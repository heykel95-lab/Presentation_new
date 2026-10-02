from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
from pypdf import PdfReader
import json,sys,shutil,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import select,NS,dump,resolve,relpath
NS['m']='http://schemas.openxmlformats.org/officeDocument/2006/math'
source=json.loads((HERE/'archive/source.json').read_text());inventory=json.loads((HERE/'inventory.json').read_text(encoding='utf-8'));layout=json.loads((HERE/'layout.json').read_text())
with ZipFile(ROOT/source['pptx']) as z:
    names=z.namelist();parts={n:z.read(n) for n in names if not n.startswith('ppt/media/')}
original=dict(parts);changed={};added={}
casepath=source['case_path'];couplingpath=source['coupling_path'];case=E.fromstring(parts[casepath]);coupling=E.fromstring(parts[couplingpath])
def find(root,name):
    matches=root.xpath('.//*[p:nvSpPr/p:cNvPr/@name=$n or p:nvPicPr/p:cNvPr/@name=$n]',namespaces=NS,n=name);assert len(matches)==1,name;return matches[0]
def frame(s,box):
    xf=s.find('p:spPr/a:xfrm',NS)
    for key,val in zip(['x','y'],box[:2]):xf.find('a:off',NS).set(key,str(round(val*12700)))
    if len(box)==4:
        for key,val in zip(['cx','cy'],box[2:]):xf.find('a:ext',NS).set(key,str(round(val*12700)))
def picture_box(s,asset,box):
    page=PdfReader(HERE/'assets'/f'{asset}.pdf').pages[0];x,y,w=box;frame(s,[x,y,w,w*float(page.mediabox.height)/float(page.mediabox.width)])
def replace_text(s,value):
    texts=s.findall('.//a:t',NS);assert len(texts)==1;texts[0].text=value
def appendix_assets(root,number):
    tree=root.find('p:cSld/p:spTree',NS);maxid=max(int(x.get('id')) for x in root.findall('.//p:cNvPr',NS))
    with ZipFile(HERE/'text_assets.pptx') as z:r=E.fromstring(z.read(f'ppt/slides/slide{number}.xml'))
    for i,s in enumerate(r.findall('p:cSld/p:spTree/p:sp',NS),1):
        s=deepcopy(s);s.find('p:nvSpPr/p:cNvPr',NS).set('id',str(maxid+i));tree.append(s)

# Retain the historical shared illustration; embed a presentation-specific variant.
casefig=find(case,'Figure - CoC_moment');picture_box(casefig,'coc_force_shift_cases',layout['case_figure'])
casefig.find('p:nvPicPr/p:cNvPr',NS).set('descr','Virtual CoC forces at p_CoC. Curved arrows show their resulting moment about TCP: r_c cross f_n. Left: supporting; right: opposing. Source: figures_and_images/sources/coc_force_shift_cases.tex.')
changed[source['case_media']]=(HERE/'assets/coc_force_shift_cases.png').read_bytes();appendix_assets(case,2)

# Rename every active CoC position symbol on the following coupling slide.
for name in ['Equation - symbol_pc','Equation - coc_displacement_definition']:
    s=find(coupling,name)
    candidates=s.xpath('.//m:sSub[m:e/m:r/m:t="p"]/m:sub/m:r',namespaces=NS)
    targets=[r for r in candidates if r.find('m:t',NS).text=='c'];assert len(targets)==1,name
    r=targets[0];r.find('m:t',NS).text='CoC';rpr=r.find('m:rPr',NS)
    if rpr is None:rpr=E.Element('{'+NS['m']+'}rPr');r.insert(0,rpr)
    sty=rpr.find('m:sty',NS)
    if sty is None:sty=E.SubElement(rpr,'{'+NS['m']+'}sty')
    sty.set('{'+NS['m']+'}val','p');frame(s,layout['coupling_equations'][name])
inline=find(coupling,'Virtual point force interpretation');runs=[r for r in inline.findall('.//a:r',NS) if r.find('a:t',NS).text=='c'];assert len(runs)==1
runs[0].find('a:t',NS).text='CoC';runs[0].find('a:rPr',NS).set('i','0')

# Clone the existing CoC slide's master/layout, title, footer and chapter label.
intro=E.fromstring(parts[casepath]);tree=intro.find('p:cSld/p:spTree',NS)
for name in ['Virtual centre definition','CoC position meaning','Figure - CoC_moment']:
    s=find(intro,name);s.getparent().remove(s)
appendix_assets(intro,1)
maxid=max(int(x.get('id')) for x in intro.findall('.//p:cNvPr',NS))
general=deepcopy(find(E.fromstring(parts[casepath]),'Figure - CoC_moment'))
cn=general.find('p:nvPicPr/p:cNvPr',NS);cn.set('id',str(maxid+1));cn.set('name','Figure - coc_force_shift_general');cn.set('descr','Force acts as if at virtual p_CoC, offset from p_TCP by r_c. Delta m is the resulting additional moment about TCP. Source: figures_and_images/sources/coc_force_shift_general.tex.')
general.find('.//a:blip',NS).set('{'+NS['r']+'}embed','rIdCocGeneral');picture_box(general,'coc_force_shift_general',layout['intro_figure']);tree.append(general)
eq=deepcopy(find(coupling,'Equation - coc_displacement_definition'));cn=eq.find('p:nvSpPr/p:cNvPr',NS);cn.set('id',str(maxid+2));cn.set('name','Equation - coc_added_moment')
style=deepcopy(eq.find('.//m:r/a:rPr',NS))
def el(local):return E.Element('{'+NS['m']+'}'+local)
def run(value):
    r=el('r');r.append(deepcopy(style));t=el('t');t.text=value;r.append(t);return r
math=eq.find('.//m:oMath',NS)
for e in list(math):math.remove(e)
sub=el('sSub');base=el('e');base.append(run('r'));sub.append(base);suffix=el('sub');suffix.append(run('c'));sub.append(suffix)
math.extend([run('Δ'),run('m'),run('='),sub,run('×'),run('f')]);frame(eq,layout['intro_equation']);tree.append(eq)

# Insert a native slide and a new notes part; keep all retained notes byte-identical.
nextslide=max(int(re.search(r'slide(\d+)\.xml$',n).group(1)) for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',n))+1
nextnote=max(int(re.search(r'notesSlide(\d+)\.xml$',n).group(1)) for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n))+1
intropath=f'ppt/slides/slide{nextslide}.xml';notepath=f'ppt/notesSlides/notesSlide{nextnote}.xml'
rels=E.fromstring(parts[relpath(casepath)]);oldnote=resolve(casepath,next(r.get('Target') for r in rels if r.get('Type').endswith('/notesSlide')))
for r in rels:
    if r.get('Type').endswith('/notesSlide'):r.set('Target','../notesSlides/'+Path(notepath).name)
rel=deepcopy(next(r for r in rels if r.get('Type').endswith('/image')));rel.set('Id','rIdCocGeneral');rel.set('Target','../media/coc_force_shift_general.png');rels.append(rel)
added[intropath]=dump(intro);added[relpath(intropath)]=dump(rels);added['ppt/media/coc_force_shift_general.png']=(HERE/'assets/coc_force_shift_general.png').read_bytes()
note=E.fromstring(parts[oldnote])
for s in note.findall('.//p:sp',NS):
    ph=s.find('p:nvSpPr/p:nvPr/p:ph',NS)
    if ph is not None and ph.get('type')=='body':
        body=s.find('p:txBody',NS)
        for p in list(body.findall('a:p',NS)):body.remove(p)
        p=E.SubElement(body,'{'+NS['a']+'}p');r=E.SubElement(p,'{'+NS['a']+'}r');E.SubElement(r,'{'+NS['a']+'}t').text='[Sources]\nPresentation-specific CoC diagram derived from the existing CoC_moment and moment_bookkeeping TikZ figures. Mechanics: MyOwn/chapters/02_theoretical_background.tex, displacement definition and commanded moment decomposition (lines 764-773 and 921-936). Delta m = r_c cross f is the additional contribution, not the complete rotational spring-damper moment. No new spoken script has been added.'
noterels=E.fromstring(parts[relpath(oldnote)])
for r in noterels:
    if r.get('Type').endswith('/slide'):r.set('Target','../slides/'+Path(intropath).name)
added[notepath]=dump(note);added[relpath(notepath)]=dump(noterels)
pres=E.fromstring(parts['ppt/presentation.xml']);sids=pres.find('p:sldIdLst',NS);newsid=str(max(int(s.get('id')) for s in sids)+1);newrid='rIdCocIntroduction'
sid=deepcopy(sids[6]);sid.set('id',newsid);sid.set('{'+NS['r']+'}id',newrid);sids.insert(6,sid)
for section in pres.findall('.//p14:section',NS):
    members=section.find('p14:sldIdLst',NS)
    for i,s in enumerate(members):
        if s.get('id')==inventory[6]['sid']:
            new=deepcopy(s);new.set('id',newsid);members.insert(i,new);break
changed['ppt/presentation.xml']=dump(pres)
pr=E.fromstring(parts['ppt/_rels/presentation.xml.rels']);r=deepcopy(next(x for x in pr if x.get('Type').endswith('/slide')));r.set('Id',newrid);r.set('Target','slides/'+Path(intropath).name);pr.append(r);changed['ppt/_rels/presentation.xml.rels']=dump(pr)
ct=E.fromstring(parts['[Content_Types].xml'])
for oldpath,newpath in [(casepath,intropath),(oldnote,notepath)]:
    c=deepcopy(next(x for x in ct if x.get('PartName')=='/'+oldpath));c.set('PartName','/'+newpath);ct.append(c)
changed['[Content_Types].xml']=dump(ct)

# Renumber main-slide footers only, preserving each remaining body and backup footer.
for item in inventory[6:24]:
    root=case if item['physical']==7 else coupling if item['physical']==8 else E.fromstring(parts[item['path']])
    footer=find(root,'TextBox 6');replace_text(footer,str(item['physical']))
    if item['physical'] in [7,8]:changed[item['path']]=dump(root)
    else:
        raw=parts[item['path']].decode('utf-8');block=next(b for b in re.findall(r'<p:sp\b[^>]*>.*?</p:sp>',raw,re.S) if 'name="TextBox 6"' in b)
        old=f'<a:t>{item["physical"]-1}</a:t>';new=f'<a:t>{item["physical"]}</a:t>';assert block.count(old)==1
        changed[item['path']]=raw.replace(block,block.replace(old,new,1),1).encode('utf-8')
app=E.fromstring(parts['docProps/app.xml'])
for key,value in [('Slides',30),('Notes',30),('HiddenSlides',5)]:app.xpath('//*[local-name()=$k]',k=key)[0].text=str(value)
app.xpath('//*[local-name()="HeadingPairs"]//*[local-name()="i4"]')[-1].text='30'
vector=app.xpath('//*[local-name()="TitlesOfParts"]/*')[0];items=list(vector);pos=len(items)-29+6;new=deepcopy(items[pos]);new.text='Centre of compliance (CoC)';vector.insert(pos,new);vector.set('size',str(len(vector)));changed['docProps/app.xml']=dump(app)

assets=HERE/'assets';catalog=json.loads((HERE/'archive/assets/native_equations.json').read_text(encoding='utf-8'))
formulas={'symbol_pc':r'\displaystyle p_{\mathrm{CoC}}','coc_displacement_definition':r'\displaystyle r_c=p_{\mathrm{CoC}}-p_{\mathrm{TCP}}','coc_added_moment':r'\displaystyle \Delta m=r_c\times f'}
for c in catalog:
    if c['slide']>=7:c['slide']+=1
    asset=c['shape'].removeprefix('Equation - ')
    if asset in formulas:c['latex']=formulas[asset]
new=deepcopy(next(c for c in catalog if c['shape']=='Equation - coc_displacement_definition'));new.update({'slide':7,'shape':'Equation - coc_added_moment','source':'sources/coc_added_moment.tex','latex':formulas['coc_added_moment']});catalog.insert(next(i for i,c in enumerate(catalog) if c['slide']>7),new)
for asset,formula in formulas.items():
    if asset=='symbol_pc':
        for rel in ['sources/symbol_pc.tex','symbol_pc.pdf','symbol_pc.png','symbol_pc.svg']:
            dest=HERE/'archive/assets'/rel;dest.parent.mkdir(exist_ok=True,parents=True)
            if not dest.exists():shutil.copy2(ASSETS/rel,dest)
    tex='\\documentclass[border=3pt]{standalone}\n\\usepackage{amsmath,xcolor,unicode-math}\n\\setmathfont{Cambria Math}\n\\begin{document}\n{\\fontsize{22}{27}\\selectfont \\color{black}$'+formula+'$}\n\\end{document}\n'
    (assets/'sources'/f'{asset}.tex').write_text(tex,encoding='utf-8')
    s=eq if asset=='coc_added_moment' else find(coupling,'Equation - '+asset)
    s.find('p:nvSpPr/p:cNvPr',NS).set('descr','Editable Office equation. Uniform Cambria Math, 22 pt, regular. LaTeX source: figures_and_images/sources/'+asset+'.tex\n'+formula)
added[intropath]=dump(intro);changed[couplingpath]=dump(coupling)
(assets/'native_equations.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=json.loads((HERE/'archive/assets/manifest.json').read_text(encoding='utf-8'))
for asset in ['coc_force_shift_general','coc_force_shift_cases','coc_added_moment']:
    manifest.append({'asset':asset,'source':'sources/'+asset+'.tex','changes':'2026-10-02: Presentation-specific CoC introduction and virtual-force/moment interpretation; p_CoC notation. Original shared figures retained for provenance.'})
for asset in ['symbol_pc','coc_displacement_definition']:
    entry=next(m for m in manifest if m.get('asset')==asset);entry['changes']='2026-10-02: Use upright CoC in p_CoC consistently with the new introduction and both cases.'
(assets/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(ROOT/source['pptx'],HERE/'updated.pptx')
with ZipFile(HERE/'updated.pptx','a',ZIP_DEFLATED) as z:
    for name,data in changed.items():
        info=z.getinfo(name);z.filelist=[i for i in z.filelist if i.filename!=name];del z.NameToInfo[name];z.writestr(info,data)
    for name,data in added.items():z.writestr(name,data)
with ZipFile(HERE/'updated.pptx') as z:select(z,{7,8,9},HERE/'native_preview.pptx')
(HERE/'build.json').write_text(json.dumps({'intro_path':intropath,'new_note':notepath,'new_sid':newsid,'added_parts':list(added),'changed_parts':list(changed),'slide_count':30,'main_slides':25,'hidden_backups':5,'native_equations':31},indent=2))
print('Inserted the CoC introduction before the two shifted-force cases and updated p_CoC on the coupling slide.')
