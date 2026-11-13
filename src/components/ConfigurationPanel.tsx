import { ArrowLeft, ArrowRight, RotateCcw } from 'lucide-react';
import { CONFIGURATION_STEPS } from '@/src/data/catalog';
import type {
  CabinConfiguration,
  ColourId,
  CompositionId,
  ConfigurationStepId,
  IlluminationId,
  MaterialId,
  ThreadId,
  TrimId,
} from '@/src/types/configuration';
import { AtelierButton, EditorialType, Surface } from './primitives';
import {
  ColourSelector,
  CompositionSelector,
  IlluminationSelector,
  MaterialSelector,
  ThreadSelector,
  TrimSelector,
} from './selectors';

export interface ConfigurationPanelProps {
  configuration: CabinConfiguration;
  activeStep: ConfigurationStepId;
  onSelectStep: (step: ConfigurationStepId) => void;
  onNextStep: () => void;
  onPreviousStep: () => void;
  onReset: () => void;
  onOpenSpecification: () => void;
  onChangeMaterial: (material: MaterialId) => void;
  onChangePrimaryColour: (colour: ColourId) => void;
  onChangeSecondaryColour: (colour: ColourId) => void;
  onChangeThread: (thread: ThreadId) => void;
  onChangeComposition: (composition: CompositionId) => void;
  onChangeTrim: (trim: TrimId) => void;
  onChangeIllumination: (illumination: IlluminationId) => void;
}

/**
 * Focused right-side (desktop) / below-viewer (mobile) configuration panel.
 * On mobile (< lg), top step tabs live above the viewer stage per Reference 03,
 * while this panel leads directly with the active step header, controls, and full-width Continue CTA.
 */
