import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import draco from 'draco3dgltf';
import validator from 'gltf-validator';
import { readFile, writeFile, mkdir, realpath } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { dirname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
export const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
export const hash = b => createHash('sha256').update(b).digest('hex');
export const kinds = ['classic', 'diamond', 'perforated'];
export const budgets = {triangles:80000, primitives:24, bytes:5242880};
export async function guard() {
  const inventory = JSON.parse(await readFile(resolve(root,'reports/download-inventory.json')));
  const results=[];
  for (const kind of kinds) {
    const local=`production_baseline/interior-l4-${kind}.glb`;
    const expected=inventory.find(x=>x.local===local);
    if (!expected) throw new Error('Missing pinned baseline inventory: '+local);
    const actual=hash(await readFile(resolve(root,local)));
    if (actual!==expected.sha256) throw new Error('BASELINE HASH MISMATCH: '+local);
    results.push({kind,sha256:actual,unchanged:true});
  }
  return results;
}
export async function outputPath(relative) {
  const path=resolve(root,relative);
  if (!['exports','working_models','textures','reports'].some(d=>path.startsWith(resolve(root,d)+sep))) throw new Error('Output outside candidate directories: '+relative);
  await mkdir(dirname(path),{recursive:true});
  const parent=await realpath(dirname(path));
  if (!parent.startsWith((await realpath(root))+sep)) throw new Error('Output symlink escapes workspace');
  return path;
}
export async function createIO(){return new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'draco3d.decoder':await draco.createDecoderModule(),'draco3d.encoder':await draco.createEncoderModule()});}
export function inspect(doc) {
  const nodes=doc.getRoot().listNodes().filter(n=>n.getMesh()).map(n=>({name:n.getName(),matrix:n.getWorldMatrix(),primitives:n.getMesh().listPrimitives().map(p=>({material:p.getMaterial()?.getName(),triangles:(p.getIndices()?.getCount()??p.getAttribute('POSITION').getCount())/3,attributes:Object.fromEntries(p.listSemantics().map(s=>[s,hash(Buffer.from(p.getAttribute(s).getArray().buffer,p.getAttribute(s).getArray().byteOffset,p.getAttribute(s).getArray().byteLength))])),indices: p.getIndices()?hash(Buffer.from(p.getIndices().getArray().buffer,p.getIndices().getArray().byteOffset,p.getIndices().getArray().byteLength)):null}))}));
  return {nodes,triangles:nodes.reduce((s,n)=>s+n.primitives.reduce((a,p)=>a+p.triangles,0),0),primitives:nodes.reduce((s,n)=>s+n.primitives.length,0),materials:doc.getRoot().listMaterials().map(m=>m.getName()),textures:doc.getRoot().listTextures().map(t=>({name:t.getName(),mime:t.getMimeType(),sha256:hash(t.getImage())}))};
}
export async function validate(bytes,io) {
  const official=await validator.validateBytes(new Uint8Array(bytes),{maxIssues:200});
  const doc=await io.readBinary(bytes); const facts=inspect(doc);
  const errors=[];
  for(const key of ['triangles','primitives']) if(facts[key]>budgets[key]) errors.push(`${key} exceeds ${budgets[key]}`);
  if(bytes.length>budgets.bytes) errors.push('bytes exceed '+budgets.bytes);
  if(official.issues.numErrors) errors.push('Khronos validator errors: '+official.issues.numErrors);
  return {passed:errors.length===0,errors,bytes:bytes.length,sha256:hash(bytes),...facts,khronos:official};
}
export async function save(relative,data){await writeFile(await outputPath(relative),typeof data==='string'||data instanceof Uint8Array?data:JSON.stringify(data,null,2)+'\n');}
