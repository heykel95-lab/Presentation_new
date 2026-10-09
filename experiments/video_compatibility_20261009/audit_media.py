from pathlib import Path
from zipfile import ZipFile
import sys, subprocess, json, hashlib, shutil, xml.etree.ElementTree as E, posixpath
H=Path(__file__).resolve().parent
ROOT=H.parents[1]
sys.path.insert(0,str(ROOT/'tmp/video_compatibility_deps'))
import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
SOURCE=ROOT/'Final Presentation/Thesis_Defense_gg0_v3.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def sha(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def inspect():
    (H/'original_media').mkdir(exist_ok=True)
    inv={'source':str(SOURCE),'source_sha256':sha(SOURCE),'ffmpeg':FFMPEG,'slides':[],'media':[]}
    with ZipFile(SOURCE) as z:
        rs={e.get('Id'):e.get('Target') for e in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
        for i,s in enumerate(E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N),1):
            n=posixpath.normpath('ppt/'+rs[s.get('{'+N['r']+'}id')]);x=E.fromstring(z.read(n))
            rel=posixpath.dirname(n)+'/_rels/'+posixpath.basename(n)+'.rels'
            vr=[dict(e.attrib) for e in E.fromstring(z.read(rel)) if e.get('Type').endswith(('/video','/media'))]
            inv['slides'].append({'physical':i,'part':n,'title':next(x.iter('{'+N['a']+'}t')).text,'hidden':x.get('show')=='0','video':vr})
        for info in z.infolist():
            if not info.filename.endswith('.mp4'):continue
            dst=H/'original_media'/Path(info.filename).name
            with z.open(info) as a,open(dst,'wb') as b:shutil.copyfileobj(a,b)
            r=subprocess.run([FFMPEG,'-hide_banner','-i',str(dst)],capture_output=True,text=True)
            item={'part':info.filename,'size':info.file_size,'sha256':sha(dst),'probe':r.stderr}
            inv['media'].append(item)
            print(info.filename, r.stderr,flush=True)
    (H/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf-8')
if __name__=='__main__':inspect()
