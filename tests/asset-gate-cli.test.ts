import { describe, expect, it } from "vitest";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS } from "@gltf-transform/extensions";
import { compareGlbBytes } from "../scripts/compare-glb.mjs";
import { createLexusSyntheticFixture } from "../scripts/make-fixture.mjs";

async function mutated(change: (doc: Awaited<ReturnType<NodeIO["readBinary"]>>) => void) {
  const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
  const base = await createLexusSyntheticFixture();
  const doc = await io.readBinary(base);
  change(doc);
  return [base, await io.writeBinary(doc)] as const;
}

const glb = (kind: string) => `public/assets/3d/lexus-rx350/interior-l4-${kind}.glb`;
const run = (args: string[]) => spawnSync(process.execPath, ["scripts/validate-glb.mjs", ...args], { encoding: "utf8", timeout: 120_000 });

describe("asset gate CLI", () => {
  it("passes the shipped classic GLB with no arguments other than a report path", () => {
    const dir = mkdtempSync(join(tmpdir(), "gate-"));
    try {
      const result = run(["--report", join(dir, "report.json")]);
      expect(result.status, result.stderr).toBe(0);
      expect(result.stdout).toContain("Asset gate PASS: 11 nodes, 66260 triangles, 24 draw calls");
      const report = JSON.parse(readFileSync(join(dir, "report.json"), "utf8"));
      expect(report.scope).toBe("lexus-front-cabin");
      expect(report.sha256).toBe("e5bdde016348df34889ec4c0ff0e406caad7e368504308bd5a4f5b725a55c056");
    } finally { rmSync(dir, { recursive: true, force: true }); }
  });
  it("prints usage for --help", () => {
    const result = run(["--help"]);
    expect(result.status).toBe(0);
    expect(result.stdout).toContain("Usage: node scripts/validate-glb.mjs");
  });
  it("fails loudly on an S-Class scope whose inputs are not in this repository", () => {
    const dir = mkdtempSync(join(tmpdir(), "gate-"));
    try {
      const result = run(["--scope", "full", "--report", join(dir, "report.json")]);
      expect(result.status).toBe(1);
      expect(result.stderr).toContain('Scope "full" is not available in this repository');
    } finally { rmSync(dir, { recursive: true, force: true }); }
  });
});

describe("GLB structural comparison", () => {
  it("reports a node moved by its transform", async () => {
    const [base, cand] = await mutated(doc => doc.getRoot().listNodes().find(n => n.getMesh())!.setTranslation([0.01, 0, 0]));
    const report = await compareGlbBytes(base, cand);
    expect(report.nodesEqual).toBe(true);
    expect(report.transformDiffs.length).toBeGreaterThan(0);
  });
  it("reports a changed material parameter", async () => {
    const [base, cand] = await mutated(doc => doc.getRoot().listMaterials()[0].setEmissiveFactor([0.5, 0, 0]));
    expect((await compareGlbBytes(base, cand)).materialDiffs.length).toBe(1);
  });
  it("treats reversed winding as a geometry change", async () => {
    const [base, cand] = await mutated(doc => {
      const indices = doc.getRoot().listMeshes().flatMap(m => m.listPrimitives()).find(p => p.getIndices())!.getIndices()!;
      const array = indices.getArray()!.slice();
      for (let t = 0; t < array.length; t += 3) [array[t + 1], array[t + 2]] = [array[t + 2], array[t + 1]];
      indices.setArray(array);
    });
    const report = await compareGlbBytes(base, cand);
    expect(report.primitiveDiffs.some((d: { geometryEquivalent?: boolean }) => d.geometryEquivalent === false)).toBe(true);
  });
  it("reports a delivered GLB as identical to itself", async () => {
    const bytes = readFileSync(glb("classic"));
    const report = await compareGlbBytes(bytes, bytes);
    expect(report.byteIdentical).toBe(true);
    expect(report.primitiveDiffs).toEqual([]);
    expect(report.textureDiffs).toEqual([]);
  });
  it("separates shared seat textures from treatment-specific ones", async () => {
    const report = await compareGlbBytes(readFileSync(glb("classic")), readFileSync(glb("diamond")));
    expect(report.byteIdentical).toBe(false);
    expect(report.nodesEqual).toBe(true);
    expect(report.primitiveDiffs).toEqual([]);
    expect(report.textureDiffs.map((d: { name: string }) => d.name).sort()).toEqual(["lexus-insert-base", "lexus-insert-normal", "lexus-insert-orm"]);
  });
});

it("keeps the shipped GLBs at their baseline hashes", () => {
  const expected = {
    classic: "e5bdde016348df34889ec4c0ff0e406caad7e368504308bd5a4f5b725a55c056",
    diamond: "4c217dd00d86d8bae3925d735beddb63b225d24c5f1bafd60726f501bfcba8ad",
    perforated: "d53f55546232db473ecadee08be9bff6454b5d3a510ee30e88415f2477ca9f9e",
  };
  for (const [kind, sha] of Object.entries(expected)) {
    expect(createHash("sha256").update(readFileSync(glb(kind))).digest("hex")).toBe(sha);
  }
});
