import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {root} from './common.mjs';
export async function checkContract(doc,stage){
 const m=JSON.parse(await readFile(resolve(root,'build_pipeline/isolated/candidate-manifest.json')));const errors=[];
 const defs=new Map(m.nodes.map(n=>[n.identifier,n]));const slots=new Map(m.materialSlots.map(s=>[s.slotIdentifier,s]));
 const markers=new Set(m.sourceNodes.filter(n=>n.identifier.startsWith('GEO_Console_')).map(n=>n.identifier));
 const names=new Set();const bounds={min:[Infinity,Infinity,Infinity],max:[-Infinity,-Infinity,-Infinity]};
 for(const n of doc.getRoot().listNodes()) {
  const name=n.getName();if(names.has(name))errors.push('Duplicate node '+name);names.add(name);
  if(n.getCamera())errors.push('Camera included');
  if(!n.getMesh()) {if(!markers.has(name)||n.getExtras().componentProvenance!=='GEO_Console_Assembly')errors.push('Unrecognized empty node '+name);continue;}
  const def=defs.get(name);if(!def){errors.push('Unrecognized mesh '+name);continue;}
  const bound=new Set();
  for(const p of n.getMesh().listPrimitives()){
   const mat=p.getMaterial();bound.add(mat?.getName());if(!def.allowedMaterialSlots.includes(mat?.getName()))errors.push('Binding mismatch '+name);
   if(p.getMode()!==4)errors.push('Non triangles '+name);
   const pos=p.getAttribute('POSITION'),indices=p.getIndices();if(!pos||!indices) {errors.push('Missing indexed positions '+name);continue;}
   if(indices.getCount()%3) errors.push('Invalid triangle index count');
   for(const v of indices.getArray())if(v>=pos.getCount()||v<0){errors.push('Index out of range');break;}
   for(const sem of p.listSemantics()){
    const a=p.getAttribute(sem);if(a.getCount()!==pos.getCount())errors.push('Attribute count mismatch '+name+sem);
    if(!a.getArray().every(Number.isFinite))errors.push('Nonfinite '+name+sem);
   }
   if(!p.getAttribute('NORMAL'))errors.push('Missing normals '+name);
   if(mat?.getNormalTexture()&&!p.getAttribute('TANGENT'))errors.push('Missing tangents '+name);
   if((mat?.getNormalTexture()||mat?.getBaseColorTexture()||mat?.getMetallicRoughnessTexture())&&!p.getAttribute('TEXCOORD_0'))errors.push('Missing UV '+name);
   const a=pos.getArray();for(let i=0;i<a.length;i++){const j=i%3;bounds.min[j]=Math.min(bounds.min[j],a[i]);bounds.max[j]=Math.max(bounds.max[j],a[i]);}
  }
  for(const slot of def.requiredMaterialSlots??[])if(!bound.has(slot))errors.push('Missing required binding '+name+slot);
 }
 for(const name of defs.keys())if(!(stage==='consolidation-proof'&&name==='GEO_Cabin_Expansion')&&!names.has(name))errors.push('Missing node '+name);
 for(const mat of doc.getRoot().listMaterials()){
  const slot=slots.get(mat.getName());if(!slot){errors.push('Unknown material '+mat.getName());continue;}
  if(Math.abs(mat.getRoughnessFactor()-slot.defaultRoughness)>1e-4||Math.abs(mat.getMetallicFactor()-slot.defaultMetallic)>1e-4)errors.push('Changed PBR factors '+mat.getName());
  if(Boolean(mat.getNormalTexture())!==slot.hasNormalMap)errors.push('Changed normal contract');
  if(Boolean(mat.getExtension('KHR_materials_clearcoat'))!==slot.hasClearcoat)errors.push('Changed clearcoat contract');
 }
 for(const slot of slots.keys())if(!doc.getRoot().listMaterials().some(m=>m.getName()===slot))errors.push('Missing material '+slot);
 for(const t of doc.getRoot().listTextures())if(t.getMimeType()!=='image/ktx2')errors.push('Non KTX2 texture');
 if(doc.getRoot().listAnimations().length)errors.push('Unapproved animation');
 for(let i=0;i<3;i++)if(bounds.max[i]-bounds.min[i]>[1.895,1.690,4.890][i])errors.push('Vehicle-envelope exceeded axis '+i);
 return {passed:errors.length===0,errors,bounds,notes:['Primitive count is a draw-call proxy, not measured GPU performance','Marker nodes preserve static console provenance; original front-cabin node gate is superseded only for these offline candidates']};
}
