from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from pypdf.generic import DecodedStreamObject, NameObject
import json

HERE=Path(__file__).resolve().parent
FINAL=HERE.parents[1]/'Final Presentation'
old=PdfReader(HERE/'archive/Thesis_Defense_gg0_v3.pdf')
native=PdfReader(HERE/'native_export.pdf')
assert len(old.pages)==len(native.pages)==31
page=native.pages[17]
blank=PageObject.create_blank_page(width=960,height=540)
stream=DecodedStreamObject()
stream.set_data(b'q 1 1 1 rg 30 95 900 310 re f 134 88 692 28 re f Q')
blank[NameObject('/Contents')]=stream
page.merge_page(blank)
figure=PdfReader(HERE/'contact_wrench_three_panels.pdf').pages[0]
assert abs(float(figure.mediabox.width)-900)<0.02
assert abs(float(figure.mediabox.height)-310)<0.02
page.merge_transformed_page(figure,Transformation().translate(tx=30,ty=95))
legend=PdfReader(FINAL/'figures_and_images/contact_legend_balanced.pdf').pages[0]
legend_width=8762898/12700
legend_left=(960-legend_width)/2
page.merge_transformed_page(legend,Transformation().scale(sx=legend_width/float(legend.mediabox.width),sy=26/float(legend.mediabox.height)).translate(tx=legend_left,ty=89))
out=PdfWriter()
for i,oldpage in enumerate(old.pages):out.add_page(page if i==17 else oldpage)
if old.metadata:out.add_metadata({k:str(v) for k,v in old.metadata.items() if v is not None})
out.write(HERE/'Thesis_Defense_gg0_v3.pdf')
supp=PdfWriter()
for p in out.pages[26:]:supp.add_page(p)
supp.write(HERE/'Supplementary_slides.pdf')
print('Full PDF: 31 pages. Supplementary PDF: five pages. Only main page 18 changed.')
