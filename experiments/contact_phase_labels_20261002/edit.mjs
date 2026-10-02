import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const layout={heading:{name:'Experiment phases heading',text:'Experiment phases:',box:[60,68,840,30]},phases:{box:[80,109,840,30]},labels:{'Normal label':'Normal translation (compliant)','Tangential translation label':'Tangential translation (stiff)','Normal rotation label':'Rotation about the surface normal (stiff)','Rotation label':'Rotations about the surface tangents (compliant)'}};
const deck=Presentation.create({slideSize:{width:1280,height:720}});const slide=deck.slides.add();
function add(name,value,box,size){const [x,y,w,h]=box;const s=slide.shapes.add({geometry:'textbox',name,position:{left:x*4/3,top:y*4/3,width:w*4/3,height:h*4/3},fill:'none',line:{fill:'none',width:0}});s.text=value;s.text.style={typeface:'Arial',fontSize:size*4/3,color:'#17365D',autoFit:'none',wrap:'none',insets:{left:0,right:0,top:0,bottom:0}};}
add(layout.heading.name,layout.heading.text,layout.heading.box,22);
for(const [name,y] of [['Normal label',190],['Tangential translation label',259],['Normal rotation label',328],['Rotation label',399]])add(name,layout.labels[name],[500,y,420,25],18);
await fs.writeFile(path.join(here,'layout.json'),JSON.stringify(layout,null,2));await(await PresentationFile.exportPptx(deck)).save(path.join(here,'text_assets.pptx'));
console.log('Authored experiment-phase heading and four directional stiffness labels.');
