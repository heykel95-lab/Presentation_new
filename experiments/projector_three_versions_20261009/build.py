from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import sys,subprocess,json,hashlib,copy,shutil,re,xml.etree.ElementTree as E,posixpath
H=Path(__file__).resolve().parent;ROOT=H.parents[1];OLD=H.parent/'video_compatibility_20261009';F=ROOT/'Final Presentation'
SOURCE=F/'Thesis_Defense_gg0_v3.pptx'
sys.path.insert(0,str(ROOT/'tmp/video_compatibility_deps'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
MEDIA=json.loads((OLD/'conversion.json').read_text())
OPTIONS={
 '01_MP4_Light_Silent':{'ext':'mp4','mime':'video/mp4','encoder':['-c:v','libx264','-profile:v','baseline','-level:v','3.1','-preset','medium','-crf','21','-maxrate','2M','-bufsize','4M','-bf','0','-refs','1','-g','60','-movflags','+faststart'],'codec':'h264'},
 '02_WebM_Silent':{'ext':'webm','mime':'video/webm','encoder':['-c:v','libvpx-vp9','-crf','28','-b:v','0','-deadline','good','-cpu-used','4','-row-mt','1','-threads','4','-g','60','-lag-in-frames','0'],'codec':'vp9'},
 '03_WMV_Silent':{'ext':'wmv','mime':'video/x-ms-wmv','encoder':['-c:v','wmv2','-b:v','3M','-maxrate','4M','-bufsize','8M','-g','30'],'codec':'wmv2'},
}
def sha(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def run(args):
 p=subprocess.run([FF,'-hide_banner','-nostdin',*args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr)
 return p.stdout+p.stderr
def build(key):
 opt=OPTIONS[key];work=H/key;(work/'media').mkdir(parents=True,exist_ok=True);(work/'logs').mkdir(exist_ok=True)
 records=[];replacements={}
 for m in MEDIA:
  src=OLD/'original_media'/Path(m['part']).name
  dst=work/'media'/Path(m['part']).with_suffix('.'+opt['ext']).name
  args=['-y','-i',str(src),'-map','0:v:0','-an','-vf','scale=720:720:flags=lanczos,setsar=1,setpts=N/(30*TB)','-r','30','-fps_mode','cfr','-pix_fmt','yuv420p','-map_metadata','-1',*opt['encoder'],str(dst)]
  print(key+': '+src.name,flush=True)
  log=run(args);(work/'logs'/(dst.name+'.encode.txt')).write_text(log)
  # A full decode both checks the recording and counts actual decoded frames.
  hashes=run(['-v','error','-xerror','-i',str(dst),'-map','0:v:0','-f','framehash','-'])
  frame_count=sum(1 for line in hashes.splitlines() if line and not line.startswith('#'))
  assert frame_count==m['frames'],(key,dst.name,frame_count,m['frames'])
  probe=subprocess.run([FF,'-hide_banner','-i',str(dst)],capture_output=True,text=True).stderr
  assert 'Audio:' not in probe and '720x720' in probe and '30 fps' in probe and ('Video: '+opt['codec']) in probe,probe
  ssim=run(['-i',str(src),'-i',str(dst),'-lavfi','[0:v]scale=720:720:flags=lanczos,setsar=1,settb=1/30,setpts=N[a];[1:v]settb=1/30,setpts=N[b];[a][b]ssim','-an','-f','null','-'])
  score=float(re.search(r'All:([0-9.]+)',ssim).group(1));assert score>.95,(key,dst.name,score)
  (work/'logs'/(dst.name+'.ssim.txt')).write_text(ssim)
  run(['-y','-v','error','-ss','3','-i',str(dst),'-frames:v','1',str(work/'logs'/(dst.name+'.jpg'))])
  newpart=str(Path(m['part']).with_suffix('.'+opt['ext'])).replace('\\','/')
  replacements[m['part']]={'part':newpart,'file':dst}
  records.append({'source':str(src),'part':newpart,'frames':frame_count,'full_decode_passed':True,'no_audio_stream':True,'ssim':score,'bytes':dst.stat().st_size,'sha256':sha(dst),'command':[FF,*args],'probe':probe})
  (work/'conversion.json').write_text(json.dumps(records,indent=2))
 dest=work/'presentation.pptx';changed=[]
 with ZipFile(SOURCE) as old,ZipFile(dest,'w',ZIP_DEFLATED) as new:
  for info in old.infolist():
   meta=copy.copy(info)
   if info.filename in replacements:
    meta.filename=replacements[info.filename]['part']
    with open(replacements[info.filename]['file'],'rb') as a,new.open(meta,'w') as b:shutil.copyfileobj(a,b,1024*1024)
    changed.append(info.filename);continue
   data=old.read(info)
   if opt['ext']!='mp4':
    if info.filename.endswith('.rels'):
     for src,rep in replacements.items():data=data.replace(('../media/'+Path(src).name).encode(),('../media/'+Path(rep['part']).name).encode())
    elif info.filename=='[Content_Types].xml':
     for src,rep in replacements.items():data=data.replace(('/'+src).encode(),('/'+rep['part']).encode())
     # Add an extension default without serializing unrelated content-type entries.
     extra=('<Default Extension="'+opt['ext']+'" ContentType="'+opt['mime']+'"/>').encode()
     assert ('Extension="'+opt['ext']+'"').encode() not in data
     data=data.replace(b'</Types>',extra+b'</Types>')
   if data!=old.read(info):changed.append(info.filename)
   new.writestr(meta,data)
 with ZipFile(SOURCE) as old,ZipFile(dest) as new:
  assert new.testzip() is None
  names=set(new.namelist())
  for n in old.namelist():
   if n not in changed:assert old.read(n)==new.read(n),n
  # Every slide, master, notes part, equation and poster is inherited without alteration.
  assert all(n.startswith('ppt/media/') or n.endswith('.rels') or n=='[Content_Types].xml' for n in changed)
  for n in new.namelist():
   if not n.endswith('.rels'):continue
   owner='' if n=='_rels/.rels' else n.replace('/_rels/','/')[:-5]
   for rel in E.fromstring(new.read(n)):
    if rel.get('TargetMode')=='External':continue
    target=posixpath.normpath(posixpath.join(posixpath.dirname(owner),rel.get('Target'))).lstrip('/')
    assert target in names,(n,target)
  ct=E.fromstring(new.read('[Content_Types].xml'))
  defaults={e.get('Extension'):e.get('ContentType') for e in ct if e.tag.endswith('Default')}
  overrides={e.get('PartName'):e.get('ContentType') for e in ct if e.tag.endswith('Override')}
  for rep in replacements.values():assert overrides.get('/'+rep['part'],defaults.get(opt['ext']))==opt['mime']
 report={'variant':key,'source_sha256':sha(SOURCE),'deck_sha256':sha(dest),'size_bytes':dest.stat().st_size,'media_count':len(records),'changed_parts':changed,'all_slide_note_master_and_poster_parts_byte_identical':True,'all_original_frames_retained':True,'audio_streams_removed':True,'codec':opt['codec'],'resolution':[720,720],'fps':30,'minimum_ssim':min(x['ssim'] for x in records)}
 (work/'package_verification.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report),flush=True)
if __name__=='__main__':
 for k in (sys.argv[1:] or OPTIONS):build(k)
