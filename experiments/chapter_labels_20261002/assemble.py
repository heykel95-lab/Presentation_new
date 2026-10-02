from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import json,re,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation'
sys.path.insert(0,str(HERE.parent/'motivation_video_20261002'))
from prepare import NS,resolve,select
source=json.loads((HERE/'archive/source.json').read_text())
inventory=json.loads((HERE/'inventory.json').read_text())
assert hashlib.sha256((ROOT/source['pptx']).read_bytes()).hexdigest()==source['pptx_sha256']
with ZipFile(ROOT/source['pptx']) as z:parts={n:z.read(n) for n in z.namelist()}
with ZipFile(HERE/'labels.pptx') as z:
    p=E.fromstring(z.read('ppt/presentation.xml'))
    r={x.get('Id'):resolve('ppt/presentation.xml',x.get('Target')) for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
    labels=[]
    for e in p.find('p:sldIdLst',NS):
        root=E.fromstring(z.read(r[e.get('{'+NS['r']+'}id')]))
        shapes=root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name="Current overview chapter"]',namespaces=NS)
        assert len(shapes)==1
        labels.append(shapes[0])
for e in inventory:
    if not e['label']:continue
    raw=parts[e['path']];root=E.fromstring(raw)
    label=deepcopy(labels[e['variant']])
    meta=label.find('p:nvSpPr/p:cNvPr',NS)
    meta.set('id',str(max(int(x.get('id')) for x in root.findall('.//p:cNvPr',NS))+1))
    meta.set('descr',('New chapter: ' if e['first_in_chapter'] else 'Current chapter: ')+e['label'])
    assert ''.join(label.xpath('.//a:t/text()',namespaces=NS))==e['label']
    # Append the authored shape, leaving every byte of existing slide content
    # intact, including native equations, timings and notes relationships.
    fragment=E.tostring(label,encoding='utf-8')
    assert raw.count(b'</p:spTree>')==1
    parts[e['path']]=raw.replace(b'</p:spTree>',fragment+b'</p:spTree>',1)
with ZipFile(HERE/'updated.pptx','w',ZIP_DEFLATED) as out:
    for n,data in parts.items():out.writestr(n,data)
with ZipFile(HERE/'updated.pptx') as z:select(z,{4,18,25},HERE/'native_preview.pptx')
print('Added labels to 23 existing content slides. All slide order, numbering and original slide objects remain unchanged.')
