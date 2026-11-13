import { ArrowRight, ArrowUpRight } from 'lucide-react';
import heroCabinImg from '@/src/assets/images/autolab_hero_cabin_1794510358513.jpg';
import materialLeatherImg from '@/src/assets/images/autolab_material_leather_1794510358246.jpg';
import colourTrioImg from '@/src/assets/images/autolab_colour_trio_1794510358860.jpg';
import cabinTrimImg from '@/src/assets/images/autolab_cabin_trim_1794510359528.jpg';
import ambientIlluminationImg from '@/src/assets/images/autolab_ambient_illumination_1794510358781.jpg';
import {
  COLOUR_OPTIONS,
  COMPOSITION_OPTIONS,
  ILLUMINATION_OPTIONS,
  MATERIAL_OPTIONS,
  TRIM_OPTIONS,
} from '@/src/data/catalog';
import { AtelierButton, EditorialType, SectionDivider, Surface } from './primitives';

export interface LandingPageProps {
  onEnterStudio: () => void;
}

interface DisciplineItem {
  id: string;
  title: string;
  kicker: string;
  description: string;
  image: string;
  imageAlt: string;
  classificationLabel: string;
}

const DISCIPLINES: DisciplineItem[] = [
  {
    id: 'material',
    title: 'Material',
    kicker: '01 / Material',
    description:
      'Explore smooth grain, diamond quilting, and micro-perforated panel treatments.',
    image: materialLeatherImg,
    imageAlt:
      'Macro view of perforated sienna brown and matte black automotive leather with contrast saddle stitching',
    classificationLabel: 'Sample selection',
  },
  {
    id: 'colour',
    title: 'Colour',
    kicker: '02 / Colour',
    description:
      'Exclusive Black, Sienna Brown, and Light Ivory hides arranged in single or two-tone compositions.',
    image: colourTrioImg,
    imageAlt:
      'Three automotive front seats upholstered in Exclusive Black, Sienna Brown, and Light Ivory leather',
    classificationLabel: 'Sample selection',
  },
  {
    id: 'trim',
    title: 'Cabin Trim',
    kicker: '03 / Cabin Trim',
    description:
      'Illustrative dash and console inlays spanning carbon fibre, poplar wood, walnut wood, and piano lacquer.',
    image: cabinTrimImg,
    imageAlt:
      'Illustrative automotive dashboard inlay in dark open-pore wood grain with brushed vents',
    classificationLabel: 'Illustrative preview',
  },
  {
    id: 'illumination',
    title: 'Ambient Illumination',
    kicker: '04 / Ambient Illumination',
    description:
      'Illustrative light washes in Cyan, Amber, Rose, Ocean, and Champagne.',
    image: ambientIlluminationImg,
    imageAlt:
      'Illustrative black stitched leather door contour accented by a subtle cyan ambient light line',
    classificationLabel: 'Illustrative preview',
  },
];

const EXPERIENCE_STEPS = [
  {
    index: '01',
    title: 'Choose Material & Hide Colour',
    detail:
      'Start with sample upholstery treatments — Classic, Diamond Quilted, or Perforated — paired with Exclusive Black, Sienna Brown, or Light Ivory.',
  },
  {
    index: '02',
    title: 'Specify Thread & Composition',
    detail:
      'Assign contrast or tonal stitching and choose between a uniform single-colour hide or a two-tone bolster and insert split.',
  },
  {
    index: '03',
    title: 'Preview Trim & Illumination',
    detail:
      'Evaluate illustrative dashboard trim inlays and ambient light moods alongside your upholstery palette.',
  },
  {
    index: '04',
    title: 'Inspect Camera Angles & Spec',
    detail:
      'Switch across four cabin perspectives and review a structured specification sheet that clearly labels illustrative previews.',
  },
];

