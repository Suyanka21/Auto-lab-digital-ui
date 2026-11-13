import { describe, expect, it } from "vitest";
import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS, KHRMaterialsClearcoat } from "@gltf-transform/extensions";
import { createLexusSyntheticFixture } from "../scripts/make-fixture.mjs";
import { validateGlbBytes } from "../scripts/validate-glb.mjs";
import { readFileSync } from "node:fs";

const components = ["Body", "Selector", "Cupholder_Front", "Cupholder_Rear", "Armrest"];
async function fixture(omit?: string, extraBinding = false) {
  const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
  const doc = await io.readBinary(await createLexusSyntheticFixture());
  const source = doc.getRoot().listMeshes()[0].listPrimitives()[0];
  const black = doc.createMaterial("MAT_Console_Black").setRoughnessFactor(.42).setMetallicFactor(0);
  const carbon = doc.createMaterial("MAT_Console_Carbon").setRoughnessFactor(.28).setMetallicFactor(0)
    .setNormalTexture(doc.getRoot().listMaterials()[0].getNormalTexture())
    .setExtension("KHR_materials_clearcoat", doc.createExtension(KHRMaterialsClearcoat).createClearcoat().setClearcoatFactor(.85).setClearcoatRoughnessFactor(.12));
  const metal = doc.createMaterial("MAT_Console_Metal").setRoughnessFactor(.3).setMetallicFactor(.7);
  doc.getRoot().listNodes().find(n => n.getName() === "GEO_Dashboard_Lexus")!.getMesh()!.addPrimitive(source.clone().setMaterial(carbon));
  for (const component of components) {
    if (component === omit) continue;
    const mesh = doc.createMesh();
    const mats = ["Body", "Selector"].includes(component) ? [black, carbon, metal] : component === "Armrest" ? [black] : [black, metal];
    for (const mat of mats) mesh.addPrimitive(source.clone().setMaterial(extraBinding ? doc.getRoot().listMaterials()[0] : mat));
    doc.getRoot().listScenes()[0].addChild(doc.createNode("GEO_Console_" + component).setMesh(mesh));
  }
  return io.writeBinary(doc);
}

describe("complete front cabin gate", () => {
  it.each(["classic", "diamond", "perforated"])("validates the delivered %s assembly without a waiver or budget increase", async kind => {
    const bytes = readFileSync(`public/assets/3d/lexus-rx350/interior-l4-${kind}.glb`);
    const report = await validateGlbBytes(bytes, { scope: "lexus-front-cabin" });
    expect(report.passed, report.errors.join("; ")).toBe(true);
    expect(report.nodeCount).toBe(11);
    expect(report.materialCount).toBe(10);
    expect(report.waivers).toEqual([]);
    expect(report.triangleCount).toBeLessThanOrEqual(80_000);
    expect(report.drawCalls).toBeLessThanOrEqual(24);
    expect(report.fileSizeBytes).toBeLessThanOrEqual(5_242_880);
  });
  it("requires the console on the new scope while keeping the historic gate usable", async () => {
    const bytes = await createLexusSyntheticFixture();
    expect((await validateGlbBytes(bytes, { scope: "lexus", synthetic: true })).passed).toBe(true);
    const report = await validateGlbBytes(bytes, { scope: "lexus-front-cabin", synthetic: true });
    expect(report.passed).toBe(false);
    expect(report.errors.join("; ")).toContain("missing node: GEO_Console_Body");
  });
  it("accepts all declared console components and fixed materials", async () => {
    const report = await validateGlbBytes(await fixture(), { scope: "lexus-front-cabin", synthetic: true });
    expect(report.passed, report.errors.join("; ")).toBe(true);
  });
  it.each(components)("rejects the missing %s component", async name => {
    const report = await validateGlbBytes(await fixture(name), { scope: "lexus-front-cabin", synthetic: true });
    expect(report.errors.join("; ")).toContain("missing node: GEO_Console_" + name);
  });
  it("rejects accidental customer upholstery binding on the fixed console", async () => {
    const report = await validateGlbBytes(await fixture(undefined, true), { scope: "lexus-front-cabin", synthetic: true });
    expect(report.errors.join("; ")).toContain("material binding mismatch: GEO_Console_");
  });
});
