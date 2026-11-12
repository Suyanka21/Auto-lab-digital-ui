import { useEffect, useState, type ReactNode } from 'react';
import { ArrowUpRight, Menu, X } from 'lucide-react';
import type { AppRoute } from '@/src/types/configuration';
import { AtelierButton } from './AtelierButton';
import { AutoLabBrand } from './AutoLabLogo';

interface AtelierShellProps {
  activeRoute: AppRoute;
  onNavigate: (route: AppRoute, sectionId?: string) => void;
  children: ReactNode;
}

export function AtelierShell({ activeRoute, onNavigate, children }: AtelierShellProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    if (!mobileMenuOpen) return;
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [mobileMenuOpen]);

  const navigateAndClose = (route: AppRoute, sectionId?: string) => {
    setMobileMenuOpen(false);
    onNavigate(route, sectionId);
  };

  return (
    <div className="min-h-screen flex flex-col bg-ivory text-ink">
      {/* 3-Zone Top Bar Contract (Desktop) · Left Menu + Brand (Mobile) */}
      <header className="sticky top-0 z-30 bg-ivory border-b border-fine-border">
        <div className="max-w-[1440px] mx-auto px-4 sm:px-8 h-16 flex items-center justify-between gap-4 lg:gap-8">
          {/* Left Zone: Mobile menu toggle on left + Brand lockup */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              type="button"
              onClick={() => setMobileMenuOpen((prev) => !prev)}
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-navigation"
              aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
              className="md:hidden -ml-2 inline-flex items-center justify-center min-w-[44px] min-h-[44px] text-ink hover:text-cyan-ink transition-colors duration-150 cursor-pointer"
            >
              {mobileMenuOpen ? (
                <X className="w-5 h-5" aria-hidden="true" />
              ) : (
                <Menu className="w-5 h-5" aria-hidden="true" />
              )}
            </button>

            <AutoLabBrand onClick={() => navigateAndClose('landing')} />
          </div>

          {/* Center Zone: Clean single-line navigation links (Desktop / Tablet) */}
          <nav aria-label="Primary" className="hidden md:flex items-center gap-5 lg:gap-7">
            <button
              type="button"
              onClick={() => navigateAndClose('landing')}
              aria-current={activeRoute === 'landing' ? 'page' : undefined}
              className={`relative min-h-[44px] px-1 inline-flex items-center text-[12px] tracking-[0.12em] uppercase whitespace-nowrap shrink-0 transition-colors duration-150 cursor-pointer ${
                activeRoute === 'landing'
                  ? 'text-ink font-medium'
                  : 'text-muted-grey hover:text-ink font-normal'
              }`}
            >
              Showroom
              {activeRoute === 'landing' && (
                <span aria-hidden="true" className="absolute bottom-0 left-0 right-0 h-[2px] bg-cyan" />
              )}
            </button>

            <button
              type="button"
              onClick={() => navigateAndClose('landing', 'materials')}
              className="inline-flex relative min-h-[44px] px-1 items-center text-[12px] tracking-[0.12em] uppercase whitespace-nowrap shrink-0 text-muted-grey hover:text-ink transition-colors duration-150 cursor-pointer"
            >
              Materials
            </button>

            <button
              type="button"
              onClick={() => navigateAndClose('landing', 'experience')}
              className="inline-flex relative min-h-[44px] px-1 items-center text-[12px] tracking-[0.12em] uppercase whitespace-nowrap shrink-0 text-muted-grey hover:text-ink transition-colors duration-150 cursor-pointer"
            >
              Experience
            </button>

            <button
              type="button"
              onClick={() => navigateAndClose('studio')}
              aria-current={activeRoute === 'studio' ? 'page' : undefined}
              className={`relative min-h-[44px] px-1 inline-flex items-center text-[12px] tracking-[0.12em] uppercase whitespace-nowrap shrink-0 transition-colors duration-150 cursor-pointer ${
                activeRoute === 'studio'
                  ? 'text-ink font-medium'
                  : 'text-muted-grey hover:text-ink font-normal'
              }`}
            >
              Studio
              {activeRoute === 'studio' && (
                <span aria-hidden="true" className="absolute bottom-0 left-0 right-0 h-[2px] bg-cyan" />
              )}
            </button>
          </nav>

          {/* Right Zone: Desktop-only primary action (hidden on mobile per clean mobile header) */}
          <div className="hidden md:flex items-center shrink-0">
            <AtelierButton
              variant={activeRoute === 'studio' ? 'secondary' : 'primary'}
              onClick={() => navigateAndClose(activeRoute === 'studio' ? 'landing' : 'studio')}
              className="px-5 text-[13px]"
            >
              <span>{activeRoute === 'studio' ? 'Showroom' : 'Enter the Studio'}</span>
              <ArrowUpRight className="w-4 h-4 text-cyan" aria-hidden="true" />
            </AtelierButton>
          </div>
        </div>

        {/* Left-anchored mobile navigation drawer */}
        {mobileMenuOpen && (
          <>
            <div
              aria-hidden="true"
              onClick={() => setMobileMenuOpen(false)}
              className="md:hidden fixed inset-0 top-16 z-20 bg-[#101114]/35"
            />
            <nav
              id="mobile-navigation"
              aria-label="Mobile navigation"
              className="md:hidden fixed left-0 top-16 bottom-0 z-30 w-64 bg-paper border-r border-fine-border px-4 py-3 divide-y divide-fine-border flex flex-col"
            >
              <button
                type="button"
                onClick={() => navigateAndClose('landing')}
                aria-current={activeRoute === 'landing' ? 'page' : undefined}
                className={`w-full min-h-[48px] flex items-center justify-between text-[12px] tracking-[0.12em] uppercase cursor-pointer ${
                  activeRoute === 'landing' ? 'text-ink font-medium' : 'text-muted-grey hover:text-ink'
                }`}
              >
                <span>Showroom</span>
                {activeRoute === 'landing' && (
                  <span className="w-4 h-[2px] bg-cyan" aria-hidden="true" />
                )}
              </button>
              <button
                type="button"
                onClick={() => navigateAndClose('landing', 'materials')}
                className="w-full min-h-[48px] flex items-center justify-between text-[12px] tracking-[0.12em] uppercase text-muted-grey hover:text-ink cursor-pointer"
              >
                <span>Materials</span>
              </button>
              <button
                type="button"
                onClick={() => navigateAndClose('landing', 'experience')}
                className="w-full min-h-[48px] flex items-center justify-between text-[12px] tracking-[0.12em] uppercase text-muted-grey hover:text-ink cursor-pointer"
              >
                <span>Experience</span>
              </button>
              <button
                type="button"
                onClick={() => navigateAndClose('studio')}
                aria-current={activeRoute === 'studio' ? 'page' : undefined}
                className={`w-full min-h-[48px] flex items-center justify-between text-[12px] tracking-[0.12em] uppercase cursor-pointer ${
                  activeRoute === 'studio' ? 'text-ink font-medium' : 'text-muted-grey hover:text-ink'
                }`}
              >
                <span>Studio</span>
                {activeRoute === 'studio' && (
                  <span className="w-4 h-[2px] bg-cyan" aria-hidden="true" />
                )}
              </button>
            </nav>
          </>
        )}
      </header>

      {/* Main Content Container */}
      <main className="flex-1 w-full max-w-[1440px] mx-auto px-4 sm:px-8 py-5 sm:py-8">
        {children}
      </main>

      {/* Quiet Atelier Footer */}
      <footer className="border-t border-fine-border bg-ivory">
        <div className="max-w-[1440px] mx-auto px-4 sm:px-8 py-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-[12px] text-muted-grey">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-medium text-ink">AutoLab Interior Studio</span>
            <span aria-hidden="true">·</span>
            <span>Nairobi, Kenya</span>
          </div>
          <p>Illustrative showroom photography · Bespoke automotive interior design</p>
        </div>
      </footer>
    </div>
  );
}
