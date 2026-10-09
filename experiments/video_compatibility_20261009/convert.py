from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import sys,subprocess,json,hashlib,shutil,copy,os,re,struct
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
sys.path.insert(0,str(ROOT/'tmp/video_compatibility_deps'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
I=json.loads((H/'inventory.json').read_text())
def run(args):
    p=subprocess.run([FF,'-hide_banner','-nostdin',*args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr)
    return p.stdout+p.stderr
def sha(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def frames(p):
    s=run(['-v','error','-i',str(p),'-map','0:v:0','-c','copy','-f','framehash','-'])
    rows=[r.split(',') for r in s.splitlines() if r and not r.startswith('#')]
    return {'frames':len(rows),'pts':sorted(int(r[2]) for r in rows),'durations':sorted(int(r[3]) for r in rows)}
def audio(p):return run(['-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).strip()
def convert():
    (H/'compatible_media').mkdir(exist_ok=True);(H/'logs').mkdir(exist_ok=True)
    records=[]
    for m in I['media']:
        name=Path(m['part']).name;src=H/'original_media'/name;dst=H/'compatible_media'/name
        args=['-y','-i',str(src),'-map','0:v:0','-map','0:a:0','-vf','scale=960:960:flags=lanczos,setsar=1,setpts=N/(30*TB)','-c:v','libx264','-preset','medium','-crf','19','-profile:v','baseline','-level:v','3.1','-pix_fmt','yuv420p','-maxrate','4M','-bufsize','8M','-g','60','-bf','0','-refs','1','-r','30','-enc_time_base','1:30','-fps_mode','cfr','-video_track_timescale','90000','-c:a','copy','-map_metadata','-1','-movflags','+faststart',str(dst)]
        print('Converting '+name,flush=True)
        if not dst.exists() or dst.stat().st_size==0:
            log=run(args);(H/'logs'/(name+'.encode.txt')).write_text(log)
        run(['-v','error','-xerror','-i',str(dst),'-f','null','-'])
        before=frames(src);after=frames(dst)
        assert before['frames']==after['frames'],(name,before['frames'],after['frames'])
        assert after['pts']==list(range(0,after['frames']*3000,3000))
        drift=max(abs(a-b) for a,b in zip(before['pts'],after['pts']))/90000
        assert drift<0.1,(name,drift)
        a,b=audio(src),audio(dst);assert a==b,(name,a,b)
        probe=subprocess.run([FF,'-hide_banner','-i',str(dst)],capture_output=True,text=True).stderr
        assert 'Constrained Baseline' in probe and '960x960' in probe and 'yuv420p' in probe
        data=dst.read_bytes();assert data.find(b'moov')<data.find(b'mdat')
        ssim=run(['-i',str(src),'-i',str(dst),'-lavfi','[0:v]scale=960:960:flags=lanczos,setsar=1,settb=1/30,setpts=N[a];[1:v]settb=1/30,setpts=N[b];[a][b]ssim','-an','-f','null','-'])
        (H/'logs'/(name+'.ssim.txt')).write_text(ssim)
        score=float(re.search(r'All:([0-9.]+)',ssim).group(1));assert score>0.97,(name,score)
        for label,t in [('start',0.2),('middle',3.0)]:
            run(['-y','-ss',str(t),'-i',str(dst),'-frames:v','1',str(H/'logs'/(name+'.'+label+'.jpg'))])
        rec={'part':m['part'],'original_size':m['size'],'new_size':dst.stat().st_size,'sha256':sha(dst),'frames':after['frames'],'all_original_frames_retained':True,'constant_fps':30,'max_timestamp_adjustment_seconds':drift,'audio_stream_sha256':a,'ssim':score,'full_decode_passed':True,'probe':probe,'command':[FF,*args]}
        records.append(rec);(H/'conversion.json').write_text(json.dumps(records,indent=2))
        print(json.dumps({k:v for k,v in rec.items() if k not in ['probe','command']}),flush=True)
    src=Path(I['source']);assert sha(src)==I['source_sha256']
    (H/'archive').mkdir(exist_ok=True)
    shutil.copy2(src,H/'archive/original.pptx')
    replacements={m['part']:H/'compatible_media'/Path(m['part']).name for m in records}
    with ZipFile(src) as old,ZipFile(H/'updated.pptx','w',ZIP_DEFLATED) as new:
        for info in old.infolist():
            if info.filename in replacements:
                with open(replacements[info.filename],'rb') as a,new.open(copy.copy(info),'w') as b:shutil.copyfileobj(a,b,1024*1024)
            else:
                with old.open(info) as a,new.open(copy.copy(info),'w') as b:shutil.copyfileobj(a,b,1024*1024)
    with ZipFile(src) as old,ZipFile(H/'updated.pptx') as new:
        assert old.namelist()==new.namelist() and new.testzip() is None
        changed=[n for n in old.namelist() if old.read(n)!=new.read(n)]
        assert set(changed)==set(replacements),changed
    (H/'package_verification.json').write_text(json.dumps({'changed_parts':changed,'all_nonvideo_parts_byte_identical':True,'source_sha256':sha(src),'updated_sha256':sha(H/'updated.pptx'),'updated_size':(H/'updated.pptx').stat().st_size},indent=2))
    print('Verified: only six embedded MP4 files changed.',flush=True)
if __name__=='__main__':convert()
