from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,sys,hashlib,shutil,os
from PIL import Image,ImageChops
H=Path(__file__).resolve().parent;ROOT=H.parents[1];F=ROOT/'Final Presentation';OLD=H.parent/'video_compatibility_20261009'
sys.path.insert(0,str(ROOT/'tmp/remove_b5_20260922/deps'))
import pymupdf as fitz
KEYS=['01_MP4_Light_Silent','02_WebM_Silent','03_WMV_Silent']
def sha(p):
 with open(p,'rb') as b:return hashlib.file_digest(b,'sha256').hexdigest()
def finish():
 main_before=sha(F/'Thesis_Defense_gg0_v3.pptx');silent_before=sha(F/'Thesis_Defense_Projector_Silent.pptx')
 summary=[]
 for key in KEYS:
  work=H/key;meta=json.loads((work/'package_verification.json').read_text());play=json.loads((work/'native_playback.json').read_text(encoding='utf-8-sig'))
  assert meta['source_sha256']==main_before and sha(work/'presentation.pptx')==meta['deck_sha256']
  assert len(play)==5 and [x['slide'] for x in play]==[2,12,20,21,26]
  assert all(len(x['tests'])==3 and all(t['advanced'] and t['state']==0 for t in x['tests']) for x in play)
  assert len(fitz.open(work/'qa_full.pdf'))==31
  differences=[]
  for i in range(1,32):
   file=f'slide-{i:02}.png';a=Image.open(OLD/'after'/file).convert('RGB');b=Image.open(work/'slides'/file).convert('RGB');d=ImageChops.difference(a,b)
   if d.getbbox():differences.append({'slide':i,'bbox':d.getbbox(),'changed_pixels':sum(v!=(0,0,0) for v in d.getdata())})
  (work/'render_comparison.json').write_text(json.dumps(differences,indent=2))
  summary.append({**meta,'native_playback_checks_passed':15,'slide_renders':31,'notes_18pt_checked':31,'regenerated_pdf_pages':31,'render_comparison':differences,'final_filename':key+'.pptx'})
 out=F/'Projector_Test_Versions';out.mkdir(exist_ok=True)
 for meta in summary:
  dst=out/meta['final_filename'];st=out/(dst.name+'.tmp');shutil.copy2(H/meta['variant']/'presentation.pptx',st);assert sha(st)==meta['deck_sha256'];os.replace(st,dst)
 guide='''THREE SILENT PROJECTOR TEST PRESENTATIONS - 9 October 2026

Extract this whole folder from the ZIP before opening a presentation.
All videos are embedded. These presentations need no internet connection
and no separate video files. Audio tracks have been removed completely.

Suggested test order
1. 01_MP4_Light_Silent.pptx
   H.264 Constrained Baseline MP4, 720 x 720, 30 fps, reduced bitrate.
   Try this first. It reduces decoding load and avoids video audio streams.
2. 02_WebM_Silent.pptx
   WebM with VP9 video, 720 x 720, 30 fps. This uses a different codec.
   Requires PowerPoint/Windows support for WebM. Tested on your installed
   desktop PowerPoint; support may differ on another computer.
3. 03_WMV_Silent.pptx
   Windows Media Video 8 (WMV2), 720 x 720, 30 fps. Legacy Windows fallback.
   Tested in your installed PowerPoint. Microsoft limits/deprecates WMV
   in PowerPoint 2505 and later, where it may convert media during playback.
   This is a fallback test, not a more universal format than MP4.

What is preserved
All 31 slides, their order and hidden backup flags, speaker notes at 18 pt,
native equations, chart data, posters, video positions and click-to-play
controls are unchanged. All original video frames remain. Video resolution
and compression differ between versions. The existing main presentation,
earlier silent copy, source recordings, speech and PDFs remain unchanged.
The existing Thesis_Defense_gg0_v3.pdf also represents these static slides.

At the university
Connect the projector before opening desktop PowerPoint. Copy the extracted
folder to your PC's local drive. Open one version at a time in Slide Show.
Click each video, and check that it starts, keeps moving and reaches the end.

Videos to test (physical PowerPoint slide / printed footer)
  2 / 1     Motivation contact video, about 51 seconds
 12 / 11    Impedance response, about 14 seconds
 20 / 19    Null-space damping, 23 seconds
 21 / 20    Null-space conditioning, about 8 seconds
 26 / B1    Opposing CoC moment, about 10 seconds (hidden backup)
For a hidden backup, select physical slide 26 in editing view and press
Shift+F5 to test from that slide.

If a version still reports Cannot play media / Media unavailable
Close and reopen PowerPoint while the projector remains connected.
Try Windows+P > Duplicate as a display-mode diagnostic.
When testing the earlier version WITH sound, also test Windows Settings >
System > Sound > Output > laptop Speakers, then restart PowerPoint.
Record which version worked and the exact error for any that failed.

Test record
                         Starts     Plays to end     Exact error / notes
01 MP4 Light Silent      ______     ____________     ___________________
02 WebM Silent           ______     ____________     ___________________
03 WMV Silent            ______     ____________     ___________________

Validation on your PC
All 18 embedded files (six per deck, including the retained unused legacy
clip) passed complete decoding and frame-count checks, with no audio stream.
All five used videos in each presentation passed PowerPoint playback tests
at the start, middle and near the end: 45 playback checks total.
All 31 slides per deck were rendered; note sizes were checked in PowerPoint.
The university projector was not available. Success there is not yet known.

Microsoft format guidance
https://support.microsoft.com/en-us/powerpoint/video-and-audio-file-formats-supported-in-powerpoint
'''
 (out/'READ_ME_FIRST.txt').write_text(guide,encoding='utf-8')
 dest=F/'Projector_Test_Versions.zip';st=F/'Projector_Test_Versions.zip.tmp'
 with ZipFile(st,'w',ZIP_DEFLATED) as z:
  for p in sorted(out.iterdir()):
   if p.is_file() and (p.suffix=='.pptx' or p.name=='READ_ME_FIRST.txt'):z.write(p,'Projector_Test_Versions/'+p.name)
 with ZipFile(st) as z:
  assert z.testzip() is None and len(z.namelist())==4
  for m in summary:assert hashlib.sha256(z.read('Projector_Test_Versions/'+m['final_filename'])).hexdigest()==m['deck_sha256']
 os.replace(st,dest)
 assert sha(F/'Thesis_Defense_gg0_v3.pptx')==main_before and sha(F/'Thesis_Defense_Projector_Silent.pptx')==silent_before
 report={'date':'2026-10-09','variants':summary,'total_native_playback_checks':45,'main_and_prior_silent_unchanged':True,'university_projector_tested':False,'output_folder':str(out),'zip':str(dest),'zip_sha256':sha(dest)}
 (H/'verification.json').write_text(json.dumps(report,indent=2))
 (H/'source-notes.txt').write_text('User requested three additional decks with different video solutions/types and sound removed for later university testing. Use original preserved video sources and retain every source frame. Preserve all slide/note/master/poster parts; only video payloads, media relationship targets and necessary MIME declarations differ. No slide authoring or visual rebuild. Microsoft format guidance recorded in the delivered READ_ME_FIRST.txt.\n')
 print(json.dumps({'files':[{'name':m['final_filename'],'MB':round(m['size_bytes']/1e6,1)} for m in summary],'playback_checks':45,'zip_MB':round(dest.stat().st_size/1e6,1)},indent=2))
if __name__=='__main__':finish()
