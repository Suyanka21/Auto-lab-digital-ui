import { navigateRadio } from './radio-navigation';
import { Check } from 'lucide-react';
import carbonFibreImg from '@/src/assets/images/autolab_trim_carbon_fibre_1794511173303.jpg';
import pianoLacquerImg from '@/src/assets/images/autolab_trim_piano_lacquer_1794511174129.jpg';
import poplarWoodImg from '@/src/assets/images/autolab_trim_poplar_wood_1794511173150.jpg';
import walnutWoodImg from '@/src/assets/images/autolab_trim_walnut_wood_1794511174478.jpg';
import { TRIM_OPTIONS } from '@/src/data/catalog';
import type { TrimId } from '@/src/types/configuration';

export interface TrimSelectorProps {
  value?: TrimId;
  onChange: (trim: TrimId) => void;
}

const TRIM_MEDIA: Record<TrimId, { src: string; alt: string }> = {
  'carbon-fibre': {
    src: carbonFibreImg,
    alt: 'Directional 2x2 twill carbon-fibre automotive trim swatch',
  },
  'poplar-wood': {
    src: poplarWoodImg,
    alt: 'Open-pore pale poplar wood grain automotive trim veneer',
  },
  'walnut-wood': {
    src: walnutWoodImg,
    alt: 'Rich figured dark walnut wood automotive trim veneer',
  },
  'piano-lacquer': {
    src: pianoLacquerImg,
    alt: 'High-gloss obsidian piano lacquer console inlay panel',
  },
};

export function TrimSelector({ value, onChange }: TrimSelectorProps) {
  return (
    <div className="space-y-3.5" data-component="TrimSelector">
      <div className="border-b border-fine-border pb-2.5 flex items-baseline justify-between gap-2">
        <span className="text-[11px] font-medium uppercase tracking-[0.12em] text-ink">
          Illustrative Preview
        </span>
        <span className="text-[11px] text-muted-grey">Visual direction only</span>
      </div>

      <div role="radiogroup" onKeyDown={navigateRadio} aria-label="Cabin trim finish (illustrative preview)" className="grid grid-cols-2 gap-2.5">
        {TRIM_OPTIONS.map((option) => {
          const isSelected = option.id === value;
          const media = TRIM_MEDIA[option.id];
          return (
            <button
              key={option.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              tabIndex={isSelected ? 0 : -1}
              onClick={() => onChange(option.id)}
              className={`group text-left rounded-[2px] overflow-hidden border transition-colors duration-150 cursor-pointer flex flex-col ${
                isSelected
                  ? 'border-cyan-ink ring-1 ring-cyan-ink bg-ivory'
                  : 'border-fine-border bg-paper hover:border-ink'
              }`}
            >
              <div className="relative aspect-[4/3] w-full bg-graphite overflow-hidden">
                <img
                  src={media.src}
                  alt={media.alt}
                  referrerPolicy="no-referrer"
                  className="w-full h-full object-cover object-center transition-transform duration-300 group-hover:scale-[1.03]"
                />
                {isSelected && (
                  <span
                    aria-hidden="true"
                    className="absolute top-2 right-2 w-5 h-5 rounded-full bg-cyan-ink text-paper border border-paper/45 flex items-center justify-center"
                  >
                    <Check className="w-3 h-3" strokeWidth={2.5} />
                  </span>
                )}
              </div>

              <div className="p-3 space-y-1 flex-1">
                <span className="block text-[13px] font-medium text-ink">
                  {option.label}
                </span>
                <span className="block text-[12px] leading-[1.4] text-muted-grey">
                  {option.description}
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
