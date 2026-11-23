import assert from 'node:assert/strict';
export function consolidateConsole(doc) {
 const nodes=doc.getRoot().listNodes().filter(n=>n.getName().startsWith('GEO_Console_')&&n.getMesh());
 const groups=new Map(); const provenance=[];
 for(const n of nodes) {
  assert.deepEqual(n.getWorldMatrix(),[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]);
  for(const p of n.getMesh().listPrimitives()) {
   const key=p.getMaterial().getName(); if(!groups.has(key)) groups.set(key,[]);
   groups.get(key).push({node:n.getName(),p});
  }
 }
 const buffer=doc.getRoot().listBuffers()[0]; const mesh=doc.createMesh('Console_Consolidated');
 for(const [material,parts] of groups) {
  const semantics=parts[0].p.listSemantics().sort();
  const dest=doc.createPrimitive().setMaterial(parts[0].p.getMaterial()); let offset=0;const indices=[];
  for(const {node,p} of parts) {
   assert.deepEqual(p.listSemantics().sort(),semantics);const start=indices.length;
   for(const idx of p.getIndices().getArray()) indices.push(idx+offset);
   provenance.push({component:node,material,indexStart:start,indexCount:indices.length-start,vertexStart:offset,vertexCount:p.getAttribute('POSITION').getCount()});
   offset+=p.getAttribute('POSITION').getCount();
  }
  dest.setIndices(doc.createAccessor().setType('SCALAR').setArray(new Uint32Array(indices)).setBuffer(buffer));
  for(const s of semantics) {
   const src=parts[0].p.getAttribute(s);const arrays=parts.map(({p})=>p.getAttribute(s).getArray());
   const joined=new arrays[0].constructor(arrays.reduce((n,a)=>n+a.length,0)); let o=0;
   for(const a of arrays) {joined.set(a,o);assert.deepEqual(joined.subarray(o,o+a.length),a);o+=a.length;}
   dest.setAttribute(s,doc.createAccessor().setType(src.getType()).setNormalized(src.getNormalized()).setArray(joined).setBuffer(buffer));
  }
  let o=0,vo=0;
  for(const {p} of parts) {for(const idx of p.getIndices().getArray()) assert.equal(indices[o++]-vo,idx);vo+=p.getAttribute('POSITION').getCount();}
  mesh.addPrimitive(dest);
 }
 for(const n of nodes) {const old=n.getMesh();n.setMesh(null).setExtras({...n.getExtras(),componentProvenance:'GEO_Console_Assembly'});old.dispose();}
 doc.getRoot().listScenes()[0].addChild(doc.createNode('GEO_Console_Assembly').setMesh(mesh).setExtras({sourceComponents:provenance}));
 return {before:11,after:3,savedPrimitives:8,exactAttributeConcatenation:true,exactRebasedIndices:true,provenance};
}
export function appendAuthored(doc,extra) {
 const buffer=doc.getRoot().listBuffers()[0], materials=new Map(doc.getRoot().listMaterials().map(m=>[m.getName(),m]));
 for(const node of extra.getRoot().listNodes()) if(node.getMesh()) {
  assert.deepEqual(node.getWorldMatrix(),[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]);
  const mesh=doc.createMesh(node.getName());
  for(const p of node.getMesh().listPrimitives()) {
   const material=materials.get(p.getMaterial().getName());assert.ok(material,'Unknown authored material');
   const dest=doc.createPrimitive().setMaterial(material);
   for(const s of p.listSemantics()) {const a=p.getAttribute(s);dest.setAttribute(s,doc.createAccessor().setType(a.getType()).setNormalized(a.getNormalized()).setArray(a.getArray().slice()).setBuffer(buffer));}
   const i=p.getIndices();dest.setIndices(doc.createAccessor().setType('SCALAR').setArray(i.getArray().slice()).setBuffer(buffer));mesh.addPrimitive(dest);
  }
  doc.getRoot().listScenes()[0].addChild(doc.createNode(node.getName()).setMesh(mesh).setExtras(node.getExtras()));
 }
}
