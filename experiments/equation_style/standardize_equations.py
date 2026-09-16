"""Normalize all editable equation shapes to 22 pt regular Cambria Math.

Preserve the native Office Math structures. The PDF and equation assets reuse
the original PowerPoint equation vectors, scaled uniformly, with bold zeros
replaced by regular zeros from the same embedded Cambria Math font.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
import json,posixpath,re,shutil
from lxml import etree as E
import fitz

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images';SNAP=HERE/'review'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
SIZE=22.0;FONT='Cambria Math'
def tag(s):p,n=s.split(':');return '{'+NS[p]+'}'+n
def parse(data):return E.fromstring(data)
def dump(root):return E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
def relpath(path):return posixpath.dirname(path)+'/_rels/'+posixpath.basename(path)+'.rels'
def shape(root,name):return next(s for s in root.findall('.//p:sp',NS) if s.find('p:nvSpPr/p:cNvPr',NS).get('name')==name)
def rect(s):
    a=s.find('p:spPr/a:xfrm/a:off',NS);b=s.find('p:spPr/a:xfrm/a:ext',NS)
    x,y=int(a.get('x'))/12700,int(a.get('y'))/12700
    return fitz.Rect(x,y,x+int(b.get('cx'))/12700,y+int(b.get('cy'))/12700)
def move(s,b):
    a=s.find('p:spPr/a:xfrm/a:off',NS);e=s.find('p:spPr/a:xfrm/a:ext',NS)
    for k,v in [('x',b.x0),('y',b.y0)]:a.set(k,str(round(v*12700)))
    for k,v in [('cx',b.width),('cy',b.height)]:e.set(k,str(round(v*12700)))
def shifted(b,dx=0,dy=0):return fitz.Rect(b.x0+dx,b.y0+dy,b.x1+dx,b.y1+dy)

with ZipFile(SNAP/'before.pptx') as z:parts={n:z.read(n) for n in z.namelist()}
original=dict(parts);pres=parse(parts['ppt/presentation.xml']);rels={r.get('Id'):r.get('Target') for r in parse(parts['ppt/_rels/presentation.xml.rels'])}
paths=[posixpath.normpath('ppt/'+rels[n.get(tag('r:id'))]) for n in pres.find('p:sldIdLst',NS)]
catalog=json.loads((SNAP/'before_equations.json').read_text());oldpdf=fitz.open(SNAP/'before.pdf');pdf=fitz.open();pdf.insert_pdf(oldpdf)
fontxref=next(f[0] for f in oldpdf[5].get_fonts() if 'CambriaMath' in f[3]);fontbuffer=oldpdf.extract_font(fontxref)[3];mathfont=fitz.Font(fontbuffer=fontbuffer)
roots={n:parse(parts[paths[n-1]]) for n in {c['slide'] for c in catalog}}
records=[]
for c in catalog:
    s=shape(roots[c['slide']],c['shape']);b=rect(s);page=oldpdf[c['slide']-1];chars=[]
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']!='CambriaMath':continue
                for ch in span['chars']:
                    cb=fitz.Rect(ch['bbox']);intersection=cb&b
                    if not intersection.is_empty and intersection.get_area()/max(cb.get_area(),.001)>.2:
                        chars.append({**ch,'size':span['size']})
    assert chars,c
    ink=fitz.Rect(chars[0]['bbox'])
    for ch in chars:ink|=fitz.Rect(ch['bbox'])
    # Matrix brackets, underbraces, scalable parentheses and fraction bars are
    # vector paths rather than ordinary character runs in a PowerPoint PDF.
    search=b+(-3,-3,3,9)
    for d in page.get_drawings():
        visible=(d.get('fill_opacity') or 0)>0 or (d.get('stroke_opacity') or 0)>0
        if visible and search.contains(d['rect']):ink|=d['rect']
    clip=ink+(-1.5,-1.5,1.5,1.5)
    primary=next(ch for ch in chars if abs(ch['size']-c['font_size_pt'])<.3 and not ch['c'].isspace())
    ratio=SIZE/c['font_size_pt'];py=primary['origin'][1];px=b.x0
    if c['shape']=='Equation - cartesian_torque_mapping':px=(ink.x0+ink.x1)/2
    dy=-6 if c['shape'] in ['Equation - symbol_ns','Equation - symbol_tangents'] else 0
    records.append({'catalog':c,'shape':s,'asset':c['shape'].removeprefix('Equation - ') if hasattr(str,'removeprefix') else c['shape'][11:],'old':b,'clip':clip,'chars':chars,'ratio':ratio,'px':px,'py':py,'dx':0,'dy':dy,'equals':[ch['origin'][0] for ch in chars if ch['c']=='=']})

byname={r['asset']:r for r in records}
for group in [['position_error_definition','equation_force'],['controller_orientation_error','equation_moment'],['coupling_point_shift','coc_displacement_definition'],['contact_normal_gain','contact_tangent_gains','contact_normal_rotation','contact_rotation_gains']]:
    target=byname[group[0]]['equals'][0]
    for name in group:
        r=byname[name];r['dx']=target-(r['px']+(r['equals'][0]-r['px'])*r['ratio'])

def transform(r,b):
    f=lambda x:r['px']+(x-r['px'])*r['ratio']+r['dx']
    g=lambda y:r['py']+(y-r['py'])*r['ratio']+r['dy']
    return fitz.Rect(f(b.x0),g(b.y0),f(b.x1),g(b.y1))

def normalize_rpr(rp):
    rp.set('sz','2200');rp.set('b','0')
    for node in list(rp):
        if E.QName(node).localname in ['solidFill','gradFill','noFill','pattFill','latin','ea','cs','sym']:rp.remove(node)
    fill=E.Element(tag('a:solidFill'));E.SubElement(fill,tag('a:srgbClr'),val='000000');rp.insert(0,fill)
    for local in ['latin','ea','cs']:E.SubElement(rp,tag('a:'+local),typeface=FONT)

sources_backup=SNAP/'sources';sources_backup.mkdir(exist_ok=True)
font_replacements=0
for r in records:
    c=r['catalog'];s=r['shape'];move(s,transform(r,r['old']))
    for rp in s.xpath('.//a:rPr|.//a:defRPr|.//a:endParaRPr',namespaces=NS):normalize_rpr(rp)
    for sty in s.findall('.//m:sty',NS):
        value=sty.get(tag('m:val'))
        if value in ['b','bi']:sty.set(tag('m:val'),'p' if value=='b' else 'i');font_replacements+=1
    c['font']=FONT;c['font_size_pt']=SIZE;c['font_weight']='regular';c['color']='#000000'
    c['latex']=c['latex'].replace('\\mathbf{0}','\\mathrm{0}')
    s.find('p:nvSpPr/p:cNvPr',NS).set('descr','Editable Office equation. Uniform Cambria Math, 22 pt, regular. LaTeX source: figures_and_images/'+c['source']+'\n'+c['latex'])
    source=ASSETS/c['source']
    if not (sources_backup/source.name).exists():shutil.copyfile(source,sources_backup/source.name)
    source.write_text('\\documentclass[border=3pt]{standalone}\n\\usepackage{amsmath,xcolor}\n\\usepackage{unicode-math}\n\\setmathfont{Cambria Math}\n% Compile with LuaLaTeX on a system with Cambria Math installed.\n% Presentation standard: 22 pt, regular weight, black.\n\\begin{document}\n{\\fontsize{22}{27}\\selectfont \\color{black}$'+c['latex']+'$}\n\\end{document}\n')

    # Isolate the original vector equation and remove all outside content.
    isolated=fitz.open();isolated.insert_pdf(oldpdf,from_page=c['slide']-1,to_page=c['slide']-1);ep=isolated[0];clip=r['clip'];w,h=ep.rect.width,ep.rect.height
    outside=[fitz.Rect(0,0,w,clip.y0),fitz.Rect(0,clip.y1,w,h),fitz.Rect(0,clip.y0,clip.x0,clip.y1),fitz.Rect(clip.x1,clip.y0,w,clip.y1)]
    for box in outside:ep.add_redact_annot(box,fill=None)
    ep.apply_redactions(images=2,graphics=2)
    zeros=[ch for ch in r['chars'] if ch['c']=='𝟎']
    for ch in zeros:ep.add_redact_annot(fitz.Rect(ch['bbox']),fill=None)
    if zeros:
        ep.apply_redactions(images=0,graphics=0);ep.insert_font(fontname='CambriaRegularZero',fontbuffer=fontbuffer)
        for ch in zeros:
            b=fitz.Rect(ch['bbox']);width=mathfont.text_length('0',fontsize=ch['size'])
            ep.insert_text(((b.x0+b.x1-width)/2,ch['origin'][1]),'0',fontname='CambriaRegularZero',fontsize=ch['size'],color=(0,0,0))
    # All equation text and vector strokes use the same black colour.
    ep.clean_contents()
    for xref in ep.get_contents():
        data=isolated.xref_stream(xref)
        number=rb'[-+]?(?:\d*\.\d+|\d+)(?:[Ee][-+]?\d+)?'
        data=re.sub(rb'(?<!\S)'+number+rb'\s+'+number+rb'\s+'+number+rb'\s+(rg|RG)\b',lambda m:b'0 g' if m.group(1)==b'rg' else b'0 G',data)
        isolated.update_stream(xref,data)
    ep.set_cropbox(clip)
    asset=fitz.open();ap=asset.new_page(width=clip.width*r['ratio'],height=clip.height*r['ratio']);ap.show_pdf_page(ap.rect,isolated,0)
    name=r['asset'];asset.save(ASSETS/(name+'.pdf'),garbage=4,deflate=True)
    ap.get_pixmap(matrix=fitz.Matrix(4,4),alpha=False).save(ASSETS/(name+'.png'))
    (ASSETS/(name+'.svg')).write_text(ap.get_svg_image())
    r['asset_pdf']=asset;r['new_clip']=transform(r,clip)

# Move the two surface-definition captions with their symbol rows, keeping
# the larger tangent symbols clear of the footer.
caption_moves=[]
for name in ['Surface normal definition','Surface tangent definition']:
    s=shape(roots[10],name);old=rect(s);new=shifted(old,dy=-6);move(s,new);caption_moves.append((10,name,old,new))

# Clear every old equation first, then insert the revised vector assets.
for r in records:pdf[r['catalog']['slide']-1].add_redact_annot(r['clip'],fill=(1,1,1))
for n,name,old,new in caption_moves:pdf[n-1].add_redact_annot(old,fill=(1,1,1))
for n in roots:pdf[n-1].apply_redactions(images=0,graphics=1)
for r in records:pdf[r['catalog']['slide']-1].show_pdf_page(r['new_clip'],r['asset_pdf'],0)
arial='/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf'
for n,name,old,new in caption_moves:
    p=pdf[n-1];p.insert_font(fontname='ArialEquationStyle',fontfile=arial)
    for block in oldpdf[n-1].get_text('rawdict',clip=old)['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                color=tuple(((span['color']>>shift)&255)/255 for shift in [16,8,0])
                for ch in span['chars']:p.insert_text((ch['origin'][0],ch['origin'][1]-6),ch['c'],fontname='ArialEquationStyle',fontsize=span['size'],color=color)

for n,root in roots.items():
    parts[paths[n-1]]=dump(root)
    rs=parse(parts[relpath(paths[n-1])]);nr=next(x for x in rs if x.get('Type').endswith('/notesSlide'));np=posixpath.normpath(posixpath.dirname(paths[n-1])+'/'+nr.get('Target'));note=parse(parts[np])
    body=next(s.find('p:txBody',NS) for s in note.findall('.//p:sp',NS) if s.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None and s.find('p:nvSpPr/p:nvPr/p:ph',NS).get('type')=='body')
    p=E.SubElement(body,tag('a:p'));run=E.SubElement(p,tag('a:r'));E.SubElement(run,tag('a:t')).text='[Equation typography]\nAll standalone equations and mathematical symbol keys use Cambria Math, 22 pt, regular weight and black. Normal mathematical subscript and superscript scaling is retained. Equation content and native Office Math structures are unchanged.'
    parts[np]=dump(note)

# Refresh the current six Overview labels from unchanged native sections.
chapters=[s.get('name') for s in pres.xpath('//*[local-name()="section"]') if s.get('name')!='Backup'];overview=parse(parts[paths[3]])
for i,title in enumerate(chapters,1):
    s=shape(overview,'Overview item '+str(i));nodes=s.findall('.//a:t',NS);assert len(nodes)==1;nodes[0].text=title
parts[paths[3]]=dump(overview)
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx','w',ZIP_DEFLATED) as z:
    for name,data in parts.items():z.writestr(name,data)
pdf.save(FINAL/'Thesis_Defense_gg0_v3.pdf',garbage=4,deflate=True)
supp=fitz.open();supp.insert_pdf(pdf,from_page=25,to_page=33);supp.save(FINAL/'Supplementary_slides.pdf',garbage=4,deflate=True)
(ASSETS/'native_equations.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
script=(SNAP/'before_script.tex').read_text();script=script.replace('\\begin{document}','% All 35 PowerPoint equations and symbol keys: 22 pt regular Cambria Math. Spoken content is unchanged.\n\\begin{document}',1)
(FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex').write_text(script)
manifest=json.loads((ASSETS/'manifest.json').read_text())
for c in catalog:
    name=c['shape'][11:];matches=[m for m in manifest if m.get('asset')==name]
    if not matches:
        entry={'asset':name,'source':c['source']};manifest.append(entry);matches=[entry]
    for entry in matches:entry['equation_style']={'font':FONT,'size_pt':SIZE,'weight':'regular','color':'#000000','rendering':'Original native PowerPoint vectors scaled to the uniform base size. Bold zeros replaced with regular Cambria Math zeros.'}
(ASSETS/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
report={'font':FONT,'size_pt':SIZE,'weight':'regular','color':'#000000','equations':len(records),'bold_math_runs_normalized':font_replacements,'changed_physical_slides':sorted(roots),'caption_rows_moved_up_pt':6,'geometry':[{'asset':r['asset'],'slide':r['catalog']['slide'],'old_size_pt':json.loads((SNAP/'before_equations.json').read_text())[i]['font_size_pt'],'old_shape':list(r['old']),'new_shape':list(transform(r,r['old'])),'old_ink':list(r['clip']),'new_ink':list(r['new_clip'])} for i,r in enumerate(records)],'pdf_method':'Original PowerPoint equation vectors isolated and uniformly scaled. All other slide content retained.'}
(HERE/'update.json').write_text(json.dumps(report,indent=2)+'\n')
print('Standardized 35 editable equations and symbol keys to 22 pt regular Cambria Math. Bold matrix zeros removed.')
