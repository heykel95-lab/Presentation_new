from pathlib import Path
import json,re
import pypdfium2 as pdfium
import pdfplumber
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
path=HERE/'Thesis_Defense_Speaking_Script.pdf'
reader=PdfReader(path)
assert len(reader.pages)==7
text='\n'.join(page.extract_text() for page in reader.pages)
assert 'manual disturbances applied' not in text
assert 'Part 1' not in text and 'Part 2' not in text
assert 'conditioning alone, damping alone' in text
assert 'now with conditioning only' in text
assert 'first without null-space control and then with damping' in ' '.join(text.split())
log=(HERE/'Thesis_Defense_Speaking_Script.log').read_text(errors='replace')
assert not re.search(r'Overfull \\[hv]box',log)
assert 'Rerun to get outlines right' not in log
with pdfplumber.open(path) as pdf:
    bounds=[]
    for i,page in enumerate(pdf.pages):
        chars=page.chars
        bbox=[min(c['x0'] for c in chars),min(c['top'] for c in chars),
              max(c['x1'] for c in chars),max(c['bottom'] for c in chars)]
        assert bbox[0]>40 and bbox[1]>40 and bbox[2]<page.width-40 and bbox[3]<page.height-40,(i,bbox)
        bounds.append(bbox)
document=pdfium.PdfDocument(path)
for i in range(len(document)):
    page=document[i];bitmap=page.render(scale=1.5)
    # Render in memory to avoid retaining redundant page images on the full drive.
    assert bitmap.width>0 and bitmap.height>0
    bitmap.close();page.close()
document.close()
verification=json.loads((HERE/'verification.json').read_text())
verification.update({'speech_pdf_pages':7,'latex_no_overfull_boxes':True,
                     'all_speech_pages_rendered':True,'speech_page_text_bounds':bounds})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Seven-page speech PDF rendered; no overflow or stale video labels.')
