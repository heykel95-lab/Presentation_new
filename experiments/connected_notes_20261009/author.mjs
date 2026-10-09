import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const deck=await PresentationFile.importPptx(await FileBlob.load(path.join(here,'notes_source.pptx')));
const notes=JSON.parse(await fs.readFile(path.join(here,'notes.json'),'utf8'));
for(let i=0;i<31;i++){
 const speaker=deck.slides.items[i].speakerNotes;
 speaker.clear();speaker.textFrame.setText(notes[i].map(({runs})=>({runs})));speaker.setVisible(true);
}
await(await PresentationFile.exportPptx(deck)).save(path.join(here,'authored.pptx'));
console.log('Authored all 31 connected speaker notes at 18 pt.');
