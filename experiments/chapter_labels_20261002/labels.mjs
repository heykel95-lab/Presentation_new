import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const inventory=JSON.parse(await fs.readFile(path.join(here,'inventory.json'),'utf8'));
const chapters=[...new Map(inventory.filter(x=>x.label).map(x=>[x.chapter,x.chapter_name])).entries()];
// These are supplemental text assets. The original presentation is preserved
// verbatim and receives only the authored native text shape for each chapter.
const deck=Presentation.create({slideSize:{width:1280,height:720}});
const variants=[];
for(const [chapter,name] of chapters){
 for(const first of [true,false]){
  const slide=deck.slides.add();
  slide.background.fill='white';
  const label=slide.shapes.add({geometry:'textbox',name:'Current overview chapter',position:{left:880,top:28,width:348.8,height:32},fill:'none',line:{fill:'none',width:0}});
  label.text=`${chapter}. ${name}`;
  label.text.style={typeface:'Arial',fontSize:first?56/3:16,bold:first,color:first?'#17365D':'#696969',alignment:'right',verticalAlignment:'middle',wrap:'none',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};
  variants.push({chapter,name,first,slide:variants.length+1});
 }
}
await (await PresentationFile.exportPptx(deck)).save(path.join(here,'labels.pptx'));
await fs.writeFile(path.join(here,'variants.json'),JSON.stringify(variants,null,2));
console.log('Created 12 native chapter label variants at the existing header size.');
