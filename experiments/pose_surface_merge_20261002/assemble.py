from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import sys,json,re,posixpath,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,dump,relpath,resolve,select
source=json.loads((HERE/'archive/source.json').read_text());inventory=json.loads((HERE/'inventory.json').read_text());layout=json.loads((HERE/'layout.json').read_text())
with ZipFile(ROOT/source['pptx']) as z:old={n:z.read(n) for n in z.namelist()}
parts=dict(old)
posepath=inventory[3]['path'];surfpath=inventory[4]['path']
pose=E.fromstring(parts[posepath]);surf=E.fromstring(parts[surfpath]);tree=pose.find('p:cSld/p:spTree',NS)
pr=E.fromstring(parts[relpath(posepath)]);sr=E.fromstring(parts[relpath(surfpath)])
def find(root,name):
    q=root.xpath('.//*[p:nvSpPr/p:cNvPr/@name=$n or p:nvPicPr/p:cNvPr/@name=$n]',namespaces=NS,n=name)
    assert len(q)==1,name
    return q[0]
def frame(node,values):
    xf=node.find('p:spPr/a:xfrm',NS);x,y=values[:2];xf.find('a:off',NS).set('x',str(round(x*12700)));xf.find('a:off',NS).set('y',str(round(y*12700)))
    if len(values)==4:
        xf.find('a:ext',NS).set('cx',str(round(values[2]*12700)));xf.find('a:ext',NS).set('cy',str(round(values[3]*12700)))
title=find(pose,'Slide title');title.find('.//a:t',NS).text=layout['title']
for name in ['Position heading','Orientation heading','Pose takeaway']:
    s=find(pose,name);s.getparent().remove(s)
for name in ['Surface frame','Equation - symbol_ns','Equation - symbol_tangents']:
    s=deepcopy(find(surf,name))
    for node in s.iter():
        for attr,value in list(node.attrib.items()):
            if attr.startswith('{'+NS['r']+'}') and value:
                newrid='rIdMergedSurface_'+value
                if not any(x.get('Id')==newrid for x in pr):
                    original=next(x for x in sr if x.get('Id')==value);rel=deepcopy(original);rel.set('Id',newrid);pr.append(rel)
                node.set(attr,newrid)
    tree.append(s)
for name,rect in layout['pictures'].items():frame(find(pose,name),rect)
for name,xy in layout['equations'].items():frame(find(pose,name),xy)
with ZipFile(HERE/'text_assets.pptx') as z:
    assets=E.fromstring(z.read('ppt/slides/slide1.xml'))
    for idx,shape in enumerate(assets.findall('p:cSld/p:spTree/p:sp',NS),200):
        shape=deepcopy(shape);shape.find('p:nvSpPr/p:cNvPr',NS).set('id',str(idx));tree.append(shape)
parts[posepath]=dump(pose);parts[relpath(posepath)]=dump(pr)
for item in inventory[5:25]:
    xml=parts[item['path']].decode('utf-8');blocks=re.findall(r'<p:sp\b[^>]*>.*?</p:sp>',xml,re.S);footer=next(x for x in blocks if 'name="TextBox 6"' in x)
    a,b=str(item['physical']-1),str(item['physical']-2)
    assert footer.count('<a:t>'+a+'</a:t>')==1
    parts[item['path']]=xml.replace(footer,footer.replace('<a:t>'+a+'</a:t>','<a:t>'+b+'</a:t>',1),1).encode('utf-8')
pres=E.fromstring(parts['ppt/presentation.xml']);removed=inventory[4];ids=pres.find('p:sldIdLst',NS)
ids.remove(next(x for x in ids if x.get('id')==removed['sid']))
for sec in pres.findall('.//p14:section',NS):
    members=sec.find('p14:sldIdLst',NS)
    for x in list(members):
        if x.get('id')==removed['sid']:members.remove(x)
parts['ppt/presentation.xml']=dump(pres)
rels=E.fromstring(parts['ppt/_rels/presentation.xml.rels']);rels.remove(next(x for x in rels if x.get('Id')==removed['rid']));parts['ppt/_rels/presentation.xml.rels']=dump(rels)
notepath=resolve(surfpath,next(x.get('Target') for x in sr if x.get('Type').endswith('/notesSlide')))
deleted=[surfpath,relpath(surfpath),notepath,relpath(notepath)]
for n in deleted:parts.pop(n)
ct=E.fromstring(parts['[Content_Types].xml'])
for x in list(ct):
    if x.get('PartName','').lstrip('/') in deleted:ct.remove(x)
parts['[Content_Types].xml']=dump(ct)
app=E.fromstring(parts['docProps/app.xml'])
for key,value in [('Slides',29),('Notes',29),('HiddenSlides',5)]:
    app.xpath('//*[local-name()=$k]',k=key)[0].text=str(value)
app.xpath('//*[local-name()="HeadingPairs"]//*[local-name()="i4"]')[-1].text='29'
vector=app.xpath('//*[local-name()="TitlesOfParts"]/*')[0];items=list(vector);items[-30+3].text=layout['title'];vector.remove(items[-30+4]);vector.set('size',str(len(vector)));parts['docProps/app.xml']=dump(app)
with ZipFile(HERE/'updated.pptx','w',ZIP_DEFLATED) as z:
    for n,data in parts.items():z.writestr(n,data)
with ZipFile(HERE/'updated.pptx') as z:select(z,{4,5},HERE/'native_preview.pptx')
catalog=json.loads((HERE/'archive/native_equations.json').read_text())
for item in catalog:
    if item['slide']==5:item['slide']=4
    elif item['slide']>5:item['slide']-=1
(HERE/'native_equations.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(HERE/'build.json').write_text(json.dumps({'removed_parts':deleted,'changed_parts':[n for n in parts if parts[n]!=old.get(n)],'slide_count':29,'main_slides':24,'backups':5,'retained_original_pages':[i for i in range(1,31) if i!=5]},indent=2))
print('Combined pose and surface frame on physical slide 4; controller follows at slide 5. All 29 native equations retained.')
