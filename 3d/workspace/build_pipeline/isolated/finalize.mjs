import {checkContract} from './contract.mjs';
import {root,kinds,guard,createIO,inspect,validate,save,budgets} from './common.mjs';
import {consolidateConsole,appendAuthored} from './assembly.mjs';
import {KHRDracoMeshCompression} from '@gltf-transform/extensions';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
const stage=process.argv[2]??'consolidation-proof';
if(!['consolidation-proof','A-frame','B1-floor','B2-rear','B3-doors','B4-pillars','B5-roof','B6-vents','C-cockpit'].includes(stage)) throw new Error('Unknown milestone');
await guard(); const io=await createIO();const reports=[];
for(const kind of kinds) {
 const doc=await io.read(resolve(root,`production_baseline/interior-l4-${kind}.glb`));const before=inspect(doc);
 const consolidation=consolidateConsole(doc);
 if(stage!=='consolidation-proof') appendAuthored(doc,await io.read(resolve(root,`working_models/${stage}-additions.glb`)));
 const facts=inspect(doc);assert.deepEqual(facts.materials,before.materials);assert.deepEqual(facts.textures,before.textures);
 if(facts.triangles>budgets.triangles||facts.primitives>budgets.primitives) throw new Error('STOP: geometry budget exceeded before encoding '+JSON.stringify({triangles:facts.triangles,primitives:facts.primitives}));
 doc.createExtension(KHRDracoMeshCompression).setRequired(true).setEncoderOptions({method:KHRDracoMeshCompression.EncoderMethod.EDGEBREAKER,encodeSpeed:5,decodeSpeed:5,quantizationBits:{POSITION:16,NORMAL:10,TEXCOORD:14,COLOR:10,GENERIC:12}});
 const bytes=await io.writeBinary(doc);const report=await validate(bytes,io);
 report.contract=await checkContract(await io.readBinary(bytes),stage); report.errors.push(...report.contract.errors); report.passed=report.errors.length===0;
 report.stage=stage;report.consolidation=consolidation;report.texturePayloadsUnchanged=true;
 report.preEncodeNonConsoleBaselineExact=before.nodes.filter(n=>!n.name.startsWith('GEO_Console_')).every(n=>JSON.stringify(n)===JSON.stringify(facts.nodes.find(m=>m.name===n.name)));
 assert.ok(report.preEncodeNonConsoleBaselineExact);
 await save(`reports/${stage}/${kind}.json`,report);
 if(!report.passed) throw new Error('STOP: candidate rejected '+JSON.stringify(report.errors));
 await save(`exports/${stage}/${kind}.glb`,bytes);
 reports.push({kind,triangles:report.triangles,primitives:report.primitives,materials:report.materials.length,bytes:report.bytes,passed:report.passed});
}
await save(`reports/${stage}/baseline-hashes.json`,await guard());console.log(JSON.stringify(reports,null,2));

