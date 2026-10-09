from pathlib import Path
from zipfile import ZipFile
import sys,json,hashlib,shutil,os,posixpath,xml.etree.ElementTree as E
H=Path(__file__).resolve().parent;ROOT=H.parents[1];F=ROOT/'Final Presentation'
sys.path.insert(0,str(ROOT/'tmp/remove_b5_20260922/deps'))
import pymupdf as fitz
def sha(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def install():
    pkg=json.loads((H/'package_verification.json').read_text());conv=json.loads((H/'conversion.json').read_text())
    playback=json.loads((H/'powerpoint_playback.json').read_text(encoding='utf-8-sig'))
    assert [p['slide'] for p in playback]==[2,12,20,21,26]
    assert all(len(p['tests'])==3 and all(t['advanced'] and t['state']==0 for t in p['tests']) for p in playback)
    assert len(conv)==6 and all(m['all_original_frames_retained'] and m['full_decode_passed'] for m in conv)
    assert sha(F/'Thesis_Defense_gg0_v3.pptx')==pkg['source_sha256']
    assert sha(H/'archive/original.pptx')==pkg['source_sha256']
    assert sha(H/'updated.pptx')==pkg['updated_sha256']
    assert len(fitz.open(H/'regenerated_full.pdf'))==31
    protected=[*F.glob('*.pdf'),*F.glob('Speaker*.txt'),*list((F/'Speaking/simple_speech').glob('*.*')),*list((F/'Video').glob('*.mp4'))]
    original_hashes={str(p.relative_to(ROOT)):sha(p) for p in protected if p.is_file()}
    (H/'protected.json').write_text(json.dumps(original_hashes,indent=2))
    backup=F/'Video/Projector_compatible';backup.mkdir(exist_ok=True)
    mapping={
      'media1.mp4':'01_Motivation_contact.mp4',
      'Plausibility_experiment_presentation.mp4':'11_Impedance_response.mp4',
      'Nullspace2_part1_0000-0023.mp4':'19_Nullspace_damping.mp4',
      'Nullspace2_part2_0023-end.mp4':'20_Nullspace_conditioning.mp4',
      'Opposing_moment_presentation.mp4':'B1_Opposing_CoC_moment.mp4',
    }
    for source,target in mapping.items():
        shutil.copy2(H/'compatible_media'/source,backup/target)
        assert sha(backup/target)==sha(H/'compatible_media'/source)
    guide='''VIDEO PLAYBACK AND PROJECTOR GUIDE - 9 October 2026

Use Thesis_Defense_gg0_v3.pptx in desktop PowerPoint. The five videos used
in the slides are embedded, so this PPTX does not depend on loose videos.
The PDF contains still images of the videos and does not play them.

Before presenting
1. Connect and switch on the projector, then open PowerPoint.
2. Copy the PPTX to the computer's local drive before opening it.
3. Start Slide Show and test the videos on footer slides 1, 11, 19, 20,
   and backup B1. Click the video to play it, as before.
4. Check the projected screen as well as the laptop screen.

If a video still fails
- Close and reopen PowerPoint with the projector already connected.
- On Windows, test Windows+P > Duplicate. Both screens will show the
  same presentation. This is a useful test of an extended-display issue.
- Open the matching MP4 in Video/Projector_compatible with an installed
  desktop video player, maximize it on the projected screen, and play it.
  Return to PowerPoint after playback. Filenames use the printed slide
  footer numbers, not PowerPoint's physical slide index.
- If the MP4 plays but the embedded video does not, test PowerPoint's
  File > Info > Optimize Compatibility on a copy, if the option appears.
- If video plays on the laptop but not the projector, ask university IT
  to check the display mode, graphics driver, adapter/dock and HDMI path.
  This symptom needs testing on that equipment; changing video encoding
  alone cannot guarantee a fix.

What changed
The original videos were already MP4/H.264 High Profile Level 4.0 with
AAC audio, but used 1440 x 1440 pixels and approximately 11-17 Mb/s.
The compatibility versions use 960 x 960 pixels, H.264 Constrained
Baseline Level 3.1, 8-bit YUV 4:2:0, constant 30 fps, constrained bitrate,
and fast-start MP4 layout. Every original frame is retained and the AAC
audio stream is copied without re-encoding. The largest frame-timing
adjustment is 33.3 ms in an unused legacy video; the used contact clip
has at most 17.5 ms adjustment. No footage is cut or rotated.

The PPTX is approximately 85 MB instead of 303 MB. Only its six MP4
payloads changed (five used videos and one retained legacy payload).
All other package parts are byte-identical: slides, notes, equations,
posters, click-to-play settings, transitions, and slide order.
Original loose recordings and the established PDFs are unchanged.
The complete original PPTX is preserved in:
../experiments/video_compatibility_20261009/archive/original.pptx

Validation
All six MP4s passed full decoding and frame/audio checks. Desktop
PowerPoint played each of the five used videos at its start, middle,
and near the end (15 checks). All 31 slides were rendered and inspected.
PowerPoint confirmed that all notes still use 18 pt. A 31-page PDF was
regenerated for checking; the established PDF is retained because its
slide content is unchanged and native export introduces small unrelated
text-rendering differences.

The university setup was unavailable, and its exact failure is still
unconfirmed. These changes reduce media requirements; test on the actual
projector before relying on that setup.

Microsoft references
https://support.microsoft.com/en-us/office/video-and-audio-file-formats-supported-in-powerpoint-d8b12450-26db-4c7b-a5c1-593d3418fb59
https://support.microsoft.com/en-us/powerpoint/are-you-having-video-or-audio-playback-issues
https://support.microsoft.com/en-us/powerpoint/tips-for-improving-audio-and-video-playback-and-compatibility-in-powerpoint
'''
    (F/'Projector_playback_help.txt').write_text(guide,encoding='utf-8')
    (backup/'README.txt').write_text('Standalone fallback videos for the active deck. Filenames use slide footer numbers. Open in your installed video player if PowerPoint playback fails. See ../../Projector_playback_help.txt. These files are byte-identical to the matching embedded compatibility videos.\n',encoding='utf-8')
    staged=F/'Thesis_Defense_gg0_v3.video-update.tmp'
    shutil.copy2(H/'updated.pptx',staged);assert sha(staged)==pkg['updated_sha256']
    os.replace(staged,F/'Thesis_Defense_gg0_v3.pptx')
    assert sha(F/'Thesis_Defense_gg0_v3.pptx')==pkg['updated_sha256']
    assert all(sha(ROOT/p)==h for p,h in original_hashes.items())
    checks={'date':'2026-10-09','active_file':str(F/'Thesis_Defense_gg0_v3.pptx'),'active_sha256':pkg['updated_sha256'],'original_sha256':pkg['source_sha256'],'old_size':(H/'archive/original.pptx').stat().st_size,'new_size':(F/'Thesis_Defense_gg0_v3.pptx').stat().st_size,'changed_package_parts':pkg['changed_parts'],'all_other_package_parts_byte_identical':True,'notes_18pt_confirmed':31,'native_slide_renders_inspected':31,'regenerated_pdf_pages':31,'established_pdfs_retained':True,'native_render_pixel_identity':False,'render_note':'Native runs show small differences in isolated text rasterization despite byte-identical nonmedia parts. All slide layouts and video posters are preserved. Established PDFs retained.','powerpoint_playback_checks_passed':15,'used_video_slides':[2,12,20,21,26],'all_original_frames_retained':True,'audio_packet_hashes_identical':True,'original_loose_videos_speech_and_pdfs_unchanged':True,'standalone_fallbacks':mapping,'university_projector_tested':False,'root_cause_confirmed':False}
    (H/'verification.json').write_text(json.dumps(checks,indent=2))
    (H/'source-notes.txt').write_text('Media-only repair of the active deck. User requests a solution for failed projector video playback. Directly replace embedded MP4 payloads to preserve all slide and note XML byte-for-byte. No slide authoring, layout changes, or template reconstruction. Source evidence and Microsoft guidance are recorded in inventory.json and the final playback help file.\n')
    (H/'qa-ledger.txt').write_text('Reviewed all 31 final native slide renders individually. Existing slide geometry, titles, notes, chart legend clearance and poster images preserved. Decoded all six videos in full; all frames and AAC audio retained. Reviewed converted frame samples for all five used videos. Native PowerPoint slideshow playback passed at three positions for each of five videos. External display/projector remains untested. PDF regenerated for QA; canonical PDFs retained to avoid unrelated native text rendering variation.\n')
    print(json.dumps(checks,indent=2))
if __name__=='__main__':install()
