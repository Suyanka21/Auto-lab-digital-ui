import { navigateRadio } from './radio-navigation';
import { Check } from 'lucide-react';
import { COLOUR_OPTIONS } from '@/src/data/catalog';
import type { ColourId, CompositionId } from '@/src/types/configuration';

export interface ColourSelectorProps {
  primaryColour: ColourId;
  secondaryColour?: ColourId;
  composition: CompositionId;
  onPrimaryChange: (colour: ColourId) => void;
  onSecondaryChange: (colour: ColourId) => void;
  onCompositionChange: (composition: CompositionId) => void;
}

export function ColourSelector({
  primaryColour,
  secondaryColour,
  composition,
  onPrimaryChange,
  onSecondaryChange,
  onCompositionChange,
}: ColourSelectorProps) {
  return (
    <div className="space-y-6" data-component="ColourSelector">
      {/* Primary Hide Colour */}
      <div className="space-y-2.5">
        <div className="flex items-baseline justify-between gap-2">
          <span className="text-[11px] font-medium uppercase tracking-[0.12em] text-ink">
            Primary Colour
          </span>
          <span className="text-[11px] text-muted-grey">Sample hide palette</span>
        </div>

        <div role="radiogroup" onKeyDown={navigateRadio} aria-label="Primary hide colour" className="space-y-2">
          {COLOUR_OPTIONS.map((option) => {
            const isSelected = option.id === primaryColour;
            return (
              <button
                key={option.id}
                type="button"
                role="radio"
                aria-checked={isSelected}
              tabIndex={isSelected ? 0 : -1}
                onClick={() => onPrimaryChange(option.id)}
                className={`w-full min-h-[54px] px-3.5 py-2.5 text-left rounded-[2px] border transition-colors duration-150 cursor-pointer flex items-center justify-between gap-3 ${
                  isSelected
                    ? 'border-cyan-ink bg-ivory'
                    : 'border-fine-border bg-paper hover:border-ink'
                }`}
              >
                <span className="flex items-center gap-3 min-w-0">
                  <span
                    aria-hidden="true"
                    className="w-8 h-8 rounded-[2px] border border-fine-border shrink-0"
                    style={{ backgroundColor: option.swatchHex }}
                  />
                  <span className="min-w-0">
                    <span className="block text-[14px] font-medium text-ink">
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

      {/* Secondary Hide Colour (Two-Tone Zoning) */}
      <div className="space-y-2.5 border-t border-fine-border pt-4">
        <div className="flex items-center justify-between gap-2">
          <div>
            <span className="block text-[11px] font-medium uppercase tracking-[0.12em] text-ink">
              Secondary Colour
            </span>
            <span className="block text-[12px] leading-[1.4] text-muted-grey">
              {composition === 'two-tone'
                ? 'Applied to bolsters, headrests and steering leather.'
                : 'Available when Two-tone composition is active.'}
            </span>
          </div>

          <button
            type="button"
            onClick={() =>
              onCompositionChange(
                composition === 'two-tone' ? 'single-colour' : 'two-tone'
              )
            }
            aria-pressed={composition === 'two-tone'}
            className={`min-h-[44px] px-3.5 py-2 text-[11px] font-medium uppercase tracking-[0.08em] rounded-[2px] border transition-colors duration-150 cursor-pointer whitespace-nowrap shrink-0 ${
              composition === 'two-tone'
                ? 'border-cyan-ink bg-cyan-ink text-paper'
                : 'border-fine-border bg-paper text-ink hover:border-ink'
            }`}
          >
            {composition === 'two-tone' ? 'Two-tone On' : 'Enable Two-tone'}
          </button>
        </div>

        {composition === 'two-tone' && (
          <div role="radiogroup" onKeyDown={navigateRadio} aria-label="Secondary hide colour" className="space-y-2 pt-1">
            {COLOUR_OPTIONS.map((option) => {
              const isSelected = option.id === secondaryColour;
              const matchesPrimary = option.id === primaryColour;
              return (
                <button
                  key={option.id}
                  type="button"
                  role="radio"
                  aria-checked={isSelected}
              tabIndex={isSelected ? 0 : -1}
                  disabled={matchesPrimary}
                  aria-disabled={matchesPrimary || undefined}
                  onClick={() => onSecondaryChange(option.id)}
                  className={`w-full min-h-[48px] px-3.5 py-2 text-left rounded-[2px] border transition-colors duration-150 flex items-center justify-between gap-3 ${
                    matchesPrimary
                      ? 'border-fine-border bg-paper/60 opacity-60 cursor-not-allowed'
                      : isSelected
                        ? 'border-cyan-ink bg-ivory cursor-pointer'
                        : 'border-fine-border bg-paper hover:border-ink cursor-pointer'
                  }`}
                >
                  <span className="flex items-center gap-3 min-w-0">
                    <span
                      aria-hidden="true"
                      className="w-7 h-7 rounded-[2px] border border-fine-border shrink-0"
                      style={{ backgroundColor: option.swatchHex }}
                    />
                    <span className="min-w-0">
                      <span className="block text-[13px] font-medium text-ink">
                        {option.label}
                        {matchesPrimary && (
                          <span className="ml-1.5 text-[11px] font-normal text-muted-grey">
                            (Assigned as primary)
                          </span>
                        )}
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
        )}
      </div>
    </div>
  );
}
