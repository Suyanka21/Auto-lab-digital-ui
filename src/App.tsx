import { useCallback, useEffect, useState } from 'react';
import { LandingPage } from '@/src/components/LandingPage';
import { StudioPage } from '@/src/components/StudioPage';
import { AtelierShell } from '@/src/components/primitives';
import { ConfigurationProvider } from '@/src/state/ConfigurationContext';
import type { AppRoute } from '@/src/types/configuration';

function ShowroomRoot() {
  const [route, setRoute] = useState<AppRoute>(() => window.location.pathname.replace(/\/$/, '').endsWith('/studio') ? 'studio' : 'landing');
  const [pendingSection, setPendingSection] = useState<string | null>(null);

  const handleNavigate = useCallback((nextRoute: AppRoute, sectionId?: string) => {
    const path = import.meta.env.BASE_URL + (nextRoute === 'studio' ? 'studio' : '');
    if (window.location.pathname !== path) window.history.pushState(null, '', path);
    setRoute(nextRoute);
    if (sectionId) {
      setPendingSection(sectionId);
    } else {
      setPendingSection(null);
      const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: prefersReduced ? 'auto' : 'smooth' });
    }
  }, []);

  useEffect(() => {
    const restore = () => setRoute(window.location.pathname.replace(/\/$/, '').endsWith('/studio') ? 'studio' : 'landing');
    window.addEventListener('popstate', restore);
    return () => window.removeEventListener('popstate', restore);
  }, []);

  useEffect(() => {
    if (route === 'landing' && pendingSection) {
      const timer = window.setTimeout(() => {
        const el = document.getElementById(pendingSection);
        if (el) {
          const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
          el.scrollIntoView({ behavior: prefersReduced ? 'auto' : 'smooth', block: 'start' });
        }
        setPendingSection(null);
      }, 40);
      return () => window.clearTimeout(timer);
    }
  }, [route, pendingSection]);

  return (
    <AtelierShell activeRoute={route} onNavigate={handleNavigate}>
      {route === 'landing' ? (
        <LandingPage onEnterStudio={() => handleNavigate('studio')} />
      ) : (
        <StudioPage />
      )}
    </AtelierShell>
  );
}

export default function App() {
  return (
    <ConfigurationProvider>
      <ShowroomRoot />
    </ConfigurationProvider>
  );
}
