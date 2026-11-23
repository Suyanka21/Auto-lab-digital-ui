import { COLOUR_OPTIONS, THREAD_OPTIONS, ILLUMINATION_OPTIONS } from '../data/catalog';
import type { CabinViewerProps, MaterialId, CameraId, TrimId } from '../types/configuration';
export type Treatment = 'classic' | 'diamond' | 'perforated';
export type RuntimeCamera = 'hero_driver' | 'cabin_pair' | 'driver_cockpit' | 'seam_macro';
const treatments: Record<MaterialId,Treatment> = { classic:'classic', 'diamond-quilted':'diamond', perforated:'perforated' };
const cameras: Record<CameraId,RuntimeCamera> = { 'driver-hero':'hero_driver', 'cabin-pair':'cabin_pair', 'cockpit-dash':'driver_cockpit', 'stitch-detail':'seam_macro' };
const trims: Record<TrimId,string> = { 'carbon-fibre':'autolab-twill-carbon', 'poplar-wood':'open-pore-poplar', 'walnut-wood':'open-pore-walnut', 'piano-lacquer':'piano-lacquer-flowing-lines' };
function hex(options: {id:string;swatchHex?:string}[], id: string | undefined, fallback: string) {
  return options.find(option=>option.id===id)?.swatchHex ?? fallback;
}
/** Translate UI IDs, never change GLB assignments or maintain a second configuration store. */
export function mapConfigurationToRuntime(value: CabinViewerProps) {
  const primaryHex = hex(COLOUR_OPTIONS,value.primaryColour,'#191A1E');
  const secondaryHex = value.composition==='two-tone' ? hex(COLOUR_OPTIONS,value.secondaryColour,primaryHex) : primaryHex;
  return {
    treatment: treatments[value.material] ?? 'classic', view: cameras[value.activeCamera] ?? 'hero_driver',
    primaryHex, secondaryHex, steeringHex: secondaryHex,
    threadHex: hex(THREAD_OPTIONS,value.accentThread,'#C8843F'),
    trimId: value.trim ? trims[value.trim] ?? 'autolab-twill-carbon' : 'autolab-twill-carbon',
    ambientHex: hex(ILLUMINATION_OPTIONS,value.ambientIllumination,'#72C4E1'),
    trimHex:'#2A2B2E', accentHex:'#787D82', cockpitBlackHex:'#121316',
  };
}
