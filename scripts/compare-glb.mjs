// Structural diff of two GLBs: proves whether a rebuild matches a baseline beyond its SHA-256.
import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS } from "@gltf-transform/extensions";
import draco3d from "draco3dgltf";
import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";

const SOUP_QUANTUM_METRES = 1e-4;
const sha = (data) => createHash("sha256").update(data).digest("hex");

async function createIO() {
  return new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({
    "draco3d.decoder": await draco3d.createDecoderModule(),
  });
}

function maxAbsDelta(a, b) {
  if (!a || !b || a.length !== b.length) return null;
  let max = 0;
  for (let i = 0; i < a.length; i++) max = Math.max(max, Math.abs(a[i] - b[i]));
  return max;
}

// Draco may renumber vertices, so equivalence is tested on an order-free triangle soup.
// Each triangle is rotated to start at its smallest corner, keeping winding (face orientation) significant.
function triangleSoupHash(positions, uvs, indices, quantum) {
  if (!positions) return null;
  const q = (v) => Math.round(v / quantum);
  const corner = (i) => [q(positions[i * 3]), q(positions[i * 3 + 1]), q(positions[i * 3 + 2]),
    ...(uvs ? [q(uvs[i * 2]), q(uvs[i * 2 + 1])] : [])].join(",");
  const index = indices ?? Array.from({ length: positions.length / 3 }, (_, i) => i);
  const triangles = [];
  for (let t = 0; t < index.length; t += 3) {
    const c = [corner(index[t]), corner(index[t + 1]), corner(index[t + 2])];
    const start = c.indexOf([...c].sort()[0]);
    triangles.push([c[start], c[(start + 1) % 3], c[(start + 2) % 3]].join("|"));
  }
  return sha(triangles.sort().join("\n"));
}

// Compares the material exactly as written in the GLB JSON, with texture indices replaced by names.
function materialSummary(json, material) {
  const textureName = (index) => {
    const texture = json.textures?.[index] ?? {};
    const source = texture.source ?? texture.extensions?.KHR_texture_basisu?.source;
    return texture.name ?? json.images?.[source]?.name ?? `texture:${index}`;
  };
  const canonical = (value, key = "") => {
    if (Array.isArray(value)) return value.map((item) => canonical(item));
    if (!value || typeof value !== "object") return value;
    const named = Number.isInteger(value.index) && /Texture$/.test(key) ? { ...value, index: textureName(value.index) } : value;
    return Object.fromEntries(Object.keys(named).sort().map((k) => [k, canonical(named[k], k)]));
  };
  return canonical(material);
}

function glbJson(bytes) {
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  return JSON.parse(new TextDecoder().decode(bytes.subarray(20, 20 + view.getUint32(12, true))));
}

function inspect(doc, json) {
  const root = doc.getRoot();
  const primitives = [];
  for (const node of root.listNodes()) {
    const mesh = node.getMesh();
    if (!mesh) continue;
    mesh.listPrimitives().forEach((primitive, index) => {
      const attributes = {};
      for (const semantic of primitive.listSemantics()) attributes[semantic] = primitive.getAttribute(semantic).getArray();
      primitives.push({
        key: `${node.getName()}#${index}`,
        material: primitive.getMaterial()?.getName() ?? null,
        vertices: primitive.getAttribute("POSITION")?.getCount() ?? 0,
        triangles: (primitive.getIndices()?.getCount() ?? primitive.getAttribute("POSITION")?.getCount() ?? 0) / 3,
        attributes,
        indices: primitive.getIndices()?.getArray() ?? null,
        soup: triangleSoupHash(attributes.POSITION, null, primitive.getIndices()?.getArray(), SOUP_QUANTUM_METRES),
        soupWithUv: triangleSoupHash(attributes.POSITION, attributes.TEXCOORD_0, primitive.getIndices()?.getArray(), SOUP_QUANTUM_METRES),
      });
    });
  }
  return {
    nodes: root.listNodes().map((n) => n.getName()).sort(),
    transforms: Object.fromEntries(root.listNodes().map((n) => [n.getName(), n.getWorldMatrix().map((v) => Number(v.toFixed(6)))])),
    materials: Object.fromEntries((json.materials ?? []).map((m, i) => [m.name ?? `material:${i}`, materialSummary(json, m)])),
    textures: Object.fromEntries(root.listTextures().map((t) => [t.getName(), { mime: t.getMimeType(), bytes: t.getImage()?.byteLength ?? 0, sha256: sha(t.getImage() ?? new Uint8Array()) }])),
    extensions: root.listExtensionsUsed().map((e) => e.extensionName).sort(),
    primitives,
  };
}

