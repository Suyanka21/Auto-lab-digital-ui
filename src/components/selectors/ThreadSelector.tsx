import { Check } from 'lucide-react';
import { THREAD_OPTIONS } from '@/src/data/catalog';
import type { ThreadId } from '@/src/types/configuration';

export interface ThreadSelectorProps {
  value: ThreadId;
  onChange: (thread: ThreadId) => void;
}

export function ThreadSelector({ value, onChange }: ThreadSelectorProps) {
  return (
    <div className="space-y-3" data-component="ThreadSelector">
      <div className="flex items-baseline justify-between gap-2">
        <span className="text-[11px] font-medium uppercase tracking-[0.12em] text-ink">
          Seam Stitch Colour
        </span>
        <span className="text-[11px] text-muted-grey">Bolsters &amp; console seams</span>
      </div>

      <div role="radiogroup" aria-label="Accent thread colour" className="space-y-2">
        {THREAD_OPTIONS.map((option) => {
          const isSelected = option.id === value;
          return (
            <button
              key={option.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              onClick={() => onChange(option.id)}
              className={`w-full min-h-[56px] px-3.5 py-2.5 text-left rounded-[2px] border transition-colors duration-150 cursor-pointer flex items-center justify-between gap-3 ${
                isSelected
                  ? 'border-cyan-ink bg-ivory'
                  : 'border-fine-border bg-paper hover:border-ink'
              }`}
            >
              <span className="flex items-center gap-3.5 min-w-0">
                {/* Tactile double-stitch sample over dark leather plate */}
                <span
                  aria-hidden="true"
                  className="w-11 h-8 rounded-[2px] bg-graphite border border-[#2A2B30] flex flex-col justify-center gap-1 px-1.5 shrink-0"
                >
                  <span
                    className="block w-full h-0 border-t-2 border-dashed"
                    style={{ borderColor: option.swatchHex }}
                  />
                  <span
                    className="block w-full h-0 border-t-2 border-dashed"
                    style={{ borderColor: option.swatchHex }}
                  />
                </span>

                <span className="min-w-0">
                  <span className="block text-[14px] font-medium text-ink">
                    {option.label}
                  </span>
                  <span className="block text-[12px] text-muted-grey">
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
