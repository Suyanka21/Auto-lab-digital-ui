import type {
  CabinConfiguration,
  CameraOptionMeta,
  ColourId,
  CompositionId,
  ConfigurationStepMeta,
  IlluminationId,
  MaterialId,
  OptionMetadata,
  ThreadId,
  TrimId,
} from '@/src/types/configuration';

export const MATERIAL_OPTIONS: OptionMetadata<MaterialId>[] = [
  {
    id: 'classic',
    label: 'Classic',
    description: 'An uninterrupted smooth grain where seam geometry and stitch lines take the lead.',
    classification: 'sample',
  },
  {
    id: 'diamond-quilted',
    label: 'Diamond Quilted',
    description: 'Structured geometric quilting across central seat inserts for depth and tactile support.',
    classification: 'sample',
  },
  {
    id: 'perforated',
    label: 'Perforated',
    description: 'Fine perforated texture across the central seat panels.',
    classification: 'sample',
  },
];

export const COLOUR_OPTIONS: OptionMetadata<ColourId>[] = [
  {
    id: 'exclusive-black',
    label: 'Exclusive Black',
    description: 'Deep charcoal-black hide with restrained tonal depth.',
    classification: 'sample',
    swatchHex: '#191A1E',
  },
  {
    id: 'sienna-brown',
    label: 'Sienna Brown',
    description: 'Warm saddle-brown leather with rich natural undertone.',
    classification: 'sample',
    swatchHex: '#7B4A2D',
  },
  {
    id: 'light-ivory',
    label: 'Light Ivory',
    description: 'Bright architectural stone hide for high-contrast cabins.',
    classification: 'sample',
    swatchHex: '#DDD5C7',
  },
];

export const THREAD_OPTIONS: OptionMetadata<ThreadId>[] = [
  {
    id: 'amber-ochre',
    label: 'Warm Ochre',
    description: 'Classic saddlery contrast stitch.',
    classification: 'sample',
    swatchHex: '#C8843F',
  },
  {
    id: 'cyan',
    label: 'Atelier Cyan',
    description: 'Signature technical contrast thread.',
    classification: 'sample',
    swatchHex: '#72C4E1',
  },
  {
    id: 'warm-ivory',
    label: 'Light Ivory',
    description: 'Crisp pale highlight along bolsters and armrests.',
    classification: 'sample',
    swatchHex: '#EAE4D7',
  },
  {
    id: 'tonal-charcoal',
    label: 'Tonal Charcoal',
    description: 'Subtle low-contrast structural stitching.',
    classification: 'sample',
    swatchHex: '#565860',
  },
];

export const COMPOSITION_OPTIONS: OptionMetadata<CompositionId>[] = [
  {
    id: 'single-colour',
    label: 'Single-colour',
    description: 'One colour across seat centres, bolsters, headrests and steering leather. Console remains black.',
    classification: 'sample',
  },
  {
    id: 'two-tone',
    label: 'Two-tone',
    description: 'Primary colour defines seat centres; secondary wraps bolsters, headrests and steering leather. Console remains black.',
    classification: 'sample',
  },
];

export const TRIM_OPTIONS: OptionMetadata<TrimId>[] = [
  {
    id: 'carbon-fibre',
    label: 'Carbon Fibre',
    description: 'Directional twill weave across dash fascia and console bridge.',
    classification: 'illustrative',
    swatchHex: '#23252A',
  },
  {
    id: 'poplar-wood',
    label: 'Poplar Wood',
    description: 'Open-pore pale grain veneer with matte architectural finish.',
    classification: 'illustrative',
    swatchHex: '#9C8368',
  },
  {
    id: 'walnut-wood',
    label: 'Walnut Wood',
    description: 'Deep figured walnut veneer with natural warm grain.',
    classification: 'illustrative',
    swatchHex: '#563724',
  },
  {
    id: 'piano-lacquer',
    label: 'Piano Lacquer',
    description: 'Mirror-smooth deep obsidian lacquer surface.',
    classification: 'illustrative',
    swatchHex: '#101114',
  },
];

export const ILLUMINATION_OPTIONS: OptionMetadata<IlluminationId>[] = [
  {
    id: 'cyan',
    label: 'Cyan',
    description: 'Cool cyan wash around the cabin.',
    classification: 'illustrative',
    swatchHex: '#72C4E1',
  },
  {
    id: 'amber',
    label: 'Amber',
    description: 'Warm amber wash around the cabin.',
    classification: 'illustrative',
    swatchHex: '#D8964B',
  },
  {
    id: 'rose',
    label: 'Rose',
    description: 'Soft evening copper-rose accent.',
    classification: 'illustrative',
    swatchHex: '#C98986',
  },
  {
    id: 'ocean',
    label: 'Ocean',
    description: 'Deep slate-blue architectural lighting.',
    classification: 'illustrative',
    swatchHex: '#3B6F8A',
  },
  {
    id: 'champagne',
    label: 'Champagne',
    description: 'Neutral warm-ivory interior wash.',
    classification: 'illustrative',
    swatchHex: '#D8C7A8',
  },
];

export const CAMERA_OPTIONS: CameraOptionMeta[] = [
  {
    id: 'driver-hero',
    index: '01',
    label: 'Driver Hero',
    focusDescription: 'Front three-quarter view prioritising seat upholstery and colour.',
  },
  {
    id: 'cabin-pair',
    index: '02',
    label: 'Cabin Pair',
    focusDescription: 'Elevated twin-seat composition highlighting bolster and insert geometry.',
  },
  {
    id: 'cockpit-dash',
    index: '03',
    label: 'Cockpit & Dash',
    focusDescription: 'Dashboard, steering and illustrative trim finishes.',
  },
  {
    id: 'stitch-detail',
    index: '04',
    label: 'Stitch Detail',
    focusDescription: 'Close-range inspection of grain, perforation, quilting, and thread tension.',
  },
];

export const CONFIGURATION_STEPS: ConfigurationStepMeta[] = [
  {
    id: 'material',
    index: '01',
    label: 'Material',
    classification: 'sample',
    summary: 'Select primary upholstery texture.',
  },
  {
    id: 'colour',
    index: '02',
    label: 'Colour',
    classification: 'sample',
    summary: 'Choose primary and optional secondary hide colours.',
  },
  {
    id: 'thread',
    index: '03',
    label: 'Accent Thread',
    classification: 'sample',
    summary: 'Specify seam stitch contrast.',
  },
  {
    id: 'composition',
    index: '04',
    label: 'Composition',
    classification: 'sample',
    summary: 'Assign single-colour or two-tone surface zoning.',
  },
  {
    id: 'trim',
    index: '05',
    label: 'Cabin Trim',
    classification: 'illustrative',
    summary: 'Illustrative preview of dash and console inlays.',
  },
  {
    id: 'illumination',
    index: '06',
    label: 'Ambient Light',
    classification: 'illustrative',
    summary: 'Illustrative coloured light wash; no installed LED strips.',
  },
];

export const DEFAULT_CONFIGURATION: CabinConfiguration = {
  material: 'classic',
  primaryColour: 'exclusive-black',
  secondaryColour: undefined,
  accentThread: 'amber-ochre',
  composition: 'single-colour',
  trim: 'carbon-fibre',
  ambientIllumination: 'cyan',
  activeCamera: 'driver-hero',
};