export function ConfigurationPanel({
  configuration,
  activeStep,
  onSelectStep,
  onNextStep,
  onPreviousStep,
  onReset,
  onOpenSpecification,
  onChangeMaterial,
  onChangePrimaryColour,
  onChangeSecondaryColour,
  onChangeThread,
  onChangeComposition,
  onChangeTrim,
  onChangeIllumination,
}: ConfigurationPanelProps) {
  const currentIndex = CONFIGURATION_STEPS.findIndex((s) => s.id === activeStep);
  const currentMeta = CONFIGURATION_STEPS[currentIndex] ?? CONFIGURATION_STEPS[0];
  const isFirst = currentIndex <= 0;
  const isLast = currentIndex >= CONFIGURATION_STEPS.length - 1;
  const nextMeta = !isLast ? CONFIGURATION_STEPS[currentIndex + 1] : null;
  const progressRatio = ((currentIndex + 1) / CONFIGURATION_STEPS.length) * 100;

  return (
    <Surface
      tone="paper"
      className="rounded-[2px] flex flex-col justify-between"
      data-component="ConfigurationPanel"
    >
      {/* Desktop Step Navigation Tabs (hidden on < lg where StudioPage renders top step strip above viewer) */}
      <div className="hidden lg:block border-b border-fine-border px-4 pt-3">
        <div className="flex items-center justify-between gap-2 pb-2">
          <span className="font-sans text-[11px] font-medium tracking-[0.06em] text-muted-grey tabular-nums">
            STEP {currentMeta.index} / 0{CONFIGURATION_STEPS.length}
          </span>
          <span className="text-[11px] text-muted-grey">
            {currentMeta.classification === 'illustrative'
              ? 'Illustrative preview'
              : 'Sample selection'}
          </span>
        </div>

        {/* Hairline progress rule */}
        <div className="h-[2px] w-full bg-fine-border/70 mb-2 overflow-hidden">
          <div
            className="h-full bg-cyan-ink transition-all duration-200 ease-out"
            style={{ width: `${progressRatio}%` }}
          />
        </div>

        <nav
          aria-label="Configuration steps"
          className="grid grid-cols-2 gap-1"
        >
          {CONFIGURATION_STEPS.map((step) => {
            const isActive = step.id === activeStep;
            return (
              <button
                key={step.id}
                type="button"
                onClick={() => onSelectStep(step.id)}
                aria-current={isActive ? 'step' : undefined}
                className={`relative min-h-[44px] px-2 py-2 text-left transition-colors duration-150 cursor-pointer flex items-center gap-1.5 ${
                  isActive
                    ? 'text-ink font-medium'
                    : 'text-muted-grey hover:text-ink font-normal'
                }`}
              >
                <span className="font-sans text-[10px] font-medium tabular-nums text-cyan-ink shrink-0">
                  {step.index}
                </span>
                <span className="text-[12px] whitespace-nowrap truncate">{step.label}</span>
                {isActive && (
                  <span
                    aria-hidden="true"
                    className="absolute bottom-0 left-1 right-1 h-[2px] bg-cyan"
                  />
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Active Step Header & Selector Body */}
      <div className="p-4 sm:p-6 space-y-4 flex-1">
        <div className="flex items-baseline justify-between gap-3 border-b border-fine-border pb-2.5 lg:border-b-0 lg:pb-0">
          <EditorialType variant="kicker" tone="muted">
            {currentMeta.label}
          </EditorialType>
          <span className="lg:hidden font-sans text-[11px] font-medium text-muted-grey tabular-nums">
            {currentMeta.index} / 0{CONFIGURATION_STEPS.length}
          </span>
        </div>

        <EditorialType variant="caption" tone="muted" className="hidden lg:block">
          {currentMeta.summary}
        </EditorialType>

        {activeStep === 'material' && (
          <MaterialSelector value={configuration.material} onChange={onChangeMaterial} />
        )}

        {activeStep === 'colour' && (
          <ColourSelector
            primaryColour={configuration.primaryColour}
            secondaryColour={configuration.secondaryColour}
            composition={configuration.composition}
            onPrimaryChange={onChangePrimaryColour}
            onSecondaryChange={onChangeSecondaryColour}
            onCompositionChange={onChangeComposition}
          />
        )}

        {activeStep === 'thread' && (
          <ThreadSelector value={configuration.accentThread} onChange={onChangeThread} />
        )}

        {activeStep === 'composition' && (
          <CompositionSelector
            value={configuration.composition}
            primaryColour={configuration.primaryColour}
            secondaryColour={configuration.secondaryColour}
            onChange={onChangeComposition}
          />
        )}

        {activeStep === 'trim' && (
          <TrimSelector value={configuration.trim} onChange={onChangeTrim} />
        )}

        {activeStep === 'illumination' && (
          <IlluminationSelector
            value={configuration.ambientIllumination}
            onChange={onChangeIllumination}
          />
        )}
      </div>

      {/* Step Footer Navigation — Reference 03 full-width Continue CTA on mobile; side-by-side on sm+ */}
      <div className="border-t border-fine-border p-4 sm:p-5 space-y-2.5 bg-paper">
        <div className="flex flex-col sm:flex-row sm:items-center gap-2.5">
          {!isFirst && (
            <AtelierButton
              variant="secondary"
              onClick={onPreviousStep}
              aria-label="Previous step"
              className="hidden sm:inline-flex px-3.5 shrink-0"
            >
              <ArrowLeft className="w-4 h-4" aria-hidden="true" />
              <span>Previous</span>
            </AtelierButton>
          )}

          {!isLast && nextMeta ? (
            <AtelierButton
              variant="primary"
              onClick={onNextStep}
              className="w-full sm:w-auto sm:flex-1 min-h-[48px] justify-between px-5"
            >
              <span className="truncate">Continue to {nextMeta.label}</span>
              <ArrowRight className="w-4 h-4 text-cyan shrink-0" aria-hidden="true" />
            </AtelierButton>
          ) : (
            <AtelierButton
              variant="primary"
              onClick={onOpenSpecification}
              className="w-full sm:w-auto sm:flex-1 min-h-[48px] justify-between px-5"
            >
              <span>Review Specification</span>
              <ArrowRight className="w-4 h-4 text-cyan shrink-0" aria-hidden="true" />
            </AtelierButton>
          )}
        </div>

        <div className="flex items-center justify-between gap-2 text-[12px] text-muted-grey">
          {!isFirst ? (
            <button
              type="button"
              onClick={onPreviousStep}
              className="sm:hidden inline-flex items-center gap-1.5 min-h-[44px] px-1 text-ink hover:text-cyan-ink transition-colors duration-150 cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5" aria-hidden="true" />
              <span>Previous step</span>
            </button>
          ) : (
            <span>Selections remain editable.</span>
          )}

          <button
            type="button"
            onClick={onReset}
            className="inline-flex items-center gap-1.5 min-h-[44px] px-1 text-muted-grey hover:text-ink transition-colors duration-150 cursor-pointer ml-auto"
          >
            <RotateCcw className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Reset</span>
          </button>
        </div>
      </div>
    </Surface>
  );
}
