from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
import hashlib, json, re, posixpath
from prepare import HERE, ROOT, FINAL, ARCHIVE, NS, dump, relpath, resolve, select

inventory=json.loads((HERE/'inventory_before.json').read_text())
layout=json.loads((HERE/'media-layout.json').read_text())
assert (HERE/'artifact-edited.pptx').exists()
with ZipFile(ARCHIVE/'Thesis_Defense_gg0_v3.pptx') as z:
    original={n:z.read(n) for n in z.namelist()}
parts=dict(original)
title=E.fromstring(parts['ppt/slides/slide1.xml'])
motivation=E.fromstring(parts['ppt/slides/slide2.xml'])
contact=E.fromstring(parts['ppt/slides/slide3.xml'])
tr=E.fromstring(parts['ppt/slides/_rels/slide1.xml.rels'])
mr=E.fromstring(parts['ppt/slides/_rels/slide2.xml.rels'])
cr=E.fromstring(parts['ppt/slides/_rels/slide3.xml.rels'])
photo=motivation.xpath('.//p:pic[p:nvPicPr/p:cNvPr/@name="Motivation robot photograph"]',namespaces=NS)[0]
video=deepcopy(contact.xpath('.//p:pic[p:nvPicPr/p:cNvPr/@name="Contact demonstration video"]',namespaces=NS)[0])

def set_frame(node,frame):
    x,y,w,h=frame;xf=node.find('p:spPr/a:xfrm',NS)
    xf.find('a:off',NS).attrib.update({'x':str(round(x*12700)),'y':str(round(y*12700))})
    xf.find('a:ext',NS).attrib.update({'cx':str(round(w*12700)),'cy':str(round(h*12700))})

# The artifact-tool edit defines media placement. Retain original DrawingML for
# the title/body styles, movie payload, playback actions, equations and notes.
photo.getparent().remove(photo)
meta=photo.find('p:nvPicPr/p:cNvPr',NS)
meta.set('id','15');meta.set('name','Title robot photograph')
photo.find('p:blipFill/a:blip',NS).set('{'+NS['r']+'}embed','rIdTitleRobot')
set_frame(photo,layout['titlePhoto'])
title.find('p:cSld/p:spTree',NS).append(photo)
E.SubElement(tr,'{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',Id='rIdTitleRobot',Type=NS['r']+'/image',Target='../media/title_robot.jpg')
for r in list(mr):
    if r.get('Id')=='rId4':mr.remove(r)
vmeta=video.find('p:nvPicPr/p:cNvPr',NS);vmeta.set('id','8')
set_frame(video,layout['motivationVideo'])
relmap={'rId2':'rIdContactVideo','rId1':'rIdContactMedia','rId6':'rIdContactPoster'}
for node in video.iter():
    for attr,value in list(node.attrib.items()):
        if attr.startswith('{'+NS['r']+'}') and value in relmap:node.set(attr,relmap[value])
for r in cr:
    if r.get('Id') in relmap:
        c=deepcopy(r);c.set('Id',relmap[r.get('Id')]);mr.append(c)
tree=motivation.find('p:cSld/p:spTree',NS)
tree.insert(7,video)
timing=deepcopy(contact.find('p:timing',NS))
timing.find('.//p:spTgt',NS).set('spid','8')
motivation.append(timing)
for n,x in [('ppt/slides/slide1.xml',title),('ppt/slides/slide2.xml',motivation),('ppt/slides/_rels/slide1.xml.rels',tr),('ppt/slides/_rels/slide2.xml.rels',mr)]:parts[n]=dump(x)

for entry in inventory[3:26]:
    path=entry['path'];xml=parts[path].decode('utf-8')
    blocks=re.findall(r'<p:sp\b[^>]*>.*?</p:sp>',xml,re.S)
    footer=next(x for x in blocks if 'name="TextBox 6"' in x)
    old=str(entry['physical']-1);new=str(entry['physical']-2)
    assert footer.count('<a:t>'+old+'</a:t>')==1
    parts[path]=xml.replace(footer,footer.replace('<a:t>'+old+'</a:t>','<a:t>'+new+'</a:t>',1),1).encode('utf-8')

pres=E.fromstring(parts['ppt/presentation.xml'])
removed=inventory[2]
sl=pres.find('p:sldIdLst',NS)
sl.remove(next(x for x in sl if x.get('id')==removed['sid']))
for sec in pres.findall('.//p14:section',NS):
    members=sec.find('p14:sldIdLst',NS)
    for x in list(members):
        if x.get('id')==removed['sid']:members.remove(x)
parts['ppt/presentation.xml']=dump(pres)
rels=E.fromstring(parts['ppt/_rels/presentation.xml.rels'])
rels.remove(next(x for x in rels if x.get('Id')==removed['rid']))
parts['ppt/_rels/presentation.xml.rels']=dump(rels)
deleted=['ppt/slides/slide3.xml','ppt/slides/_rels/slide3.xml.rels','ppt/notesSlides/notesSlide3.xml','ppt/notesSlides/_rels/notesSlide3.xml.rels']
for n in deleted:parts.pop(n)
ct=E.fromstring(parts['[Content_Types].xml'])
for x in list(ct):
    if x.get('PartName','').lstrip('/') in deleted:ct.remove(x)
