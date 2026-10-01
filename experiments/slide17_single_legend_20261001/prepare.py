from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream
from PIL import ImageChops, ImageDraw
import pypdfium2 as pdfium
import io, json, hashlib, re, math

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
ARCHIVE.mkdir(exist_ok=True)
PART='ppt/slides/slide20.xml'
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx') as deck:
    before={n:hashlib.sha256(deck.read(n)).hexdigest() for n in deck.namelist()}
    (ARCHIVE/'package_hashes_before.json').write_text(json.dumps(before,indent=2))
    with (FINAL/'Thesis_Defense_gg0_v3.pptx').open('rb') as original:
        original.seek(deck.start_dir)
        (ARCHIVE/'original_zip_directory.bin').write_bytes(original.read())
    (ARCHIVE/'zip_checkpoint.json').write_text(json.dumps({'start_dir':deck.start_dir}))
    old=deck.read(PART).decode('utf-8')
    (ARCHIVE/'slide20.xml').write_bytes(deck.read(PART))
    pictures=re.findall(r'<p:pic\b[^>]*>.*?</p:pic>',old,re.S)
    middle=next(s for s in pictures if 'name="Legend - normal force"' in s)
    removed=[s for s in pictures if any('name="'+name+'"' in s for name in
             ['Legend - angular error','Legend - TCP moment'])]
    assert len(removed)==2
    updated=old
    for shape in removed:updated=updated.replace(shape,'',1)
    assert middle in updated and updated.count('name="Legend - ')==1
    E.fromstring(updated)
    (HERE/'slide20.xml').write_text(updated,encoding='utf-8')

original=(FINAL/'Thesis_Defense_gg0_v3.pdf').read_bytes()
parent=HERE.parent/'slide21_swap_settings_20261001'
prior=json.loads((parent/'pdf_checkpoint.json').read_text())
assert hashlib.sha256(original).hexdigest()==prior['updated_sha256']
(ARCHIVE/'pdf_before.json').write_text(json.dumps({
    'parent_recipe':str((parent/'archive/pdf_before.json').relative_to(ROOT)),
    'append_file':str((parent/'presentation_pdf_update.bin').relative_to(ROOT)),
    'sha256':prior['updated_sha256'],'size':len(original)
},indent=2))

# Remove exactly the two independently wrapped vector legend groups. All other
# drawing operations, resources, original plot vectors and text remain intact.
writer=PdfWriter(io.BytesIO(original),incremental=True)
page=writer.pages[17]
stream=ContentStream(page.get_contents(),writer)
ops=stream.operations
intervals=[]
for i,(args,op) in enumerate(ops):
    if op!=b'cm' or len(args)!=6:continue
    values=[float(v) for v in args]
    if values[:4]!=[1,0,0,1] or abs(values[5]-81.841)>.001:continue
    if not any(abs(values[4]-x)<.001 for x in [142.809,742.809]):continue
    assert ops[i-1][1]==b'q'
    depth=0
    for end in range(i-1,len(ops)):
        if ops[end][1]==b'q':depth+=1
        elif ops[end][1]==b'Q':depth-=1
        if depth==0:
            intervals.append((i-1,end+1));break
assert len(intervals)==2 and intervals[0][1]<=intervals[1][0]
stream.operations=[item for i,item in enumerate(ops) if not any(a<=i<b for a,b in intervals)]
assert sum(op==b'cm' and len(args)==6 and abs(float(args[4])-442.809)<.001
           and float(args[0])==1 for args,op in stream.operations)==1
assert len(stream.get_data())>1000
page.replace_contents(stream.flate_encode())
memory=io.BytesIO();writer.write(memory)
result=memory.getvalue()
assert result[:len(original)]==original
tail=result[len(original):]
(HERE/'presentation_pdf_update.bin').write_bytes(tail)
(HERE/'pdf_checkpoint.json').write_text(json.dumps({
    'original_size':len(original),'original_sha256':hashlib.sha256(original).hexdigest(),
    'updated_sha256':hashlib.sha256(result).hexdigest(),'append_bytes':len(tail)
},indent=2))

before_pdf,after_pdf=pdfium.PdfDocument(original),pdfium.PdfDocument(result)
assert len(before_pdf)==len(after_pdf)==31
changed=[]
for i in range(31):
    old_page,new_page=before_pdf[i],after_pdf[i]
    old_bitmap,new_bitmap=old_page.render(scale=1),new_page.render(scale=1)
    old_image,new_image=old_bitmap.to_pil().convert('RGB'),new_bitmap.to_pil().convert('RGB')
    difference=ImageChops.difference(old_image,new_image)
    if difference.getbbox():changed.append(i+1)
    if i==17:
        # Comparison mask only, not an edit to any presentation image.
        mask=ImageDraw.Draw(difference)
        for x in [142.809,742.809]:
            mask.rectangle((math.floor(x)-1,397,math.ceil(x+126.382)+1,460),fill=(0,0,0))
        assert difference.getbbox() is None,'Pixels changed outside the removed legends'
    old_bitmap.close();new_bitmap.close();old_page.close();new_page.close()
before_pdf.close();after_pdf.close()
assert changed==[18],changed
verification={'date':'2026-10-01','footer':17,'physical_slide':18,
    'removed_legends':['Legend - angular error','Legend - TCP moment'],
    'retained_legend':'Legend - normal force','retained_legend_unchanged':True,
    'retained_legend_position_pt':[442.809,398,126.382,60.159],
    'full_pdf_pages':31,'other_30_pages_pixel_identical':True,
    'changed_physical_pages':changed,'only_removed_legend_areas_differ':True,
    'all_plot_vectors_and_other_slide_elements_preserved':True,
    'pdf_increment_bytes':len(tail),
    'supplementary_pdf_sha256':hashlib.sha256((FINAL/'Supplementary_slides.pdf').read_bytes()).hexdigest(),
    'speaking_file_hashes':{str(p.relative_to(FINAL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        [FINAL/'Thesis_Defense_Speaking_Script.pdf',FINAL/'Thesis_Defense_Speaking_Script_updated.pdf',
         FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex',FINAL/'Speaker_notes_and_timing.txt']}}
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Prepared one retained middle legend. All other pixels on all 31 pages are unchanged.')
