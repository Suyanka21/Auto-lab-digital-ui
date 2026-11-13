import { describe, expect, it, vi } from 'vitest';
import { MeshPhysicalMaterial, Texture } from 'three';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import assets from '../src/config/trim-preview-assets.json';
import { applyCabinTrim, createTrimMaps, type TrimMaps } from '../src/lib/three/cabin-trim';

describe('shared decorative trim', () => {
  it('delivers four versioned 512px KTX2 files with mipmaps', () => {
    for(const asset of Object.values(assets)) {
      const bytes=readFileSync('public'+asset.url.split('?')[0]);
      expect(createHash('sha256').update(bytes).digest('hex')).toBe(asset.sha256);
      expect(asset.url).toContain('?v='+asset.sha256);
      expect(bytes.subarray(0,12).toString('hex')).toBe('ab4b5458203230bb0d0a1a0a');
      expect(bytes.readUInt32LE(20)).toBe(512);
      expect(bytes.readUInt32LE(24)).toBe(512);
      expect(bytes.readUInt32LE(40)).toBe(10);
    }
  });
  it('restores original carbon maps after repeated finish changes and unknown IDs', () => {
    const carbon = new MeshPhysicalMaterial({map:new Texture(),normalMap:new Texture(),roughnessMap:new Texture(),metalnessMap:new Texture()});
    carbon.normalScale.set(.45,.45);
    const originals = [carbon.map,carbon.normalMap,carbon.roughnessMap,carbon.metalnessMap];
    const maps: TrimMaps = {poplar:new Texture(),walnut:new Texture(),lacquer:new Texture(),normal:new Texture()};
    const environment = new Texture();
    for (let round=0;round<3;round++) {
      applyCabinTrim(carbon,'open-pore-walnut',maps,environment);
      expect(carbon.envMap).toBe(environment);
      expect(carbon.map).toBe(maps.walnut);
      expect(carbon.normalMap).toBe(maps.normal);
      expect(carbon.roughnessMap).toBeNull();
      applyCabinTrim(carbon,'piano-lacquer-flowing-lines',maps);
      expect(carbon.normalMap).toBeNull();
      applyCabinTrim(carbon,round===2?'__proto__':'autolab-twill-carbon',maps);
      expect([carbon.map,carbon.normalMap,carbon.roughnessMap,carbon.metalnessMap]).toEqual(originals);
      expect(carbon.normalScale.x).toBe(.45);
      expect(carbon.userData.trimPreview).toBe('autolab-twill-carbon');
    }
  });
  it('loads four maps once and disposes them after the owner releases', async () => {
    vi.useFakeTimers();
    const textures = Array.from({length:4},()=>new Texture());
    const disposed = textures.map(texture=>vi.spyOn(texture,'dispose'));
    let index=0;
    const load=vi.fn(async()=>textures[index++]);
    const resource=createTrimMaps(load);
    resource.acquire();
    let pending: unknown;
    try { resource.read(); } catch (value) { pending=value; }
    await pending;
    expect(resource.read().walnut).toBe(textures[1]);
    resource.read();
    expect(load).toHaveBeenCalledTimes(4);
    resource.release(); resource.acquire();
    vi.runAllTimers();
    expect(disposed[0]).not.toHaveBeenCalled();
    resource.release(); vi.runAllTimers();
    disposed.forEach(spy=>expect(spy).toHaveBeenCalledTimes(1));
    vi.useRealTimers();
  });
  it('surfaces failed texture loads instead of silently showing the wrong finish', async () => {
    const resource=createTrimMaps(async()=>{ throw new Error('503'); });
    let pending: unknown;
    try { resource.read(); } catch (value) { pending=value; }
    await pending;
    expect(()=>resource.read()).toThrow(/Cabin trim textures could not load: 503/);
  });
});
