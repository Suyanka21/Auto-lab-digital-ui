import { describe, it, expect } from 'vitest';
import { DEFAULT_CONFIGURATION } from '../src/data/catalog';
import { mapConfigurationToRuntime } from '../src/viewer/configuration-adapter';

describe('configuration to real cabin', () => {
  it('starts with Driver Hero and leaves source cockpit/console colours fixed', () => {
    const result = mapConfigurationToRuntime(DEFAULT_CONFIGURATION);
    expect(result.view).toBe('hero_driver');
    expect(result.primaryHex).toBe('#191A1E');
    expect(result.secondaryHex).toBe(result.primaryHex);
    expect(result.steeringHex).toBe(result.secondaryHex);
    expect(result.trimHex).toBe('#2A2B2E');
    expect(result.cockpitBlackHex).toBe('#121316');
    expect(result.trimId).toBe('autolab-twill-carbon');
  });
  it('maps single colour to both seats even with stale secondary input', () => {
    const value = mapConfigurationToRuntime({ ...DEFAULT_CONFIGURATION, secondaryColour: 'light-ivory' });
    expect(value.secondaryHex).toBe(value.primaryHex);
  });
  it('maps two-tone inserts and bolsters independently, with steering following bolsters', () => {
    const value = mapConfigurationToRuntime({ ...DEFAULT_CONFIGURATION, composition: 'two-tone', primaryColour: 'sienna-brown', secondaryColour: 'light-ivory' });
    expect(value.primaryHex).toBe('#7B4A2D');
    expect(value.secondaryHex).toBe('#DDD5C7');
    expect(value.steeringHex).toBe('#DDD5C7');
    expect(value.trimHex).toBe('#2A2B2E');
  });
  it('safely renders an incomplete two-tone selection without an invented colour', () => {
    const value = mapConfigurationToRuntime({ ...DEFAULT_CONFIGURATION, composition: 'two-tone', secondaryColour: undefined });
    expect(value.secondaryHex).toBe(value.primaryHex);
  });
  it.each([['classic','classic'],['diamond-quilted','diamond'],['perforated','perforated']] as const)('maps treatment %s', (material, treatment) => {
    expect(mapConfigurationToRuntime({ ...DEFAULT_CONFIGURATION, material }).treatment).toBe(treatment);
  });
  it.each([['driver-hero','hero_driver'],['cabin-pair','cabin_pair'],['cockpit-dash','driver_cockpit'],['stitch-detail','seam_macro']] as const)('maps camera %s', (activeCamera, view) => {
    expect(mapConfigurationToRuntime({ ...DEFAULT_CONFIGURATION, activeCamera }).view).toBe(view);
  });
  it('carries thread, trim and ambient sample values without changing leather', () => {
    const value = mapConfigurationToRuntime({ ...DEFAULT_CONFIGURATION, accentThread: 'warm-ivory', trim: 'walnut-wood', ambientIllumination: 'amber' });
    expect(value.threadHex).toBe('#EAE4D7');
    expect(value.trimId).toBe('open-pore-walnut');
    expect(value.ambientHex).toBe('#D8964B');
    expect(value.primaryHex).toBe('#191A1E');
  });
});
