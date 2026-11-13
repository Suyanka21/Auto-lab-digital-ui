export type MaterialId = 'classic' | 'diamond-quilted' | 'perforated';

export type ColourId = 'exclusive-black' | 'sienna-brown' | 'light-ivory';

export type ThreadId = 'amber-ochre' | 'cyan' | 'warm-ivory' | 'tonal-charcoal';

export type CompositionId = 'single-colour' | 'two-tone';

export type TrimId = 'carbon-fibre' | 'poplar-wood' | 'walnut-wood' | 'piano-lacquer';

export type IlluminationId = 'cyan' | 'amber' | 'rose' | 'ocean' | 'champagne';

export type CameraId = 'driver-hero' | 'cabin-pair' | 'cockpit-dash' | 'stitch-detail';

export type ConfigurationStepId =
  | 'material'
  | 'colour'
  | 'thread'
  | 'composition'
  | 'trim'
  | 'illumination';

export type OfferingClassification = 'sample' | 'illustrative';

export type AppRoute = 'landing' | 'studio';

export interface CabinConfiguration {
  material: MaterialId;
  primaryColour: ColourId;
  secondaryColour?: ColourId;
  accentThread: ThreadId;
  composition: CompositionId;
  trim?: TrimId;
  ambientIllumination?: IlluminationId;
  activeCamera: CameraId;
}

export interface CabinViewerProps {
  material: MaterialId;
  primaryColour: ColourId;
  secondaryColour?: ColourId;
  accentThread: ThreadId;
  composition: CompositionId;
  trim?: TrimId;
  ambientIllumination?: IlluminationId;
  activeCamera: CameraId;
}

export interface OptionMetadata<T extends string> {
  id: T;
  label: string;
  description: string;
  classification: OfferingClassification;
  swatchHex?: string;
}

export interface ConfigurationStepMeta {
  id: ConfigurationStepId;
  index: string;
  label: string;
  classification: OfferingClassification;
  summary: string;
}

export interface CameraOptionMeta {
  id: CameraId;
  index: string;
  label: string;
  focusDescription: string;
}
