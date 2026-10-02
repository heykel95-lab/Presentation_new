import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const slide=deck.slides.add();
slide.background.fill='white';
const layout={
 headings:{'Position heading':{text:'Force',xy:[60,78]},'Rotation heading':{text:'Moment',xy:[510,78]}},
 newHeadings:[{from:'Position heading',name:'Positional error heading',text:'Positional error',xy:[60,170]},{from:'Rotation heading',name:'Rotational error heading',text:'Rotational error',xy:[510,170]}],
 positions:{'Equation - equation_force':[80,117],'Equation - equation_moment':[530,117],'Equation - position_error_definition':[79.899,229],'Equation - controller_orientation_error':[529.78,227],'Figure - position_error_sketch':[247,196],'Figure - rotation_error_sketch':[697,196],'Controller scope':[60,328],'Equation - controller_wrench_blocks':[80,365],'Decoupling statement':[68,459]}
};
// Importing the native equations raises "Unsupported a14:m payload".
// Author editable heading assets here, then apply this layout to the original
// OOXML so every original Office Math payload and picture remains intact.
for(const item of [...Object.entries(layout.headings).map(([name,v])=>({name,...v})),...layout.newHeadings]){
 const shape=slide.shapes.add({geometry:'textbox',name:item.name,position:{left:item.xy[0]*4/3,top:item.xy[1]*4/3,width:390*4/3,height:30*4/3},fill:'none',line:{fill:'none',width:0}});
 shape.text=item.text;
 shape.text.style={typeface:'Arial',fontSize:22*4/3,color:'#17365D',alignment:'left',verticalAlignment:'middle',autoFit:'none',wrap:'none',insets:{left:0,right:0,top:0,bottom:0}};
}
await fs.writeFile(path.join(here,'layout.json'),JSON.stringify(layout,null,2));
await (await PresentationFile.exportPptx(deck)).save(path.join(here,'artifact_layout.pptx'));
console.log('Authored Force and Moment first, errors second, and Cartesian wrench last.');
