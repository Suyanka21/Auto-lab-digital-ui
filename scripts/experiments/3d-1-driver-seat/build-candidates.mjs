// 3D-1 driver-seat experiment: builds scratch candidate GLBs from the production GLBs.
// Only GEO_Seat_Front_Driver and GEO_Seat_Stitching_Front are edited. Topology, UVs, vertex
// colours, materials and textures are kept, so the thread mask and KTX2 textures still apply.
// Output goes to reports/3d-1/candidates/ (git-ignored). Production files are never written.
// Usage (repository root): node scripts/experiments/3d-1-driver-seat/build-candidates.mjs
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS, KHRDracoMeshCompression } from '@gltf-transform/extensions';
import draco from 'draco3dgltf';
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { deformBackrest, jacobian, transformDirection, transformNormal } from './seat-profile.mjs';

export const EDITED_NODES = ['GEO_Seat_Front_Driver', 'GEO_Seat_Stitching_Front'];
export const KINDS = ['classic', 'diamond', 'perforated'];
// Same Draco settings as the production finalize step (3D-0 report, section 2).
const DRACO = { method: KHRDracoMeshCompression.EncoderMethod.EDGEBREAKER, encodeSpeed: 5, decodeSpeed: 5,
  quantizationBits: { POSITION: 16, NORMAL: 10, TEXCOORD: 14, COLOR: 10, GENERIC: 12 } };
// Measured on the production mesh: the backrest shell is the only seat part spanning this height.
const BACKREST_SPAN_Y = [0.5, 1.0];
// Stitches above this height belong to the headrest, which is not edited.
const STITCH_MAX_Y = 1.07;
const STITCH_MAX_Z = -0.15;
const WELD = 2e-5;

/** Labels vertices by connected part, joining vertices that share a position. */
function components(position, indices) {
  const count = position.getCount(), parent = new Int32Array(count).map((_, i) => i), seen = new Map(), p = [0, 0, 0];
  const find = (i) => { while (parent[i] !== i) { parent[i] = parent[parent[i]]; i = parent[i]; } return i; };
  const union = (a, b) => { parent[find(a)] = find(b); };
  for (let i = 0; i < count; i++) {
    position.getElement(i, p);
    const key = p.map((v) => Math.round(v / WELD)).join(',');
    if (seen.has(key)) union(i, seen.get(key)); else seen.set(key, i);
  }
  const idx = indices.getArray();
  for (let i = 0; i < idx.length; i += 3) { union(idx[i], idx[i + 1]); union(idx[i], idx[i + 2]); }
  return (i) => find(i);
}

function deformVertices(prim, selected) {
  const position = prim.getAttribute('POSITION'), normal = prim.getAttribute('NORMAL'), tangent = prim.getAttribute('TANGENT');
  const p = [0, 0, 0], n = [0, 0, 0], t = [0, 0, 0, 0];
  let moved = 0, maxMove = 0;
  for (let i = 0; i < position.getCount(); i++) {
    if (!selected(i)) continue;
    position.getElement(i, p);
    const q = deformBackrest(p), J = jacobian(p);
    const move = Math.hypot(q[0] - p[0], q[1] - p[1], q[2] - p[2]);
    if (move > 0) moved++;
    maxMove = Math.max(maxMove, move);
    position.setElement(i, q);
    if (normal) normal.setElement(i, transformNormal(J, normal.getElement(i, n)));
    if (tangent) { tangent.getElement(i, t); tangent.setElement(i, [...transformDirection(J, t), t[3]]); }
  }
  return { moved, maxMove };
}

