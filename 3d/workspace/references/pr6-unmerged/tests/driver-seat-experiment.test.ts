import { describe, expect, it } from "vitest";
import type { Document, Primitive } from "@gltf-transform/core";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { applyDriverSeatExperiment, buildCandidateBytes, createIO, EDITED_NODES, KINDS } from "../scripts/experiments/3d-1-driver-seat/build-candidates.mjs";
import { deformBackrest, SEAT_CENTRE_X } from "../scripts/experiments/3d-1-driver-seat/seat-profile.mjs";

const assetPath = (kind: string) => `public/assets/3d/lexus-rx350/interior-l4-${kind}.glb`;
const digest = (array: ArrayLike<number> | null | undefined) => (array ? createHash("sha256").update(Buffer.from(Float32Array.from(array).buffer)).digest("hex") : null);
const snapshot = (doc: Document) => Object.fromEntries(doc.getRoot().listNodes().filter(n => n.getMesh()).map(node => [
  node.getName(),
  node.getMesh()!.listPrimitives().map((p: Primitive) => ({
    material: p.getMaterial()!.getName(),
    triangles: p.getIndices()!.getCount() / 3,
    indices: digest(p.getIndices()!.getArray()),
    attributes: Object.fromEntries(p.listSemantics().map(s => [s, digest(p.getAttribute(s)!.getArray())])),
  })),
]));

describe("3D-1 driver-seat displacement field", () => {
  it("leaves the cushion, plinth and seat centre line where they are", () => {
    const fixed: [number, number, number][] = [[0.6, 0.5, 0.1], [0.7, 0.35, 0], [SEAT_CENTRE_X, 0.9, -0.34], [0.492, 1.05, -0.435]];
    for (const point of fixed) {
      expect(deformBackrest(point)).toEqual(point);
    }
  });

  it("is mirror-symmetric about the seat centre and never folds the surface", () => {
    for (let y = 0.6; y <= 1.06; y += 0.02) {
      let previous = -Infinity;
      for (let a = 0; a <= 0.29; a += 0.005) {
        const right = deformBackrest([SEAT_CENTRE_X + a, y, -0.3]), left = deformBackrest([SEAT_CENTRE_X - a, y, -0.3]);
        expect(right[0] - SEAT_CENTRE_X).toBeCloseTo(SEAT_CENTRE_X - left[0], 9);
        expect(right[0]).toBeGreaterThanOrEqual(previous);
        previous = right[0];
      }
    }
  });

  it("narrows the mid-height bulge and widens the shoulders", () => {
    expect(deformBackrest([SEAT_CENTRE_X + 0.286, 0.86, -0.33])[0]).toBeLessThan(SEAT_CENTRE_X + 0.286);
    expect(deformBackrest([SEAT_CENTRE_X + 0.2257, 1.0, -0.42])[0]).toBeGreaterThan(SEAT_CENTRE_X + 0.2257);
  });
});

describe("3D-1 driver-seat candidate build", () => {
  it.each(KINDS)("changes only driver-seat positions, normals and tangents in %s", async kind => {
    const io = await createIO(), bytes = readFileSync(assetPath(kind));
    const before = snapshot(await io.readBinary(bytes));
    const doc = await io.readBinary(bytes);
    const stats = applyDriverSeatExperiment(doc);
    const after = snapshot(doc);

    expect(Object.keys(after)).toEqual(Object.keys(before));
    expect(stats.map(s => s.node)).toEqual(["GEO_Seat_Front_Driver", "GEO_Seat_Front_Driver", "GEO_Seat_Stitching_Front"]);
    for (const s of stats) expect(s.moved).toBeGreaterThan(0);
    for (const [name, primitives] of Object.entries(before)) {
      if (!EDITED_NODES.includes(name)) { expect(after[name]).toEqual(primitives); continue; }
      primitives.forEach((primitive, i) => {
        const candidate = after[name][i];
        expect(candidate.material).toBe(primitive.material);
        expect(candidate.triangles).toBe(primitive.triangles);
        expect(candidate.indices).toBe(primitive.indices);
        for (const [semantic, hash] of Object.entries(primitive.attributes)) {
          // UVs carry the thread-mask contract; vertex colours carry baked shading.
          if (["POSITION", "NORMAL", "TANGENT"].includes(semantic)) continue;
          expect(candidate.attributes[semantic]).toBe(hash);
        }
        expect(candidate.attributes.POSITION).not.toBe(primitive.attributes.POSITION);
      });
    }
  }, 60000);

  // Draco renumbers vertices, so the written file is checked per triangle, not per vertex.
  // UVs are compared as whole steps of a 14-bit grid, the precision they are stored at.
  const uvTriangles = (primitive: Primitive, min: number[], step: number[]) => {
    const uv = primitive.getAttribute("TEXCOORD_0")!, index = primitive.getIndices()!.getArray()!, keys: string[] = [];
    const corner = (i: number) => { const [u, v] = uv.getElement(i, [0, 0]); return `${Math.round((u - min[0]) / step[0])}:${Math.round((v - min[1]) / step[1])}`; };
    for (let i = 0; i < index.length; i += 3) {
      const c = [corner(index[i]), corner(index[i + 1]), corner(index[i + 2])];
      // Draco may rotate a triangle's corners; take the smallest rotation so equal corners cannot change the key.
      keys.push([0, 1, 2].map(r => [c[r], c[(r + 1) % 3], c[(r + 2) % 3]].join("|")).sort()[0]);
    }
    return keys.sort();
  };

  it.each(KINDS)("keeps every triangle's UVs in the written %s candidate file", async kind => {
    const io = await createIO(), bytes = readFileSync(assetPath(kind));
    const production = await io.readBinary(bytes);
    const written = await io.readBinary((await buildCandidateBytes(io, bytes)).bytes);
    const meshes = (doc: Document) => doc.getRoot().listNodes().filter(n => n.getMesh());
    expect(meshes(written).map(n => n.getName())).toEqual(meshes(production).map(n => n.getName()));
    meshes(production).forEach((node, n) => {
      const candidates = meshes(written)[n].getMesh()!.listPrimitives();
      node.getMesh()!.listPrimitives().forEach((primitive, i) => {
        expect(candidates[i].getMaterial()!.getName()).toBe(primitive.getMaterial()!.getName());
        expect(candidates[i].getIndices()!.getCount()).toBe(primitive.getIndices()!.getCount());
        if (!EDITED_NODES.includes(node.getName())) return;
        const uv = primitive.getAttribute("TEXCOORD_0")!, min = uv.getMin([0, 0]), max = uv.getMax([0, 0]);
        const size = Math.max(max[0] - min[0], max[1] - min[1]) / 16383, step = [size, size];
        expect(uvTriangles(candidates[i], min, step)).toEqual(uvTriangles(primitive, min, step));
      });
    });
  }, 120000);
});
