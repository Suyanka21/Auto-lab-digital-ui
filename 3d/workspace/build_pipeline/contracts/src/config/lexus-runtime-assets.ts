// Content versions prevent an existing browser's immutable, console-free GLB
// cache from winning after a cabin update. The regression test checks each
// version against the actual file: refresh these hashes whenever assets change.
const revisions = {
  classic: 'e5bdde016348df34889ec4c0ff0e406caad7e368504308bd5a4f5b725a55c056',
  diamond: '4c217dd00d86d8bae3925d735beddb63b225d24c5f1bafd60726f501bfcba8ad',
  perforated: 'd53f55546232db473ecadee08be9bff6454b5d3a510ee30e88415f2477ca9f9e',
} as const;

export const LEXUS_L4_ASSET_URLS = {
  classic: `${import.meta.env.BASE_URL}assets/3d/lexus-rx350/interior-l4-classic.glb?v=${revisions.classic}`,
  diamond: `${import.meta.env.BASE_URL}assets/3d/lexus-rx350/interior-l4-diamond.glb?v=${revisions.diamond}`,
  perforated: `${import.meta.env.BASE_URL}assets/3d/lexus-rx350/interior-l4-perforated.glb?v=${revisions.perforated}`,
} as const;
