// Reproducible inputs from the accepted pre-production commit, never from our output.
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import draco from 'draco3dgltf';
import { execFileSync } from 'node:child_process';
import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
const out = resolve('blender/out/front-cabin');
await mkdir(out, {recursive:true});
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'draco3d.decoder':await draco.createDecoderModule()});
const records = [];
for (const kind of ['classic','diamond','perforated']) {
  const path = `public/assets/3d/lexus-rx350/interior-l4-${kind}.glb`;
  const bytes = execFileSync('git',['show',`fa3d62a:${path}`],{maxBuffer:16*1024*1024});
  const doc = await io.readBinary(bytes);
  const record = {kind, sourceCommit:'fa3d62a', sha256:createHash('sha256').update(bytes).digest('hex'), primitives:[], textures:[]};
  for (const mesh of doc.getRoot().listMeshes()) for (const p of mesh.listPrimitives()) record.primitives.push({mesh:mesh.getName(),material:p.getMaterial().getName(),triangles:p.getIndices().getCount()/3});
  for (const tex of doc.getRoot().listTextures()) {
    const name = tex.getName(), stem = resolve(out,kind+'-'+name);
    await writeFile(stem+'.ktx2',tex.getImage());
    record.textures.push({name, file:kind+'-'+name+'.ktx2'});
    if (kind === 'classic') {
      execFileSync('C:/Program Files/KTX-Software/bin/ktx.exe',['extract','--transcode','rgba8','--level','0',stem+'.ktx2',stem+'.png'],{timeout:120000});
      tex.setImage(await readFile(stem+'.png')).setMimeType('image/png');
    }
  }
  if (kind === 'classic') {
    for (const ext of [...doc.getRoot().listExtensionsUsed()]) if (['KHR_texture_basisu','KHR_draco_mesh_compression'].includes(ext.extensionName)) ext.dispose();
    await io.write(resolve(out,'source-render.glb'),doc);
  }
  records.push(record);
}
await writeFile(resolve(out,'inputs.json'),JSON.stringify(records,null,2));
console.log(JSON.stringify(records,null,2));
