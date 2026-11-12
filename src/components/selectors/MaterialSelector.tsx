import { Check, ChevronLeft, ChevronRight } from 'lucide-react';
import classicLeatherImg from '@/src/assets/images/autolab_material_classic_1794511172047.jpg';
import diamondQuiltedImg from '@/src/assets/images/autolab_material_diamond_quilted_1794511173024.jpg';
import perforatedLeatherImg from '@/src/assets/images/autolab_material_leather_1794510358246.jpg';
import { MATERIAL_OPTIONS } from '@/src/data/catalog';
import type { MaterialId } from '@/src/types/configuration';

export interface MaterialSelectorProps {
  value: MaterialId;
  onChange: (material: MaterialId) => void;
}

const MATERIAL_MEDIA: Record<MaterialId, { src: string; alt: string }> = {
  classic: {
    src: classicLeatherImg,
    alt: 'Smooth matte black Nappa leather with single-seam warm saddle stitching',
  },
  'diamond-quilted': {
    src: diamondQuiltedImg,
    alt: 'Padded diamond-quilted dark charcoal automotive leather seat insert',
  },
  perforated: {
    src: perforatedLeatherImg,
    alt: 'Micro-perforated sienna brown and black automotive leather bolster',
  },
};

export function MaterialSelector({ value, onChange }: MaterialSelectorProps) {
  const activeIndex = Math.max(
    0,
    MATERIAL_OPTIONS.findIndex((item) => item.id === value)
  );
  const activeMeta = MATERIAL_OPTIONS[activeIndex] ?? MATERIAL_OPTIONS[0];
  const media = MATERIAL_MEDIA[activeMeta.id];

  const cycleMaterial = (direction: -1 | 1) => {
    const nextIndex =
      (activeIndex + direction + MATERIAL_OPTIONS.length) % MATERIAL_OPTIONS.length;
    onChange(MATERIAL_OPTIONS[nextIndex].id);
  };

  return (
    <div className="space-y-4" data-component="MaterialSelector">
      {/* Mobile Reference 03 layout: Compact horizontal swatch + serif detail; Desktop Reference 02: Full-width tactile preview */}
      <div className="sm:hidden flex items-start gap-4">
        <div className="relative w-[136px] shrink-0 overflow-hidden rounded-[2px] border border-[#2A2B30] bg-graphite aspect-[4/3]">
          <img
            src={media.src}
            alt={media.alt}
            referrerPolicy="no-referrer"
            className="w-full h-full object-cover object-center"
          />
          <span className="absolute bottom-1.5 left-2 font-sans text-[10px] font-medium text-paper bg-[#101114]/75 px-1.5 py-0.5 tabular-nums">
            0{activeIndex + 1} / 0{MATERIAL_OPTIONS.length}
          </span>
        </div>

        <div className="flex-1 min-w-0 space-y-1.5">
          <span className="block w-5 h-[2px] bg-cyan" aria-hidden="true" />
          <p className="font-serif italic text-[22px] leading-[1.15] text-ink">
            {activeMeta.label}
          </p>
          <p className="text-[12px] leading-[1.45] text-muted-grey">
            {activeMeta.description}
          </p>
          <p className="text-[11px] text-muted-grey">Illustrative sample</p>
        </div>
      </div>

      {/* Desktop / Tablet Material Photograph */}
      <div className="hidden sm:block relative overflow-hidden rounded-[2px] border border-[#2A2B30] bg-graphite aspect-[16/10]">
        <img
          src={media.src}
          alt={media.alt}
          referrerPolicy="no-referrer"
          className="w-full h-full object-cover object-center transition-opacity duration-200"
        />
        <div
          aria-hidden="true"
          className="absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-[#101114]/90 to-transparent"
        />
        <div className="absolute inset-x-0 bottom-0 px-3.5 pb-2.5 flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="font-sans text-[11px] font-medium text-paper tabular-nums">
              0{activeIndex + 1} / 0{MATERIAL_OPTIONS.length}
            </span>
            <span className="text-[11px] text-[#B8B4AC]">· Illustrative sample</span>
          </div>
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => cycleMaterial(-1)}
              aria-label="Previous material"
              className="inline-flex items-center justify-center w-11 h-11 rounded-[2px] border border-[#3B3D45] bg-[#101114]/85 text-paper hover:border-cyan transition-colors duration-150 cursor-pointer"
            >
              <ChevronLeft className="w-4 h-4" aria-hidden="true" />
            </button>
            <button
              type="button"
              onClick={() => cycleMaterial(1)}
              aria-label="Next material"
              className="inline-flex items-center justify-center w-11 h-11 rounded-[2px] border border-[#3B3D45] bg-[#101114]/85 text-paper hover:border-cyan transition-colors duration-150 cursor-pointer"
            >
              <ChevronRight className="w-4 h-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>

      {/* Radio List of Confirmed Materials */}
      <div role="radiogroup" aria-label="Upholstery material" className="space-y-2">
        {MATERIAL_OPTIONS.map((option) => {
          const isSelected = option.id === value;
          return (
            <button
              key={option.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              onClick={() => onChange(option.id)}
              className={`w-full min-h-[48px] sm:min-h-[52px] px-3.5 py-2.5 sm:py-3 text-left rounded-[2px] border transition-colors duration-150 cursor-pointer flex items-start gap-3 ${
                isSelected
                  ? 'border-cyan-ink bg-ivory'
                  : 'border-fine-border bg-paper hover:border-ink'
              }`}
            >
              <span
                aria-hidden="true"
                className={`mt-0.5 w-4 h-4 rounded-full border flex items-center justify-center shrink-0 ${
                  isSelected ? 'border-cyan-ink bg-cyan-ink text-paper' : 'border-muted-grey'
                }`}
              >
                {isSelected && <Check className="w-2.5 h-2.5" strokeWidth={3} />}
              </span>
              <span className="space-y-0.5 min-w-0">
                <span className="block text-[14px] font-medium text-ink">
                  {option.label}
                </span>
                <span className="hidden sm:block text-[12px] leading-[1.45] text-muted-grey">
                  {option.description}
                </span>
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
