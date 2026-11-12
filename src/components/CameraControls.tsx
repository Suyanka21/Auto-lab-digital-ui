import { CAMERA_OPTIONS } from '@/src/data/catalog';
import type { CameraId } from '@/src/types/configuration';

export interface CameraControlsProps {
  activeCamera: CameraId;
  onSelectCamera: (camera: CameraId) => void;
}

/**
 * Integrated stage camera switcher positioned along the base of the Graphite viewer.
 * Preserves clear numbered states and keyboard/touch accessibility without faking 3D orbit.
 */
export function CameraControls({ activeCamera, onSelectCamera }: CameraControlsProps) {
  return (
    <div
      className="bg-graphite border-t border-[#26282E] px-2 sm:px-4"
      data-component="CameraControls"
      role="group"
      aria-label="Cabin camera viewpoints"
    >
      <div className="grid grid-cols-2 sm:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-[#26282E]">
        {CAMERA_OPTIONS.map((cam) => {
          const isSelected = cam.id === activeCamera;
          return (
            <button
              key={cam.id}
              type="button"
              onClick={() => onSelectCamera(cam.id)}
              aria-pressed={isSelected}
              className={`relative min-h-[44px] px-3 py-2 text-left transition-colors duration-150 focus-visible:outline-offset-[-2px] cursor-pointer flex items-center sm:flex-col sm:items-start sm:justify-center gap-2 sm:gap-0.5 ${
                isSelected
                  ? 'text-paper bg-[#17191E]'
                  : 'text-[#9A968E] hover:text-paper hover:bg-[#14161A]'
              }`}
            >
              <span className="font-sans text-[10px] font-medium tracking-[0.1em] tabular-nums text-[#8E8A82] shrink-0">
                {cam.index}
              </span>
              <span className="text-[12px] sm:text-[13px] font-medium whitespace-nowrap truncate">
                {cam.label}
              </span>
              {isSelected && (
                <span
                  aria-hidden="true"
                  className="absolute bottom-0 left-0 right-0 h-[2px] bg-cyan"
                />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
