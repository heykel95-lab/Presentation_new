from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,sys
import pypdfium2 as pdfium
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(ROOT/'Final Presentation/Thesis_Defense_gg0_v3.pptx') as z:
    root=E.fromstring(z.read('ppt/slides/slide7.xml'))
    inventory=[]
    for s in root.findall('.//p:sp',NS):
        name=s.find('p:nvSpPr/p:cNvPr',NS).get('name');xf=s.find('p:spPr/a:xfrm',NS)
        item={'name':name,'text':' '.join(s.xpath('.//a:t/text()',namespaces=NS)),'math':' '.join(s.xpath('.//m:t/text()',namespaces=NS))}
        if xf is not None:item['box']=[int(v)/12700 for v in [xf.find('a:off',NS).get('x'),xf.find('a:off',NS).get('y'),xf.find('a:ext',NS).get('cx'),xf.find('a:ext',NS).get('cy')]]
        inventory.append(item)
        if s.find('.//m:oMath',NS) is not None:(HERE/(name.removeprefix('Equation - ')+'.xml')).write_bytes(E.tostring(s,pretty_print=True))
    (HERE/'inventory.json').write_text(json.dumps(inventory,indent=2))
    print(json.dumps([x for x in inventory if not x['name'].startswith('Feedback diagram - ')],indent=2))
pdf=pdfium.PdfDocument(ROOT/'Final Presentation/Thesis_Defense_gg0_v3.pdf')
for i in [5,6]:
    page=pdf[i];bitmap=page.render(scale=1.5);bitmap.to_pil().save(HERE/f'before-{i+1}.png');bitmap.close();page.close()
pdf.close()