/** Applies the experiment to a decoded production document and returns per-primitive statistics. */
export function applyDriverSeatExperiment(doc) {
  const stats = [];
  for (const node of doc.getRoot().listNodes()) {
    if (!EDITED_NODES.includes(node.getName())) continue;
    const prims = node.getMesh().listPrimitives();
    if (node.getName() === 'GEO_Seat_Front_Driver') {
      // The insert and bolster primitives share seam positions, so parts are found across both.
      const roots = new Map(), spans = new Map();
      prims.forEach((prim, k) => {
        const position = prim.getAttribute('POSITION'), find = components(position, prim.getIndices()), p = [0, 0, 0];
        for (let i = 0; i < position.getCount(); i++) {
          position.getElement(i, p);
          const id = `${k}:${find(i)}`, span = spans.get(id) ?? [Infinity, -Infinity];
          spans.set(id, [Math.min(span[0], p[1]), Math.max(span[1], p[1])]);
        }
        roots.set(prim, (i) => `${k}:${find(i)}`);
      });
      // Backrest = shell spanning the backrest height, plus the insert island that lies inside that span.
      const isBackrestPart = (id) => { const [lo, hi] = spans.get(id); return (lo < BACKREST_SPAN_Y[0] && hi > BACKREST_SPAN_Y[1]) || (lo > BACKREST_SPAN_Y[0] && hi < 1.03 && hi > 0.9); };
      for (const prim of prims) {
        const root = roots.get(prim);
        stats.push({ node: node.getName(), material: prim.getMaterial().getName(), vertices: prim.getAttribute('POSITION').getCount(), ...deformVertices(prim, (i) => isBackrestPart(root(i))) });
      }
    } else {
      for (const prim of prims) {
        // Each stitch is its own tiny part; it follows the backrest when its centre is on the backrest.
        const position = prim.getAttribute('POSITION'), find = components(position, prim.getIndices()), sum = new Map(), p = [0, 0, 0];
        for (let i = 0; i < position.getCount(); i++) {
          position.getElement(i, p);
          const s = sum.get(find(i)) ?? [0, 0, 0]; s[0] += p[1]; s[1] += p[2]; s[2]++; sum.set(find(i), s);
        }
        const onBackrest = (i) => { const s = sum.get(find(i)); return s[0] / s[2] < STITCH_MAX_Y && s[1] / s[2] < STITCH_MAX_Z; };
        stats.push({ node: node.getName(), material: prim.getMaterial().getName(), vertices: position.getCount(), ...deformVertices(prim, onBackrest) });
      }
    }
  }
  return stats;
}

export async function createIO() {
  return new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({
    'draco3d.decoder': await draco.createDecoderModule(), 'draco3d.encoder': await draco.createEncoderModule() });
}

/** Production GLB bytes in, candidate GLB bytes out: the exact path used for the candidate files. */
export async function buildCandidateBytes(io, sourceBytes) {
  const doc = await io.readBinary(sourceBytes);
  const stats = applyDriverSeatExperiment(doc);
  doc.getRoot().listExtensionsUsed().find((e) => e.extensionName === 'KHR_draco_mesh_compression').setEncoderOptions(DRACO);
  return { bytes: await io.writeBinary(doc), stats };
}

async function main() {
  const out = resolve('reports/3d-1/candidates');
  await mkdir(out, { recursive: true });
  const io = await createIO(), records = [];
  for (const kind of KINDS) {
    const source = `public/assets/3d/lexus-rx350/interior-l4-${kind}.glb`;
    const sourceBytes = await readFile(source);
    const { bytes, stats } = await buildCandidateBytes(io, sourceBytes), target = resolve(out, `interior-l4-${kind}.glb`);
    await writeFile(target, bytes);
    records.push({ kind, source, sourceSha256: createHash('sha256').update(sourceBytes).digest('hex'), sourceBytes: sourceBytes.length,
      candidate: `reports/3d-1/candidates/interior-l4-${kind}.glb`, candidateSha256: createHash('sha256').update(bytes).digest('hex'), candidateBytes: bytes.length, stats });
  }
  await writeFile(resolve(out, 'build.json'), JSON.stringify(records, null, 2) + '\n');
  console.log(JSON.stringify(records, null, 2));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await main();
