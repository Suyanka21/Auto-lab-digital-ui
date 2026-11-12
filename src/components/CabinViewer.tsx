import {
  CAMERA_OPTIONS,
  COLOUR_OPTIONS,
  ILLUMINATION_OPTIONS,
  MATERIAL_OPTIONS,
  THREAD_OPTIONS,
  TRIM_OPTIONS,
} from '@/src/data/catalog';
import driverHeroImg from '@/src/assets/images/autolab_hero_cabin_1794510358513.jpg';
import cabinPairImg from '@/src/assets/images/autolab_camera_cabin_pair_1794510798594.jpg';
import cockpitDashImg from '@/src/assets/images/autolab_camera_cockpit_dash_1794510798204.jpg';
import stitchDetailImg from '@/src/assets/images/autolab_camera_stitch_detail_1794510798794.jpg';
import type { CabinViewerProps, CameraId } from '@/src/types/configuration';

const CAMERA_MEDIA: Record<CameraId, { src: string; alt: string }> = {
  'driver-hero': {
    src: driverHeroImg,
    alt: 'Driver Hero illustrative perspective from behind the front seats looking forward across the cabin',
  },
  'cabin-pair': {
    src: cabinPairImg,
    alt: 'Cabin Pair illustrative perspective showcasing both front seats, bolsters, and centre armrest',
  },
  'cockpit-dash': {
    src: cockpitDashImg,
    alt: 'Cockpit & Dash illustrative perspective focusing on the steering wheel, dash inlay, and console',
  },
  'stitch-detail': {
    src: stitchDetailImg,
    alt: 'Stitch Detail illustrative macro view of automotive leather grain and double-row saddle stitching',
  },
};

function labelOf<T extends string>(list: { id: T; label: string }[], id?: T): string {
  if (!id) return 'None';
  return list.find((item) => item.id === id)?.label ?? id;
}

/**
 * Replaceable CabinViewer component.
 * Receives strictly typed presentation props (CabinViewerProps).
 * Contains zero configuration business logic and makes no assumptions about a 3D engine.
 * Future engineering agents can replace this component with AutoLab's Three.js / R3F stage.
 */
export function CabinViewer({
  material,
  primaryColour,
  secondaryColour,
  accentThread,
  composition,
  trim,
  ambientIllumination,
  activeCamera,
}: CabinViewerProps) {
  const cameraMeta = CAMERA_OPTIONS.find((c) => c.id === activeCamera) ?? CAMERA_OPTIONS[0];
  const materialLabel = labelOf(MATERIAL_OPTIONS, material);
  const primaryMeta = COLOUR_OPTIONS.find((c) => c.id === primaryColour);
  const secondaryMeta = secondaryColour
    ? COLOUR_OPTIONS.find((c) => c.id === secondaryColour)
    : undefined;
  const threadMeta = THREAD_OPTIONS.find((t) => t.id === accentThread);
  const trimLabel = trim ? labelOf(TRIM_OPTIONS, trim) : null;
  const lightMeta = ILLUMINATION_OPTIONS.find((i) => i.id === ambientIllumination);

  const colourSummary =
    composition === 'two-tone' && secondaryMeta
      ? `${primaryMeta?.label ?? primaryColour} + ${secondaryMeta.label}`
      : (primaryMeta?.label ?? primaryColour);

  return (
    <div
      className="relative w-full aspect-[4/3] sm:aspect-[16/9] bg-graphite overflow-hidden select-none"
      data-component="CabinViewer"
      data-camera={activeCamera}
    >
      {/* Cross-fading curated studio camera perspectives */}
      {(Object.keys(CAMERA_MEDIA) as CameraId[]).map((camId) => {
        const media = CAMERA_MEDIA[camId];
        const isActive = camId === activeCamera;
        return (
          <img
            key={camId}
            src={media.src}
            alt={media.alt}
            referrerPolicy="no-referrer"
            aria-hidden={!isActive}
            className={`absolute inset-0 w-full h-full object-cover object-center transition-opacity duration-300 ease-out ${
              isActive ? 'opacity-100 z-0' : 'opacity-0 pointer-events-none'
            }`}
          />
        );
      })}

      {/* Measured top & bottom contrast scrims for legible HUD labels */}
      <div
        aria-hidden="true"
        className="absolute inset-x-0 top-0 h-16 bg-gradient-to-b from-[#101114]/85 via-[#101114]/35 to-transparent z-10 pointer-events-none"
      />
      <div
        aria-hidden="true"
        className="absolute inset-x-0 bottom-0 h-22 bg-gradient-to-t from-[#101114]/92 via-[#101114]/45 to-transparent z-10 pointer-events-none"
      />

      {/* Top Overlay Metadata */}
      <div className="absolute inset-x-0 top-0 z-20 px-4 sm:px-6 pt-3.5 sm:pt-4 flex items-center justify-between gap-4">
        <div className="flex items-center gap-2 text-[11px] tracking-[0.14em] uppercase text-[#E5E1D8] min-w-0">
          <span className="whitespace-nowrap">Your Interior</span>
          <span aria-hidden="true" className="text-[#8E8A82]">·</span>
          <span className="text-[#B8B4AC] truncate">Illustrative · Not 3D</span>
        </div>

        <span className="text-[12px] font-medium text-cyan whitespace-nowrap">
          {cameraMeta.label}
        </span>
      </div>

      {/* Bottom Overlay Live Configuration Swatch Strip & Readout */}
      <div className="absolute inset-x-0 bottom-0 z-20 px-4 sm:px-6 pb-3 sm:pb-3.5 flex items-end justify-between gap-3">
        <div className="flex items-center gap-2.5 min-w-0">
          {/* Compact hide + thread swatch indicator */}
          <span className="inline-flex items-center gap-1 shrink-0" aria-hidden="true">
            <span
              className="w-3.5 h-3.5 rounded-[1px] border border-[#65615B]"
              style={{ backgroundColor: primaryMeta?.swatchHex }}
            />
            {composition === 'two-tone' && secondaryMeta && (
              <span
                className="w-3.5 h-3.5 rounded-[1px] border border-[#65615B]"
                style={{ backgroundColor: secondaryMeta.swatchHex }}
              />
            )}
            {threadMeta && (
              <span
                className="w-1.5 h-3.5 rounded-[1px] border border-[#2A2B30]"
                style={{ backgroundColor: threadMeta.swatchHex }}
              />
            )}
          </span>

          <div className="min-w-0">
            <p className="font-serif italic text-[13px] sm:text-[15px] text-paper leading-tight truncate">
              {colourSummary} / {materialLabel}
            </p>
            <p className="hidden sm:block text-[11px] text-[#C8C4BC] truncate">
              {threadMeta ? `${threadMeta.label} thread` : ''}
              {trimLabel ? ` · ${trimLabel} (illustrative)` : ''}
              {lightMeta ? ` · ${lightMeta.label} light (illustrative)` : ''}
            </p>
          </div>
        </div>

        <p className="hidden sm:block text-[11px] text-[#B8B4AC] whitespace-nowrap shrink-0">
          Fixed angle · Not 3D
        </p>
      </div>

      {/* Hairline perimeter light tone indicator along stage bottom edge */}
      {lightMeta && (
        <div
          aria-hidden="true"
          className="absolute inset-x-0 bottom-0 h-[2px] z-30 transition-colors duration-200"
          style={{ backgroundColor: lightMeta.swatchHex }}
        />
      )}
    </div>
  );
}
