import { ArrowUpRight } from 'lucide-react';
import { CONFIGURATION_STEPS } from '@/src/data/catalog';
import { useConfiguration } from '@/src/state/ConfigurationContext';
import type { ConfigurationStepId } from '@/src/types/configuration';
import { CabinViewer } from './CabinViewer';
import { CameraControls } from './CameraControls';
import { ConfigurationPanel } from './ConfigurationPanel';
import { EditorialType } from './primitives';
import { SpecificationSummary } from './SpecificationSummary';

/**
 * StudioPage uniting the CabinViewer stage, CameraControls, ConfigurationPanel selectors,
 * and SpecificationSummary against the centralized ConfigurationContext.
 * Mobile (< lg) renders Reference 03's numbered step strip directly above the dominant viewer stage.
 */
export function StudioPage() {
  const {
    configuration,
    activeStep,
    setActiveStep,
    goToNextStep,
    goToPreviousStep,
    setMaterial,
    setPrimaryColour,
    setSecondaryColour,
    setAccentThread,
    setComposition,
    setTrim,
    setAmbientIllumination,
    setActiveCamera,
    resetConfiguration,
  } = useConfiguration();

  const scrollToSpecification = () => {
    const el = document.getElementById('studio-specification');
    if (el) {
      const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      el.scrollIntoView({ behavior: prefersReduced ? 'auto' : 'smooth', block: 'start' });
    }
  };

  const handleEditStep = (step: ConfigurationStepId) => {
    setActiveStep(step);
    const el = document.getElementById('studio-configuration-panel');
    if (el) {
      const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      el.scrollIntoView({ behavior: prefersReduced ? 'auto' : 'smooth', block: 'nearest' });
    }
  };

  return (
    <section className="space-y-4 sm:space-y-6" data-component="StudioPage">
      {/* Compact Editorial Studio Subheader */}
      <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 sm:gap-3 border-b border-fine-border pb-3.5 sm:pb-4">
        <div className="space-y-1">
          <div className="flex items-center justify-between gap-3">
            <EditorialType variant="kicker" tone="muted">
              The Interior Studio
            </EditorialType>
            <button
              type="button"
              onClick={scrollToSpecification}
              className="sm:hidden inline-flex items-center gap-1 min-h-[44px] text-[12px] font-medium text-ink hover:text-cyan-ink transition-colors duration-150 cursor-pointer whitespace-nowrap shrink-0"
            >
              <span>Specification</span>
              <ArrowUpRight className="w-3.5 h-3.5 text-cyan-ink" aria-hidden="true" />
            </button>
          </div>
          <div className="flex flex-wrap items-baseline gap-x-5 gap-y-1">
            <EditorialType as="h1" variant="section" className="text-[clamp(1.65rem,3vw,2.5rem)]">
              Make it <em className="italic">personal.</em>
            </EditorialType>
            <span className="hidden md:inline-block h-4 w-px bg-fine-border" aria-hidden="true" />
            <EditorialType variant="caption" tone="muted">
              Consider the whole. Then the smallest detail.
            </EditorialType>
          </div>
        </div>

        <button
          type="button"
          onClick={scrollToSpecification}
          className="hidden sm:inline-flex items-center gap-1.5 min-h-[44px] text-[13px] font-medium text-ink hover:text-cyan-ink transition-colors duration-150 cursor-pointer self-end whitespace-nowrap shrink-0"
        >
          <span>Your specification</span>
          <ArrowUpRight className="w-4 h-4 text-cyan-ink" aria-hidden="true" />
        </button>
      </header>

      {/* Mobile / Tablet Step Navigation Strip positioned above Viewer Stage per Reference 03 */}
      <nav
        aria-label="Mobile configuration steps"
        className="lg:hidden grid grid-cols-3 gap-x-2 border-b border-fine-border pb-1"
      >
        {CONFIGURATION_STEPS.map((step) => {
          const isActive = step.id === activeStep;
          return (
            <button
              key={step.id}
              type="button"
              onClick={() => setActiveStep(step.id)}
              aria-current={isActive ? 'step' : undefined}
              className={`relative min-h-[44px] px-1.5 py-2 text-left transition-colors duration-150 cursor-pointer flex flex-col justify-center ${
                isActive ? 'text-ink font-medium' : 'text-muted-grey hover:text-ink font-normal'
              }`}
            >
              <span className="font-sans text-[10px] font-medium tabular-nums text-cyan-ink leading-none">
                {step.index}
              </span>
              <span className="mt-1 text-[11px] sm:text-[12px] leading-tight whitespace-nowrap truncate">
                {step.label}
              </span>
              {isActive && (
                <span
                  aria-hidden="true"
                  className="absolute bottom-0 left-0 right-0 h-[2px] bg-cyan"
                />
              )}
            </button>
          );
        })}
      </nav>

      {/* Main Studio Workspace: Desktop 2/3 Viewer + 1/3 Panel | Mobile Dominant Viewer + Below Controls */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 sm:gap-6 items-start">
        {/* 1. Cabin Viewer Stage (8/12 = ~66.7% on Desktop) */}
        <div className="lg:col-span-8 lg:col-start-1 lg:row-start-1 overflow-hidden rounded-[2px] border border-[#2A2B30] bg-graphite">
          <CabinViewer
            material={configuration.material}
            primaryColour={configuration.primaryColour}
            secondaryColour={configuration.secondaryColour}
            accentThread={configuration.accentThread}
            composition={configuration.composition}
            trim={configuration.trim}
            ambientIllumination={configuration.ambientIllumination}
            activeCamera={configuration.activeCamera}
          />
          <CameraControls
            activeCamera={configuration.activeCamera}
            onSelectCamera={setActiveCamera}
          />
        </div>

        {/* 2. Focused Configuration Panel (4/12 = ~33.3% on Desktop, below viewer on Mobile) */}
        <div
          id="studio-configuration-panel"
          className="lg:col-span-4 lg:col-start-9 lg:row-start-1 lg:row-span-2 lg:self-start scroll-mt-24"
        >
          <ConfigurationPanel
            configuration={configuration}
            activeStep={activeStep}
            onSelectStep={setActiveStep}
            onNextStep={goToNextStep}
            onPreviousStep={goToPreviousStep}
            onReset={resetConfiguration}
            onOpenSpecification={scrollToSpecification}
            onChangeMaterial={setMaterial}
            onChangePrimaryColour={setPrimaryColour}
            onChangeSecondaryColour={setSecondaryColour}
            onChangeThread={setAccentThread}
            onChangeComposition={setComposition}
            onChangeTrim={setTrim}
            onChangeIllumination={setAmbientIllumination}
          />
        </div>

        {/* 3. Specification Summary (Single DOM instance across Desktop & Mobile) */}
        <div
          id="studio-specification"
          className="lg:col-span-8 lg:col-start-1 lg:row-start-2 scroll-mt-24"
        >
          <SpecificationSummary
            configuration={configuration}
            onEditStep={handleEditStep}
          />
        </div>
      </div>
    </section>
  );
}
