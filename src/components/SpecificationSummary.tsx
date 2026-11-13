import {
  CAMERA_OPTIONS,
  COLOUR_OPTIONS,
  COMPOSITION_OPTIONS,
  ILLUMINATION_OPTIONS,
  MATERIAL_OPTIONS,
  THREAD_OPTIONS,
  TRIM_OPTIONS,
} from '@/src/data/catalog';
import type { CabinConfiguration, ConfigurationStepId } from '@/src/types/configuration';
import { EditorialType, Surface } from './primitives';

export interface SpecificationSummaryProps {
  configuration: CabinConfiguration;
  onEditStep?: (step: ConfigurationStepId) => void;
}

function findLabel<T extends string>(
  items: { id: T; label: string }[],
  id: T | undefined
): string {
  if (!id) return 'Not selected';
  return items.find((item) => item.id === id)?.label ?? id;
}

interface SpecRow {
  label: string;
  value: string;
  illustrative?: boolean;
  stepId?: ConfigurationStepId;
}

/**
 * Structured specification readout reflecting shared configuration state.
 * Clearly distinguishes workshop selections from illustrative preview choices.
 */
export function SpecificationSummary({
  configuration,
  onEditStep,
}: SpecificationSummaryProps) {
  const rows: SpecRow[] = [
    {
      label: 'MATERIAL',
      value: findLabel(MATERIAL_OPTIONS, configuration.material),
      stepId: 'material',
    },
    {
      label: 'PRIMARY COLOUR',
      value: findLabel(COLOUR_OPTIONS, configuration.primaryColour),
      stepId: 'colour',
    },
    ...(configuration.composition === 'two-tone'
      ? [
          {
            label: 'SECONDARY COLOUR',
            value: findLabel(COLOUR_OPTIONS, configuration.secondaryColour),
            stepId: 'colour' as ConfigurationStepId,
          },
        ]
      : []),
    {
      label: 'ACCENT THREAD',
      value: findLabel(THREAD_OPTIONS, configuration.accentThread),
      stepId: 'thread',
    },
    {
      label: 'COMPOSITION',
      value: findLabel(COMPOSITION_OPTIONS, configuration.composition),
      stepId: 'composition',
    },
    ...(configuration.trim
      ? [
          {
            label: 'CABIN TRIM',
            value: findLabel(TRIM_OPTIONS, configuration.trim),
            illustrative: true,
            stepId: 'trim' as ConfigurationStepId,
          },
        ]
      : []),
    ...(configuration.ambientIllumination
      ? [
          {
            label: 'AMBIENT LIGHT',
            value: findLabel(ILLUMINATION_OPTIONS, configuration.ambientIllumination),
            illustrative: true,
            stepId: 'illumination' as ConfigurationStepId,
          },
        ]
      : []),
    {
      label: 'CAMERA',
      value: findLabel(CAMERA_OPTIONS, configuration.activeCamera),
    },
  ];

  return (
    <Surface
      tone="paper"
      className="p-5 sm:p-6 rounded-[2px]"
      data-component="SpecificationSummary"
    >
      <div className="flex flex-wrap items-baseline justify-between gap-2 pb-3 border-b border-ink">
        <div>
          <EditorialType variant="kicker" tone="muted">
            Current Configuration
          </EditorialType>
          <EditorialType variant="title" className="mt-1">
            Specification Summary
          </EditorialType>
        </div>
        <span className="text-[11px] text-muted-grey">
          Exploratory interior specification
        </span>
      </div>

      <dl className="divide-y divide-fine-border border-b border-fine-border">
        {rows.map((row) => (
          <div
            key={row.label}
            className="min-h-[44px] py-2 flex items-center justify-between gap-4 text-[13px]"
          >
            <dt className="font-sans text-[11px] font-medium tracking-[0.1em] text-muted-grey shrink-0">
              {row.label}
            </dt>
            <dd className="text-right text-ink font-medium min-w-0">
              {row.stepId && onEditStep ? (
                <button
                  type="button"
                  onClick={() => onEditStep(row.stepId!)}
                  aria-label={`Edit ${row.label.toLowerCase()}: ${row.value}`}
                  className="min-h-[44px] inline-flex items-center justify-end gap-2 hover:text-cyan-ink hover:underline underline-offset-4 decoration-cyan-ink transition-colors duration-150 cursor-pointer text-right"
                >
                  <span>
                    {row.value}
                    {row.illustrative && (
                      <span className="font-normal text-muted-grey"> — illustrative</span>
                    )}
                  </span>
                </button>
              ) : (
                <span>
                  {row.value}
                  {row.illustrative && (
                    <span className="font-normal text-muted-grey"> — illustrative</span>
                  )}
                </span>
              )}
            </dd>
          </div>
        ))}
      </dl>

      <p className="mt-3 text-[11px] leading-[1.5] text-muted-grey">
        All colours and upholstery treatments are digital samples. Trim and lighting are
        illustrative previews. Workshop availability and physical finish require consultation.
      </p>
    </Surface>
  );
}
