import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';
import { CONFIGURATION_STEPS, DEFAULT_CONFIGURATION } from '@/src/data/catalog';
import type {
  CabinConfiguration,
  CameraId,
  ColourId,
  CompositionId,
  ConfigurationStepId,
  IlluminationId,
  MaterialId,
  ThreadId,
  TrimId,
} from '@/src/types/configuration';

interface ConfigurationContextValue {
  configuration: CabinConfiguration;
  activeStep: ConfigurationStepId;
  setActiveStep: (step: ConfigurationStepId) => void;
  goToNextStep: () => void;
  goToPreviousStep: () => void;
  setMaterial: (material: MaterialId) => void;
  setPrimaryColour: (colour: ColourId) => void;
  setSecondaryColour: (colour: ColourId) => void;
  setAccentThread: (thread: ThreadId) => void;
  setComposition: (composition: CompositionId) => void;
  setTrim: (trim: TrimId) => void;
  setAmbientIllumination: (illumination: IlluminationId) => void;
  setActiveCamera: (camera: CameraId) => void;
  resetConfiguration: () => void;
}

const ConfigurationContext = createContext<ConfigurationContextValue | null>(null);

function pickFallbackSecondary(primary: ColourId): ColourId {
  if (primary === 'exclusive-black') return 'sienna-brown';
  if (primary === 'sienna-brown') return 'light-ivory';
  return 'exclusive-black';
}

export function ConfigurationProvider({ children }: { children: ReactNode }) {
  const [configuration, setConfiguration] = useState<CabinConfiguration>(DEFAULT_CONFIGURATION);
  const [activeStep, setActiveStep] = useState<ConfigurationStepId>('material');

  const setMaterial = useCallback((material: MaterialId) => {
    setConfiguration((prev) => ({ ...prev, material }));
  }, []);

  const setPrimaryColour = useCallback((primaryColour: ColourId) => {
    setConfiguration((prev) => ({
      ...prev,
      primaryColour,
      secondaryColour:
        prev.composition === 'two-tone'
          ? prev.secondaryColour && prev.secondaryColour !== primaryColour
            ? prev.secondaryColour
            : pickFallbackSecondary(primaryColour)
          : undefined,
    }));
  }, []);

  const setSecondaryColour = useCallback((secondaryColour: ColourId) => {
    setConfiguration((prev) => {
      if (secondaryColour === prev.primaryColour) {
        return prev;
      }
      return {
        ...prev,
        composition: 'two-tone',
        secondaryColour,
      };
    });
  }, []);

  const setAccentThread = useCallback((accentThread: ThreadId) => {
    setConfiguration((prev) => ({ ...prev, accentThread }));
  }, []);

  const setComposition = useCallback((composition: CompositionId) => {
    setConfiguration((prev) => ({
      ...prev,
      composition,
      secondaryColour:
        composition === 'two-tone'
          ? prev.secondaryColour && prev.secondaryColour !== prev.primaryColour
            ? prev.secondaryColour
            : pickFallbackSecondary(prev.primaryColour)
          : undefined,
    }));
  }, []);

  const setTrim = useCallback((trim: TrimId) => {
    setConfiguration((prev) => ({ ...prev, trim }));
  }, []);

  const setAmbientIllumination = useCallback((ambientIllumination: IlluminationId) => {
    setConfiguration((prev) => ({ ...prev, ambientIllumination }));
  }, []);

  const setActiveCamera = useCallback((activeCamera: CameraId) => {
    setConfiguration((prev) => ({ ...prev, activeCamera }));
  }, []);

  const goToNextStep = useCallback(() => {
    setActiveStep((current) => {
      const idx = CONFIGURATION_STEPS.findIndex((s) => s.id === current);
      if (idx === -1 || idx >= CONFIGURATION_STEPS.length - 1) return current;
      return CONFIGURATION_STEPS[idx + 1].id;
    });
  }, []);

  const goToPreviousStep = useCallback(() => {
    setActiveStep((current) => {
      const idx = CONFIGURATION_STEPS.findIndex((s) => s.id === current);
      if (idx <= 0) return current;
      return CONFIGURATION_STEPS[idx - 1].id;
    });
  }, []);

  const resetConfiguration = useCallback(() => {
    setConfiguration(DEFAULT_CONFIGURATION);
    setActiveStep('material');
  }, []);

  const value = useMemo<ConfigurationContextValue>(
    () => ({
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
    }),
    [
      configuration,
      activeStep,
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
    ]
  );

  return (
    <ConfigurationContext.Provider value={value}>{children}</ConfigurationContext.Provider>
  );
}

export function useConfiguration(): ConfigurationContextValue {
  const ctx = useContext(ConfigurationContext);
  if (!ctx) {
    throw new Error('useConfiguration must be used within a ConfigurationProvider');
  }
  return ctx;
}
