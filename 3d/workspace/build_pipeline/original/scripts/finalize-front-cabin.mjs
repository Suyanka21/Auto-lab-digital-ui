// Convert the reproducible Blender output to KTX2, validate before promotion.
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS, KHRTextureBasisu, KHRDracoMeshCompression } from '@gltf-transform/extensions';
import draco from 'draco3dgltf';
import { execFileSync } from 'node:child_process';
import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { validateGlbBytes } from './validate-glb.mjs';
const out=resolve('blender/out/front-cabin'), ev=resolve('docs/review/front-cabin-2026-11-05/evidence');
await mkdir(ev,{recursive:true});
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'draco3d.decoder':await draco.createDecoderModule(),'draco3d.encoder':await draco.createEncoderModule()});
const raw=await readFile(resolve(out,'cabin-raw.glb'));
const inputs=JSON.parse(await readFile(resolve(out,'inputs.json'),'utf8'));
const manifests=JSON.parse(await readFile('src/config/scene-manifest.front-cabin.json','utf8'));
const records=[];
const encodedTextures=new Map();
for(const role of ['base','normal','orm']){
  const stem=resolve(out,'front-cabin-classic-'+role);
  execFileSync('C:/Program Files/KTX-Software/bin/toktx.exe',['--t2','--encode','uastc','--uastc_quality','2','--uastc_rdo_l','1.1','--zcmp','9','--genmipmap','--assign_oetf',role==='base'?'srgb':'linear','--threads','4',stem+'.ktx2',stem+'.png'],{timeout:180000});
  execFileSync('C:/Program Files/KTX-Software/bin/ktx.exe',['validate',stem+'.ktx2'],{timeout:30000});
}
for(const kind of ['classic','diamond','perforated']){
  const doc=await io.readBinary(raw);
  for(const tex of doc.getRoot().listTextures()){
    const name=tex.getName();
    // Imported packed maps retain names; Blender may append .001 for shared copies.
    const original=inputs[0].textures.find(t=>name===t.name || name.startsWith(t.name+'.'));
    let bytes;
    if(original){
      const treatment= name.startsWith('lexus-insert-') ? kind : 'classic';
      const smooth=kind==='classic' && name.startsWith('lexus-insert-');
      bytes=await readFile(resolve(out,smooth?'front-cabin-classic-'+original.name.split('-').at(-1)+'.ktx2':treatment+'-'+original.name+'.ktx2'));
      tex.setName(original.name);
    }else if(encodedTextures.has(name)){
      bytes=encodedTextures.get(name);
    }else{
      const png=resolve(out,name+'.png'),ktx=resolve(out,name+'.ktx2');
      await writeFile(png,tex.getImage());
      execFileSync('C:/Program Files/KTX-Software/bin/toktx.exe',['--t2','--encode','uastc','--uastc_quality','2','--uastc_rdo_l','1.1','--zcmp','9','--genmipmap','--assign_oetf',/normal|orm|roughness|metallic/i.test(name)?'linear':'srgb','--threads','4',ktx,png],{timeout:180000});
      execFileSync('C:/Program Files/KTX-Software/bin/ktx.exe',['validate',ktx],{timeout:30000});
      bytes=await readFile(ktx);
      encodedTextures.set(name,bytes);
    }
    tex.setImage(bytes).setMimeType('image/ktx2');
  }
  doc.createExtension(KHRTextureBasisu).setRequired(true);
  doc.createExtension(KHRDracoMeshCompression).setRequired(true).setEncoderOptions({method:KHRDracoMeshCompression.EncoderMethod.EDGEBREAKER,encodeSpeed:5,decodeSpeed:5,quantizationBits:{POSITION:16,NORMAL:10,TEXCOORD:14,COLOR:10,GENERIC:12}});
  for(const mat of doc.getRoot().listMaterials()){
    const spec=manifests.materialSlots.find(s=>s.slotIdentifier===mat.getName());
    if(!spec)throw new Error('Undeclared material '+mat.getName());
    mat.setRoughnessFactor(spec.defaultRoughness).setMetallicFactor(spec.defaultMetallic);
    if(['MAT_Seat_Primary','MAT_Seat_Secondary','MAT_Steering_Leather'].includes(mat.getName()))mat.setBaseColorFactor([.009,.009,.011,1]);
    // Keep pores below silhouette scale; existing baked quilting remains in the atlas.
    if(mat.getName()==='MAT_Seat_Secondary')mat.setNormalScale(.35);
    if(mat.getName()==='MAT_Seat_Primary')mat.setNormalScale(kind==='diamond'?.8:.5);
  }
  const bytes=await io.writeBinary(doc),path=resolve(out,kind+'.glb');await writeFile(path,bytes);
  const report=await validateGlbBytes(bytes,{scope:'lexus-front-cabin'});
  await writeFile(resolve(ev,kind+'-gate.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({kind,passed:report.passed,triangles:report.triangleCount,calls:report.drawCalls,bytes:bytes.length,errors:report.errors}));
  if(!report.passed)throw new Error(kind+' gate failed; active assets not promoted');
  records.push({kind,path,sha256:report.sha256,triangles:report.triangleCount,calls:report.drawCalls,bytes:bytes.length});
}
// All three must pass before any active asset is replaced.
for(const record of records)await copyFile(record.path,`public/assets/3d/lexus-rx350/interior-l4-${record.kind}.glb`);
await writeFile(resolve(ev,'assets.json'),JSON.stringify(records,null,2)+'\n');
await copyFile(resolve(out,'build.json'),resolve(ev,'blender-build.json'));
await copyFile(resolve(out,'inputs.json'),resolve(ev,'inputs.json'));
