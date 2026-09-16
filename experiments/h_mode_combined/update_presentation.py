"""Update OOXML parts directly, preserving native equations and embedded videos.
PDF uses the original exported pages with only the changed regions rebuilt from
matching text and vector plots. Requires lxml and PyMuPDF.

Historical six-setting extension builder. This restores the earlier 30-slide
layout. For the approved 25-main / 9-backup narrative, use
experiments/nullspace_narrative/restructure_presentation.py and its README.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
import posixpath,json,re
from lxml import etree as E
import fitz

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FINAL=ROOT/'Final Presentation';ASSETS=FINAL/'figures_and_images'
BACK=HERE/'review';NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
RNS='http://schemas.openxmlformats.org/package/2006/relationships'
def tag(k):a,b=k.split(':');return '{'+NS[a]+'}'+b
def xml(b):return E.fromstring(b)
def dump(r):return E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(BACK/'original.pptx') as z:parts={n:z.read(n) for n in z.namelist()}
orig=dict(parts)
pres=xml(parts['ppt/presentation.xml']);rels=xml(parts['ppt/_rels/presentation.xml.rels']);targets={r.get('Id'):r.get('Target') for r in rels}
paths=[posixpath.normpath('ppt/'+targets[s.get(tag('r:id'))]) for s in pres.find('p:sldIdLst',NS)]
pdf=fitz.open(BACK/'original.pdf');fontpath='/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf';font=fitz.Font(fontfile=fontpath)
navy=(23/255,54/255,93/255);black=(20/255,)*3

def shape(root,name):return next(s for s in root.findall('.//p:sp',NS) if s.find('p:nvSpPr/p:cNvPr',NS).get('name')==name)
def rect(sp):
 x=sp.find('p:spPr/a:xfrm/a:off',NS);s=sp.find('p:spPr/a:xfrm/a:ext',NS)
 return fitz.Rect(int(x.get('x'))/12700,int(x.get('y'))/12700,(int(x.get('x'))+int(s.get('cx')))/12700,(int(x.get('y'))+int(s.get('cy')))/12700)
def text_shape(sp,text):
 body=sp.find('p:txBody',NS);p=deepcopy(body.find('a:p',NS));rp=p.find('a:r/a:rPr',NS);rp=deepcopy(rp) if rp is not None else E.Element(tag('a:rPr'),sz='2000')
 for ch in list(p):
  if ch.tag!=tag('a:pPr'):p.remove(ch)
 for i,line in enumerate(text.split('\n')):
  if i:E.SubElement(p,tag('a:br'))
  r=E.SubElement(p,tag('a:r'));r.append(deepcopy(rp));E.SubElement(r,tag('a:t')).text=line
 for old in body.findall('a:p',NS):body.remove(old)
 body.append(p)
 return int(rp.get('sz','2000'))/100

def modify_text(i,root,name,text,rename=None):
 sp=shape(root,name);box=rect(sp);pdf[i].add_redact_annot(box,fill=(1,1,1));pdf[i].apply_redactions(images=0,graphics=0)
 size=text_shape(sp,text);colour=navy if name=='Settings heading' else black
 if rename:sp.find('p:nvSpPr/p:cNvPr',NS).set('name',rename)
 x=box.x0+20;y=box.y0+size
 pdf[i].insert_font(fontname='ArialNew',fontfile=fontpath)
 pdf[i].insert_text((box.x0,y),'•',fontname='ArialNew',fontsize=size*.8,color=navy)
 for line in text.split('\n'):
  assert font.text_length(line,fontsize=size)<=box.width-20, (name,line,'overflow')
  pdf[i].insert_text((x,y),line,fontname='ArialNew',fontsize=size,color=colour);y+=size*1.1

notes={
28:["Contact reduced angular error for both larger entry tilts while the desired orientation stayed fixed. The estimate retains calibration and tool-mount uncertainty.","Higher rotational stiffness increased angular error. CoC displacement changes the angular error and can carry it through zero.","Adding damping reduced cumulative joint motion by 33.2 percent at 1.5 newton metres and 50.7 percent at 2 newton metres compared with the respective conditioning-only settings. Mean net joint motion remained near zero in the tested disturbance direction.","Future work is a more rigid tool mount and adaptive CoC selection, returning to the TCP after alignment."],
20:["The desired position and orientation stay fixed while joint torques apply the equivalent of a virtual 20-newton point force on link three.","Six settings have three trials each. Both combined settings use mode three, with conditioning at 1.5 or 2 newton metres and damping at 2 newton metre seconds per radian.","Both terms are active before and during the disturbance. The initial posture, Cartesian impedance, disturbance and analysis window match the original study.","We compare cumulative joint motion, net joint motion, measured joint-one motion and minimum singular value."],
21:["Cumulative joint motion adds projected movement in both directions. Damping alone reduces it from 7.60 to 5.69 degrees.","Conditioning alone gives 0.29 degrees at 1.5 newton metres and 1.69 degrees at 2 newton metres. Adding damping gives 0.19 degrees at 1.5 newton metres and 0.83 degrees at 2 newton metres, reductions of 33.2 and 50.7 percent respectively.","Curves show three-trial means and one sample standard deviation. The same recorded 5-to-9-second interval is displayed from zero to four seconds."],
22:["Net joint motion retains direction, so returning motion reduces its value. All seven projected joint velocities are integrated using the same fixed baseline reference direction.","The left plot shows six settings. The right plot enlarges conditioning and both combined settings in the same degree units.","Both combined conditions also end near zero. Curves show three-trial means and one sample standard deviation."],
23:["These are measured joint-one angles relative to each trial's angle at disturbance onset. All three trials per setting are shown at their original sampling times, about 20 hertz.","The right panel enlarges the first second for conditioning and both combined settings. Adding damping reduces the cumulative projected motion over the full interval, although individual joint reversals remain visible.","Conditioning is active during settling, so the settings can start the disturbance at different arm configurations."],
24:["Repetition one is shown for each of the six settings, using the same selection rule throughout.","The measured joint-one angle is relative to disturbance onset. The first-second close-up compares both conditioning magnitudes with both combined settings.","Individual reversals remain visible. The following slide combines all three trials."],
25:["Each setting shows the mean of three onset-relative joint-one angle changes. Shading is one sample standard deviation.","The mean uses exact measured timestamps shared by the three trials. There is no interpolation or smoothing.","Joint-one motion is distinct from cumulative and net projected motion of all seven joints. Both null-space terms remain active in both combined settings."],
26:["A smaller minimum singular value means some tool motions require larger joint velocities under this Jacobian convention.","It decreases with no null-space torque and with damping alone. Both conditioning settings and both combined settings keep it nearly constant during the disturbance.","The curves show three-trial means and one sample standard deviation. A small difference in their absolute levels does not establish a meaningful conditioning advantage."],
27:["Net joint motion is the projected motion remaining after opposite movements cancel. It is 7.52 degrees without null-space torque and 5.61 degrees with damping alone.","Both conditioning settings and both combined settings end near zero. The combined mean is about two thousandths of a degree at 1.5 newton metres and minus twelve thousandths at 2 newton metres.","Adding damping lowers cumulative motion from 0.29 to 0.19 degrees at 1.5 newton metres and from 1.69 to 0.83 degrees at 2 newton metres. Small net motion alone does not mean that the arm was stationary."]}
updates={
28:{'Conclusion null-space':'Combined damping and conditioning reduced redundant motion'},
20:{'Settings heading':'Six settings with three trials each','Measured quantities':'Combined (mode 3): 1.5 and 2 N m\nDamping: 2 N m s/rad'},
21:{'Null-space finding 1':'Damping alone: 7.60° to 5.69°. Conditioning alone: 0.29° and 1.69°.','Null-space finding 2':'Combined: 0.19° at 1.5 N m and 0.83° at 2 N m.'},
22:{'Null-space finding 1':'Returning motion reduces the net joint motion.','Null-space finding 2':'Conditioning and combined control end near zero.'},
23:{'Null-space finding 1':'Six settings, including conditioning with damping.','Null-space finding 2':'Three individual trials per setting, each starting at zero.'},
24:{'Null-space finding 1':'Repetition 1 for each of the six settings.','Null-space finding 2':'The close-up compares conditioning with and without damping.'},
25:{'Null-space finding 1':'Three-trial mean and one sample standard deviation.','Null-space finding 2':'Joint 1 motion, including both combined settings.'},
26:{'Null-space finding 1':'Minimum singular value decreased with no torque and damping alone.','Null-space finding 2':'Conditioning and combined control kept the indicator nearly constant.'},
27:{'Null-space finding 1':'Both combined settings left nearly zero mean net joint motion.','Null-space finding 2':'Adding damping reduced cumulative motion at both conditioning settings.'}}
figures={21:'nullspace_damping',22:'nullspace_displacement_time',23:'joint_motion_time',24:'joint_motion_single',25:'joint_motion_mean',26:'nullspace_conditioning',27:'nullspace_net_displacement'}
for number,changes in updates.items():
 i=number-1;path=paths[i];root=xml(parts[path]);relpath=posixpath.dirname(path)+'/_rels/'+posixpath.basename(path)+'.rels';relroot=xml(parts[relpath])
 for name,text in changes.items():modify_text(i,root,name,text,'Setting combined' if name=='Measured quantities' else None)
 if number in figures:
  name=figures[number]
  # Clear the previous figure and separate headings, keeping slide furniture.
  pdf[i].add_redact_annot(fitz.Rect(55,55,910,421),fill=(1,1,1));pdf[i].apply_redactions(images=2,graphics=1)
  for s in root.findall('.//p:sp',NS):
   if s.find('p:nvSpPr/p:cNvPr',NS).get('name') in ['All-settings heading','Conditioning-detail heading']:s.getparent().remove(s)
  pic=next(p for p in root.findall('.//p:pic',NS) if p.find('p:nvPicPr/p:cNvPr',NS).get('name')=='Figure - '+name)
  target=name+'_combined.png';media='ppt/media/'+target;parts[media]=(ASSETS/target).read_bytes()
  rid='rIdCombinedResult';E.SubElement(relroot,'{'+RNS+'}Relationship',Id=rid,Type=NS['r']+'/image',Target='../media/'+target)
  pic.find('p:blipFill/a:blip',NS).set(tag('r:embed'),rid)
  pic.find('p:nvPicPr/p:cNvPr',NS).set('name','Figure - '+name+'_combined')
  if number in [22,23,24,25]:box=fitz.Rect(110,52,850,422)
  else:box=fitz.Rect(100,62,860,62+760*4.2/9)
  off=pic.find('p:spPr/a:xfrm/a:off',NS);ext=pic.find('p:spPr/a:xfrm/a:ext',NS)
  for k,v in [('x',box.x0),('y',box.y0)]:off.set(k,str(round(v*12700)))
  for k,v in [('cx',box.width),('cy',box.height)]:ext.set(k,str(round(v*12700)))
  plotpdf=fitz.open(ASSETS/(name+'_combined.pdf'));pdf[i].show_pdf_page(box,plotpdf,0);plotpdf.close()
 # Synchronize spoken notes and retain the previous source block.
 nr=next(r for r in relroot if r.get('Type','').endswith('/notesSlide'))
 npth=posixpath.normpath(posixpath.dirname(path)+'/'+nr.get('Target'));nroot=xml(parts[npth])
 bodysp=next(s for s in nroot.findall('.//p:sp',NS) if s.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None and s.find('p:nvSpPr/p:nvPr/p:ph',NS).get('type')=='body')
 tx=bodysp.find('p:txBody',NS);old='\n'.join(tx.xpath('.//a:t/text()',namespaces=NS));sources='[Sources]'+old.split('[Sources]',1)[1] if '[Sources]' in old else '[Sources]'
 technical='[Combined experiment]\nMode 3: tau_null = tau_sigma + tau_damping. k_sigma = 1.5 or 2 N m, d_null = 2 N m s/rad. Three trials per combined setting on 2026-09-16. Exact archived controller revision 0210e7f2 and saved parameters, with only mode 2 changed to mode 3. Original 5–9 s interval, displayed as 0–4 s. Later acquisition session: session effects were not independently controlled.\nexperiments/h_mode_combined/README.md\nexperiments/h_mode_combined_1p5/README.md\nfigures_and_images/sources/combined_nullspace_provenance.json\nfigures_and_images/sources/make_combined_nullspace.py'
 for p in tx.findall('a:p',NS):tx.remove(p)
 for line in notes[number]+[sources,technical]:
  p=E.SubElement(tx,tag('a:p'));r=E.SubElement(p,tag('a:r'));E.SubElement(r,tag('a:t')).text=line
 parts[npth]=dump(nroot);parts[path]=dump(root);parts[relpath]=dump(relroot)

# Verify Overview chapter names against native sections. Chapters/order unchanged.
chapters=[s.get('name') for s in pres.xpath('//*[local-name()="sectionLst"]/*[local-name()="section"]') if s.get('name')!='Backup']
overview=xml(parts[paths[3]])
items=[]
for sp in overview.findall('.//p:sp',NS):
 name=sp.find('p:nvSpPr/p:cNvPr',NS).get('name')
 if name.startswith('Overview item '):items.append((int(name.split()[-1]),''.join(sp.xpath('.//a:t/text()',namespaces=NS))))
assert [v for _,v in sorted(items)]==chapters and len(chapters)==6
# Every native equation and every video is preserved byte-for-byte within its part.
for p in paths:
 before=xml(orig[p]);after=xml(parts[p]);get=lambda r:[E.tostring(x) for x in r.xpath('//*[local-name()="oMath"]')]
 assert get(before)==get(after), ('equations changed',p)
for name in orig:
 if name.endswith(('.mp4','.wmv')):assert parts[name]==orig[name]
assert sum(xml(parts[p]).get('show')=='0' for p in paths)==2
with ZipFile(FINAL/'Thesis_Defense_gg0_v3.pptx','w',ZIP_DEFLATED) as z:
 for name,content in parts.items():z.writestr(name,content)
pdf.save(FINAL/'Thesis_Defense_gg0_v3.pdf',garbage=4,deflate=True)
sup=fitz.open();sup.insert_pdf(pdf,from_page=28,to_page=29);sup.save(FINAL/'Supplementary_slides.pdf');sup.close();pdf.close()

# Update the speaking source in the same pass as the slide notes.
script=(BACK/'original_script.tex').read_text()
for number,bullets in notes.items():
 root=xml(parts[paths[number-1]]);title=''.join(shape(root,'Slide title').xpath('.//a:t/text()',namespaces=NS))
 start=script.index('\\section*{'+title+'}');end=script.find('\\section*{',start+10)
 if end<0:end=script.index('\\end{document}',start)
 section='\\section*{'+title+'}\n\\begin{itemize}\n'+'\n'.join('\\item '+t.replace('%','\\%') for t in bullets)+'\n\\end{itemize}\n\n'
 script=script[:start]+section+script[end:]
# Portable fallback for hosts without the original newtx font package.
script=script.replace('\\usepackage{newtxtext,newtxmath}','\\IfFileExists{newtxtext.sty}{\\usepackage{newtxtext,newtxmath}}{\\usepackage{mathptmx}}')
script=script.replace(r'\mbox{pseudoinverse \(J^+\)}',r'pseudoinverse \(J^+\)')
(FINAL/'Speaking/Thesis_Defense_Speaking_Script.tex').write_text(script)
manifest=json.loads((ASSETS/'manifest.json').read_text())
manifest=[x for x in manifest if not x.get('asset','').endswith('_combined')]
for name in figures.values():manifest.append({'asset':name+'_combined','source':'sources/make_combined_nullspace.py; sources/combined_nullspace_provenance.json','changes':'Includes three measured mode-3 trials at each of k_sigma=1.5 and 2 N m, both with d_null=2 N m s/rad. Original four conditions verified. Exact 5–9 s interval, three-trial mean/sample SD, same reference direction, no smoothing/interpolation. Presentation-only extension. PDF/PNG/SVG synchronized.'})
(ASSETS/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(HERE/'presentation_validation.json').write_text(json.dumps({'slides':30,'hidden_backups':2,'updated_slides':list(updates),'native_equations_preserved':True,'embedded_videos_preserved':True,'overview_chapters_verified':chapters,'overview_note':'PowerShell unavailable on Linux. Equivalent XML chapter synchronization check passed; no structure change required.','pdf_method':'Original PowerPoint PDF with changed text regions and vector figure replacements at matching OOXML coordinates.'},indent=2)+'\n')
print('Updated final PowerPoint, 30-page PDF, two-page supplementary PDF, notes and speaking source.')
