"""Verify requested media edits, playback links, preservation and PDF coverage."""
from pathlib import Path
from zipfile import ZipFile
import hashlib,json,posixpath,re,struct,subprocess
from urllib.parse import unquote
import fitz,imageio_ffmpeg
from lxml import etree as E
from pptx import Presentation

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
P14='http://schemas.microsoft.com/office/powerpoint/2010/main'
R='{'+NS['r']+'}'
def resolve(owner,target):return posixpath.normpath(posixpath.join(posixpath.dirname(owner),unquote(target))).lstrip('/')
def relpath(owner):return posixpath.dirname(owner)+'/_rels/'+posixpath.basename(owner)+'.rels'
def sha(data):return hashlib.sha256(data).hexdigest()
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx') as z:
    assert z.testzip() is None
    parts={n:z.read(n) for n in z.namelist()}
with ZipFile(HERE/'review/before.pptx') as z:old={n:z.read(n) for n in z.namelist()}
refs=0
for name,data in parts.items():
    if not name.endswith('.rels'):continue
    owner='' if name=='_rels/.rels' else name.replace('/_rels/','/')[:-5]
    for rel in E.fromstring(data):
        if rel.get('TargetMode')!='External':
            assert resolve(owner,rel.get('Target')) in parts,(name,rel.get('Target'))
            refs+=1
pres=E.fromstring(parts['ppt/presentation.xml']);rels={r.get('Id'):r.get('Target') for r in E.fromstring(parts['ppt/_rels/presentation.xml.rels'])}
ids=list(pres.find('p:sldIdLst',NS));paths=[resolve('ppt/presentation.xml',rels[n.get(R+'id')]) for n in ids]
assert len(paths)==34
assert parts['ppt/presentation.xml']==old['ppt/presentation.xml']
math=lambda root:[E.tostring(n) for n in root.xpath('//*[local-name()="oMath"]')]
for i,path in enumerate(paths,1):
    root=E.fromstring(parts[path]);before=E.fromstring(old[path])
    assert (root.get('show')=='0')==(i>25)
    assert math(root)==math(before),i
    shapeids=root.xpath('//*[local-name()="cNvPr"]/@id')
    assert len(shapeids)==len(set(shapeids)),i
    if i not in [1,2,4,27]:assert parts[path]==old[path],i

# Three active embedded movies: original contact plus the two supplied clips.
assert parts['ppt/media/media1.mp4']==old['ppt/media/media1.mp4']
assert 'ppt/media/media2.mp4' not in parts
assert len([n for n in parts if n.endswith('.mp4')])==3
root=E.fromstring(parts[paths[26]]);rs={r.get('Id'):r.get('Target') for r in E.fromstring(parts[relpath(paths[26])])}
videos=root.xpath('//p:pic[p:nvPicPr/p:nvPr/a:videoFile]',namespaces=NS)
assert len(videos)==2
for n,v in enumerate(videos,1):
    meta=v.find('p:nvPicPr/p:cNvPr',NS);sid=meta.get('id')
    assert meta.find('a:hlinkClick',NS).get('action')=='ppaction://media'
    vid=v.find('.//a:videoFile',NS).get(R+'link');media=v.find('.//{'+P14+'}media').get(R+'embed')
    assert rs[vid]==rs[media]=='../media/Nullspace'+str(n)+'_presentation.mp4'
    assert parts[resolve(paths[26],rs[vid])]==(FINAL/'Video'/f'Nullspace{n}_presentation.mp4').read_bytes()
    timer=root.xpath('//p:video[p:cMediaNode/p:tgtEl/p:spTgt/@spid="'+sid+'"]',namespaces=NS)
    assert len(timer)==1 and timer[0].find('.//p:cond',NS).get('delay')=='indefinite'
assert parts['ppt/media/title_robot.jpg']==(ASSETS/'title_robot.jpg').read_bytes()
assert parts['ppt/media/thesis_figure_1_1.png']==(ASSETS/'thesis_figure_1_1.png').read_bytes()

