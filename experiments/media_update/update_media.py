"""Apply the requested title photo, thesis Figure 1.1 and two video replacements.

Edits selected OOXML parts to preserve native maths and unrelated slides.
Uses the local pre-edit snapshot in review/, not an older narrative template.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
import hashlib,json,posixpath,re,shutil
from lxml import etree as E
import fitz

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ASSETS=FINAL/'figures_and_images'
SNAP=HERE/'review'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
PKG='http://schemas.openxmlformats.org/package/2006/relationships'
P14='http://schemas.microsoft.com/office/powerpoint/2010/main'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
def tag(s):p,n=s.split(':');return '{'+NS[p]+'}'+n
def parse(s):return E.fromstring(s)
def dump(s):return E.tostring(s,encoding='UTF-8',xml_declaration=True,standalone=True)
def relpath(s):return posixpath.dirname(s)+'/_rels/'+posixpath.basename(s)+'.rels'
def resolve(path,target):return posixpath.normpath(posixpath.join(posixpath.dirname(path),target))
def shape(root,name):return next(s for s in root.findall('.//p:sp',NS) if s.find('p:nvSpPr/p:cNvPr',NS).get('name')==name)
def rectangle(s):
    o=s.find('p:spPr/a:xfrm/a:off',NS);e=s.find('p:spPr/a:xfrm/a:ext',NS)
    x,y=int(o.get('x'))/12700,int(o.get('y'))/12700
    return fitz.Rect(x,y,x+int(e.get('cx'))/12700,y+int(e.get('cy'))/12700)
def move(s,box):
    o=s.find('p:spPr/a:xfrm/a:off',NS);e=s.find('p:spPr/a:xfrm/a:ext',NS)
    for k,v in [('x',box.x0),('y',box.y0)]:o.set(k,str(round(v*12700)))
    for k,v in [('cx',box.width),('cy',box.height)]:e.set(k,str(round(v*12700)))
def text(s,value):
    body=s.find('p:txBody',NS);p=deepcopy(body.find('a:p',NS));style=deepcopy(p.find('a:r/a:rPr',NS))
    for ch in list(p):
        if ch.tag!=tag('a:pPr'):p.remove(ch)
    r=E.SubElement(p,tag('a:r'));r.append(style);E.SubElement(r,tag('a:t')).text=value
    for ch in body.findall('a:p',NS):body.remove(ch)
    body.append(p)
def clear(page,box,images=2):
    page.add_redact_annot(box,fill=(1,1,1));page.apply_redactions(images=images,graphics=1)
def relate(rels,rid,kind,target):
    E.SubElement(rels,'{'+PKG+'}Relationship',Id=rid,Type=kind,Target=target)
def clean_creation_ids(s):
    for node in s.xpath('//*[local-name()="creationId"]'):
        node.getparent().remove(node)

with ZipFile(SNAP/'before.pptx') as z:parts={n:z.read(n) for n in z.namelist()}
original=dict(parts)
pres=parse(parts['ppt/presentation.xml'])
prels={r.get('Id'):r.get('Target') for r in parse(parts['ppt/_rels/presentation.xml.rels'])}
paths=[resolve('ppt/presentation.xml',prels[n.get(tag('r:id'))]) for n in pres.find('p:sldIdLst',NS)]
assert len(paths)==34
oldpdf=fitz.open(SNAP/'before.pdf');pdf=fitz.open();pdf.insert_pdf(oldpdf)
fontfile='/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf';font=fitz.Font(fontfile=fontfile)

# Title photo: preserve the full photograph and existing text positions.
root=parse(parts[paths[0]]);rels=parse(parts[relpath(paths[0])])
photo=(ASSETS/'title_robot.jpg').read_bytes();parts['ppt/media/title_robot.jpg']=photo
pic=deepcopy(parse(parts[paths[1]]).xpath('//p:pic[p:nvPicPr/p:cNvPr/@name="Figure — motivation_rig"]',namespaces=NS)[0])
meta=pic.find('p:nvPicPr/p:cNvPr',NS);meta.set('id','15');meta.set('name','Title robot photograph');meta.set('descr','User-supplied robot photograph, 20260916_150937.jpg. Full image, unchanged aspect ratio.')
pic.find('p:blipFill/a:blip',NS).set(tag('r:embed'),'rIdTitleRobot')
for node in list(pic.findall('p:blipFill/a:srcRect',NS)):node.getparent().remove(node)
clean_creation_ids(pic)
box=fitz.Rect(592,103,921.6,103+329.6*2908/2858);move(pic,box)
root.find('p:cSld/p:spTree',NS).append(pic)
relate(rels,'rIdTitleRobot',NS['r']+'/image','../media/title_robot.jpg')
for name in ['Thesis title','Presenter','Degree programme','Supervisors']:
    s=shape(root,name);b=rectangle(s);move(s,fitz.Rect(b.x0,b.y0,b.x0+520,b.y1))
pdf[0].insert_image(box,stream=photo,keep_proportion=True)
parts[paths[0]]=dump(root);parts[relpath(paths[0])]=dump(rels)

# Motivation: Figure 1.1 above the same Problem / Idea wording.
root=parse(parts[paths[1]]);rels=parse(parts[relpath(paths[1])]);page=pdf[1]
clear(page,fitz.Rect(37,52,923,493))
pic=root.xpath('//p:pic[p:nvPicPr/p:cNvPr/@name="Figure — motivation_rig"]',namespaces=NS)[0]
meta=pic.find('p:nvPicPr/p:cNvPr',NS);meta.set('name','Figure - thesis_figure_1_1');meta.set('descr','Thesis Figure 1.1: Sources of angular offset at surface entry. Exact vector figure from printed page 1.')
rid=pic.find('p:blipFill/a:blip',NS).get(tag('r:embed'))
next(r for r in rels if r.get('Id')==rid).set('Target','../media/thesis_figure_1_1.png')
parts['ppt/media/thesis_figure_1_1.png']=(ASSETS/'thesis_figure_1_1.png').read_bytes()
for node in list(pic.findall('p:blipFill/a:srcRect',NS)):node.getparent().remove(node)
fig=fitz.open(ASSETS/'thesis_figure_1_1.pdf');box=fitz.Rect(135,62,825,62+690*fig[0].rect.height/fig[0].rect.width)
move(pic,box);page.show_pdf_page(box,fig,0)
positions={'TextBox 8':(52,302),'TextBox 9':(72,338),'TextBox 10':(72,386),'TextBox 13':(484,302),'TextBox 14':(504,338),'Passive contact alignment':(504,386),'Compliance permits contact rotation':(504,434)}
for name,(x,y) in positions.items():
    s=shape(root,name);old=rectangle(s);new=fitz.Rect(x,y,x+old.width,y+old.height)
    move(s,new);page.insert_font(fontname='ArialMedia',fontfile=fontfile)
    # Move only the text glyphs. Importing a page clip can also carry the old
    # slide's full-page white background into neighbouring content.
    for block in oldpdf[1].get_text('rawdict',clip=old)['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                colour=tuple(((span['color']>>shift)&255)/255 for shift in [16,8,0])
                for char in span['chars']:
                    ox,oy=char['origin']
                    page.insert_text((ox+new.x0-old.x0,oy+new.y0-old.y0),char['c'],fontname='ArialMedia',fontsize=span['size'],color=colour)
parts[paths[1]]=dump(root);parts[relpath(paths[1])]=dump(rels)

# Replace the old disturbance clip with two independent click-to-play videos.
root=parse(parts[paths[26]]);rels=parse(parts[relpath(paths[26])]);tree=root.find('p:cSld/p:spTree',NS);page=pdf[26]
clear(page,fitz.Rect(50,55,911,499))
first=root.xpath('//p:pic[p:nvPicPr/p:cNvPr/@name="Disturbance demonstration video"]',namespaces=NS)[0]
second=deepcopy(first);clean_creation_ids(second)
second.find('p:nvPicPr/p:cNvPr',NS).set('id','22');tree.append(second)
cue=shape(root,'Video viewing cue');cue2=deepcopy(cue);clean_creation_ids(cue2)
cue2.find('p:nvSpPr/p:cNvPr',NS).set('id','23');tree.append(cue2)
page.insert_font(fontname='ArialMedia',fontfile=fontfile)
for n,video,label,x in [(1,first,cue,60),(2,second,cue2,505)]:
    stem=f'Nullspace{n}'
    media=f'{stem}_presentation.mp4';poster=f'{stem}_poster.png'
    parts['ppt/media/'+media]=(FINAL/'Video'/media).read_bytes()
    parts['ppt/media/'+poster]=(FINAL/'Video'/poster).read_bytes()
    meta=video.find('p:nvPicPr/p:cNvPr',NS);meta.set('name',stem+' video');meta.set('descr',stem+'.mp4. Upright presentation copy with original audio and full duration. Click to play.')
    vf=video.find('.//a:videoFile',NS);pm=video.find('.//{'+P14+'}media');blip=video.find('p:blipFill/a:blip',NS)
    if n==1:
        for rid,target in [(vf.get(tag('r:link')),media),(pm.get(tag('r:embed')),media),(blip.get(tag('r:embed')),poster)]:
            next(r for r in rels if r.get('Id')==rid).set('Target','../media/'+target)
    else:
        for attr,node,rid,kind,target in [('r:link',vf,'rIdNullspace2Video',NS['r']+'/video',media),('r:embed',pm,'rIdNullspace2Media','http://schemas.microsoft.com/office/2007/relationships/media',media),('r:embed',blip,'rIdNullspace2Poster',NS['r']+'/image',poster)]:
            node.set(tag(attr),rid);relate(rels,rid,kind,'../media/'+target)
    box=fitz.Rect(x,63,x+395,458);move(video,box);page.insert_image(box,stream=parts['ppt/media/'+poster])
    label.find('p:nvSpPr/p:cNvPr',NS).set('name',stem+' label');text(label,f'Null-space demonstration {n}')
    b=fitz.Rect(x,471,x+395,499);move(label,b)
    phrase=f'Null-space demonstration {n}';length=font.text_length(phrase,fontsize=19)
    page.insert_text((x+(395-length)/2,490),phrase,fontname='ArialMedia',fontsize=19,color=(23/255,54/255,93/255))
timing=root.find('p:timing',NS);v=deepcopy(timing.find('.//p:video',NS));v.find('.//p:cTn',NS).set('id','3');v.find('.//p:spTgt',NS).set('spid','22')
timing.find('.//p:childTnLst',NS).append(v)
parts[paths[26]]=dump(root);parts[relpath(paths[26])]=dump(rels)

# Remove obsolete embedded disturbance media only when no package part uses it.
targets=set()
for name,data in parts.items():
    if name.endswith('.rels'):
        owner='' if name=='_rels/.rels' else name.replace('/_rels/','/')[:-5]
        for r in parse(data):
            if r.get('TargetMode')!='External':targets.add(resolve(owner,r.get('Target')))
removed=[]
for name in ['ppt/media/media2.mp4','ppt/media/image58.png']:
    if name not in targets and name in parts:del parts[name];removed.append(name)
ct=parse(parts['[Content_Types].xml'])
if not any(n.get('Extension')=='jpg' for n in ct):E.SubElement(ct,'{'+CT+'}Default',Extension='jpg',ContentType='image/jpeg')
for n in list(ct):
    if n.get('PartName','').lstrip('/') in removed:ct.remove(n)
parts['[Content_Types].xml']=dump(ct)
app=parse(parts['docProps/app.xml'])
app.xpath('//*[local-name()="MMClips"]')[0].text='3'
parts['docProps/app.xml']=dump(app)

# Synchronize narration and technical source notes for changed content.
spoken={
2:["Grinding needs the tool face aligned with the physical surface. The figure separates uncertainty in the surface orientation from the difference between desired and achieved tool orientation.","Both contributions can leave an angular mismatch at contact. With a tilted tool, normal pressing creates a contact moment.","Cartesian impedance makes position and rotation compliant. Low rotational stiffness lets the contact moment turn the tool towards alignment while the desired orientation stays fixed."],
27:["These two recordings show manual disturbances applied to the robot arm. They provide a qualitative view of its joint motion.","The experimental plots provide the quantitative comparison between the null-space settings."]}
notes=[]
for i,path in enumerate(paths,1):
    root=parse(parts[path]);rr=parse(parts[relpath(path)])
    nr=next(r for r in rr if r.get('Type').endswith('/notesSlide'));note=resolve(path,nr.get('Target'));nroot=parse(parts[note])
    body=next(s.find('p:txBody',NS) for s in nroot.findall('.//p:sp',NS) if s.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None and s.find('p:nvSpPr/p:nvPr/p:ph',NS).get('type')=='body')
    old='\n'.join(body.xpath('.//a:t/text()',namespaces=NS));bullets=spoken.get(i,old.split('[Sources]',1)[0].strip().splitlines())
    if i in [1,2,27]:
        if i==27:
            source='[Sources]\nVideo/Nullspace1.mp4 and Video/Nullspace2.mp4, supplied by the user. Both contain a video-rotation flag. Upright presentation copies retain all frames and copy the original AAC audio without re-encoding. The videos are independently triggered on click. The old no-torque / damping / conditioning sequence belongs to the replaced clip and is not assigned to these recordings. Numerical controller settings are not established by the new filenames.'
        else:
            source='[Sources]'+old.split('[Sources]',1)[1] if '[Sources]' in old else '[Sources]'
            source+='\n[Media update]\n'+('Title photo: figures_and_images/title_robot.jpg, copied unchanged from the user attachment 20260916_150937.jpg. Full image displayed on the right.' if i==1 else 'Motivation image replaced by thesis Figure 1.1, Sources of angular offset at surface entry. Exact vector extraction from MyOwn-thesis/Thesis.pdf, physical page 27 / printed page 1. Source: figures/ch01/surface_entry_concept.tex. The earlier robot photograph is no longer shown on this slide.')
        for p in body.findall('a:p',NS):body.remove(p)
        for line in bullets+[source]:
            p=E.SubElement(body,tag('a:p'));r=E.SubElement(p,tag('a:r'));E.SubElement(r,tag('a:t')).text=line
        parts[note]=dump(nroot)
    title='Master Thesis Presentation' if i==1 else ''.join(shape(root,'Slide title').xpath('.//a:t/text()',namespaces=NS))
    notes.extend([title,'-'*len(title),'\n'.join(bullets),''])
script=(SNAP/'before_script.tex').read_text()
for n,title in [(2,'Motivation'),(27,'Disturbance demonstration')]:
    pattern=r'(\\section\*\{'+re.escape(title)+r'\}).*?(?=\\section\*\{|\\end\{document\})'
    replacement='\\section*{'+title+'}\n\\begin{itemize}\n'+'\n'.join('\\item '+v for v in spoken[n])+'\n\\end{itemize}\n\n'
    script,count=re.subn(pattern,lambda m:replacement,script,flags=re.S);assert count==1
(FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex').write_text(script)
(FINAL/'Speaker_notes_and_timing.txt').write_text('\n'.join(notes).rstrip()+'\n')

# Overview membership is unchanged. Refresh its six existing labels from sections.
chapters=[s.get('name') for s in pres.xpath('//*[local-name()="section"]') if s.get('name')!='Backup']
overview=parse(parts[paths[3]])
for n,title in enumerate(chapters,1):
    s=shape(overview,'Overview item '+str(n))
    assert ''.join(s.xpath('.//a:t/text()',namespaces=NS))==title
    text(s,title)
parts[paths[3]]=dump(overview)

for path in paths:
    a=parse(original[path]);b=parse(parts[path]);math=lambda r:[E.tostring(n) for n in r.xpath('//*[local-name()="oMath"]')]
    assert math(a)==math(b),path
assert parts['ppt/media/media1.mp4']==original['ppt/media/media1.mp4']
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx','w',ZIP_DEFLATED) as z:
    for name,data in parts.items():z.writestr(name,data)
pdf.save(FINAL/'Thesis_Defense_gg0_v3.pdf',garbage=4,deflate=True)
supp=fitz.open();supp.insert_pdf(pdf,from_page=25,to_page=33);supp.save(FINAL/'Supplementary_slides.pdf',garbage=4,deflate=True)
manifest=json.loads((ASSETS/'manifest.json').read_text())
for name,source,change in [('title_robot','User attachment 20260916_150937.jpg','Full photograph on the title slide, right side. Original bytes and aspect ratio retained.'),('thesis_figure_1_1','MyOwn-thesis/Thesis.pdf, page 27, Figure 1.1. sources/thesis_figure_1_1_source.tex','Exact vector extraction, replacing the Motivation photograph. PDF, PNG and SVG variants retained.')]:
    manifest=[m for m in manifest if m.get('asset')!=name];manifest.append({'asset':name,'source':source,'changes':change})
(ASSETS/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(HERE/'update.json').write_text(json.dumps({'changed_physical_slides':[1,2,27],'total_slides':34,'hidden_backups':9,'removed_obsolete_embedded_media':removed,'overview_chapters':chapters,'native_equations_preserved':True,'contact_video_preserved':True,'new_videos':['Nullspace1_presentation.mp4','Nullspace2_presentation.mp4'],'pdf_method':'Original pages retained, with exact thesis vector figure, photo and video poster replacements. Motivation text glyphs redrawn at matching positions.'},indent=2)+'\n')
print('Updated title photo, Motivation Figure 1.1, and two click-to-play videos. Deck remains 34 slides.')
