import {root,kinds,guard,createIO,inspect,validate,save,outputPath} from './common.mjs';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
const io=await createIO(); const before=await guard(); const reports=[];
await assert.rejects(()=>outputPath('production_baseline/overwrite.glb'));
await assert.rejects(()=>outputPath('../escape.glb'));
await assert.rejects(()=>io.readBinary(new Uint8Array([0,1,2,3])));
for (const kind of kinds) {
 const bytes=await readFile(resolve(root,`production_baseline/interior-l4-${kind}.glb`));
 const doc=await io.readBinary(bytes); const source=inspect(doc);
 const report=await validate(bytes,io);
 await save(`reports/pipeline/${kind}-baseline.json`,report);
 if(!report.passed) throw new Error(`${kind} baseline fails: ${report.errors}`);
 // Independent preservation probe: lossless decoded export, original KTX2 payloads.
 for(const ext of [...doc.getRoot().listExtensionsUsed()]) if(ext.extensionName==='KHR_draco_mesh_compression') ext.dispose();
 const decoded=await io.writeBinary(doc);
 const roundtrip=inspect(await io.readBinary(decoded));
 assert.deepEqual(roundtrip,source,'decoded roundtrip changes attributes, indices, transforms or texture bytes');
 await save(`working_models/pipeline-probe-${kind}.glb`,decoded);
 // Review-output export exercises the safe path without re-encoding the accepted assets.
 await save(`exports/pipeline-probe/${kind}.glb`,bytes);
 reports.push({kind,baselinePassed:report.passed,triangles:report.triangles,primitives:report.primitives,bytes:report.bytes,decodedRoundtripExact:true,decodedBytes:decoded.length,warningCount:report.khronos.issues.numWarnings});
}
const result={purpose:'Pipeline proof only; no cabin geometry added',before,after:await guard(),negativeTests:['protected baseline output rejected','workspace escape rejected','malformed GLB rejected'],reports};
await save('reports/pipeline/proof.json',result); console.log(JSON.stringify(result,null,2));
