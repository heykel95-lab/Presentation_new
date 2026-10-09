from pathlib import Path
import sys
_workspace=next(p for p in Path(__file__).resolve().parents if (p/'Final Presentation').is_dir())
sys.path[:0]=[str(_workspace/'tmp/connected_notes_deps'),str(_workspace/'tmp/remove_b5_20260922/deps')]
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,KeepTogether,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
from xml.sax.saxutils import escape
import json,re,hashlib,shutil,os,sys

HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'Final Presentation').is_dir());FINAL=ROOT/'Final Presentation'
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
FONT=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('SpeechArial',str(FONT/'arial.ttf')))
pdfmetrics.registerFont(TTFont('SpeechArialBold',str(FONT/'arialbd.ttf')))
pdfmetrics.registerFontFamily('SpeechArial',normal='SpeechArial',bold='SpeechArialBold')
navy=HexColor('#17365D');teal=HexColor('#197E83');ink=HexColor('#202C36');gray=HexColor('#687680')
styles={
 'heading':ParagraphStyle('Slide heading',fontName='SpeechArialBold',fontSize=12.8,leading=16,textColor=navy,spaceBefore=6,spaceAfter=6,keepWithNext=True),
 'opening':ParagraphStyle('Spoken opening',fontName='SpeechArialBold',fontSize=13.5,leading=18.5,textColor=ink,spaceAfter=4,allowWidows=0,allowOrphans=0),
 'body':ParagraphStyle('Spoken script',fontName='SpeechArial',fontSize=13.5,leading=18.5,textColor=ink,spaceAfter=4,allowWidows=0,allowOrphans=0),
 'cue':ParagraphStyle('Unspoken instruction',fontName='SpeechArial',fontSize=10.2,leading=13,textColor=gray,spaceBefore=3,spaceAfter=4),
 'intro':ParagraphStyle('Reading instructions',fontName='SpeechArial',fontSize=10.7,leading=14,textColor=gray,spaceAfter=6),
}
GROUPS=[[1,2,3],[4,5,6],[7,8,9,10],[11,12,13,14],[15,16,17,18],[19,20,21],[22,23],[24,25],[26,27,28],[29,30,31]]
MAIN_PAGES=sum(max(group)<=25 for group in GROUPS)
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def spoken(s):return [s['opening'],*s['paragraphs'],*([s['after_video']] if 'after_video' in s else [])]
def count(s):return sum(len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*",p)) for p in spoken(s))
def prepare():
 archive=HERE/'archive';archive.mkdir(exist_ok=True)
 source=FINAL/'Simple_speech_updated.pdf';dest=archive/'Simple_speech_before.pdf'
 assert not dest.exists();shutil.copy2(source,dest)
 protect=[FINAL/'Thesis_Defense_gg0_v3.pptx',FINAL/'Thesis_Defense_gg0_v3.pdf',FINAL/'Supplementary_slides.pdf',FINAL/'Speaker_notes_and_timing.txt',FINAL/'figures_and_images/native_equations.json']
 protect += [p for p in FINAL.glob('*.pdf') if p.name!='Simple_speech_updated.pdf' and p not in protect]
 protect += list((FINAL/'Speaking').rglob('*.tex'))
 (archive/'protected.json').write_text(json.dumps({str(p.relative_to(ROOT)):sha(p) for p in protect},indent=2))
 (HERE/'source-notes.txt').write_text('Source: the editable script.json in this folder. The 25 main scripts preserve the spoken wording supplied by the user on 2026-10-03; the six existing backup scripts are retained. Nonspoken audio-download links are omitted. Video timings are preserved from the existing presentation. No external research or added claims. This standalone builder updates only the speech PDF; synchronize PowerPoint sentence-opening prompts separately when spoken wording changes.\n',encoding='utf-8')
 print('Archived the previous PDF and recorded protected-file hashes.')
def header(canvas,doc):
 page=doc.page;canvas.saveState();w,h=A4
 canvas.setFont('SpeechArialBold',17);canvas.setFillColor(navy)
 canvas.drawString(20*mm,h-20*mm,'Simple presentation speech')
 canvas.setFont('SpeechArial',9.5);canvas.setFillColor(gray)
 canvas.drawRightString(w-20*mm,h-20*mm,'MAIN TALK' if page<=MAIN_PAGES else 'OPTIONAL BACKUPS')
 canvas.setStrokeColor(HexColor('#DCE4E8'));canvas.setLineWidth(.6);canvas.line(20*mm,h-24*mm,w-20*mm,h-24*mm)
 canvas.setFillColor(teal);canvas.rect(20*mm,h-24*mm,32,2,fill=1,stroke=0)
 canvas.setFont('SpeechArial',9);canvas.setFillColor(gray)
 canvas.drawString(20*mm,13*mm,'Heykel Khadhraoui | Thesis presentation | 09.10.2026')
 canvas.drawRightString(w-20*mm,13*mm,f'{page} / {len(GROUPS)}')
 canvas.restoreState()
def build():
 assert [s['physical'] for s in DATA]==list(range(1,32))
 words=sum(count(s) for s in DATA[:25]);videos=sum(s.get('video_seconds',0) for s in DATA[:25]);pauses=30
 times={str(w):round(words/w+(videos+pauses)/60,2) for w in [90,100,110,120,125,130,140,150]}
 assert times['130']<15.5  # Keep this revision close to the original fallback length.
 story=[]
 for page,group in enumerate(GROUPS,1):
  if page>1:story.append(PageBreak())
  if group[0]==26:
   story.append(Paragraph('Use only the relevant backup when answering a question. These six scripts are outside the 15-minute main talk. Each can be read on its own.',styles['intro']))
   story.append(Spacer(1,6))
  for n in group:
   s=DATA[n-1];block=[Paragraph(escape(s['label']+' | '+s['title']),styles['heading']),Paragraph(escape(s['opening']),styles['opening'])]
   block.extend(Paragraph(escape(p),styles['body']) for p in s['paragraphs'])
   if 'video_seconds' in s:
    block.append(Paragraph(f'[Play the full video: about {s["video_seconds"]:.0f} seconds. Then say:]',styles['cue']))
    block.append(Paragraph(escape(s['after_video']),styles['body']))
   if n==25:block.append(Paragraph('[End of the main talk. Use backups only if needed for questions.]',styles['cue']))
   story.append(KeepTogether(block));story.append(Spacer(1,9))
 doc=SimpleDocTemplate(str(HERE/'Simple_speech.pdf'),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=31*mm,bottomMargin=22*mm,title='Simple speech - complete read-aloud presentation script',author='Heykel Khadhraoui',subject='Complete spoken script with slide transitions, video cues and optional backup answers',pageCompression=1)
 doc.build(story,onFirstPage=header,onLaterPages=header)
 reader=PdfReader(HERE/'Simple_speech.pdf');assert len(reader.pages)==len(GROUPS),len(reader.pages)
 norm=lambda t:' '.join(t.split())
 for i,group in enumerate(GROUPS):
  extracted=norm(reader.pages[i].extract_text())
  for n in group:
   s=DATA[n-1]
   for p in [s['label']+' | '+s['title'],*spoken(s)]:assert norm(p) in extracted,(n,p)
 txt=[]
 for s in DATA:
  txt.extend([s['label']+' | '+s['title'],'',s['opening'],*s['paragraphs']])
  if 'video_seconds' in s:txt.extend([f'[Play video: about {s["video_seconds"]:.0f} seconds.]',s['after_video']])
  txt.extend(['[End of main talk.]' if s['physical']==25 else '',''])
 (HERE/'Simple_speech.txt').write_text('\n\n'.join(txt),encoding='utf-8')
 report={'main_slides':25,'optional_backup_slides':6,'pages':len(GROUPS),'main_talk_pages':MAIN_PAGES,'optional_backup_pages':len(GROUPS)-MAIN_PAGES,'main_spoken_word_count':words,'backup_spoken_word_count':sum(count(s) for s in DATA[25:]),'all_main_videos_seconds':round(videos,3),'pause_allowance_seconds':pauses,'estimated_total_minutes_including_full_videos_separately':times,'openings_for_all_slides':True,'full_spoken_paragraphs_no_bullet_prompts':True,'before_and_after_video_speech':True,'all_spoken_text_verified_on_expected_pages':True,'pdf_sha256':sha(HERE/'Simple_speech.pdf'),'installed':False}
 report.update(planned_words_per_minute=130,minimum_words_per_minute_for_15_minutes=round(words/(15-(videos+pauses)/60),1))
 (HERE/'verification.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
def install():
 report=json.loads((HERE/'verification.json').read_text());assert report['visually_reviewed_pages']==len(GROUPS)
 for p,h in json.loads((HERE/'archive/protected.json').read_text()).items():assert sha(ROOT/p)==h,p
 dest=FINAL/'Simple_speech_updated.pdf';assert sha(dest)==sha(HERE/'archive/Simple_speech_before.pdf')
 pending=dest.with_name('Simple_speech_updated.pending.pdf');assert not pending.exists()
 os.link(HERE/'Simple_speech.pdf',pending);os.replace(pending,dest)
 report.update(installed=True,installed_by_atomic_replacement=True,deck_notes_slide_pdfs_and_other_speaking_files_unchanged=True)
 (HERE/'verification.json').write_text(json.dumps(report,indent=2))
 print('Installed the full read-aloud speech PDF; protected files are unchanged.')
if __name__=='__main__':globals()[sys.argv[1]]()
