import {root,guard,createIO,save,outputPath} from './common.mjs';
import {resolve} from 'node:path';
import {readFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
await guard(); const io=await createIO();
const doc=await io.read(resolve(root,'production_baseline/interior-l4-classic.glb'));
const bounds=[];
for(const n of doc.getRoot().listNodes()) if(n.getMesh()) {
 const min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
 for(const p of n.getMesh().listPrimitives()) {const a=p.getAttribute('POSITION').getArray();for(let i=0;i<a.length;i++) {const j=i%3;min[j]=Math.min(min[j],a[i]);max[j]=Math.max(max[j],a[i]);}}
 bounds.push({node:n.getName(),min,max});
}
let index=0;
for(const tex of doc.getRoot().listTextures()) {
 const stem=`textures/baseline-${index++}`;
 const ktx=await outputPath(stem+'.ktx2'); await save(stem+'.ktx2',tex.getImage());
 const png=await outputPath(stem+'.png');
 execFileSync('C:/Program Files/KTX-Software/bin/ktx.exe',['extract','--transcode','rgba8','--level','0',ktx,png],{timeout:120000});
 tex.setImage(await readFile(png)).setMimeType('image/png');
}
for(const ext of [...doc.getRoot().listExtensionsUsed()]) if(['KHR_draco_mesh_compression','KHR_texture_basisu'].includes(ext.extensionName)) ext.dispose();
await save('working_models/baseline-render.glb',await io.writeBinary(doc));
await save('reports/pipeline/bounds.json',bounds);await guard(); console.log(JSON.stringify(bounds,null,2));
