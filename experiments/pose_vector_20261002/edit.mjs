import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const slide=deck.slides.add();slide.background.fill='white';
function text(name,value,box,size=19,color='#000000',align='left'){
 const [x,y,w,h]=box;
 const shape=slide.shapes.add({geometry:'textbox',name,position:{left:x*4/3,top:y*4/3,width:w*4/3,height:h*4/3},fill:'none',line:{fill:'none',width:0}});
 shape.text=value;
 shape.text.style={typeface:'Arial',fontSize:size*4/3,color,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'none',insets:{left:0,right:0,top:0,bottom:0}};
}
text('Full Cartesian pose heading','Cartesian pose of the end-effector (EE)',[42,65,578,30],22,'#17365D','center');
const layout={
 text:{'Position heading':{xy:[42,181]},'Orientation heading':{xy:[336,181]},
 'Pose takeaway':{text:'Position depends on all 7 joint angles:',box:[42,396,386,28]},
 'Pose reference frame':{text:'Pose and controller equations use the robot base frame.',box:[42,428,880,26]},
 'Surface-axis components':{xy:[52,455]},'Next impedance quantities':{xy:[52,477]}},
 remove:['Controller calculation frame'],
 pictures:{'End effector position figure':[82,218,200,200*3184354/3818365],'End effector orientation figure':[376,213,200,200*3365500/3686487]},
 equations:{'Equation - pose_joint_configuration':[438,396,178,29],'Equation - cartesian_pose_vector':[209,101,250,65]},
 branches:[{name:'Pose branch stem',from:[331,168],to:[331,173]},{name:'Pose branch crossbar',from:[182,173],to:[476,173]},{name:'Pose branch position',from:[182,173],to:[182,181],arrow:true},{name:'Pose branch orientation',from:[476,173],to:[476,181],arrow:true}]
};
await fs.writeFile(path.join(here,'layout.json'),JSON.stringify(layout,null,2));
await (await PresentationFile.exportPptx(deck)).save(path.join(here,'text_assets.pptx'));
console.log('Authored the centred Cartesian-pose introduction and position/orientation split.');
