"""Presentation-only feedback diagram based on thesis Figure 3.2.

Generate matching editable DrawingML and vector PDF/SVG from one scene.
The diagram separates operations (rectangles), signed junctions (crossed
circles), signals (arrows) and controller parameters. The thesis is unchanged.
Requires PyMuPDF and lxml. Run from any working directory.
"""
from pathlib import Path
import argparse
import math
from lxml import etree as E
import fitz

ASSETS=Path(__file__).resolve().parents[1]
FINAL=ASSETS.parent
P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
NS={'p':P,'a':A}
CLIP=fitz.Rect(30,205,930,448)
SCENE=[]

def rect(name,b,text,size=17):
    SCENE.append(dict(kind='rect',name=name,box=b,text=text,size=size))
def text(name,b,value,size=16):
    SCENE.append(dict(kind='text',name=name,box=b,text=value,size=size))
def mathtext(name,b,runs,size=22):
    SCENE.append(dict(kind='math',name=name,box=b,runs=runs,size=size))
def line(name,x1,y1,x2,y2,arrow=False,width=1.25):
    SCENE.append(dict(kind='line',name=name,points=[x1,y1,x2,y2],arrow=arrow,width=width))
def junction(name,x,y,negative=False):
    SCENE.append(dict(kind='ellipse',name=name,box=[x-18,y-18,x+18,y+18]))
    r=18/math.sqrt(2)
    line(name+' cross rising',x-r,y+r,x+r,y-r,width=.8)
    line(name+' cross falling',x-r,y-r,x+r,y+r,width=.8)
    text(name+' left plus',[x-16,y-6,x-5,y+6],'+',11)
    if negative:text(name+' lower minus',[x-6,y+5,x+6,y+16],'−',11)
    else:text(name+' upper plus',[x-6,y-16,x+6,y-5],'+',11)

# Main signal path at y=321. Parameter inputs occupy y=219--289.
# Feedback has a separate horizontal run at y=420, with a q branch at x=611.
rect('Desired reference block',[44,214,194,258],'Desired reference',17)
rect('Impedance controller block',[292,294,480,348],'Impedance controller',17)
SCENE.append(dict(kind='rect',name='Jacobian transpose block',box=[565,294,657,348],text='',size=22))
mathtext('Jacobian transpose operation',[569,298,653,344],[('𝐽','math',1,0),('T','text',.7,-.35),('(𝑞)','math',1,0)])
rect('Robot block',[815,294,917,348],'Robot',19)
junction('Reference minus measured state',180,321,True)
junction('Additive torque sum',716,321,False)

line('Desired reference down',56,258,56,321)
line('Desired reference to plus',56,321,162,321,True)
text('Desired signal label',[72,272,194,295],'Reference state',14.5)
line('Errors to impedance',198,321,292,321,True)
text('Pose and velocity error signal',[198,273,292,311],'Pose and\nvelocity errors',14.5)

text('Impedance parameter description',[292,219,480,239],'Stiffness and damping',14.5)
mathtext('Impedance parameter symbols',[348,241,424,271],[('𝐾','math',1,0),(', ','text',1,0),('𝐷','math',1,0)])
line('Parameters to impedance',386,273,386,294,True)

line('Wrench to Jacobian transpose',480,321,565,321,True)
mathtext('Wrench signal',[505,280,541,313],[('𝐹','math',1,0)])
line('Cartesian torque to sum',657,321,698,321,True)
mathtext('Cartesian torque signal',[660,280,695,313],[('𝜏','math',1,0)])
line('Commanded torque to robot',734,321,815,321,True)
mathtext('Commanded torque signal',[742,280,806,313],[('𝜏','math',1,0),('cmd','text',.7,.25)])

text('Additional torque sources',[622,214,810,235],'Model + null-space',15.5)
text('Additional torque signal',[677,239,755,259],'Torques',14.5)
line('Other torques to plus',716,266,716,303,True)

line('Robot state down',866,348,866,420)
line('Measured state return',866,420,180,420)
line('Measured feedback to minus',180,420,180,339,True)
text('Measured Cartesian feedback label',[233,386,557,410],'Measured state',16)
text('State definition',[233,425,557,445],'State: pose and velocity',15)
text('Measured robot state label',[625,425,852,445],'Measured robot state',15)
SCENE.append(dict(kind='dot',name='Measured state branch',box=[609,418,613,422]))
line('Measured q to Jacobian',611,420,611,348,True)
mathtext('Joint configuration signal',[620,367,653,399],[('𝑞','math',1,0)])