export async function compareGlbBytes(baselineBytes, candidateBytes) {
  const io = await createIO();
  const [baseline, candidate] = [new Uint8Array(baselineBytes), new Uint8Array(candidateBytes)];
  const a = inspect(await io.readBinary(baseline), glbJson(baseline));
  const b = inspect(await io.readBinary(candidate), glbJson(candidate));
  const primitiveDiffs = [];
  const candidateByKey = new Map(b.primitives.map((p) => [p.key, p]));
  for (const base of a.primitives) {
    const cand = candidateByKey.get(base.key);
    if (!cand) { primitiveDiffs.push({ key: base.key, missing: true }); continue; }
    const attributeDelta = {};
    for (const semantic of new Set([...Object.keys(base.attributes), ...Object.keys(cand.attributes)])) {
      attributeDelta[semantic] = maxAbsDelta(base.attributes[semantic], cand.attributes[semantic]);
    }
    const indicesEqual = (!base.indices && !cand.indices) || (base.indices && cand.indices && base.indices.length === cand.indices.length
      && base.indices.every((v, i) => v === cand.indices[i]));
    const same = base.material === cand.material && base.vertices === cand.vertices && base.triangles === cand.triangles
      && indicesEqual && Object.values(attributeDelta).every((d) => d === 0);
    if (!same) primitiveDiffs.push({ key: base.key, geometryEquivalent: base.soup === cand.soup, uvEquivalent: base.soupWithUv === cand.soupWithUv, material: [base.material, cand.material], vertices: [base.vertices, cand.vertices], triangles: [base.triangles, cand.triangles], indicesEqual, attributeDelta });
  }
  for (const cand of b.primitives) if (!a.primitives.some((p) => p.key === cand.key)) primitiveDiffs.push({ key: cand.key, extra: true });
  const textureDiffs = [];
  for (const name of new Set([...Object.keys(a.textures), ...Object.keys(b.textures)])) {
    const [x, y] = [a.textures[name], b.textures[name]];
    if (!x || !y || x.sha256 !== y.sha256) textureDiffs.push({ name, baseline: x ?? null, candidate: y ?? null });
  }
  const transformDiffs = [];
  for (const name of new Set([...Object.keys(a.transforms), ...Object.keys(b.transforms)])) {
    if (JSON.stringify(a.transforms[name]) !== JSON.stringify(b.transforms[name])) transformDiffs.push({ name, baseline: a.transforms[name] ?? null, candidate: b.transforms[name] ?? null });
  }
  const materialDiffs = [];
  for (const name of new Set([...Object.keys(a.materials), ...Object.keys(b.materials)])) {
    if (JSON.stringify(a.materials[name]) !== JSON.stringify(b.materials[name])) materialDiffs.push({ name, baseline: a.materials[name] ?? null, candidate: b.materials[name] ?? null });
  }
  return {
    byteIdentical: sha(baselineBytes) === sha(candidateBytes),
    baseline: { sha256: sha(baselineBytes), bytes: baselineBytes.length },
    candidate: { sha256: sha(candidateBytes), bytes: candidateBytes.length },
    nodesEqual: JSON.stringify(a.nodes) === JSON.stringify(b.nodes),
    extensionsEqual: JSON.stringify(a.extensions) === JSON.stringify(b.extensions),
    primitiveCount: [a.primitives.length, b.primitives.length],
    primitiveDiffs, transformDiffs, materialDiffs, textureDiffs,
  };
}

async function main() {
  const [baseline, candidate, ...rest] = process.argv.slice(2);
  if (!baseline || !candidate || baseline === "--help") {
    console.log("Usage: node scripts/compare-glb.mjs <baseline.glb> <candidate.glb> [--report out.json]");
    process.exitCode = baseline === "--help" ? 0 : 2;
    return;
  }
  const report = await compareGlbBytes(await readFile(resolve(baseline)), await readFile(resolve(candidate)));
  const reportIndex = rest.indexOf("--report");
  if (reportIndex >= 0) await writeFile(resolve(rest[reportIndex + 1]), `${JSON.stringify(report, null, 2)}\n`);
  console.log(JSON.stringify({
    byteIdentical: report.byteIdentical, baseline: report.baseline, candidate: report.candidate,
    nodesEqual: report.nodesEqual, extensionsEqual: report.extensionsEqual, primitiveCount: report.primitiveCount,
    primitiveDiffs: report.primitiveDiffs.length,
    geometryNotEquivalent: report.primitiveDiffs.filter((d) => !d.geometryEquivalent).map((d) => d.key),
    uvNotEquivalent: report.primitiveDiffs.filter((d) => !d.uvEquivalent).map((d) => d.key),
    transformDiffs: report.transformDiffs.map((d) => d.name),
    materialDiffs: report.materialDiffs.map((d) => d.name),
    textureDiffs: report.textureDiffs.map((d) => d.name),
  }, null, 2));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await main();
