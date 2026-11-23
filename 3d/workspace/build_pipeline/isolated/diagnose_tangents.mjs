import {root,createIO,save} from './common.mjs';
import {resolve} from 'node:path';
const io=await createIO(); const d=await io.read(resolve(root,'working_models/B3-doors-additions.glb'));
const r=d.getRoot().listMeshes().flatMap(m=>m.listPrimitives().map(p=>({material:p.getMaterial().getName(),semantics:p.listSemantics(),triangles:p.getIndices().getCount()/3,needsTangents:!!p.getMaterial().getNormalTexture(),hasTangents:!!p.getAttribute('TANGENT')})));
await save('reports/reference-r2/tangent-before.json',r);console.log(JSON.stringify(r,null,2));
