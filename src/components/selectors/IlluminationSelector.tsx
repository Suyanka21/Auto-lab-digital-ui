import { navigateRadio } from './radio-navigation';
import { Check } from 'lucide-react';
import { ILLUMINATION_OPTIONS } from '@/src/data/catalog';
import type { IlluminationId } from '@/src/types/configuration';

export interface IlluminationSelectorProps {
  value?: IlluminationId;
  onChange: (illumination: IlluminationId) => void;
}

export function IlluminationSelector({ value, onChange }: IlluminationSelectorProps) {
  const activeOption = ILLUMINATION_OPTIONS.find((o) => o.id === value) ?? ILLUMINATION_OPTIONS[0];

  return (
    <div className="space-y-4" data-component="IlluminationSelector">
      <div className="border-b border-fine-border pb-2.5 flex items-baseline justify-between gap-2">
        <span className="text-[11px] font-medium uppercase tracking-[0.12em] text-ink">
          Illustrative Preview
        </span>
        <span className="text-[11px] text-muted-grey">Visual direction only</span>
      </div>

      {/* Restrained Perimeter Light Line Preview on Graphite */}
      <div className="rounded-[2px] bg-graphite border border-[#2A2B30] p-4 space-y-2.5">
        <div className="flex items-center justify-between text-[11px] text-[#B8B4AC]">
          <span className="uppercase tracking-[0.12em]">Ambient Wash Tone</span>
          <span className="text-paper font-medium">{activeOption.label}</span>
        </div>
        <div className="h-[2px] w-full rounded-[2px] bg-[#22242A] overflow-hidden">
          <div
            className="h-full w-full transition-colors duration-200"
            style={{ backgroundColor: activeOption.swatchHex }}
          />
        </div>
      </div>

      <div
        role="radiogroup" onKeyDown={navigateRadio}
        aria-label="Ambient illumination mood (illustrative preview)"
        className="space-y-2"
      >
        {ILLUMINATION_OPTIONS.map((option) => {
          const isSelected = option.id === value;
          return (
            <button
              key={option.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              tabIndex={isSelected ? 0 : -1}
              onClick={() => onChange(option.id)}
              className={`w-full min-h-[50px] px-3.5 py-2.5 text-left rounded-[2px] border transition-colors duration-150 cursor-pointer flex items-center justify-between gap-3 ${
                isSelected
                  ? 'border-cyan-ink bg-ivory'
                  : 'border-fine-border bg-paper hover:border-ink'
              }`}
            >
              <span className="flex items-center gap-3 min-w-0">
                <span
                  aria-hidden="true"
                  className="w-8 h-6 rounded-[2px] bg-graphite border border-[#2A2B30] flex items-center justify-center px-1.5 shrink-0"
                >
                  <span
                    className="block w-full h-[3px] rounded-[1px]"
                    style={{ backgroundColor: option.swatchHex }}
                  />
                </span>
                <span className="min-w-0">
                  <span className="block text-[13px] font-medium text-ink">
                    {option.label}
                  </span>
                  <span className="block text-[12px] leading-[1.4] text-muted-grey">
                    {option.description}
                  </span>
                </span>
              </span>

              <span
                aria-hidden="true"
                className={`w-5 h-5 rounded-full border flex items-center justify-center shrink-0 ${
                  isSelected
                    ? 'border-cyan-ink bg-cyan-ink text-paper'
                    : 'border-fine-border'
                }`}
              >
                {isSelected && <Check className="w-3 h-3" strokeWidth={2.5} />}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