def q(prefix,name):return '{'+NS[prefix]+'}'+name
def sub(parent,prefix,local,**attrs):return E.SubElement(parent,q(prefix,local),**{k:str(v) for k,v in attrs.items()})
def colour(parent):sub(sub(parent,'a','solidFill'),'a','srgbClr',val='000000')
def xfrm(parent,b,flipH=False,flipV=False):
    attrs={}
    if flipH:attrs['flipH']='1'
    if flipV:attrs['flipV']='1'
    x=sub(parent,'a','xfrm',**attrs)
    sub(x,'a','off',x=round(b[0]*12700),y=round(b[1]*12700))
    sub(x,'a','ext',cx=round((b[2]-b[0])*12700),cy=round((b[3]-b[1])*12700))

def add_text(parent,item):
    tb=sub(parent,'p','txBody')
    bp=sub(tb,'a','bodyPr',wrap='none',lIns=0,rIns=0,tIns=0,bIns=0,anchor='ctr')
    sub(bp,'a','noAutofit');sub(tb,'a','lstStyle')
    lines=[item['runs']] if 'runs' in item else [[(line,'text',1,0)] for line in item.get('text','').split('\n')]
    for runs in lines:
        p=sub(tb,'a','p');pr=sub(p,'a','pPr',algn='ctr',marL=0,indent=0)
        spacing=sub(pr,'a','lnSpc')
        if len(lines)>1:sub(spacing,'a','spcPts',val=round(item['size']*100))
        else:sub(spacing,'a','spcPct',val=100000)
        sub(pr,'a','buNone')
        for value,font,ratio,dy in runs:
            r=sub(p,'a','r');attrs=dict(sz=round(item['size']*ratio*100),b='0')
            if dy:attrs['baseline']=round(-dy*100000)
            rp=sub(r,'a','rPr',**attrs);colour(rp)
            face='Cambria Math' if font=='math' else 'Arial'
            for key in ['latin','ea','cs']:sub(rp,'a',key,typeface=face)
            t=sub(r,'a','t');t.text=value
            if value.startswith(' ') or value.endswith(' '):t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')

def native_scene():
    tree=E.Element(q('p','spTree'),nsmap=NS)
    for idx,item in enumerate(SCENE,1000):
        k=item['kind']
        if k=='line':
            sh=sub(tree,'p','cxnSp');nv=sub(sh,'p','nvCxnSpPr')
            sub(nv,'p','cNvPr',id=idx,name='Feedback diagram - '+item['name'])
            sub(nv,'p','cNvCxnSpPr');sub(nv,'p','nvPr');sp=sub(sh,'p','spPr')
            x1,y1,x2,y2=item['points'];xfrm(sp,[min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2)],x2<x1,y2<y1)
            sub(sub(sp,'a','prstGeom',prst='straightConnector1'),'a','avLst')
            ln=sub(sp,'a','ln',w=round(item['width']*12700));colour(ln)
            if item['arrow']:sub(ln,'a','tailEnd',type='triangle',w='sm',len='sm')
        else:
            sh=sub(tree,'p','sp');nv=sub(sh,'p','nvSpPr')
            sub(nv,'p','cNvPr',id=idx,name='Feedback diagram - '+item['name'])
            sub(nv,'p','cNvSpPr',txBox='1' if k in ['text','math'] else '0');sub(nv,'p','nvPr')
            sp=sub(sh,'p','spPr');xfrm(sp,item['box'])
            sub(sub(sp,'a','prstGeom',prst='ellipse' if k in ['ellipse','dot'] else 'rect'),'a','avLst')
            if k=='dot':colour(sp)
            else:sub(sp,'a','noFill')
            ln=sub(sp,'a','ln',w=15875 if k in ['rect','ellipse'] else 0)
            if k in ['rect','ellipse']:colour(ln)
            else:sub(ln,'a','noFill')
            if k in ['rect','text','math']:add_text(sh,item)
    return tree