export function LandingPage({ onEnterStudio }: LandingPageProps) {
  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      el.scrollIntoView({ behavior: prefersReduced ? 'auto' : 'smooth', block: 'start' });
    }
  };

  return (
    <div className="space-y-12 sm:space-y-16" data-component="LandingPage">
      {/* Cinematic Automotive-Interior Hero */}
      <section aria-labelledby="landing-hero-title">
        <div className="overflow-hidden rounded-[2px] bg-graphite border border-[#2A2B30] sm:relative sm:min-h-[500px] lg:min-h-[530px] sm:flex sm:items-center">
          {/* Mobile: unobstructed 16:9 cabin stage stacked above copy; Desktop: full-bleed backdrop */}
          <div className="relative aspect-[16/9] sm:aspect-auto sm:absolute sm:inset-0 bg-graphite">
            <img
              src={heroCabinImg}
              alt="Bespoke dark leather automotive cabin looking forward from between the front seats toward the steering wheel and dashboard"
              referrerPolicy="no-referrer"
              className="w-full h-full object-cover object-center"
            />
            <div
              aria-hidden="true"
              className="hidden sm:block absolute inset-0 bg-gradient-to-r from-[#101114]/95 via-[#101114]/72 to-[#101114]/15"
            />
            <div
              aria-hidden="true"
              className="sm:hidden absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-[#101114] to-transparent"
            />
          </div>

          <div className="relative z-10 w-full px-6 py-8 sm:px-12 lg:px-14 sm:py-12 max-w-2xl space-y-5">
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <span className="inline-block w-8 h-[2px] bg-cyan" aria-hidden="true" />
                <EditorialType variant="kicker" tone="inverse-muted" className="text-[#D2CEC5]">
                  AutoLab Interior Studio · Nairobi, Kenya
                </EditorialType>
              </div>

              <EditorialType
                id="landing-hero-title"
                as="h1"
                variant="display"
                tone="inverse"
                className="text-[clamp(2.25rem,4.6vw,4rem)]"
              >
                Make it <em className="italic">personal.</em>
              </EditorialType>
            </div>

            <EditorialType variant="body" tone="inverse" className="text-[#E5E1D8] max-w-lg text-[15px] sm:text-[16px]">
              Explore bespoke automotive upholstery, hand-selected leather grains, hide colours,
              and cabin finishes tailored to your driving space.
            </EditorialType>

            <div className="flex flex-wrap items-center gap-5 pt-1">
              <AtelierButton variant="outline-cyan" onClick={onEnterStudio}>
                <span>Enter the Studio</span>
                <ArrowRight className="w-4 h-4 text-cyan" aria-hidden="true" />
              </AtelierButton>

              <button
                type="button"
                onClick={() => scrollToSection('experience')}
                className="inline-flex items-center gap-2 min-h-[44px] text-[13px] font-medium text-paper border-b border-[#65615B] hover:border-cyan transition-colors duration-150 cursor-pointer whitespace-nowrap"
              >
                <span>How the Studio works</span>
                <ArrowUpRight className="w-3.5 h-3.5 text-cyan" aria-hidden="true" />
              </button>
            </div>

            <p className="sm:hidden pt-1 text-[11px] tracking-[0.04em] text-[#A8A39B]">
              Illustrative studio photography · Not a live 3D model
            </p>
          </div>

          <p className="hidden sm:block absolute bottom-4 right-6 z-10 text-[11px] tracking-[0.04em] text-[#B8B4AC]">
            Illustrative studio photography · Not a live 3D model
          </p>
        </div>
      </section>

      {/* Four Interior Craft Disciplines */}
      <section id="materials" className="space-y-6 scroll-mt-24" aria-labelledby="disciplines-heading">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-fine-border pb-5">
          <div className="space-y-1.5">
            <EditorialType variant="kicker" tone="muted">
              Interior Architecture
            </EditorialType>
            <EditorialType id="disciplines-heading" variant="section">
              Material, colour, trim, and atmosphere.
            </EditorialType>
          </div>
          <EditorialType variant="caption" tone="muted" className="max-w-md">
            Each discipline pairs tactile automotive surfaces with clear distinction between
            sample upholstery and illustrative finish previews.
          </EditorialType>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {DISCIPLINES.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={onEnterStudio}
              className="group text-left overflow-hidden rounded-[2px] bg-graphite border border-[#2A2B30] hover:border-[#494B52] transition-colors duration-150 flex flex-col cursor-pointer"
            >
              <div className="relative aspect-[4/3] w-full overflow-hidden bg-graphite">
                <img
                  src={item.image}
                  alt={item.imageAlt}
                  referrerPolicy="no-referrer"
                  className="w-full h-full object-cover object-center transition-transform duration-300 ease-out group-hover:scale-[1.03]"
                />
                <div
                  aria-hidden="true"
                  className="absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-[#101114] to-transparent"
                />
              </div>

              <div className="p-5 bg-graphite text-paper flex-1 flex flex-col justify-between gap-4 w-full">
                <div className="space-y-2">
                  <div className="flex items-center justify-between gap-2 text-[11px] tracking-[0.1em] uppercase">
                    <span className="text-[#B8B4AC]">{item.kicker}</span>
                    <span className="text-[#9A968E] whitespace-nowrap">
                      {item.classificationLabel}
                    </span>
                  </div>

                  <h3 className="font-serif text-[22px] leading-[1.2] text-paper flex items-center justify-between gap-2">
                    <span>{item.title}</span>
                    <ArrowRight
                      className="w-4 h-4 text-cyan shrink-0 transition-transform duration-150 group-hover:translate-x-0.5"
                      aria-hidden="true"
                    />
                  </h3>

                  <p className="text-[13px] leading-[1.55] text-[#C8C4BC]">
                    {item.description}
                  </p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </section>

      <SectionDivider label="Sample Upholstery & Illustrative Finishes" />

      {/* Asymmetric Editorial Breakdown: Hairline Typography without Box-in-Box Clutter */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start" aria-label="Material and Finish Catalogue">
        <div className="lg:col-span-5 space-y-4">
          <EditorialType variant="kicker" tone="muted">
            Exploration Scope
          </EditorialType>
          <EditorialType variant="section">
            Explore upholstery and illustrative finishes.
          </EditorialType>
          <EditorialType variant="body" tone="muted">
            Explore leather grain, sample colours, contrast stitching and single or two-tone seats.
            These digital choices are a starting point for a conversation, not a stock catalogue
            or a promise of workshop availability. Trim and lighting remain illustrative.
          </EditorialType>
        </div>

        <div className="lg:col-span-7 space-y-8">
          <div className="space-y-3">
            <div className="flex items-baseline justify-between gap-2 border-b border-ink pb-2.5">
              <EditorialType variant="title">Sample Studio Selections</EditorialType>
              <span className="text-[12px] text-cyan-ink font-medium">
                Sample selection
              </span>
            </div>

            <dl className="divide-y divide-fine-border border-b border-fine-border">
              <div className="py-3 grid grid-cols-1 sm:grid-cols-12 gap-1 sm:gap-4 text-[14px]">
                <dt className="sm:col-span-4 font-medium text-ink">Upholstery Material</dt>
                <dd className="sm:col-span-8 text-muted-grey">
                  {MATERIAL_OPTIONS.map((m) => m.label).join(' · ')}
                </dd>
              </div>
              <div className="py-3 grid grid-cols-1 sm:grid-cols-12 gap-1 sm:gap-4 text-[14px]">
                <dt className="sm:col-span-4 font-medium text-ink">Hide Palette</dt>
                <dd className="sm:col-span-8 text-muted-grey">
                  {COLOUR_OPTIONS.map((c) => c.label).join(' · ')}
                </dd>
              </div>
              <div className="py-3 grid grid-cols-1 sm:grid-cols-12 gap-1 sm:gap-4 text-[14px]">
                <dt className="sm:col-span-4 font-medium text-ink">Surface Composition</dt>
                <dd className="sm:col-span-8 text-muted-grey">
                  {COMPOSITION_OPTIONS.map((c) => c.label).join(' · ')}
                </dd>
              </div>
            </dl>
          </div>

          <div className="space-y-3">
            <div className="flex items-baseline justify-between gap-2 border-b border-fine-border pb-2.5">
              <EditorialType variant="title">Illustrative Finish Previews</EditorialType>
              <span className="text-[12px] text-muted-grey">
                Illustrative preview only
              </span>
            </div>

            <dl className="divide-y divide-fine-border border-b border-fine-border">
              <div className="py-3 grid grid-cols-1 sm:grid-cols-12 gap-1 sm:gap-4 text-[14px]">
                <dt className="sm:col-span-4 font-medium text-ink">Cabin Trim</dt>
                <dd className="sm:col-span-8 text-muted-grey">
                  {TRIM_OPTIONS.map((t) => t.label).join(' · ')}
                </dd>
              </div>
              <div className="py-3 grid grid-cols-1 sm:grid-cols-12 gap-1 sm:gap-4 text-[14px]">
                <dt className="sm:col-span-4 font-medium text-ink">Ambient Illumination</dt>
                <dd className="sm:col-span-8 text-muted-grey">
                  {ILLUMINATION_OPTIONS.map((i) => i.label).join(' · ')}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </section>

      {/* Configuration Experience Walkthrough */}
      <section
        id="experience"
        className="space-y-6 scroll-mt-24 pt-2"
        aria-labelledby="experience-heading"
      >
        <div className="space-y-1.5 max-w-2xl">
          <EditorialType variant="kicker" tone="muted">
            The Configuration Experience
          </EditorialType>
          <EditorialType id="experience-heading" variant="section">
            Consider the whole. Then the smallest detail.
          </EditorialType>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-px bg-fine-border border-t border-b border-fine-border">
          {EXPERIENCE_STEPS.map((step) => (
            <div key={step.index} className="bg-paper p-6 space-y-2.5">
              <span className="font-sans text-[12px] font-medium tracking-[0.06em] text-cyan-ink tabular-nums block">
                {step.index}
              </span>
              <h3 className="font-serif text-[20px] leading-[1.25] text-ink">
                {step.title}
              </h3>
              <p className="text-[13px] leading-[1.6] text-muted-grey">
                {step.detail}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Closing Route into Studio */}
      <section aria-label="Enter the Studio">
        <Surface
          tone="graphite"
          className="p-7 sm:p-12 flex flex-col md:flex-row md:items-center justify-between gap-6 rounded-[2px]"
        >
          <div className="space-y-2 max-w-xl">
            <EditorialType variant="kicker" tone="inverse-muted" className="text-[#C8C4BC]">
              AutoLab Digital Showroom
            </EditorialType>
            <EditorialType variant="section" tone="inverse">
              Step into the cabin configurator.
            </EditorialType>
            <EditorialType variant="caption" tone="inverse-muted" className="text-[#D2CEC5]">
              Build your interior specification step by step and review every selection in a
              single structured readout.
            </EditorialType>
          </div>

          <AtelierButton variant="outline-cyan" onClick={onEnterStudio}>
            <span>Enter the Studio</span>
            <ArrowRight className="w-4 h-4 text-cyan" aria-hidden="true" />
          </AtelierButton>
        </Surface>
      </section>
    </div>
  );
}
