import { MeshPhysicalMaterial, RepeatWrapping, SRGBColorSpace, type MeshStandardMaterial, type Texture } from 'three';
import { DEFAULT_TRIM_ID } from '../trim-specification';
import assets from '../../config/trim-preview-assets.json';

export type TrimMaps = Record<keyof typeof assets, Texture>;
const finishRoles = {
  'open-pore-poplar': 'poplar', 'open-pore-walnut': 'walnut', 'piano-lacquer-flowing-lines': 'lacquer',
} as const;
type FinishId = keyof typeof finishRoles;
const originals = new WeakMap<MeshStandardMaterial, {
  map: Texture | null; normalMap: Texture | null; roughnessMap: Texture | null; metalnessMap: Texture | null;
  normalX: number; normalY: number;
}>();

/** Mutate the one shared insert material; never recolour dashboard leather or cup wells. */
export function applyCabinTrim(material: MeshStandardMaterial, requested: string, maps: TrimMaps, environment: Texture | null = null) {
  if (!originals.has(material)) originals.set(material, {
    map: material.map, normalMap: material.normalMap, roughnessMap: material.roughnessMap, metalnessMap: material.metalnessMap,
    normalX: material.normalScale.x, normalY: material.normalScale.y,
  });
  const original = originals.get(material)!;
  const role = Object.hasOwn(finishRoles, requested) ? finishRoles[requested as FinishId] : null;
  const id = role ? requested : DEFAULT_TRIM_ID;
  const nextMap = role ? maps[role] : original.map;
  const nextNormal = role === 'lacquer' ? null : role ? maps.normal : original.normalMap;
  const nextRoughness = role ? null : original.roughnessMap;
  const nextMetalness = role ? null : original.metalnessMap;
  const topologyChanged = Boolean(material.normalMap) !== Boolean(nextNormal)
    || Boolean(material.map) !== Boolean(nextMap) || Boolean(material.roughnessMap) !== Boolean(nextRoughness)
    || Boolean(material.metalnessMap) !== Boolean(nextMetalness) || material.envMap !== environment;
  material.map = nextMap;
  material.normalMap = nextNormal;
  material.roughnessMap = nextRoughness;
  material.metalnessMap = nextMetalness;
  material.color.set('#ffffff');
  material.normalScale.set(role ? 1 : original.normalX, role ? 1 : original.normalY);
  material.metalness = 0;
  material.roughness = role === 'lacquer' ? .23 : role ? .5 : .36;
  // Restrain the broad room highlight that previously obscured the dark weave.
  material.envMapIntensity = role ? .45 : .28;
  // Three r186 WebGLRenderer overrides envMapIntensity with scene.environmentIntensity
  // when material.envMap is null. Share the existing PMREM explicitly; no extra map/context.
  material.envMap = environment;
  if (material instanceof MeshPhysicalMaterial) {
    material.clearcoat = role === 'lacquer' ? .5 : role ? .08 : .5;
    material.clearcoatRoughness = .25;
  }
  material.userData.trimPreview = id;
  if (topologyChanged) material.needsUpdate = true;
}

/** One bounded set of four KTX maps, decoded by the existing renderer-owned loader. */
export function createTrimMaps(load: (url: string) => Promise<Texture>) {
  let pending: Promise<void> | undefined;
  let maps: TrimMaps | undefined;
  let failure: Error | undefined;
  let retired = false;
  let retirement: ReturnType<typeof setTimeout> | undefined;
  const owned = new Set<Texture>();
  const dispose = () => { retired = true; owned.forEach(texture => texture.dispose()); owned.clear(); };
  return {
    acquire() { if (retirement) clearTimeout(retirement); },
    release() { retirement = setTimeout(dispose, 0); },
    read(): TrimMaps {
      if (failure) throw failure;
      if (maps) return maps;
      if (!pending) pending = Promise.all(Object.entries(assets).map(async ([role, asset]) => {
        const texture = await load(import.meta.env.BASE_URL + asset.url.replace(/^\//, ""));
        if (retired || failure) { texture.dispose(); throw new Error('Trim preview load cancelled'); }
        owned.add(texture);
        // Existing carbon UVs represent 44.8mm. These veneers use a 448mm tile.
        texture.wrapS = texture.wrapT = RepeatWrapping;
        texture.repeat.set(.1,.1);
        texture.flipY = false;
        if (role !== 'normal') texture.colorSpace = SRGBColorSpace;
        texture.needsUpdate = true;
        return [role,texture] as const;
      })).then(entries => { maps = Object.fromEntries(entries) as TrimMaps; }).catch(error => {
        failure = new Error(`Cabin trim textures could not load: ${error instanceof Error ? error.message : String(error)}`);
        owned.forEach(texture => texture.dispose()); owned.clear();
      });
      throw pending;
    },
  };
}
