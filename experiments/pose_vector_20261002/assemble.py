from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
from pypdf import PdfReader
import json,sys,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import select,NS,dump
NS['m']='http://schemas.openxmlformats.org/officeDocument/2006/math'
source=json.loads((HERE/'archive/source.json').read_text());layout=json.loads((HERE/'layout.json').read_text());PART='ppt/slides/slide5.xml'
with ZipFile(ROOT/source['pptx']) as z:raw=z.read(PART)
root=E.fromstring(raw);tree=root.find('p:cSld/p:spTree',NS)
def find(name):
    matches=root.xpath('.//*[p:nvSpPr/p:cNvPr/@name=$n or p:nvPicPr/p:cNvPr/@name=$n]',namespaces=NS,n=name)
    assert len(matches)==1,name
    return matches[0]
def frame(s,box):
    xf=s.find('p:spPr/a:xfrm',NS)
    for key,val in zip(['x','y'],box[:2]):xf.find('a:off',NS).set(key,str(round(val*12700)))
    if len(box)==4:
        for key,val in zip(['cx','cy'],box[2:]):xf.find('a:ext',NS).set(key,str(round(val*12700)))
for name,settings in layout['text'].items():
    s=find(name);frame(s,settings.get('box',settings.get('xy')))
    if 'text' in settings:
        ts=s.findall('.//a:t',NS);assert len(ts)==1;ts[0].text=settings['text']
for name in layout['remove']:
    s=find(name);s.getparent().remove(s)
for name,box in layout['pictures'].items():frame(find(name),box)

template=deepcopy(find('Equation - pose_joint_configuration'))
run_style=deepcopy(template.find('.//m:r/a:rPr',NS))
def elem(local,**attributes):return E.Element('{'+NS['m']+'}'+local,{'{'+NS['m']+'}'+k:v for k,v in attributes.items()})
def run(text,plain=False):
    r=elem('r')
    if plain:
        p=elem('rPr');p.append(elem('sty',val='p'));r.append(p)
    r.append(deepcopy(run_style));t=elem('t');t.text=text;r.append(t);return r
def sub(symbol,suffix='EE'):
    s=elem('sSub');e=elem('e');e.append(run(symbol));s.append(e);bottom=elem('sub');bottom.append(run(suffix,True));s.append(bottom);return s
def transpose(content):
    s=elem('sSup');e=elem('e');e.extend(content);s.append(e);top=elem('sup');top.append(run('⊤',True));s.append(top);return s
def column(rows):
    d=elem('d');dp=elem('dPr');dp.append(elem('begChr',val='['));dp.append(elem('endChr',val=']'));d.append(dp)
    de=elem('e');matrix=elem('m');mp=elem('mPr');mp.append(elem('baseJc',val='center'))
    mcs=elem('mcs');mc=elem('mc');mcp=elem('mcPr');mcp.append(elem('count',val='1'));mcp.append(elem('mcJc',val='center'));mc.append(mcp);mcs.append(mc);mp.append(mcs);matrix.append(mp)
    for content in rows:
        mr=elem('mr');e=elem('e');e.extend(content);mr.append(e);matrix.append(mr)
    de.append(matrix);d.append(de);return d
def set_math(shape,content):
    math=shape.find('.//m:oMath',NS)
    for child in list(math):math.remove(child)
    math.extend(content)
def description(shape,name,latex):
    shape.find('p:nvSpPr/p:cNvPr',NS).set('descr','Editable Office equation. Uniform Cambria Math, 22 pt, regular. LaTeX source: figures_and_images/sources/'+name+'.tex\n'+latex)
joint_latex=r'\displaystyle p_{\mathrm{EE}}=p_{\mathrm{EE}}(q)'
joint=find('Equation - pose_joint_configuration');set_math(joint,[sub('p'),run('='),sub('p'),run('('),run('q'),run(')')]);frame(joint,layout['equations']['Equation - pose_joint_configuration']);description(joint,'pose_joint_configuration',joint_latex)
maxid=max(int(x.get('id')) for x in root.findall('.//p:cNvPr',NS))
def newid():
    global maxid
    maxid+=1;return str(maxid)
pose_latex=r'\displaystyle x_{\mathrm{EE}}=\begin{bmatrix}p_{\mathrm{EE}}\\\eta_{\mathrm{EE}}\end{bmatrix}=\begin{bmatrix}(x,y,z)^{\top}\\(\phi,\theta,\psi)^{\top}\end{bmatrix}'
full=deepcopy(template);cn=full.find('p:nvSpPr/p:cNvPr',NS);cn.set('id',newid());cn.set('name','Equation - cartesian_pose_vector')
ext=cn.find('a:extLst',NS)
if ext is not None:cn.remove(ext)
pose_components=column([[transpose([run('(x,y,z)')])],[transpose([run('(φ,θ,ψ)')])]])
set_math(full,[sub('x'),run('='),column([[sub('p')],[sub('η')]]),run('='),pose_components])
frame(full,layout['equations']['Equation - cartesian_pose_vector']);description(full,'cartesian_pose_vector',pose_latex);tree.append(full)