# Inspect MP4 video-track sample count and display matrix without changing it.
def boxes(data):
    pos=0
    while pos+8<=len(data):
        size,kind=struct.unpack('>I4s',data[pos:pos+8]);start=pos+8
        if size==1:size=struct.unpack('>Q',data[start:start+8])[0];start+=8
        if size==0:size=len(data)-pos
        assert size>=8
        yield kind,data[start:pos+size]
        pos+=size
def child(data,kind):return next(b for t,b in boxes(data) if t==kind)
def video_info(path):
    moov=child(path.read_bytes(),b'moov')
    for kind,track in boxes(moov):
        if kind!=b'trak':continue
        mdia=child(track,b'mdia')
        if child(mdia,b'hdlr')[8:12]!=b'vide':continue
        tkhd=child(track,b'tkhd');offset=52 if tkhd[0]==1 else 40
        matrix=struct.unpack('>9i',tkhd[offset:offset+36])
        stsz=child(child(child(mdia,b'minf'),b'stbl'),b'stsz')
        frames=struct.unpack('>I',stsz[8:12])[0]
        return {'frames':frames,'display_matrix':list(matrix)}
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe();media_checks=[]
for n in [1,2]:
    source=FINAL/'Video'/f'Nullspace{n}.mp4';target=FINAL/'Video'/f'Nullspace{n}_presentation.mp4'
    a,b=video_info(source),video_info(target)
    assert a['frames']==b['frames']
    assert b['display_matrix']==[65536,0,0,0,65536,0,0,0,1073741824]
    hashes=[]
    for file in [source,target]:
        result=subprocess.run([ffmpeg,'-v','error','-i',str(file),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],capture_output=True,text=True,check=True)
        hashes.append(result.stdout.strip())
    assert hashes[0]==hashes[1]
    subprocess.run([ffmpeg,'-v','error','-i',str(target),'-f','null','-'],capture_output=True,check=True)
    media_checks.append({'clip':n,'frames':b['frames'],'upright':True,'audio_payload_preserved':True,'full_decode_passed':True,'source_sha256':sha(source.read_bytes()),'presentation_sha256':sha(target.read_bytes())})

pdf=fitz.open(FINAL/'Thesis_Defense_gg0_v3.pdf');before=fitz.open(HERE/'review/before.pdf');supp=fitz.open(FINAL/'Supplementary_slides.pdf')
assert len(pdf)==34 and len(supp)==9
pixels=lambda p:p.get_pixmap(alpha=False).samples
for i in range(34):
    if i not in [0,1,26]:assert pixels(pdf[i])==pixels(before[i]),i+1
for i in range(9):assert pixels(pdf[i+25])==pixels(supp[i]),i+26
# Continuous title rule remains visible after the changed Motivation layout.
assert pdf[1].get_pixmap(clip=fitz.Rect(37.44,48.1,921.6,49.1)).samples==before[1].get_pixmap(clip=fitz.Rect(37.44,48.1,921.6,49.1)).samples
prs=Presentation(FINAL/'Thesis_Defense_gg0_v3.pptx')
titles=['Master Thesis Presentation']+[next(s.text for s in slide.shapes if s.name=='Slide title') for slide in list(prs.slides)[1:]]
script=(FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex').read_text()
assert re.findall(r'\\section\*\{([^}]+)\}',script)==titles
assert 'Without null-space torque, the disturbance moves the arm.' not in script
result={'slides':34,'main_slides':25,'hidden_backups':9,'updated_physical_slides':[1,2,27],'native_equations_preserved':True,'unrelated_slides_and_pdf_pages_preserved':True,'internal_relationships_resolved':refs,'video_objects':3,'new_video_click_triggers_verified':2,'media':media_checks,'full_pdf_pages':34,'supplementary_pdf_pages':9,'speaking_order_matches':True,'visual_review':'Title, Motivation and disturbance demonstration inspected. Full photo, readable thesis figure, upright posters and original title rule verified.'}
(HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
