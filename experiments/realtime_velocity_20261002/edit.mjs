import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const slide=deck.slides.add();slide.background.fill='white';
const layout={headings:{'Joint-torque command heading':'Commanded joint torques (motors):','Jacobian velocity mapping':'Jacobian:'},equations:{'Equation - cartesian_torque_mapping':[209,119,175,34],'Equation - jacobian_velocity_mapping':[667,119,200,34]},captions:[{name:'Torque contribution definition',text:'Cartesian contribution',box:[52,165,418,24]},{name:'Cartesian velocity definition',text:'Linear and angular velocity (geometric)',box:[532,165,385,24]}]};
for(const item of layout.captions){
 const [x,y,w,h]=item.box;
 const s=slide.shapes.add({geometry:'textbox',name:item.name,position:{left:x*4/3,top:y*4/3,width:w*4/3,height:h*4/3},fill:'none',line:{fill:'none',width:0}});
 s.text=item.text;s.text.style={typeface:'Arial',fontSize:18*4/3,color:'#000000',alignment:'center',verticalAlignment:'middle',autoFit:'none',wrap:'none',insets:{left:0,right:0,top:0,bottom:0}};
}
await fs.writeFile(path.join(here,'layout.json'),JSON.stringify(layout,null,2));
await (await PresentationFile.exportPptx(deck)).save(path.join(here,'text_assets.pptx'));
console.log('Authored the compact velocity and motor-torque labels.');