# Native connectors show the requested split and sit behind the labels.
for branch in layout['branches']:
    s=E.Element('{'+NS['p']+'}cxnSp');nv=E.SubElement(s,'{'+NS['p']+'}nvCxnSpPr');E.SubElement(nv,'{'+NS['p']+'}cNvPr',id=newid(),name=branch['name']);E.SubElement(nv,'{'+NS['p']+'}cNvCxnSpPr');E.SubElement(nv,'{'+NS['p']+'}nvPr')
    props=E.SubElement(s,'{'+NS['p']+'}spPr');xf=E.SubElement(props,'{'+NS['a']+'}xfrm')
    x,y=branch['from'];xx,yy=branch['to'];E.SubElement(xf,'{'+NS['a']+'}off',x=str(round(x*12700)),y=str(round(y*12700)));E.SubElement(xf,'{'+NS['a']+'}ext',cx=str(round((xx-x)*12700)),cy=str(round((yy-y)*12700)))
    geom=E.SubElement(props,'{'+NS['a']+'}prstGeom',prst='line');E.SubElement(geom,'{'+NS['a']+'}avLst');ln=E.SubElement(props,'{'+NS['a']+'}ln',w='12700');fill=E.SubElement(ln,'{'+NS['a']+'}solidFill');E.SubElement(fill,'{'+NS['a']+'}srgbClr',val='17365D')
    if branch.get('arrow'):E.SubElement(ln,'{'+NS['a']+'}tailEnd',type='triangle',w='sm',len='sm')
    tree.insert(2,s)
with ZipFile(HERE/'text_assets.pptx') as z:
    assets=E.fromstring(z.read('ppt/slides/slide1.xml'))
    for shape in assets.findall('p:cSld/p:spTree/p:sp',NS):
        shape=deepcopy(shape);shape.find('p:nvSpPr/p:cNvPr',NS).set('id',newid());tree.append(shape)
(HERE/'slide5.xml').write_bytes(dump(root))
new_png=(HERE/'assets/cartesian_pose_position.png').read_bytes()
with ZipFile(ROOT/source['pptx']) as z,ZipFile(HERE/'updated.pptx','w',ZIP_DEFLATED) as out:
    for info in z.infolist():
        out.writestr(info,dump(root) if info.filename==PART else new_png if info.filename==source['position_media'] else z.read(info.filename))
with ZipFile(HERE/'updated.pptx') as z:select(z,{4},HERE/'native_preview.pptx')
catalog=json.loads((HERE/'archive/assets/native_equations.json').read_text())
entry=next(x for x in catalog if x['shape']=='Equation - pose_joint_configuration');entry['latex']=joint_latex
new=deepcopy(entry);new.update({'shape':'Equation - cartesian_pose_vector','source':'sources/cartesian_pose_vector.tex','latex':pose_latex});catalog.insert(0,new)
(HERE/'assets/native_equations.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name,latex in [('pose_joint_configuration',joint_latex),('cartesian_pose_vector',pose_latex)]:
    text='\\documentclass[border=3pt]{standalone}\n\\usepackage{amsmath,xcolor,unicode-math}\n\\setmathfont{Cambria Math}\n% Native PowerPoint equivalent: 22 pt regular Cambria Math.\n\\begin{document}\n{\\fontsize{22}{27}\\selectfont \\color{black}$'+latex+'$}\n\\end{document}\n'
    (HERE/'assets/sources'/f'{name}.tex').write_text(text,encoding='utf-8')
manifest=json.loads((HERE/'archive/assets/manifest.json').read_text())
for name,change in [('cartesian_pose_position','2026-10-02: The end-effector position arrow is labelled p_EE. Original diagram geometry and parenthesized (EE) label retained.'),('pose_joint_configuration','2026-10-02: The end-effector position is explicitly p_EE = p_EE(q). Native 22 pt Cambria Math equation and PDF/PNG/SVG assets agree.'),('cartesian_pose_vector','2026-10-02: Native two-row Cartesian pose coordinate vector: position p_EE and roll-pitch-yaw orientation eta_EE, expanded to (x,y,z)^T and (phi,theta,psi)^T. The orientation coordinates describe the existing roll-pitch-yaw illustration.')]:
    matches=[m for m in manifest if m.get('asset')==name]
    if matches:matches[0]['changes']=change
    else:manifest.append({'asset':name,'source':'sources/'+name+'.tex','changes':change,'equation_style':{'font':'Cambria Math','size_pt':22,'weight':'regular','color':'#000000'}})
(HERE/'assets/manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Prepared slide 4 with p_EE in both places, a native full-pose vector, and the two-part diagram split.')
