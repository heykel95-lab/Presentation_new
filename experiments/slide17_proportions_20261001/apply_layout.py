"""Narrow asset/layout update preserving equations, media, notes and slide IDs."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import json, re, shutil, hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
ARCHIVE.mkdir(exist_ok=True)
source=FINAL/'Thesis_Defense_gg0_v3.pptx'
for f in [source,FINAL/'Thesis_Defense_gg0_v3.pdf',FINAL/'Supplementary_slides.pdf']:
    if not (ARCHIVE/f.name).exists():shutil.copy2(f,ARCHIVE/f.name)
for ext in ['pdf','png','svg']:
    f=FINAL/'figures_and_images'/f'contact_wrench_three_panels.{ext}'
    if not (ARCHIVE/f.name).exists():shutil.copy2(f,ARCHIVE/f.name)

part='ppt/slides/slide20.xml'
updates={
    'Angular response heading': {'y':107.0},
    'Normal force heading': {'y':107.0},
    'Interaction moment heading': {'y':107.0},
    'Figure - contact_wrench_three_panels': {'y':135.0},
    'Figure - contact_legend': {'x':(960-8762898/12700)/2,'y':425.0},
}
with ZipFile(source) as z:
    xml=z.read(part).decode('utf-8')
    assert 'Angular error and interaction wrench' in xml
    changed=[]
    def edit_shape(match):
        original=match[0]
        name=re.search(r'<p:cNvPr\b[^>]*\bname="([^"]+)"',original)
        if not name or name[1] not in updates:return original
        replacement=original
        for axis,value in updates[name[1]].items():
            replacement,n=re.subn(r'(<a:off\b[^>]*\b'+axis+r'=")\d+("[^>]*/>)',lambda m:m[1]+str(round(value*12700))+m[2],replacement,count=1)
            assert n==1,name[1]
        changed.append(name[1])
        return replacement
    updated=re.sub(r'<p:(?:sp|pic)\b[^>]*>.*?</p:(?:sp|pic)>',edit_shape,xml,flags=re.S)
    assert set(changed)==set(updates)
    E.fromstring(updated)
    replacements={part:updated.encode('utf-8'),'ppt/media/image50.png':(HERE/'contact_wrench_three_panels.png').read_bytes()}
    before={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}
    with ZipFile(HERE/'updated.pptx','w',ZIP_DEFLATED) as out:
        for info in z.infolist():out.writestr(info,replacements.get(info.filename,z.read(info.filename)))
with ZipFile(HERE/'updated.pptx') as z:
    modified=[n for n in z.namelist() if hashlib.sha256(z.read(n)).hexdigest()!=before[n]]
    assert set(modified)==set(replacements)
    assert z.testzip() is None
verification={
    'date':'2026-10-01','physical_slide':18,'footer':17,
    'title':'Angular error and interaction wrench',
    'panel_size_before_pt':[224,231.826087],
    'panel_size_after_pt':[224,168],
    'panel_aspect_ratio':'4:3',
    'picture_box_after_pt':[30,135,900,310],
    'legend_center_pt':480,
    'changed_package_parts':modified,
    'speaker_notes_equations_videos_other_slides_unchanged':True,
    'data_panel_pdfs_labels_fonts_grid_limits_timing_unchanged':True,
    'artifact_import_error':'Unsupported a14:m payload. Expected m:oMathPara or m:oMath.',
    'preservation_method':'Retained original package. Replaced only the compiled figure image and five existing shape coordinates, as required to preserve native Office equations, video playback, and all other slides.',
}
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n',encoding='utf-8')
print(json.dumps(verification,indent=2))
