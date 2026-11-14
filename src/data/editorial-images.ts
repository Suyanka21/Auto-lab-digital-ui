import cover from '@/src/assets/editorial/atelier-cover.webp';
import classic from '@/src/assets/editorial/classic-study.webp';
import diamond from '@/src/assets/editorial/diamond-study.webp';
import perforated from '@/src/assets/editorial/perforated-study.webp';
import trims from '@/src/assets/editorial/trim-studies.webp';
import type { MaterialId, TrimId } from '@/src/types/configuration';

/** AI-generated editorial studies only. Never used as model textures or colour specifications. */
export const EDITORIAL_IMAGES = { cover, classic, diamond, perforated, trims };
export const MATERIAL_STUDIES: Record<MaterialId, string> = { classic, 'diamond-quilted': diamond, perforated };
export const TRIM_STUDY_POSITION: Record<TrimId, string> = {
  'poplar-wood': '0%', 'walnut-wood': '33.333%', 'piano-lacquer': '66.667%', 'carbon-fibre': '100%',
};