def fonts(pdf_source,arial_file):
    doc=fitz.open(pdf_source)
    required='𝐾𝐷𝐽𝑞𝐹𝜏,()'
    for page in doc:
        for entry in page.get_fonts():
            if 'CambriaMath' not in entry[3]:continue
            data=doc.extract_font(entry[0])[3];font=fitz.Font(fontbuffer=data)
            if all(font.has_glyph(ord(c)) for c in required):return fitz.Font(fontfile=arial_file),font,data
    raise RuntimeError('No embedded Cambria Math font covers the diagram symbols.')

def draw(page,arial_file,math_data,offset=(0,0)):
    page.insert_font(fontname='DiagramArial',fontfile=arial_file)
    page.insert_font(fontname='DiagramMath',fontbuffer=math_data)
    fontmap={'text':fitz.Font(fontfile=arial_file),'math':fitz.Font(fontbuffer=math_data)}
    def point(x,y):return fitz.Point(x-offset[0],y-offset[1])
    def rectbox(b):return fitz.Rect(b[0]-offset[0],b[1]-offset[1],b[2]-offset[0],b[3]-offset[1])
    for item in SCENE:
        kind=item['kind']
        if kind=='line':
            x1,y1,x2,y2=item['points'];page.draw_line(point(x1,y1),point(x2,y2),color=(0,0,0),width=item['width'])
            if item['arrow']:
                angle=math.atan2(y2-y1,x2-x1);length=6;half=2.8
                a=(x2-length*math.cos(angle)+half*math.sin(angle),y2-length*math.sin(angle)-half*math.cos(angle))
                b=(x2-length*math.cos(angle)-half*math.sin(angle),y2-length*math.sin(angle)+half*math.cos(angle))
                path=page.new_shape();path.draw_polyline([point(x2,y2),point(*a),point(*b),point(x2,y2)])
                path.finish(color=(0,0,0),fill=(0,0,0),width=.3,closePath=True);path.commit()
            continue
        box=rectbox(item['box'])
        if kind=='rect':page.draw_rect(box,color=(0,0,0),width=1.25)
        elif kind in ['ellipse','dot']:page.draw_oval(box,color=(0,0,0),fill=(0,0,0) if kind=='dot' else None,width=1.25)
        if kind not in ['rect','text','math']:continue
        lines=[item['runs']] if 'runs' in item else [[(line,'text',1,0)] for line in item.get('text','').split('\n')]
        for line_index,runs in enumerate(lines):
            for value,font,ratio,dy in runs:
                assert all(fontmap[font].has_glyph(ord(c)) for c in value),(item['name'],value)
            width=sum(fontmap[font].text_length(value,fontsize=item['size']*ratio) for value,font,ratio,dy in runs)
            assert width<=box.width-2,(item['name'],width,box.width)
            x=box.x0+(box.width-width)/2
            basefont=fontmap['math' if kind=='math' else 'text']
            baseline=(box.y0+box.y1)/2+item['size']*(basefont.ascender+basefont.descender)/2
            baseline+=(line_index-(len(lines)-1)/2)*item['size']
            for value,font,ratio,dy in runs:
                size=item['size']*ratio
                page.insert_text((x,baseline+dy*item['size']),value,fontname='DiagramMath' if font=='math' else 'DiagramArial',fontsize=size,color=(0,0,0))
                x+=fontmap[font].text_length(value,fontsize=size)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=ASSETS)
    parser.add_argument('--pdf-source',type=Path,default=FINAL/'Thesis_Defense_gg0_v3.pdf')
    parser.add_argument('--arial',default='/home/hm-panda/Desktop/usr/share/gazebo-11/media/fonts/arial.ttf')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    _,_,math_data=fonts(args.pdf_source,args.arial)
    document=fitz.open();page=document.new_page(width=CLIP.width,height=CLIP.height)
    draw(page,args.arial,math_data,(CLIP.x0,CLIP.y0))
    stem=args.out/'controller_feedback_diagram'
    document.save(stem.with_suffix('.pdf'),garbage=4,deflate=True)
    stem.with_suffix('.svg').write_text(page.get_svg_image(text_as_path=True))
    stem.with_suffix('.xml').write_bytes(E.tostring(native_scene(),encoding='UTF-8',xml_declaration=True,pretty_print=True))
    print('Generated diagram PDF, SVG and editable DrawingML from the shared scene.')

if __name__=='__main__':main()