parts['[Content_Types].xml']=dump(ct)
app=E.fromstring(parts['docProps/app.xml'])
for key,val in [('Slides',30),('Notes',30),('HiddenSlides',5)]:
    nodes=app.xpath('//*[local-name()=$key]',key=key)
    if nodes:nodes[0].text=str(val)
hp=app.xpath('//*[local-name()="HeadingPairs"]//*[local-name()="i4"]')
if hp:hp[-1].text='30'
v=app.xpath('//*[local-name()="TitlesOfParts"]/*')
if v:
    vector=v[0];items=list(vector);assert len(items)>=31
    vector.remove(items[-31+2]);vector.set('size',str(len(vector)))
parts['docProps/app.xml']=dump(app)

with ZipFile(HERE/'updated.pptx','w',ZIP_DEFLATED) as out:
    for n,data in parts.items():out.writestr(n,data)
with ZipFile(HERE/'updated.pptx') as z:select(z,{1,2},HERE/'native_preview.pptx')
catalog=json.loads((ARCHIVE/'native_equations.json').read_text())
for item in catalog:
    assert item['slide']!=3
    if item['slide']>3:item['slide']-=1
(HERE/'native_equations.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Preserve original PDF glyphs and figure streams. Move the image drawing and
# reuse the original video poster XObject; replace only the footer text blocks.
reader=PdfReader(ARCHIVE/'Thesis_Defense_gg0_v3.pdf')
writer=PdfWriter()
retained=[i for i in range(31) if i!=2]
for i in retained:writer.add_page(reader.pages[i])
if reader.metadata:writer.add_metadata({k:str(v) for k,v in reader.metadata.items() if isinstance(v,str)})
def content(page,data):
    stream=DecodedStreamObject();stream.set_data(data);page[NameObject('/Contents')]=writer._add_object(stream)

p=writer.pages[0];x,y,w,h=layout['titlePhoto']
assert '/fzImg0' in p['/Resources']['/XObject']
data=p.get_contents().get_data()+f'\nq\n{w:.8f} 0 0 {h:.8f} {x:.8f} {540-y-h:.8f} cm\n/fzImg0 Do\nQ\n'.encode()
content(p,data)
p=writer.pages[1];data=p.get_contents().get_data()
pattern=rb'q\s+400 0 0 406\.9979 521\.6 61\.501054 cm\s+/fzImg0 Do\s+Q'
assert len(re.findall(pattern,data))==1
poster_candidates=[(name,obj) for name,obj in reader.pages[2]['/Resources']['/XObject'].items() if obj.get_object().get('/Subtype')=='/Image' and obj.get_object().get('/Width',0)>1000]
assert len(poster_candidates)==1,[(k,o.get_object().get('/Width')) for k,o in poster_candidates]
p['/Resources']['/XObject'][NameObject('/ContactPoster')]=poster_candidates[0][1].clone(writer)
x,y,w,h=layout['motivationVideo']
replacement=f'q\n{w} 0 0 {h} {x} {540-y-h} cm\n/ContactPoster Do\nQ'.encode()
content(p,re.sub(pattern,replacement,data))

footer_font=reader.pages[3]['/Resources']['/Font']['/F2']
assert footer_font['/Subtype']=='/TrueType' and footer_font['/Encoding']=='/WinAnsiEncoding'
widths=footer_font['/Widths'];first=int(footer_font['/FirstChar'])
for idx in range(2,25):
    page=writer.pages[idx];data=page.get_contents().get_data()
    chunks=re.findall(rb'BT\b.*?ET',data,re.S)
    targets=[b for b in chunks if re.search(rb'(?<![\d.])9\d{2}(?:\.\d+)?\s+2\d(?:\.\d+)?\s+(?:Tm|TD|Td)\b',b)]
    assert len(targets)==1,(idx+1,targets)
    text=str(idx);width=sum(float(widths[ord(c)-first]) for c in text)*8.04/1000
    # Keep the right edge and original baseline, using the deck's Arial footer.
    baseline=26.64 if b'26.64' in targets[0] else 26.52
    footer=f'BT /MovedFooter 8.04 Tf 1 0 0 1 {921.8-width:.6f} {baseline} Tm 0.412 g 0.412 G 0 Tc [({text})] TJ ET'.encode()
    resources=DictionaryObject(page['/Resources'])
    fonts=DictionaryObject(resources['/Font'])
    fonts[NameObject('/MovedFooter')]=footer_font.clone(writer)
    resources[NameObject('/Font')]=fonts;page[NameObject('/Resources')]=resources
    content(page,data.replace(targets[0],footer,1))
writer.write(HERE/'updated.pdf')

changed=[n for n in parts if n in original and parts[n]!=original[n]]
(HERE/'build.json').write_text(json.dumps({'changed_parts':changed,'deleted_parts':deleted,'slide_count':30,'main_slides':25,'hidden_backups':5,'retained_original_pages':[x+1 for x in retained],'media_layout':layout},indent=2))
print('Built 30-slide deck and PDF; original body text, equations, video bytes and retained notes preserved.')
