from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import sys,json,subprocess,hashlib,shutil,copy,os
H=Path(__file__).resolve().parent;ROOT=H.parents[1];F=ROOT/'Final Presentation'
sys.path.insert(0,str(ROOT/'tmp/video_compatibility_deps'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
def run(args):
 p=subprocess.run([FF,'-hide_banner','-nostdin',*args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr)
 return p.stdout+p.stderr
def vhash(p):return run(['-v','error','-i',str(p),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-']).strip()
def sha(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
(H/'silent_media').mkdir(exist_ok=True)
conversions=json.loads((H/'conversion.json').read_text());replacements={};report=[]
for m in conversions:
 name=Path(m['part']).name;src=H/'compatible_media'/name;out=H/'silent_media'/name
 run(['-y','-v','error','-i',str(src),'-map','0:v:0','-c:v','copy','-an','-map_metadata','-1','-movflags','+faststart',str(out)])
 assert vhash(src)==vhash(out)
 probe=subprocess.run([FF,'-hide_banner','-i',str(out)],capture_output=True,text=True).stderr
 assert 'Audio:' not in probe and 'Video: h264 (Constrained Baseline)' in probe
 replacements[m['part']]=out;report.append({'part':m['part'],'video_stream_identical':True,'no_audio_stream':True,'sha256':sha(out)})
with ZipFile(H/'updated.pptx') as old,ZipFile(H/'silent.pptx','w',ZIP_DEFLATED) as new:
 for info in old.infolist():
  with (open(replacements[info.filename],'rb') if info.filename in replacements else old.open(info)) as a,new.open(copy.copy(info),'w') as b:shutil.copyfileobj(a,b,1024*1024)
with ZipFile(H/'updated.pptx') as old,ZipFile(H/'silent.pptx') as new:
 assert old.namelist()==new.namelist() and new.testzip() is None
 changed=[n for n in old.namelist() if old.read(n)!=new.read(n)]
 assert set(changed)==set(replacements)
(H/'silent_verification.json').write_text(json.dumps({'source':str(H/'updated.pptx'),'sha256':sha(H/'silent.pptx'),'changed_parts':changed,'all_nonmedia_parts_byte_identical':True,'media':report,'purpose':'Optional fallback to test/remove video audio-stream playback when projection triggers Cannot play media. Main deck retains original audio. University root cause unconfirmed.'},indent=2))
print('Built silent fallback without re-encoding or changing any video frames.')
