from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import sys,json,copy,hashlib,shutil,os,posixpath,re,importlib.util
H=Path(__file__).resolve().parent;ROOT=H.parents[1];F=ROOT/'Final Presentation';S=F/'Speaking/simple_speech'
sys.path[:0]=[str(ROOT/'tmp/remove_b5_20260922/deps'),str(ROOT/'tmp/connected_notes_deps')]
from lxml import etree as E
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
DECKS=[F/'Thesis_Defense_gg0_v3.pptx',F/'Thesis_Defense_Projector_Silent.pptx',F/'Projector_Test_Versions/02_WebM_Silent.pptx',F/'Projector_Test_Versions/03_WMV_Silent.pptx']
FALLBACK=F/'Projector_Test_Versions/01_MP4_Light_Silent.pptx'
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def dump(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
def resolve(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rp(p):return posixpath.dirname(p)+'/_rels/'+posixpath.basename(p)+'.rels' if p else '_rels/.rels'
def inventory(z):
 rels={x.get('Id'):resolve('ppt/presentation.xml',x.get('Target')) for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 out=[]
 for i,s in enumerate(E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',NS),1):
  part=rels[s.get('{'+NS['r']+'}id')]
  note=next(resolve(part,x.get('Target')) for x in E.fromstring(z.read(rp(part))) if x.get('Type').endswith('/notesSlide'))
  out.append(dict(physical=i,part=part,notes=note))
 return out
def body(r):return r.xpath('.//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]/p:txBody',namespaces=NS)[0]
def text(p):return ''.join(p.xpath('.//a:t/text()',namespaces=NS))
def paragraphs(r):return [text(p) for p in body(r).findall('a:p',NS)]
def lite(z,dest,title_only=False,changes=None):
 overrides=dict(changes or {})
 for n in z.namelist():
  if n.startswith('ppt/slides/slide') and n.endswith('.xml'):
   r=E.fromstring(z.read(n))
   if title_only:
    tree=r.find('p:cSld/p:spTree',NS)
    for el in list(tree):
     if E.QName(el).localname not in ['nvGrpSpPr','grpSpPr'] and not el.xpath('.//p:cNvPr[@name="Slide title"]',namespaces=NS):tree.remove(el)
   for el in r.xpath('//*[local-name()="videoFile" or local-name()="media" or local-name()="timing"]'):el.getparent().remove(el)
   overrides[n]=dump(r)
  elif n.startswith('ppt/slides/_rels/') and n.endswith('.rels'):
   r=E.fromstring(z.read(n))
   for el in list(r):
    typ=el.get('Type')
    if (title_only and not typ.endswith(('/slideLayout','/notesSlide'))) or typ.endswith(('/video','/audio','/media')):r.remove(el)
   overrides[n]=dump(r)
 read=lambda n:overrides[n] if n in overrides else z.read(n)
 names=set(z.namelist());included=set();pending=['']
 while pending:
  owner=pending.pop()
  if owner in included:continue
  if owner:included.add(owner)
  rel=rp(owner)
  if rel not in names:continue
  included.add(rel)
  for el in E.fromstring(read(rel)):
   if el.get('TargetMode')!='External':pending.append(resolve(owner,el.get('Target')))
 ct=E.fromstring(z.read('[Content_Types].xml'))
 for el in list(ct):
  if el.tag.endswith('Override') and el.get('PartName').lstrip('/') not in included:ct.remove(el)
 overrides['[Content_Types].xml']=dump(ct);included.add('[Content_Types].xml')
 with ZipFile(dest,'w',ZIP_DEFLATED) as out:
  for n in sorted(included):out.writestr(n,read(n))
def prepare():
 a=H/'archive';a.mkdir(exist_ok=True)
 for d in DECKS:
  if not (a/d.name).exists():os.link(d,a/d.name)
 for n in ['script.json','sentence_prompts.json','Simple_speech.txt','build.py','verification.json','README.txt']:
  if not (a/n).exists():shutil.copy2(S/n,a/n)
 if not (a/'speech.pdf').exists():os.link(F/'Simple_speech_updated.pdf',a/'speech.pdf')
 if not (a/'projector_READ_ME_FIRST.txt').exists():shutil.copy2(F/'Projector_Test_Versions/READ_ME_FIRST.txt',a/'projector_READ_ME_FIRST.txt')
 protected=[FALLBACK,F/'Projector_Test_Versions/01_Fallback_Original_Speech.pdf',F/'Thesis_Defense_gg0_v3.pdf',F/'Supplementary_slides.pdf',F/'Speaker_notes_and_timing.txt',F/'figures_and_images/native_equations.json']
 manifest={'decks':{str(d.relative_to(ROOT)):sha(d) for d in DECKS},'protected':{str(p.relative_to(ROOT)):sha(p) for p in protected}}
 (a/'manifest.json').write_text(json.dumps(manifest,indent=2))
 data=json.loads((H/'script.json').read_text(encoding='utf-8'));notes=[];mapping=[]
 with ZipFile(DECKS[0]) as z:
  inv=inventory(z);lite(z,H/'notes_source.pptx',True)
  for entry,s in zip(inv,data):
   old=paragraphs(E.fromstring(z.read(entry['notes'])))
   cues=[t for t in old if t.startswith('[')]
   rows=[(s['opening'],'opening'),*((p,'body') for p in s['paragraphs'])]
   if 'video_seconds' in s:
    assert len(cues)==1,(s['physical'],cues)
    rows.extend([(cues[0],'cue'),(s['after_video'],'body')])
   else:rows.extend((cue,'cue') for cue in cues)
   notes.append([{'runs':[{'run':t,'textStyle':{'fontSize':'18pt','bold':kind=='opening','italic':kind=='cue'}}],'kind':kind} for t,kind in rows])
   for t,kind in rows:
    if kind=='cue':continue
    for sentence in re.split(r'(?<=[.!?])\s+',t):mapping.append(dict(slide=s['physical'],sentence=sentence,prompt=sentence))
 (H/'notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf-8')
 (H/'sentence_prompts.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
 (H/'inventory.json').write_text(json.dumps(inv,indent=2))
 (H/'template-frame-map.json').write_text(json.dumps({'outputSlides':[{'outputSlide':i,'sourceSlide':i,'reuseMode':'duplicate-slide','editTargets':['speaker notes only']} for i in range(1,32)]},indent=2))
 (H/'source-notes.txt').write_text('User requests smoother connected notes, expanded explanations using the displayed impedance and CoC equations and clearer null-space roles. Local native equation sources and existing slides supply all technical claims. Existing full torque formula stays in backup B2. Preserve 01_MP4_Light_Silent.pptx exactly as fallback. Update notes in the other four decks and synchronize current speech. Preserve 18 pt inherited notes master, opening/cue styles, paragraph spacing and geometry. Artifact Tool authors notes; only verified notes bodies are transferred to preserve every other package part.\n',encoding='utf-8')
 print('Prepared 31 connected notes; original decks and speech archived.')
def assemble():
 notes=json.loads((H/'notes.json').read_text(encoding='utf-8'));changes={}
 with ZipFile(H/'authored.pptx') as az,ZipFile(H/'archive'/DECKS[0].name) as old:
  for src,authored,rows in zip(inventory(old),inventory(az),notes):
   ar=E.fromstring(az.read(authored['notes']));assert paragraphs(ar)==[p['runs'][0]['run'] for p in rows]
   assert set(body(ar).xpath('.//a:rPr/@sz',namespaces=NS))=={'1800'}
   r=E.fromstring(old.read(src['notes']));target=body(r);ps=target.findall('a:p',NS)
   templates={'opening':ps[0],'body':next(p for p in ps[1:] if not text(p).startswith('['))}
   cues=[p for p in ps if text(p).startswith('[')]
   if cues:templates['cue']=cues[0]
   for p in ps:target.remove(p)
   for row in rows:
    p=copy.deepcopy(templates[row['kind']]);runs=p.findall('a:r',NS);assert len(runs)==1
    runs[0].find('a:t',NS).text=row['runs'][0]['run'];target.append(p)
   if dump(r)!=old.read(src['notes']):changes[src['notes']]=dump(r)
  lite(old,H/'native_preview.pptx',False,changes)
 for d in DECKS:
  with ZipFile(H/'archive'/d.name) as old,ZipFile(H/d.name,'w',ZIP_DEFLATED) as out:
   for item in old.infolist():
    if item.filename in changes:out.writestr(copy.copy(item),changes[item.filename])
    else:
     with old.open(item) as source,out.open(copy.copy(item),'w') as dest:shutil.copyfileobj(source,dest,1024*1024)
 (H/'changed_parts.json').write_text(json.dumps(list(changes),indent=2))
 print('Assembled four presentations; changes confined to the five expanded notes.')
def speech():
 spec=importlib.util.spec_from_file_location('speech',H/'build.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.build()
 os.replace(H/'verification.json',H/'speech_verification.json')
def verify():
 manifest=json.loads((H/'archive/manifest.json').read_text());notes=json.loads((H/'notes.json').read_text());changed=set(json.loads((H/'changed_parts.json').read_text()));report={}
 for d in DECKS:
  with ZipFile(H/'archive'/d.name) as old,ZipFile(H/d.name) as new:
   assert old.namelist()==new.namelist() and new.testzip() is None
   diff=[]
   for n in old.namelist():
    with old.open(n) as a,new.open(n) as b:
     if hashlib.file_digest(a,'sha256').digest()!=hashlib.file_digest(b,'sha256').digest():diff.append(n)
   assert set(diff)==changed,(d,diff)
   for row,expected in zip(inventory(new),notes):
    r=E.fromstring(new.read(row['notes']));before=E.fromstring(old.read(row['notes']));nb=body(r);ob=body(before)
    assert paragraphs(r)==[p['runs'][0]['run'] for p in expected]
    assert not nb.xpath('.//a:rPr/@sz|.//a:defRPr/@sz|.//a:endParaRPr/@sz',namespaces=NS)
    for p,exp in zip(nb.findall('a:p',NS),expected):
     pr=p.find('a:r/a:rPr',NS);assert (pr.get('b')=='1')==(exp['kind']=='opening');assert (pr.get('i')=='1')==(exp['kind']=='cue')
    nb.getparent().replace(nb,copy.deepcopy(ob));assert E.tostring(r,method='c14n')==E.tostring(before,method='c14n')
   assert E.fromstring(new.read('ppt/notesMasters/notesMaster1.xml')).xpath('./p:notesStyle/*/a:defRPr/@sz',namespaces=NS)==['1800']*9
  report[d.name]={'sha256':sha(H/d.name),'changed_parts':len(diff),'all_other_parts_byte_identical':True,'notes_match_speech':True}
 for name,digest in manifest['protected'].items():assert sha(ROOT/name)==digest,name
 bounds=json.loads((H/'powerpoint_notes_check.json').read_text(encoding='utf-8-sig'))
 assert len(bounds)==31
 for b,expected in zip(bounds,notes):
  assert b['fontSize']==18 and b['boundHeight']<b['height']-10
  assert b['text'].split('\r')==[p['runs'][0]['run'] for p in expected]
 import pymupdf as fitz
 pdf=fitz.open(H/'notes_preview.pdf');assert len(pdf)==31
 compact=lambda t:re.sub(r'\s+','',t)
 for page,expected in zip(pdf,notes):
  t=compact(page.get_text())
  for p in expected:assert compact(p['runs'][0]['run']) in t,p
 pdf.close()
 report={'decks':report,'fallback_unchanged':True,'fallback_sha256':sha(FALLBACK),'notes_font_pt':18,'max_notes_height_pt':max(b['boundHeight'] for b in bounds),'notes_body_height_pt':540,'slides_equations_media_and_static_pdfs_unchanged':True,'all_31_notes_native_powerpoint_verified':True,'installed':False}
 (H/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
def put(src,dst):
 pending=dst.with_name(dst.name+'.pending');assert not pending.exists();os.link(src,pending);os.replace(pending,dst);assert sha(src)==sha(dst)
def install():
 report=json.loads((H/'verification.json').read_text());assert report['visual_review_passed']
 manifest=json.loads((H/'archive/manifest.json').read_text())
 for n,h in {**manifest['decks'],**manifest['protected']}.items():assert sha(ROOT/n)==h,n
 assert sha(F/'Simple_speech_updated.pdf')==sha(H/'archive/speech.pdf')
 for n in ['script.json','sentence_prompts.json','Simple_speech.txt','build.py','verification.json','README.txt']:assert sha(S/n)==sha(H/'archive'/n),n
 for d in DECKS:put(H/d.name,d)
 put(H/'Simple_speech.pdf',F/'Simple_speech_updated.pdf')
 for n in ['script.json','sentence_prompts.json','Simple_speech.txt','build.py','README.txt']:put(H/n,S/n)
 put(H/'Simple_speech.pdf',S/'Simple_speech.pdf')
 sr=json.loads((H/'speech_verification.json').read_text());sr.update(installed=True,visually_reviewed_pages=sr['pages'],notes_format='connected_spoken_paragraphs',notes_match_all_spoken_text=True,unchanged_fallback='Projector_Test_Versions/01_MP4_Light_Silent.pptx')
 (H/'speech_verification.json').write_text(json.dumps(sr,indent=2));put(H/'speech_verification.json',S/'verification.json')
 for n in ['script.json','Simple_speech.txt']:
  target=ROOT/'tmp/pdfs/simple_speech_read_aloud_20261003'/n
  if target.exists():put(H/n,target)
 put(H/'Simple_speech.pdf',F/'Projector_Test_Versions/02_03_Improved_Speech.pdf')
 put(H/'READ_ME_FIRST.txt',F/'Projector_Test_Versions/READ_ME_FIRST.txt')
 bundle=H/'Projector_Test_Versions.zip'
 with ZipFile(bundle,'w',ZIP_DEFLATED,compresslevel=1) as z:
  for p in sorted((F/'Projector_Test_Versions').iterdir()):
   if p.is_file():z.write(p,'Projector_Test_Versions/'+p.name)
 with ZipFile(bundle) as z:assert z.testzip() is None
 put(bundle,F/'Projector_Test_Versions.zip')
 for name,digest in manifest['protected'].items():assert sha(ROOT/name)==digest,name
 report.update(installed=True,atomic_replacement=True,zip_updated=True);(H/'verification.json').write_text(json.dumps(report,indent=2))
 print('Installed four updated decks, synchronized speech and the projector bundle. Fallback deck is byte-identical.')
if __name__=='__main__':globals()[sys.argv[1]]()
