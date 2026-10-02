import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const deck=Presentation.create({slideSize:{width:1280,height:720}});const intro=deck.slides.add();intro.background.fill='white';
function text(slide,name,value,box,size=19,color='#000000',align='left'){
 const [x,y,w,h]=box;const s=slide.shapes.add({geometry:'textbox',name,position:{left:x*4/3,top:y*4/3,width:w*4/3,height:h*4/3},fill:'none',line:{fill:'none',width:0}});
 s.text=value;s.text.style={typeface:'Arial',fontSize:size*4/3,color,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'none',insets:{left:0,right:0,top:0,bottom:0}};
}
text(intro,'TCP introduction heading','Tool centre point (TCP)',[60,105,335,30],22,'#17365D');
text(intro,'TCP introduction definition','Controlled reference point\non the (EE).',[60,144,335,58]);
text(intro,'CoC introduction heading','Centre of compliance (CoC)',[60,235,340,30],22,'#17365D');
text(intro,'CoC introduction definition','Virtual reference point\nfor Cartesian impedance.',[60,274,335,58]);
text(intro,'Virtual shifted force meaning','The force acts as if applied at the virtual CoC.',[60,397,840,30],22);
text(intro,'Additional CoC moment heading','Additional moment about the TCP:',[60,446,438,30],22);
const cases=deck.slides.add();cases.background.fill='white';
text(cases,'Virtual CoC moment interpretation','Curved arrows show the moment about the TCP from the force at the virtual CoC.',[60,458,840,28],18,'#000000','center');
await fs.writeFile(path.join(here,'layout.json'),JSON.stringify({insert_before:7,intro_figure:[426,98,470],case_figure:[130,198,700],intro_equation:[520,447,260,32],coupling_equations:{'Equation - symbol_pc':[76.356535433,152.16,45,24],'Equation - coc_displacement_definition':[77.776614173,266.93,190,28]}},null,2));
await (await PresentationFile.exportPptx(deck)).save(path.join(here,'text_assets.pptx'));
console.log('Authored the CoC introduction and the explanatory case caption.');
