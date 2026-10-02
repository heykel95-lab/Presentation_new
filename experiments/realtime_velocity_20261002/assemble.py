from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,sys,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import select,NS,dump
NS['m']='http://schemas.openxmlformats.org/officeDocument/2006/math'
source=json.loads((HERE/'archive/source.json').read_text());layout=json.loads((HERE/'layout.json').read_text());PART='ppt/slides/slide7.xml'
with ZipFile(ROOT/source['pptx']) as z:root=E.fromstring(z.read(PART))
tree=root.find('p:cSld/p:spTree',NS)
def shape(name):
    s=root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$n]',namespaces=NS,n=name);assert len(s)==1,name;return s[0]
def frame(s,box):
    xf=s.find('p:spPr/a:xfrm',NS)
    for key,val in zip(['x','y'],box[:2]):xf.find('a:off',NS).set(key,str(round(val*12700)))
    for key,val in zip(['cx','cy'],box[2:]):xf.find('a:ext',NS).set(key,str(round(val*12700)))
for name,value in layout['headings'].items():
    texts=shape(name).findall('.//a:t',NS);assert len(texts)==1;texts[0].text=value
# Match the Jacobian heading to the original PDF and its adjacent bullet.
# The older native shape had a stale 20 pt black override.
for rpr in shape('Jacobian velocity mapping').xpath('.//a:rPr|.//a:defRPr|.//a:endParaRPr',namespaces=NS):
    rpr.set('sz','2200');rpr.find('a:solidFill/a:srgbClr',NS).set('val','17365D')
torque=shape('Equation - cartesian_torque_mapping');math=torque.find('.//m:oMath',NS)
children=list(math);start=next(i for i,c in enumerate(children) if c.find('m:t',NS) is not None and c.find('m:t',NS).text=='τ')
for c in children[:start]:math.remove(c)
velocity=shape('Equation - jacobian_velocity_mapping');math=velocity.find('.//m:oMath',NS)
stack=math[0];assert E.QName(stack).localname=='d'
xdot=deepcopy(stack.find('.//m:sSub',NS));letter=xdot.find('.//m:acc/m:e/m:r/m:t',NS);assert letter.text=='p';letter.text='x';math.replace(stack,xdot)
latex={'cartesian_torque_mapping':r'\displaystyle \tau=J^\top(q)F','jacobian_velocity_mapping':r'\displaystyle \dot{x}_{\mathrm{EE}}=J(q)\dot{q}'}
for name,box in layout['equations'].items():
    s=shape(name);frame(s,box);asset=name.removeprefix('Equation - ')
    desc='Editable Office equation. Uniform Cambria Math, 22 pt, regular. LaTeX source: figures_and_images/sources/'+asset+'.tex\n'+latex[asset]
    if asset=='jacobian_velocity_mapping':desc+='\nHere x-dot_EE denotes the geometric Cartesian velocity [p-dot_EE; omega_EE], not derivatives of roll-pitch-yaw coordinates.'
    s.find('p:nvSpPr/p:cNvPr',NS).set('descr',desc)
maxid=max(int(x.get('id')) for x in root.findall('.//p:cNvPr',NS))
with ZipFile(HERE/'text_assets.pptx') as z:
    assets=E.fromstring(z.read('ppt/slides/slide1.xml'))
    for i,s in enumerate(assets.findall('p:cSld/p:spTree/p:sp',NS),1):
        s=deepcopy(s);s.find('p:nvSpPr/p:cNvPr',NS).set('id',str(maxid+i));tree.append(s)
data=dump(root);(HERE/'slide7.xml').write_bytes(data)
shutil.copyfile(ROOT/source['pptx'],HERE/'updated.pptx')
with ZipFile(HERE/'updated.pptx','a',ZIP_DEFLATED) as z:
    info=z.getinfo(PART);z.filelist=[i for i in z.filelist if i.filename!=PART];del z.NameToInfo[PART];z.writestr(info,data)
with ZipFile(HERE/'updated.pptx') as z:select(z,{6},HERE/'native_preview.pptx')
out=HERE/'assets';(out/'sources').mkdir(exist_ok=True,parents=True)
catalog=json.loads((HERE/'archive/assets/native_equations.json').read_text(encoding='utf-8'))
manifest=json.loads((HERE/'archive/assets/manifest.json').read_text(encoding='utf-8'))
for asset,formula in latex.items():
    entry=next(c for c in catalog if c['shape']=='Equation - '+asset);entry['latex']=formula
    if asset=='jacobian_velocity_mapping':entry['notation']='x-dot_EE denotes geometric Cartesian velocity: linear velocity stacked with angular velocity; it is not a vector of Euler-angle derivatives.'
    note='% x-dot_EE is geometric linear/angular velocity, not the derivative of the RPY coordinate vector.\n' if asset=='jacobian_velocity_mapping' else '% Cartesian contribution; model and null-space torques are added in the preserved diagram.\n'
    tex='\\documentclass[border=3pt]{standalone}\n\\usepackage{amsmath,xcolor,unicode-math}\n\\setmathfont{Cambria Math}\n'+note+'\\begin{document}\n{\\fontsize{22}{27}\\selectfont \\color{black}$'+formula+'$}\n\\end{document}\n'
    (out/'sources'/f'{asset}.tex').write_text(tex,encoding='utf-8')
    m=next(m for m in manifest if m.get('asset')==asset)
    m['changes']='2026-10-02: '+('Use compact x-dot_EE = J(q)q-dot for geometric linear/angular Cartesian velocity; native 22 pt regular Cambria Math.' if asset=='jacobian_velocity_mapping' else 'Retain only tau = J^T(q)F, removing the repeated stacked wrench definition; native 22 pt regular Cambria Math.')
(out/'native_equations.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(out/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Prepared compact Cartesian velocity and motor torque mapping with colon-ended headings.')
