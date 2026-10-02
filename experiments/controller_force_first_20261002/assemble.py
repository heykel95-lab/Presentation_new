from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import json,re,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import select,NS
source=json.loads((HERE/'archive/source.json').read_text());layout=json.loads((HERE/'layout.json').read_text())
assert (HERE/'artifact_layout.pptx').exists()
PART='ppt/slides/slide6.xml'
with ZipFile(ROOT/source['pptx']) as z:raw=z.read(PART).decode('utf-8')
blocks=re.findall(r'<p:(?:sp|pic)\b[^>]*>.*?</p:(?:sp|pic)>',raw,re.S)
def get(name):
    choices=[b for b in blocks if 'name="'+name+'"' in b];assert len(choices)==1,name;return choices[0]
def move(block,xy):
    new=f'<a:off x="{round(xy[0]*12700)}" y="{round(xy[1]*12700)}"'
    block,count=re.subn(r'<a:off\s+x="[^"]+"\s+y="[^"]+"',new,block,count=1);assert count==1;return block
updated=raw
for name,item in layout['headings'].items():
    block=get(name);replacement=move(block,item['xy'])
    replacement,count=re.subn(r'<a:t>[^<]*</a:t>','<a:t>'+item['text']+'</a:t>',replacement,count=1);assert count==1
    updated=updated.replace(block,replacement,1)
for name,xy in layout['positions'].items():updated=updated.replace(get(name),move(get(name),xy),1)
maxid=max(int(x.get('id')) for x in E.fromstring(raw.encode()).findall('.//p:cNvPr',NS))
for i,item in enumerate(layout['newHeadings'],1):
    block=move(get(item['from']),item['xy'])
    block=re.sub(r'(<p:cNvPr\s+id=")[^"]+',lambda m:m.group(1)+str(maxid+i),block,count=1)
    block=block.replace('name="'+item['from']+'"','name="'+item['name']+'"',1)
    updated=updated.replace('</p:spTree>',block+'</p:spTree>',1)
E.fromstring(updated.encode())
(HERE/'slide6.xml').write_text(updated,encoding='utf-8')
with ZipFile(ROOT/source['pptx']) as z,ZipFile(HERE/'updated.pptx','w',ZIP_DEFLATED) as out:
    for info in z.infolist():out.writestr(info,updated.encode() if info.filename==PART else z.read(info.filename))
with ZipFile(HERE/'updated.pptx') as z:select(z,{5},HERE/'native_preview.pptx')
print('Changed only the impedance-controller slide: Force/Moment above the error definitions, then Cartesian wrench.')
