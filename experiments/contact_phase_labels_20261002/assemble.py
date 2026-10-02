from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,sys,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,select,dump
source=json.loads((HERE/'archive/source.json').read_text());layout=json.loads((HERE/'layout.json').read_text())
with ZipFile(ROOT/source['pptx']) as z:root=E.fromstring(z.read(source['part']))
def find(name):
 result=root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$n]',namespaces=NS,n=name);assert len(result)==1,name;return result[0]
def frame(shape,box):
 xf=shape.find('p:spPr/a:xfrm',NS)
 for key,value in zip(['x','y'],box[:2]):xf.find('a:off',NS).set(key,str(round(value*12700)))
 for key,value in zip(['cx','cy'],box[2:]):xf.find('a:ext',NS).set(key,str(round(value*12700)))
with ZipFile(HERE/'text_assets.pptx') as z:authored=E.fromstring(z.read('ppt/slides/slide1.xml'))
values={s.find('p:nvSpPr/p:cNvPr',NS).get('name'):''.join(s.xpath('.//a:t/text()',namespaces=NS)) for s in authored.findall('.//p:sp',NS)}
for name,value in layout['labels'].items():
 assert values[name]==value
 target=find(name);texts=target.findall('.//a:t',NS);assert len(texts)==1;texts[0].text=value
heading=deepcopy(find('Contact settings heading'));cn=heading.find('p:nvSpPr/p:cNvPr',NS);cn.set('id',str(max(int(x.get('id')) for x in root.findall('.//p:cNvPr',NS))+1));cn.set('name',layout['heading']['name'])
for ext in list(cn):cn.remove(ext)
heading.find('.//a:t',NS).text=values[layout['heading']['name']];frame(heading,layout['heading']['box']);root.find('p:cSld/p:spTree',NS).append(heading)
frame(find('Contact phases'),layout['phases']['box'])
(HERE/'updated_slide.xml').write_bytes(dump(root))
with ZipFile(HERE/'archive/original_contact_slide.pptx') as z,ZipFile(HERE/'native_preview.pptx','w',ZIP_DEFLATED) as out:
 for info in z.infolist():out.writestr(info,dump(root) if info.filename==source['part'] else z.read(info.filename))
print('Changed only the Contact experiment slide; native equations, figure and notes preserved.');
