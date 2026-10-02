import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const deck=await PresentationFile.importPptx(await FileBlob.load(path.join(here,'source_first_two.pptx')));
await fs.writeFile(path.join(here,'artifact-inspection.ndjson'),(await deck.inspect({kind:'slide,image,shape,layout',maxChars:50000})).ndjson ?? JSON.stringify(await deck.inspect({kind:'slide,image,shape,layout',maxChars:50000})));
const title=deck.slides.items[0], motivation=deck.slides.items[1];
console.log('Frames',title.frame, motivation.images.items.map(x=>({id:x.id,alt:x.alt,frame:x.frame})));
const photo=motivation.images.items.find(x=>x.frame.width>400);
if(!photo)throw new Error('Original Motivation photo not identified');
const factor=title.frame.width/960;
const p=(l,t,w,h)=>({left:l*factor,top:t*factor,width:w*factor,height:h*factor});
title.images.add({blob:await fs.readFile(path.resolve(here,'../../Final Presentation/figures_and_images/title_robot.jpg')),contentType:'image/jpeg',alt:'Title robot photograph',fit:'contain',position:p(592,103,329.6,329.6*2908/2858)});
photo.replace({blob:await fs.readFile(path.join(here,'contact_poster.png')),contentType:'image/png',alt:'Contact demonstration video poster',fit:'contain'});
photo.frame=p(521.6,75,400,400);
await fs.writeFile(path.join(here,'media-layout.json'),JSON.stringify({units:'pt',titlePhoto:[592,103,329.6,329.6*2908/2858],motivationVideo:[521.6,75,400,400]},null,2));
for(let i=0;i<2;i++){
 const slide=deck.slides.items[i];
 await fs.writeFile(path.join(here,`artifact-slide-${i+1}.layout.json`),await (await slide.export({format:'layout'})).text());
}
await (await PresentationFile.exportPptx(deck)).save(path.join(here,'artifact-edited.pptx'));
console.log('Exported two edited source slides with the requested photo/poster placement.');
