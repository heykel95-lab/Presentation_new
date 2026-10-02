import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const slide=deck.slides.add();slide.background.fill='white';
function text(name,value,box,size=19,color='#000000',bold=false,align='left'){
 const [x,y,w,h]=box;
 const shape=slide.shapes.add({geometry:'textbox',name,position:{left:x*4/3,top:y*4/3,width:w*4/3,height:h*4/3},fill:'none',line:{fill:'none',width:0}});
 shape.text=value;
 shape.text.style={typeface:'Arial',fontSize:size*4/3,color,bold,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'none',insets:{left:0,right:0,top:0,bottom:0}};
 return shape;
}
text('Position heading','Position: 3 translations',[42,78,280,30],22,'#17365D',false,'center');
text('Orientation heading','Orientation: 3 rotations',[336,78,280,30],22,'#17365D',false,'center');
text('Surface-relative compliance heading','Surface frame',[644,78,280,30],22,'#17365D',false,'center');
text('Pose reference frame','Pose is expressed in the robot base frame.',[42,333,570,26],19);
text('Pose takeaway','The (EE) position depends on all 7 joint angles:',[42,365,470,28],19);
text('Surface normal definition','outward surface normal',[695,333,229,27],18);
text('Surface tangent definition','perpendicular tangents',[695,365,229,27],18);
text('Surface-axis components','Surface axes define force and moment components and the directions for impedance gains.',[52,409,872,28],18);
text('Next impedance quantities','Next: force f, moment m, stiffness K and damping D in the impedance law.',[52,445,872,30],20,'#17365D');
text('Controller calculation frame','The controller equations are evaluated in the robot base frame.',[52,475,872,22],16,'#696969');
// The original equations and symbols remain editable Office Math and are
// positioned without changing their contents or 22 pt Cambria Math styling.
const layout={title:'Cartesian pose and surface frame',pictures:{'End effector position figure':[62,119,240,240*3184354/3818365],'End effector orientation figure':[366,113,220,220*3365500/3686487],'Surface frame':[654,113,266,266*3590160/4572000]},equations:{'Equation - pose_joint_configuration':[516,365],'Equation - symbol_ns':[649,335],'Equation - symbol_tangents':[631,367]}};
await fs.writeFile(path.join(here,'layout.json'),JSON.stringify(layout,null,2));
await (await PresentationFile.exportPptx(deck)).save(path.join(here,'text_assets.pptx'));
console.log('Authored the three-column layout and the transition to force, moment, stiffness and damping.');
