// Read geometry only: Blender's importer does not support the shipped BasisU extension.
// No GLB is written. The temporary JSON is in Blender world axes, in metres.
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import draco from 'draco3dgltf';
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';

const source = new URL('../../public/assets/3d/lexus-rx350/interior-l4-classic.glb', import.meta.url);
const bytes = await readFile(source);
const hash = createHash('sha256').update(bytes).digest('hex');
if (hash !== 'e5bdde016348df34889ec4c0ff0e406caad7e368504308bd5a4f5b725a55c056') {
  throw new Error('Cabin changed: revisit the placement datum before comparing.');
}
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS)
  .registerDependencies({ 'draco3d.decoder': await draco.createDecoderModule() });
const doc = await io.readBinary(bytes);
const nodes = [];
for (const n of doc.getRoot().listNodes()) {
  if (!n.getMesh()) continue;
  const m = n.getWorldMatrix();
  const vertices = [], faces = [];
  for (const p of n.getMesh().listPrimitives()) {
    if (p.getMode() !== 4) throw new Error('Expected triangles');
    const pos = p.getAttribute('POSITION'), base = vertices.length;
    for (let i = 0; i < pos.getCount(); i++) {
      const [x, y, z] = pos.getElement(i, []);
      const w = [0, 1, 2].map(k => m[k]*x + m[k+4]*y + m[k+8]*z + m[k+12]);
      vertices.push([w[0], -w[2], w[1]]);
    }
    const idx = p.getIndices();
    for (let i = 0; i < (idx?.getCount() ?? pos.getCount()); i += 3) {
      faces.push([0, 1, 2].map(k => base + (idx ? idx.getScalar(i+k) : i+k)));
    }
  }
  nodes.push({ name: n.getName(), vertices, faces });
}
await writeFile(process.argv[2], JSON.stringify({ hash, nodes }), { flag: 'wx' });
