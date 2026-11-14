import { navigateRadio } from './radio-navigation';
import { Check } from 'lucide-react';
import { COLOUR_OPTIONS, COMPOSITION_OPTIONS } from '@/src/data/catalog';
import type { ColourId, CompositionId } from '@/src/types/configuration';

export interface CompositionSelectorProps {
  value: CompositionId;
  primaryColour: ColourId;
  secondaryColour?: ColourId;
  onChange: (composition: CompositionId) => void;
}

function SeatZoneDiagram({
  mode,
  primaryHex,
  secondaryHex,
}: {
  mode: CompositionId;
  primaryHex: string;
  secondaryHex: string;
}) {
  const bolsterFill = mode === 'two-tone' ? secondaryHex : primaryHex;
  return (
    <svg
      width="44"
      height="52"
      viewBox="0 0 44 52"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      className="shrink-0"
    >
      {/* Headrest */}
      <rect
        x="14"
        y="3"
        width="16"
        height="9"
        rx="2"
        fill={bolsterFill}
        stroke="#65615B"
        strokeWidth="1"
      />
      {/* Outer bolsters */}
      <rect
        x="7"
        y="15"
        width="30"
        height="22"
        rx="3"
        fill={bolsterFill}
        stroke="#65615B"
        strokeWidth="1"
      />
      {/* Central insert */}
      <rect
        x="13"
        y="17"
        width="18"
        height="18"
        rx="1.5"
        fill={primaryHex}
        stroke="#65615B"
        strokeWidth="0.75"
      />
      {/* Lower cushion */}
      <rect
        x="7"
        y="40"
        width="30"
        height="9"
        rx="2"
        fill={bolsterFill}
        stroke="#65615B"
        strokeWidth="1"
      />
      <rect
        x="13"
        y="41.5"
        width="18"
        height="6"
        rx="1"
        fill={primaryHex}
        stroke="#65615B"
        strokeWidth="0.75"
      />
    </svg>
  );
}

export function CompositionSelector({
  value,
  primaryColour,
  secondaryColour,
  onChange,
}: CompositionSelectorProps) {
  const primaryMeta = COLOUR_OPTIONS.find((c) => c.id === primaryColour);
  const secondaryMeta = COLOUR_OPTIONS.find((c) => c.id === secondaryColour);
  const primaryHex = primaryMeta?.swatchHex ?? '#191A1E';
  const secondaryHex = secondaryMeta?.swatchHex ?? '#7B4A2D';

  return (
    <div className="space-y-4" data-component="CompositionSelector">
      <div role="radiogroup" onKeyDown={navigateRadio} aria-label="Upholstery composition" className="space-y-2.5">
        {COMPOSITION_OPTIONS.map((option) => {
          const isSelected = option.id === value;
          return (
            <button
              key={option.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              tabIndex={isSelected ? 0 : -1}
              onClick={() => onChange(option.id)}
              className={`w-full min-h-[82px] p-3.5 text-left rounded-[2px] border transition-colors duration-150 cursor-pointer flex items-start justify-between gap-3.5 ${
                isSelected
                  ? 'border-cyan-ink bg-ivory'
                  : 'border-fine-border bg-paper hover:border-ink'
              }`}
            >
              <span className="flex items-start gap-3.5 min-w-0">
                <SeatZoneDiagram
                  mode={option.id}
                  primaryHex={primaryHex}
                  secondaryHex={secondaryHex}
                />
                <span className="space-y-1 min-w-0">
                  <span className="block text-[14px] font-medium text-ink">
                    {option.label}
                  </span>
                  <span className="block text-[12px] leading-[1.5] text-muted-grey">
                    {option.description}
                  </span>
                </span>
              </span>

              <span
                aria-hidden="true"
                className={`mt-1 w-5 h-5 rounded-full border flex items-center justify-center shrink-0 ${
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

      {/* Explicit Surface Mapping Guide */}
      <div className="border-t border-fine-border pt-3 space-y-1.5 text-[12px]">
        <p className="font-medium text-ink">Surface zoning</p>
        <p className="text-muted-grey leading-[1.5]">
          {value === 'two-tone'
            ? `Seat centres remain ${primaryMeta?.label ?? 'Primary'}; bolsters, headrests and steering leather switch to ${secondaryMeta?.label ?? 'Secondary'}. Dashboard and console keep their existing finishes.`
            : `Seat centres, bolsters, headrests and steering leather share ${primaryMeta?.label ?? 'Primary'}. Dashboard and console keep their existing finishes.`}
        </p>
      </div>
    </div>
  );
}
